import os
import tempfile
import unittest

import pygame

from tests import helpers
import picto
from picto import registry


class PictoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.display.init()
        pygame.display.set_mode((1, 1))

    def test_there_are_many_pictograms(self):
        board = [i for i in picto.ICONS if not i.startswith("ui_")]
        self.assertGreaterEqual(len(board), 100)

    def test_every_pictogram_draws_something_visible_and_inside_canvas(self):
        for pid in picto.ICONS:
            s = picto.render(pid, 128)
            self.assertEqual(s.get_size(), (128, 128))
            bbox = s.get_bounding_rect(min_alpha=40)
            area = bbox.w * bbox.h
            self.assertGreater(area, 128 * 128 * 0.12, pid)
            self.assertGreater(pygame.mask.from_surface(s, 40).count(), 128 * 128 * 0.08, pid)

    def test_labels_unique_among_board_pictograms(self):
        labels = {}
        for pid, ic in picto.ICONS.items():
            if pid.startswith("ui_"):
                continue
            self.assertTrue(ic.label.strip(), pid)
            labels.setdefault(ic.label, []).append(pid)
        self.assertEqual({k: v for k, v in labels.items() if len(v) > 1}, {})

    def test_cache_returns_same_surface(self):
        self.assertIs(picto.render("comer", 100), picto.render("comer", 100))

    def test_duplicate_id_rejected(self):
        with self.assertRaises(ValueError):
            registry.icon("comer", "X")(lambda c: None)

    def test_png_override(self):
        tmp = tempfile.mkdtemp()
        img = pygame.Surface((40, 20), pygame.SRCALPHA)
        img.fill((255, 0, 0, 255))
        pygame.image.save(img, os.path.join(tmp, "comer.png"))
        old = registry.OVERRIDE_DIR
        registry.OVERRIDE_DIR = tmp
        try:
            registry.clear_cache()
            s = picto.render("comer", 100)
            self.assertEqual(s.get_at((50, 50))[:3], (255, 0, 0))     # centro: el PNG
            self.assertEqual(s.get_at((50, 5))[3], 0)                 # franja superior: transparente
            self.assertNotEqual(picto.render("beber", 100).get_at((50, 50))[:3], (255, 0, 0))
        finally:
            registry.OVERRIDE_DIR = old
            registry.clear_cache()


if __name__ == "__main__":
    unittest.main()
