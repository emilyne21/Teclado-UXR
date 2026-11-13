import os
import sys
import tempfile

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from aac.config import load_config                       # noqa: E402
from aac.app import App                                  # noqa: E402
from aac.logger import SessionLogger                     # noqa: E402
from aac.speech import Speaker                           # noqa: E402


def make_app(mode="mouse", gaze=None, dwell=500, size=(1440, 900), **cfg_over):
    cfg = load_config(os.path.join(ROOT, "config.json"))
    cfg["dwell_time_ms"] = dwell
    cfg["speech"]["enabled"] = False
    cfg.update(cfg_over)
    tmp = tempfile.mkdtemp(prefix="picto_test_")
    logger = SessionLogger(cfg, ROOT, log_dir=tmp, stamp="TEST")
    app = App(cfg, ROOT, headless=True, mode=mode, gaze=gaze, logger=logger,
              speaker=Speaker(enabled=False), size=size)
    return app, tmp


def center(app, uid):
    return app.board.key_by_uid(uid).rect.center
