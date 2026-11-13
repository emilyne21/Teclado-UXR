import os
import sys
import time

import pygame

import picto
from . import pages
from .board import Board
from .config import rgb
from .dwell import DwellTracker
from .gaze import GazeReceiver, launch_bridge, now_ms
from .logger import SessionLogger
from .speech import Speaker

FONT_NAMES = "segoeui,arial,helvetica,dejavusans,freesans,liberationsans"


def _mix(c, white):
    """Mezcla un color con blanco (white=0 -> c, white=1 -> blanco)."""
    return tuple(int(v + (255 - v) * white) for v in c)


def _contrast(c):
    lum = 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
    return (25, 25, 25) if lum > 150 else (255, 255, 255)


def _enable_dpi_awareness():
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


class App(object):
    def __init__(self, cfg, base_dir, headless=False, mode=None, start=None,
                 gaze=None, speaker=None, logger=None, size=None):
        if headless:
            os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        else:
            _enable_dpi_awareness()
        self.cfg = cfg
        self.base_dir = base_dir
        self.headless = headless
        self.mode = mode or cfg["input_mode"]
        pygame.display.init()
        pygame.font.init()
        flags = 0
        req = tuple(size) if size else tuple(cfg["window_size"])
        if cfg["fullscreen"] and not headless:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(req, flags)
        self.size = self.screen.get_size()
        pygame.display.set_caption("Teclado de pictogramas")

        c = cfg["colors"]
        self.col = {k: rgb(v) for k, v in c.items()}
        self.board = Board(self.size, cfg, picto.ICONS, start=start)
        self.dwell = DwellTracker(cfg["dwell_time_ms"])
        self.hyst = int(cfg["feedback"]["hysteresis_px"])
        self.flash_ms = int(cfg["feedback"]["selection_flash_ms"])
        self.item_color = {}
        for cat in pages.CATEGORIES:
            for i in cat.items:
                self.item_color.setdefault(i, cat.color)

        self.t0 = now_ms()
        self.running = False
        self.overlay = False
        self.show_gaze = False
        self.flash = None               # (uid, t_inicio_ms)
        self.pointer = None
        self.selections = 0
        self.no_signal = False
        self.fps_now = 0.0
        self._fonts = {}
        self._labels = {}
        self._static = None
        self._static_key = None
        self._ov = {}
        self.bridge_proc = None
        self.notice = ""                # mensaje breve del operador (se ve en el panel F2)

        self.logger = logger or SessionLogger(cfg, base_dir)
        sp = cfg["speech"]
        self.speaker = speaker or Speaker(sp["enabled"], sp["language"], sp["rate"], sp["volume"])
        self.gaze = gaze
        if self.mode == "tobii":
            self._start_tobii()
        if self.mode == "tobii" and not cfg["tobii"]["show_pointer"] and not headless:
            pygame.mouse.set_visible(False)
        self.log("session_start", detail="mode=%s dwell=%d size=%dx%d voice=%s" % (
            self.mode, self.dwell.dwell_ms, self.size[0], self.size[1], self.speaker.backend))

    # ------------------------------------------------------------------ Tobii
    def _start_tobii(self):
        t = self.cfg["tobii"]
        if self.gaze is None:
            self.gaze = GazeReceiver(t["udp_ip"], t["udp_port"], t["source_screen_width_px"],
                                     t["source_screen_height_px"], t["sample_stale_after_ms"],
                                     t["treat_zero_zero_as_invalid"])
            self.gaze.start()
            if t["launch_bridge"]:
                log_path = os.path.join(self.logger.log_dir, "bridge_output.log")
                try:
                    self.bridge_proc, msg = launch_bridge(t, self.base_dir, log_path)
                except Exception as exc:        # no se esconde: queda en el log y en pantalla
                    self.bridge_proc, msg = None, "Error al iniciar el puente: %s" % exc
                self.notice = msg
                print(msg)
                self.log("bridge", detail=msg)
                if self.bridge_proc is not None:
                    time.sleep(t["startup_wait_ms"] / 1000.0)

    # ------------------------------------------------------------------- util
    def t(self, now):
        return now - self.t0

    def log(self, name, now=None, target="", detail=""):
        now = now_ms() if now is None else now
        page = self.page_label()
        self.logger.event(self.t(now), name, page, target, detail)

    def page_label(self):
        b = self.board
        return b.category + ("#%d" % (b.page + 1) if b.page_count > 1 else "")

    def font(self, size):
        size = max(8, int(size))
        f = self._fonts.get(size)
        if f is None:
            f = pygame.font.SysFont(FONT_NAMES, size, bold=True)
            self._fonts[size] = f
        return f

    def label_surface(self, text, max_w, max_size, color, max_lines=2, min_scale=0.72):
        """Texto que cabe en `max_w`: una línea si se puede, si no dos líneas equilibradas."""
        key = (text, int(max_w), int(max_size), color, max_lines, min_scale)
        s = self._labels.get(key)
        if s is not None:
            return s
        max_size = max(10, int(max_size))
        one_min = max(10, int(max_size * min_scale))
        size = max_size
        while size > one_min and self.font(size).size(text)[0] > max_w:
            size -= 1
        if self.font(size).size(text)[0] <= max_w or " " not in text or max_lines < 2:
            f = self.font(size)
            while size > 9 and f.size(text)[0] > max_w:
                size -= 1
                f = self.font(size)
            s = f.render(text, True, color)
        else:
            words = text.split(" ")
            best = None
            for i in range(1, len(words)):
                a, b = " ".join(words[:i]), " ".join(words[i:])
                w = max(self.font(max_size).size(a)[0], self.font(max_size).size(b)[0])
                if best is None or w < best[0]:
                    best = (w, a, b)
            _, a, b = best
            size = max_size
            while size > 9 and max(self.font(size).size(a)[0], self.font(size).size(b)[0]) > max_w:
                size -= 1
            f = self.font(size)
            sa, sb = f.render(a, True, color), f.render(b, True, color)
            s = pygame.Surface((max(sa.get_width(), sb.get_width()), sa.get_height() + sb.get_height() - 2),
                               pygame.SRCALPHA)
            s.blit(sa, ((s.get_width() - sa.get_width()) // 2, 0))
            s.blit(sb, ((s.get_width() - sb.get_width()) // 2, sa.get_height() - 2))
        self._labels[key] = s
        return s

    # ---------------------------------------------------------------- dibujo
    def _draw_cell(self, surf, key):
        r, cat_col = key.rect, key.color
        rad = max(8, int(r.h * 0.09))
        paging = key.kind in ("prev", "next")
        pygame.draw.rect(surf, _mix(cat_col, 0.85) if paging else (255, 255, 255), r, border_radius=rad)
        pygame.draw.rect(surf, cat_col, r, 4, border_radius=rad)
        bar_h = max(8, int(r.h * 0.06))
        lab = self.label_surface(key.label, r.w - 20, r.h * 0.14, self.col["ink"])
        lab_y = r.bottom - bar_h - 15 - lab.get_height()
        isz = int(min(r.w * 0.82, lab_y - r.y - 8))
        surf.blit(picto.render(key.ref, isz), (r.centerx - isz // 2, r.y + 6 + max(0, (lab_y - r.y - 8 - isz) // 2)))
        surf.blit(lab, (r.centerx - lab.get_width() // 2, lab_y))

    def _draw_tab(self, surf, key):
        r = key.rect
        cur = key.ref == self.board.category
        cat = pages.BY_ID[key.ref]
        fill = key.color if cur else _mix(key.color, 0.84)
        txt = _contrast(fill)
        rad = max(8, int(r.h * 0.18))
        pygame.draw.rect(surf, fill, r, border_radius=rad)
        pygame.draw.rect(surf, key.color, r, 3, border_radius=rad)
        isz = r.h - 12
        pygame.draw.circle(surf, (255, 255, 255), (r.x + 6 + isz // 2, r.centery), isz // 2)
        surf.blit(picto.render(cat.icon, isz - 4), (r.x + 8, r.centery - (isz - 4) // 2))
        tx = r.x + isz + 14
        lab = self.label_surface(key.label, r.right - tx - 8, r.h * 0.27, txt, max_lines=2, min_scale=0.92)
        surf.blit(lab, (tx, r.centery - lab.get_height() // 2))

    def _draw_button(self, surf, key):
        r = key.rect
        rad = max(8, int(r.h * 0.12))
        pygame.draw.rect(surf, key.color, r, border_radius=rad)
        pygame.draw.rect(surf, (30, 30, 30), r, 3, border_radius=rad)
        isz = int(r.h * 0.56)
        surf.blit(picto.render(key.ref, isz), (r.centerx - isz // 2, r.y + int(r.h * 0.06)))
        lab = self.label_surface(key.label, r.w - 14, r.h * 0.17, (255, 255, 255), max_lines=1)
        surf.blit(lab, (r.centerx - lab.get_width() // 2, r.bottom - lab.get_height() - int(r.h * 0.07)))

    def _draw_strip(self, surf):
        b = self.board
        r = b.strip_rect
        rad = max(8, int(r.h * 0.1))
        pygame.draw.rect(surf, self.col["panel"], r, border_radius=rad)
        pygame.draw.rect(surf, self.col["border"], r, 3, border_radius=rad)
        shown, more = b.visible_sentence()
        for i, slot in enumerate(b.slot_rects):
            if i < len(shown):
                pid = shown[i]
                col = self.item_color.get(pid, self.col["border"])
                pygame.draw.rect(surf, (255, 255, 255), slot, border_radius=10)
                pygame.draw.rect(surf, col, slot, 3, border_radius=10)
                lh = int(slot.h * 0.24)
                isz = int(min(slot.w * 0.84, (slot.h - lh) * 0.96))
                surf.blit(picto.render(pid, isz), (slot.centerx - isz // 2, slot.y + 3))
                lab = self.label_surface(picto.ICONS[pid].label, slot.w - 8, slot.h * 0.15,
                                         self.col["ink"], max_lines=1)
                surf.blit(lab, (slot.centerx - lab.get_width() // 2, slot.bottom - lh // 2 - lab.get_height() // 2))
            else:
                pygame.draw.rect(surf, (225, 225, 225), slot, 2, border_radius=10)
        if more:
            f = self.font(r.h * 0.22)
            t = f.render("…", True, self.col["ink"])
            surf.blit(t, (r.x + 2, r.centery - t.get_height() // 2))

    def render_static(self):
        surf = pygame.Surface(self.size)
        surf.fill(self.col["background"])
        self._draw_strip(surf)
        for key in self.board.keys():
            if key.kind in ("picto", "prev", "next"):
                self._draw_cell(surf, key)
            elif key.kind == "tab":
                self._draw_tab(surf, key)
            else:
                self._draw_button(surf, key)
        return surf

    def static_layer(self):
        b = self.board
        k = (b.category, b.page, tuple(b.sentence), self.size)
        if k != self._static_key:
            self._static = self.render_static()
            self._static_key = k
        return self._static

    def _overlay_surface(self, w, h, color, alpha):
        key = (w, h, color, alpha)
        s = self._ov.get(key)
        if s is None:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            s.fill(tuple(color) + (alpha,))
            if len(self._ov) > 80:
                self._ov.clear()
            self._ov[key] = s
        return s

    def _draw_focus(self, surf, key, now):
        r = key.rect
        prog = self.dwell.progress(now)
        done = self.dwell.fired
        rad = max(8, int(r.h * 0.1))
        surf.blit(self._overlay_surface(r.w, r.h, self.col["focus_background"], 105), r.topleft)
        pygame.draw.rect(surf, self.col["selected"] if done else self.col["focus"], r, 7, border_radius=rad)
        bh = max(8, int(r.h * 0.06))
        track = pygame.Rect(r.x + 14, r.bottom - bh - 12, r.w - 28, bh)
        pygame.draw.rect(surf, self.col["progress_track"], track, border_radius=bh // 2)
        fill = track.copy()
        fill.w = max(bh if prog > 0 else 0, int(track.w * prog))
        if fill.w:
            pygame.draw.rect(surf, self.col["selected"] if done else self.col["focus"], fill,
                             border_radius=bh // 2)

    def draw(self, now=None):
        now = now_ms() if now is None else now
        surf = self.screen
        surf.blit(self.static_layer(), (0, 0))
        if self.dwell.target is not None:
            key = self.board.key_by_uid(self.dwell.target)
            if key is not None:
                self._draw_focus(surf, key, now)
        if self.flash is not None:
            uid, t0 = self.flash
            age = now - t0
            key = self.board.key_by_uid(uid)
            if age < self.flash_ms and key is not None:
                a = int(150 * (1.0 - age / float(self.flash_ms)))
                surf.blit(self._overlay_surface(key.rect.w, key.rect.h, self.col["selected"], a), key.rect.topleft)
            elif age >= self.flash_ms:
                self.flash = None
        if self.mode == "tobii":
            self._draw_signal_banner(surf)
        if self.show_gaze and self.pointer is not None:
            pygame.draw.circle(surf, (220, 30, 30), (int(self.pointer[0]), int(self.pointer[1])), 14, 3)
            pygame.draw.circle(surf, (220, 30, 30), (int(self.pointer[0]), int(self.pointer[1])), 3)
        if self.overlay:
            self._draw_overlay(surf, now)

    def _draw_signal_banner(self, surf):
        g = self.gaze
        if g is None:
            return
        if g.silent_for_ms() > 1000:
            text = "SIN SEÑAL DEL TOBII  (no llegan datos a %s:%d)" % (g.ip, g.port)
            f = self.font(self.size[1] * 0.034)
            t = f.render(text, True, (255, 255, 255))
            r = pygame.Rect(0, 0, t.get_width() + 40, t.get_height() + 16)
            r.midbottom = (self.size[0] // 2, self.size[1] - 6)
            pygame.draw.rect(surf, (192, 30, 30), r, border_radius=10)
            surf.blit(t, (r.x + 20, r.y + 8))

    def _draw_overlay(self, surf, now):
        g = self.gaze
        lines = [
            "MODO %s   DWELL %d ms   FPS %.0f   ventana %dx%d" % (
                self.mode.upper(), self.dwell.dwell_ms, self.fps_now, self.size[0], self.size[1]),
            "Puntero: %s   Objetivo: %s   progreso %d%%" % (
                "—" if self.pointer is None else "(%d, %d)" % (self.pointer[0], self.pointer[1]),
                self.dwell.target or "—", int(100 * self.dwell.progress(now))),
        ]
        if g is not None:
            lines.append("Tobii: %d paquetes, %d mal formados, mirada %s, sin datos hace %s ms" % (
                g.packets, g.bad_packets, "OK" if g.sample(now) is not None else "no válida",
                "∞" if g.silent_for_ms(now) == float("inf") else int(g.silent_for_ms(now))))
        lines += [
            "Participante %s  sesión %s  selecciones %d  voz: %s" % (
                self.cfg["participant_id"], self.cfg["sessionID"], self.selections, self.speaker.backend),
            "Log: %s" % os.path.basename(self.logger.paths["selections"]),
            "F2 panel · F3 punto de mirada · +/- dwell · ENTER hablar · RETROCESO borrar · SUPR limpiar · 1-9 página · ESC salir",
        ]
        if self.notice:
            lines.append(self.notice)
        f = self.font(self.size[1] * 0.021)
        rendered = [f.render(l, True, (255, 255, 255)) for l in lines]
        w = max(t.get_width() for t in rendered) + 24
        h = sum(t.get_height() for t in rendered) + 20
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 205))
        y = 10
        for t in rendered:
            panel.blit(t, (12, y))
            y += t.get_height()
        surf.blit(panel, (self.board.margin, self.board.content_top))

    # ---------------------------------------------------------------- lógica
    def pointer_in_window(self, p):
        return p is not None and 0 <= p[0] < self.size[0] and 0 <= p[1] < self.size[1]

    def step(self, now, pointer):
        """Un ciclo de lógica con el puntero dado (ventana, px) o None. Devuelve 'select' o None."""
        self.pointer = pointer
        valid = self.pointer_in_window(pointer)
        key = None
        if valid:
            key = self.board.hit(pointer[0], pointer[1], prefer=self.dwell.target, margin=self.hyst)
        ev = self.dwell.update(now, key.uid if key else None, valid)
        px, py = (pointer if pointer is not None else (None, None))
        self.logger.sample(self.t(now), px, py, valid, key.uid if key else None)
        if ev == "select":
            self.activate(key, now, source=self.mode, dwell_ms=self.dwell.elapsed(now))
        return ev

    def activate(self, key, now, source="", dwell_ms=0):
        page = self.page_label()        # página donde estaba la tecla (antes de que cambie)
        res = self.board.activate(key)
        typ = res["type"]
        self.flash = (key.uid, now)
        self.selections += 1
        t = self.t(now)
        sentence = list(self.board.sentence)
        label = key.label
        target = key.ref if key.kind in ("picto", "tab") else key.kind
        self.logger.selection(t, page, key.kind, target, label, dwell_ms, sentence)
        sp = self.cfg["speech"]
        if typ == "add":
            if sp["speak_on_select"]:
                self.speaker.say(res["speech"])
        elif typ == "speak":
            if res["n"]:
                self.speaker.say(res["text"])
            self.log("speak", now, key.uid, res["text"])
        elif typ == "category":
            self.log("category", now, res["id"], "changed=%s via=%s" % (res["changed"], source))
        elif typ in ("delete", "clear", "page", "full"):
            self.log(typ, now, key.uid, str({k: v for k, v in res.items() if k != "type"}))
        return res

    def operator(self, action, now=None):
        """Acciones del operador por teclado (se registran con origen 'keyboard')."""
        now = now_ms() if now is None else now
        b = self.board
        if action in ("speak", "delete", "clear"):
            key = [k for k in b.button_keys if k.kind == action][0]
            return self.activate(key, now, source="keyboard")
        if action.startswith("category:"):
            cid = action.split(":", 1)[1]
            key = [k for k in b.tab_keys if k.ref == cid][0]
            return self.activate(key, now, source="keyboard")
        if action in ("dwell+", "dwell-"):
            d = self.dwell.dwell_ms + (100 if action == "dwell+" else -100)
            d = max(200, min(3000, d))
            self.dwell.set_dwell(d)
            self.log("dwell_change", now, detail=str(d))
            return {"type": "dwell", "ms": d}
        return None

    def handle_events(self, now):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.KEYDOWN:
                k = ev.key
                if k == pygame.K_ESCAPE:
                    self.running = False
                elif k == pygame.K_F2:
                    self.overlay = not self.overlay
                    self.log("overlay", now, detail=str(self.overlay))
                elif k == pygame.K_F3:
                    self.show_gaze = not self.show_gaze
                elif k in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.operator("speak", now)
                elif k == pygame.K_BACKSPACE:
                    self.operator("delete", now)
                elif k == pygame.K_DELETE:
                    self.operator("clear", now)
                elif k in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                    self.operator("dwell+", now)
                elif k in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    self.operator("dwell-", now)
                elif pygame.K_1 <= k <= pygame.K_9:
                    i = k - pygame.K_1
                    if i < len(pages.CATEGORIES):
                        self.operator("category:" + pages.CATEGORIES[i].id, now)

    def read_pointer(self, now):
        if self.mode == "mouse":
            if not pygame.mouse.get_focused():
                return None
            return pygame.mouse.get_pos()
        g = self.gaze
        g.poll()
        s = g.sample(now)
        if s is None:
            return None
        return g.to_window(s, self.size)

    def _check_signal(self, now):
        if self.mode != "tobii" or self.gaze is None:
            return
        lost = self.gaze.silent_for_ms(now) > 1000
        if lost != self.no_signal:
            self.no_signal = lost
            self.log("no_signal" if lost else "signal_restored", now)

    def run(self):
        clock = pygame.time.Clock()
        self.running = True
        fps = int(self.cfg["fps"])
        try:
            while self.running:
                now = now_ms()
                self.handle_events(now)
                self.step(now, self.read_pointer(now))
                self._check_signal(now)
                self.draw(now)
                pygame.display.flip()
                clock.tick(fps)
                self.fps_now = clock.get_fps()
        finally:
            self.close()

    def close(self):
        if self.logger.closed:
            return
        self.log("session_end", detail="selections=%d sentence=%s" % (
            self.selections, " ".join(self.board.sentence)))
        self.logger.close()
        self.speaker.close()
        if self.gaze is not None:
            self.gaze.close()
        if self.bridge_proc is not None:
            try:
                self.bridge_proc.terminate()
            except Exception:
                pass
        try:
            pygame.mouse.set_visible(True)
        except Exception:
            pass

    # -------------------------------------------------------------- vistas previas
    def save_preview(self, path, focus_uid=None, progress=0.0, overlay=False):
        """Guarda una imagen del tablero tal como se ve (con una tecla en foco opcional)."""
        now = 10000.0
        if focus_uid is not None:
            self.dwell.reset()
            self.dwell.update(now - progress * self.dwell.dwell_ms, focus_uid, True)
        else:
            self.dwell.reset()
        old = self.overlay
        self.overlay = overlay
        self.draw(now)
        self.overlay = old
        pygame.image.save(self.screen, path)
        self.dwell.reset()