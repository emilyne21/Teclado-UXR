import math

import pygame

from . import pages


class Key(object):
    __slots__ = ("uid", "kind", "rect", "ref", "label", "color")

    def __init__(self, uid, kind, rect, ref=None, label="", color=None):
        self.uid = uid          # identificador único dentro de la pantalla
        self.kind = kind        # picto | tab | speak | delete | clear | prev | next
        self.rect = rect
        self.ref = ref          # id de pictograma o de categoría
        self.label = label
        self.color = color


class Board(object):
    def __init__(self, size, cfg, icons, start=None):
        self.cfg = cfg
        self.icons = icons                      # picto.ICONS
        self.cols = int(cfg["grid"]["columns"])
        self.rows = int(cfg["grid"]["rows"])
        self.max_items = int(cfg["feedback"]["sentence_max_items"])
        self.categories = pages.CATEGORIES
        self.category = start if start in pages.BY_ID else cfg.get("start_page", "necesidades")
        if self.category not in pages.BY_ID:
            self.category = self.categories[0].id
        self.page = 0
        self.sentence = []
        self.layout(size)

    # ------------------------------------------------------------ distribución
    def layout(self, size):
        W, H = int(size[0]), int(size[1])
        self.size = (W, H)
        m = max(6, int(round(0.0125 * W)))
        g = max(4, int(round(0.008 * W)))
        top_h = int(round(0.165 * H))
        side_w = int(round(0.15 * W))
        btn_w = int(round(0.105 * W))
        self.margin, self.gap = m, g

        # botones de la frase (derecha de la franja superior)
        strip_h = top_h - m
        bx0 = W - m - (3 * btn_w + 2 * g)
        self.button_keys = []
        for i, (kind, label, icon, color) in enumerate((
                ("speak", "HABLAR", "ui_hablar", (46, 125, 50)),
                ("delete", "BORRAR", "ui_borrar", (230, 126, 34)),
                ("clear", "LIMPIAR", "ui_limpiar", (192, 57, 43)))):
            r = pygame.Rect(bx0 + i * (btn_w + g), m, btn_w, strip_h)
            k = Key("btn:" + kind, kind, r, icon, label, color)
            self.button_keys.append(k)

        # franja de la frase
        self.strip_rect = pygame.Rect(m, m, bx0 - g - m, strip_h)
        pad = max(4, int(strip_h * 0.06))
        slot_h = strip_h - 2 * pad
        slot_w = int(slot_h * 0.96)
        sg = max(4, int(g * 0.8))
        inner_w = self.strip_rect.w - 2 * pad
        self.slot_n = max(1, (inner_w + sg) // (slot_w + sg))
        total_w = self.slot_n * slot_w + (self.slot_n - 1) * sg
        sx0 = self.strip_rect.x + pad + (inner_w - total_w) // 2
        self.slot_rects = [pygame.Rect(sx0 + i * (slot_w + sg), self.strip_rect.y + pad, slot_w, slot_h)
                           for i in range(self.slot_n)]

        # zona de contenido
        top = top_h + g + m // 2
        self.content_top = top
        self.grid_rect = pygame.Rect(m, top, W - 2 * m - side_w - g, H - m - top)
        n = len(self.categories)
        tab_h = (self.grid_rect.h - (n - 1) * g) // n
        tx = W - m - side_w
        self.tab_keys = []
        for i, cat in enumerate(self.categories):
            r = pygame.Rect(tx, top + i * (tab_h + g), side_w, tab_h)
            self.tab_keys.append(Key("tab:" + cat.id, "tab", r, cat.id, cat.label, cat.color))

        self._cell_cache = {}

    def _cells(self, rows):
        """Celdas de la rejilla para `rows` filas (ocupan siempre toda la zona de contenido)."""
        cells = self._cell_cache.get(rows)
        if cells is None:
            g = self.gap
            cw = (self.grid_rect.w - (self.cols - 1) * g) // self.cols
            ch = (self.grid_rect.h - (rows - 1) * g) // rows
            cells = [pygame.Rect(self.grid_rect.x + c * (cw + g), self.grid_rect.y + r * (ch + g), cw, ch)
                     for r in range(rows) for c in range(self.cols)]
            self._cell_cache[rows] = cells
        return cells

    def rows_used(self):
        """Filas que se usan en la página actual (menos figuras -> celdas más grandes)."""
        if self.page_count > 1:
            return self.rows
        n = len(self.page_items())
        need = int(math.ceil(n / float(self.cols)))
        return max(min(self.rows, int(self.cfg["grid"].get("min_rows", self.rows - 1))), need)

    # ----------------------------------------------------------------- páginas
    @property
    def cat(self):
        return pages.BY_ID[self.category]

    @property
    def per_page(self):
        total = len(self.cat.items)
        cells = self.cols * self.rows
        return cells if total <= cells else cells - 2

    @property
    def page_count(self):
        return max(1, int(math.ceil(len(self.cat.items) / float(self.per_page))))

    def page_items(self):
        pp = self.per_page
        return self.cat.items[self.page * pp:(self.page + 1) * pp]

    def keys(self):
        """Teclas activas ahora mismo (rejilla + paso de página + pestañas + botones)."""
        out = []
        cat = self.cat
        cells = self._cells(self.rows_used())
        for i, pid in enumerate(self.page_items()):
            out.append(Key("picto:" + pid, "picto", cells[i], pid, self.icons[pid].label, cat.color))
        if self.page_count > 1:
            if self.page > 0:
                out.append(Key("nav:prev", "prev", cells[-2], "ui_anterior", "ANTERIOR", cat.color))
            if self.page < self.page_count - 1:
                out.append(Key("nav:next", "next", cells[-1], "ui_siguiente", "SIGUIENTE", cat.color))
        out.extend(self.tab_keys)
        out.extend(self.button_keys)
        return out

    def hit(self, x, y, prefer=None, margin=0):
        """Tecla bajo (x, y). `prefer` es el uid actual: se le da `margin` px de tolerancia."""
        keys = self.keys()
        if prefer is not None and margin > 0:
            for k in keys:
                if k.uid == prefer and k.rect.inflate(2 * margin, 2 * margin).collidepoint(x, y):
                    return k
        for k in keys:
            if k.rect.collidepoint(x, y):
                return k
        return None

    def key_by_uid(self, uid):
        for k in self.keys():
            if k.uid == uid:
                return k
        return None

    # ------------------------------------------------------------------ frase
    def sentence_text(self):
        words = [self.icons[i].speech for i in self.sentence if self.icons[i].speech]
        if not words:
            return ""
        text = " ".join(words)
        return text[0].upper() + text[1:] + "."

    def visible_sentence(self):
        """(ids visibles, hay_mas_a_la_izquierda)."""
        if len(self.sentence) <= self.slot_n:
            return list(self.sentence), False
        return self.sentence[-self.slot_n:], True

    # ---------------------------------------------------------------- acciones
    def set_category(self, cat_id):
        if cat_id in pages.BY_ID:
            self.category = cat_id
            self.page = 0

    def activate(self, key):
        """Ejecuta la tecla y devuelve un dict describiendo lo ocurrido."""
        k = key.kind
        if k == "picto":
            if len(self.sentence) >= self.max_items:
                return {"type": "full", "id": key.ref}
            self.sentence.append(key.ref)
            return {"type": "add", "id": key.ref, "speech": self.icons[key.ref].speech}
        if k == "tab":
            changed = key.ref != self.category
            self.set_category(key.ref)
            return {"type": "category", "id": key.ref, "changed": changed}
        if k == "speak":
            return {"type": "speak", "text": self.sentence_text(), "n": len(self.sentence)}
        if k == "delete":
            removed = self.sentence.pop() if self.sentence else None
            return {"type": "delete", "id": removed}
        if k == "clear":
            n = len(self.sentence)
            self.sentence = []
            return {"type": "clear", "n": n}
        if k == "prev":
            self.page = max(0, self.page - 1)
            return {"type": "page", "page": self.page}
        if k == "next":
            self.page = min(self.page_count - 1, self.page + 1)
            return {"type": "page", "page": self.page}
        return {"type": "none"}
