import csv
import glob
import os
import shutil
import unittest

from tests import helpers
from tests.helpers import make_app, center
from aac.gaze import GazeReceiver


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


class Clock(object):
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


def dwell_on(app, uid, t0, dur=None, dt=16):
    """Mantiene el puntero sobre la tecla y devuelve (t_final, número de selecciones)."""
    dur = app.dwell.dwell_ms + 100 if dur is None else dur
    pos = center(app, uid)
    n, t = 0, t0
    while t <= t0 + dur:
        if app.step(t, pos) == "select":
            n += 1
        t += dt
    return t, n


class MouseFlowTests(unittest.TestCase):
    def tearDown(self):
        if hasattr(self, "tmp"):
            shutil.rmtree(self.tmp, ignore_errors=True)

    def new(self, **kw):
        app, self.tmp = make_app(**kw)
        self.addCleanup(app.close)
        return app

    def test_mouse_has_dwell_without_click(self):
        app = self.new()
        _, n = dwell_on(app, "picto:comer", 1000)
        self.assertEqual(n, 1)
        self.assertEqual(app.board.sentence, ["comer"])

    def test_not_selected_before_dwell_time(self):
        app = self.new(dwell=800)
        _, n = dwell_on(app, "picto:comer", 1000, dur=700)
        self.assertEqual(n, 0)
        self.assertEqual(app.board.sentence, [])

    def test_no_repeat_and_rearm(self):
        app = self.new()
        t, n = dwell_on(app, "picto:comer", 1000, dur=3000)
        self.assertEqual(n, 1)
        self.assertEqual(app.step(t, (2, 899)), None)             # sale de la tecla
        t, n = dwell_on(app, "picto:comer", t + 50)
        self.assertEqual(n, 1)
        self.assertEqual(app.board.sentence, ["comer", "comer"])

    def test_pointer_outside_window_or_none_never_selects(self):
        app = self.new()
        for t in range(0, 3000, 16):
            self.assertIsNone(app.step(t, (-50, 100)))
            self.assertIsNone(app.step(t, None))
        self.assertEqual(app.board.sentence, [])

    def test_leaving_between_keys_resets_progress(self):
        app = self.new(dwell=800)
        pos = center(app, "picto:comer")
        for t in range(0, 600, 16):
            app.step(t, pos)
        app.step(620, (2, 899))
        self.assertEqual(app.dwell.progress(620), 0.0)
        n = 0
        for t in range(640, 1300, 16):
            n += app.step(t, pos) == "select"
        self.assertEqual(n, 0)

    def test_full_sentence_with_category_change_and_speak(self):
        app = self.new()
        t = 0
        for uid in ("picto:yo", "picto:quiero", "tab:comida", "picto:manzana"):
            t, n = dwell_on(app, uid, t + 300)
            self.assertEqual(n, 1, uid)
        self.assertEqual(app.board.category, "comida")
        self.assertEqual(app.board.sentence, ["yo", "quiero", "manzana"])
        t, n = dwell_on(app, "btn:speak", t + 300)
        self.assertEqual(n, 1)
        self.assertEqual(app.speaker.history[-1], "Yo quiero una manzana.")

    def test_speak_on_select_says_each_word(self):
        app = self.new()
        dwell_on(app, "picto:bano", 0)
        self.assertEqual(app.speaker.history, ["ir al baño"])

    def test_speak_on_select_can_be_disabled(self):
        app = self.new()
        app.cfg["speech"]["speak_on_select"] = False
        dwell_on(app, "picto:bano", 0)
        self.assertEqual(app.speaker.history, [])

    def test_delete_and_clear_buttons(self):
        app = self.new()
        t = 0
        for uid in ("picto:yo", "picto:quiero", "btn:delete"):
            t, _ = dwell_on(app, uid, t + 300)
        self.assertEqual(app.board.sentence, ["yo"])
        t, _ = dwell_on(app, "btn:clear", t + 300)
        self.assertEqual(app.board.sentence, [])

    def test_hysteresis_prevents_losing_key_on_jitter(self):
        app = self.new(dwell=800)
        k = app.board.key_by_uid("picto:comer")
        inside = k.rect.center
        edge = (k.rect.right + 6, k.rect.centery)                  # fuera, pero dentro de la tolerancia
        n, t = 0, 0
        while t < 1000:
            pos = edge if (t // 100) % 2 else inside
            n += app.step(t, pos) == "select"
            t += 16
        self.assertEqual(n, 1)

    def test_operator_keys(self):
        app = self.new(dwell=500)
        app.operator("dwell+")
        self.assertEqual(app.dwell.dwell_ms, 600)
        for _ in range(30):
            app.operator("dwell-")
        self.assertEqual(app.dwell.dwell_ms, 200)
        app.operator("category:bebida")
        self.assertEqual(app.board.category, "bebida")
        app.operator("speak")
        app.operator("delete")
        app.operator("clear")

    def test_dwell_progress_is_drawn_without_error(self):
        app = self.new()
        pos = center(app, "picto:comer")
        for t in range(0, 300, 16):
            app.step(t, pos)
            app.draw(t)
        app.overlay = True
        app.draw(300)

    def test_logs_have_expected_columns_and_content(self):
        app = self.new()
        t, _ = dwell_on(app, "picto:quiero", 0)
        t, _ = dwell_on(app, "picto:beber", t + 300)
        sel = None
        app.logger._files["selections"].flush()
        sel = rows(app.logger.paths["selections"])
        self.assertEqual([r["target"] for r in sel], ["quiero", "beber"])
        self.assertEqual([r["seq"] for r in sel], ["1", "2"])
        self.assertTrue(all(int(r["dwell_ms"]) >= 500 for r in sel))
        self.assertEqual(sel[-1]["sentence"], "quiero beber")
        self.assertEqual(sel[-1]["page"], "necesidades")
        t, _ = dwell_on(app, "btn:speak", t + 300)
        t, _ = dwell_on(app, "tab:comida", t + 300)
        app.close()
        sel = rows(app.logger.paths["selections"])
        self.assertEqual([(r["kind"], r["target"]) for r in sel[2:]], [("speak", "speak"), ("tab", "comida")])
        self.assertEqual(sel[-1]["page"], "necesidades")     # la pestaña estaba en la página de origen
        ev = rows(app.logger.paths["events"])
        self.assertEqual(ev[0]["event"], "session_start")
        self.assertEqual(ev[-1]["event"], "session_end")
        smp = rows(app.logger.paths["samples"])
        self.assertGreater(len(smp), 50)
        self.assertEqual(smp[0]["valid"], "1")
        self.assertTrue(os.path.isfile(app.logger.paths["config"]))

    def test_session_finish_closes_logger_once(self):
        app = self.new()
        app.close()
        app.close()
        self.assertTrue(app.logger.closed)


class TobiiFlowTests(unittest.TestCase):
    def setUp(self):
        self.clk = Clock()
        self.gaze = GazeReceiver(src_w=1920, src_h=1200, stale_ms=150, clock=self.clk)
        self.app, self.tmp = make_app(mode="tobii", gaze=self.gaze, size=(1440, 900))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.addCleanup(self.app.close)

    def send(self, t, x, y):
        self.clk.t = t
        self.gaze.feed(("%d,%d,%d" % (t * 1000, x, y)).encode(), rx_ms=t)

    def gaze_xy_for(self, uid):
        cx, cy = center(self.app, uid)
        return cx * 1920 / 1440.0, cy * 1200 / 900.0

    def test_gaze_selects_after_dwell(self):
        gx, gy = self.gaze_xy_for("picto:beber")
        sel, t = 0, 1000
        while t < 1800:
            self.send(t, gx, gy)
            s = self.gaze.sample(t)
            sel += self.app.step(t, self.gaze.to_window(s, self.app.size)) == "select"
            t += 16
        self.assertEqual(sel, 1)
        self.assertEqual(self.app.board.sentence, ["beber"])

    def test_zero_zero_and_stale_reset_dwell(self):
        gx, gy = self.gaze_xy_for("picto:beber")
        t = 1000
        sel = 0
        while t < 1400:
            self.send(t, gx, gy)
            s = self.gaze.sample(t)
            sel += self.app.step(t, self.gaze.to_window(s, self.app.size)) == "select"
            t += 16
        self.send(t, 0, 0)                                    # ojos no detectados
        self.assertIsNone(self.gaze.sample(t))
        self.assertIsNone(self.app.step(t, None))
        self.assertEqual(self.app.dwell.progress(t), 0.0)
        # muestra vieja (sin paquetes nuevos durante más de 150 ms)
        self.send(t + 20, gx, gy)
        self.assertIsNone(self.gaze.sample(t + 20 + 200))
        self.assertEqual(sel, 0)

    def test_gaze_outside_screen_selects_nothing(self):
        for i, (x, y) in enumerate(((2078, 600), (900, -130), (900, 1494), (-10, 100))):
            sel, t = 0, 1000 + i * 3000
            while t < 1000 + i * 3000 + 1500:
                self.send(t, x, y)
                s = self.gaze.sample(t)
                sel += self.app.step(t, self.gaze.to_window(s, self.app.size)) == "select"
                t += 16
            self.assertEqual(sel, 0, (x, y))

    def test_no_silent_fallback_to_mouse(self):
        import pygame
        pygame.mouse.set_pos(center(self.app, "picto:yo"))
        self.clk.t = 5000
        self.assertIsNone(self.app.read_pointer(5000))

    def test_banner_and_overlay_draw_when_no_signal(self):
        self.clk.t = 9000
        self.app.overlay = True
        self.app.draw(9000)


class PreviewTests(unittest.TestCase):
    def test_make_previews(self):
        from aac.preview import make_previews
        out = os.path.join(__import__("tempfile").mkdtemp(), "p")
        files = make_previews(helpers.load_config(os.path.join(helpers.ROOT, "config.json")), helpers.ROOT, out)
        self.assertEqual(len(files), 11)
        for f in files:
            self.assertGreater(os.path.getsize(f), 5000)
        shutil.rmtree(os.path.dirname(out), ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
