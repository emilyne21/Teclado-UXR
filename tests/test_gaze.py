import socket
import unittest

from tests import helpers  # noqa: F401
from aac.gaze import GazeReceiver, parse_packet


class Clock(object):
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


class GazeTests(unittest.TestCase):
    def setUp(self):
        self.clk = Clock()
        self.g = GazeReceiver(src_w=1920, src_h=1200, stale_ms=150, clock=self.clk)

    def test_parse(self):
        self.assertEqual(parse_packet(b"123456,960,600\n"), (123456, 960.0, 600.0))
        self.assertIsNone(parse_packet(b"hola"))
        self.assertIsNone(parse_packet(b"1,2"))
        self.assertIsNone(parse_packet(b"a,b,c"))
        self.assertIsNone(parse_packet(b"1,nan,3"))
        self.assertIsNone(parse_packet(b"\xff\xfe"))

    def test_valid_sample_and_stale(self):
        self.clk.t = 1000
        self.assertTrue(self.g.feed(b"1,100,200"))
        self.assertEqual(self.g.sample(1100), (100.0, 200.0))
        self.assertIsNone(self.g.sample(1151))      # más vieja que 150 ms

    def test_zero_zero_is_invalid_and_overrides_previous(self):
        self.clk.t = 1000
        self.g.feed(b"1,100,200")
        self.clk.t = 1010
        self.g.feed(b"2,0,0")
        self.assertIsNone(self.g.sample(1020))

    def test_bad_packets_counted_and_ignored(self):
        self.clk.t = 1000
        self.g.feed(b"1,100,200")
        self.assertFalse(self.g.feed(b"basura"))
        self.assertEqual(self.g.bad_packets, 1)
        self.assertEqual(self.g.sample(1050), (100.0, 200.0))

    def test_to_window_scales_and_does_not_clamp(self):
        x, y = self.g.to_window((960, 600), (1440, 900))
        self.assertEqual((x, y), (720.0, 450.0))
        x, y = self.g.to_window((2078, -130), (1440, 900))
        self.assertGreater(x, 1440)
        self.assertLess(y, 0)

    def test_silent_for(self):
        self.g.started_ms = 0
        self.clk.t = 2500
        self.assertEqual(self.g.silent_for_ms(), 2500)
        self.g.feed(b"1,5,5", rx_ms=2400)
        self.assertEqual(self.g.silent_for_ms(), 100)

    def test_udp_loopback(self):
        g = GazeReceiver(ip="127.0.0.1", port=0)
        g.start()
        try:
            port = g.sock.getsockname()[1]
            tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            tx.sendto(b"10,300,400", ("127.0.0.1", port))
            tx.sendto(b"11,310,410", ("127.0.0.1", port))
            tx.sendto(b"xx", ("127.0.0.1", port))
            tx.close()
            import time
            time.sleep(0.05)
            n = g.poll()
            self.assertEqual(n, 3)
            self.assertEqual(g.sample(), (310.0, 410.0))
            self.assertEqual(g.bad_packets, 1)
        finally:
            g.close()


if __name__ == "__main__":
    unittest.main()
