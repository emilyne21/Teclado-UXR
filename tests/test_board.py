import unittest

import pygame

from tests import helpers
import picto
from aac import pages
from aac.board import Board
from aac.config import load_config
import os


def make_board(size=(1440, 900), **over):
    cfg = load_config(os.path.join(helpers.ROOT, "config.json"))
    cfg.update(over)
    return Board(size, cfg, picto.ICONS)


class BoardTests(unittest.TestCase):
    def test_every_page_item_has_a_pictogram(self):
        self.assertEqual(pages.check(picto.ICONS), [])

    def test_no_duplicates_inside_a_page_and_page_fits_without_paging(self):
        for c in pages.CATEGORIES:
            self.assertEqual(len(c.items), len(set(c.items)), c.id)
            self.assertLessEqual(len(c.items), 20, c.id)

    def test_keys_inside_window_and_not_overlapping(self):
        for size in ((1440, 900), (1920, 1200), (1280, 720), (1024, 768)):
            b = make_board(size)
            for cat in pages.CATEGORIES:
                b.set_category(cat.id)
                keys = b.keys()
                W, H = size
                for k in keys:
                    self.assertTrue(pygame.Rect(0, 0, W, H).contains(k.rect), (size, cat.id, k.uid, k.rect))
                for i, a in enumerate(keys):
                    for c in keys[i + 1:]:
                        self.assertFalse(a.rect.colliderect(c.rect), (size, cat.id, a.uid, c.uid))

    def test_cells_are_big_enough_for_eye_tracking(self):
        b = make_board((1440, 900))
        for cat in pages.CATEGORIES:
            b.set_category(cat.id)
            for k in b.keys():
                if k.kind == "picto":
                    self.assertGreaterEqual(k.rect.w, 200)
                    self.assertGreaterEqual(k.rect.h, 160)

    def test_hit_and_miss(self):
        b = make_board()
        k = b.key_by_uid("picto:comer")
        self.assertEqual(b.hit(*k.rect.center).uid, "picto:comer")
        self.assertIsNone(b.hit(1, 899))

    def test_hysteresis_keeps_current_key_just_outside_border(self):
        b = make_board()
        k = b.key_by_uid("picto:comer")
        x, y = k.rect.right + 8, k.rect.centery
        self.assertIsNone(b.hit(x, y))                              # sin tolerancia, fuera
        self.assertEqual(b.hit(x, y, prefer="picto:comer", margin=14).uid, "picto:comer")
        other = b.hit(k.rect.right + 30, y, prefer="picto:comer", margin=14)      # ya en la vecina
        self.assertNotEqual(getattr(other, "uid", None), "picto:comer")

    def test_add_delete_clear_and_sentence_text(self):
        b = make_board()
        for uid in ("picto:yo", "picto:quiero", "picto:comer"):
            b.activate(b.key_by_uid(uid))
        self.assertEqual(b.sentence, ["yo", "quiero", "comer"])
        self.assertEqual(b.sentence_text(), "Yo quiero comer.")
        res = b.activate(b.key_by_uid("btn:delete"))
        self.assertEqual(res["id"], "comer")
        self.assertEqual(b.sentence, ["yo", "quiero"])
        res = b.activate(b.key_by_uid("btn:clear"))
        self.assertEqual(res["n"], 2)
        self.assertEqual(b.sentence, [])
        self.assertEqual(b.sentence_text(), "")
        self.assertEqual(b.activate(b.key_by_uid("btn:delete"))["id"], None)

    def test_bano_is_spoken_as_ir_al_bano(self):
        b = make_board()
        b.activate(b.key_by_uid("picto:quiero"))
        b.activate(b.key_by_uid("picto:bano"))
        self.assertEqual(b.sentence_text(), "Quiero ir al baño.")

    def test_sentence_limit(self):
        b = make_board()
        k = b.key_by_uid("picto:yo")
        for _ in range(12):
            self.assertEqual(b.activate(k)["type"], "add")
        self.assertEqual(b.activate(k)["type"], "full")
        self.assertEqual(len(b.sentence), 12)

    def test_tabs_change_category_and_keep_sentence(self):
        b = make_board()
        b.activate(b.key_by_uid("picto:quiero"))
        res = b.activate(b.key_by_uid("tab:comida"))
        self.assertEqual((res["type"], res["changed"]), ("category", True))
        self.assertEqual(b.category, "comida")
        self.assertIsNotNone(b.key_by_uid("picto:manzana"))
        self.assertIsNone(b.key_by_uid("picto:comer"))
        self.assertEqual(b.sentence, ["quiero"])
        self.assertFalse(b.activate(b.key_by_uid("tab:comida"))["changed"])

    def test_visible_sentence_scrolls(self):
        b = make_board()
        n = b.slot_n
        b.sentence = ["yo"] * (n + 3)
        shown, more = b.visible_sentence()
        self.assertEqual(len(shown), n)
        self.assertTrue(more)

    def test_paging_with_long_category(self):
        extra = pages.Category("larga", "LARGA", "yo", (10, 10, 10), list(picto.ICONS)[:45])
        pages.CATEGORIES.append(extra)
        pages.BY_ID["larga"] = extra
        try:
            b = make_board()
            b.set_category("larga")
            self.assertEqual(b.per_page, 18)
            self.assertEqual(b.page_count, 3)
            self.assertIsNone(b.key_by_uid("nav:prev"))
            self.assertIsNotNone(b.key_by_uid("nav:next"))
            b.activate(b.key_by_uid("nav:next"))
            self.assertEqual(b.page, 1)
            self.assertIsNotNone(b.key_by_uid("nav:prev"))
            b.activate(b.key_by_uid("nav:next"))
            self.assertEqual(b.page, 2)
            self.assertIsNone(b.key_by_uid("nav:next"))
            self.assertEqual(len([k for k in b.keys() if k.kind == "picto"]), 45 - 36)
            b.activate(b.key_by_uid("nav:prev"))
            self.assertEqual(b.page, 1)
        finally:
            pages.CATEGORIES.remove(extra)
            del pages.BY_ID["larga"]


if __name__ == "__main__":
    unittest.main()
