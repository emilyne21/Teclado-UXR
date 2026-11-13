import unittest

from tests import helpers  # noqa: F401
from aac.dwell import DwellTracker


class DwellTests(unittest.TestCase):
    def test_fires_at_threshold_not_before(self):
        d = DwellTracker(500)
        self.assertIsNone(d.update(0, "a"))
        self.assertIsNone(d.update(499, "a"))
        self.assertEqual(d.update(500, "a"), "select")

    def test_no_repeat_while_inside(self):
        d = DwellTracker(500)
        d.update(0, "a")
        self.assertEqual(d.update(500, "a"), "select")
        for t in range(520, 3000, 20):
            self.assertIsNone(d.update(t, "a"))

    def test_rearm_by_leaving_and_reentering(self):
        d = DwellTracker(500)
        d.update(0, "a")
        d.update(500, "a")
        d.update(600, None)
        d.update(620, "a")
        self.assertIsNone(d.update(1100, "a"))
        self.assertEqual(d.update(1120, "a"), "select")

    def test_invalid_sample_resets_progress(self):
        d = DwellTracker(500)
        d.update(0, "a")
        d.update(300, "a")
        d.update(320, "a", valid=False)
        self.assertEqual(d.progress(320), 0.0)
        self.assertIsNone(d.update(340, "a"))
        self.assertIsNone(d.update(800, "a"))
        self.assertEqual(d.update(840, "a"), "select")

    def test_changing_target_restarts(self):
        d = DwellTracker(500)
        d.update(0, "a")
        d.update(400, "b")
        self.assertIsNone(d.update(800, "b"))
        self.assertEqual(d.update(900, "b"), "select")

    def test_progress_values(self):
        d = DwellTracker(1000)
        d.update(0, "a")
        self.assertAlmostEqual(d.progress(250), 0.25)
        d.update(1000, "a")
        self.assertEqual(d.progress(1200), 1.0)

    def test_set_dwell(self):
        d = DwellTracker(500)
        d.set_dwell(200)
        d.update(0, "a")
        self.assertEqual(d.update(200, "a"), "select")


if __name__ == "__main__":
    unittest.main()
