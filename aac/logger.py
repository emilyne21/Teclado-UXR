import csv
import json
import os
import time

EVENT_COLS = ["t_ms", "event", "page", "target", "detail"]
SELECTION_COLS = ["t_ms", "seq", "page", "kind", "target", "label", "dwell_ms", "sentence_len", "sentence"]
SAMPLE_COLS = ["t_ms", "x_px", "y_px", "valid", "target"]


class SessionLogger(object):
    def __init__(self, cfg, base_dir, log_dir=None, stamp=None):
        self.cfg = cfg
        log_dir = log_dir or cfg.get("log_dir", "logs")
        if not os.path.isabs(log_dir):
            log_dir = os.path.join(base_dir, log_dir)
        os.makedirs(log_dir, exist_ok=True)
        self.log_dir = log_dir
        stamp = stamp or time.strftime("%Y%m%d_%H%M%S")
        self.base = "%s_S%s_%s" % (cfg.get("participant_id", "P"), cfg.get("sessionID", 1), stamp)
        self.paths = {k: os.path.join(log_dir, "%s_%s.log" % (self.base, k))
                      for k in ("events", "selections", "samples")}
        self.paths["config"] = os.path.join(log_dir, self.base + "_config.json")
        with open(self.paths["config"], "w", encoding="utf-8") as fh:
            json.dump(cfg, fh, indent=2, ensure_ascii=False)
        self._files = {}
        self._writers = {}
        self._open("events", EVENT_COLS)
        self._open("selections", SELECTION_COLS)
        self.samples_on = bool(cfg.get("log_samples", True))
        if self.samples_on:
            self._open("samples", SAMPLE_COLS)
        self.seq = 0
        self._last_flush = time.monotonic()
        self.closed = False

    def _open(self, name, cols):
        fh = open(self.paths[name], "w", newline="", encoding="utf-8")
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        self._files[name] = fh
        self._writers[name] = w

    def event(self, t_ms, name, page="", target="", detail=""):
        if self.closed:
            return
        self._writers["events"].writerow([int(t_ms), name, page, target, detail])
        self._files["events"].flush()

    def selection(self, t_ms, page, kind, target, label, dwell_ms, sentence):
        if self.closed:
            return 0
        self.seq += 1
        self._writers["selections"].writerow([int(t_ms), self.seq, page, kind, target, label,
                                              int(dwell_ms), len(sentence), " ".join(sentence)])
        self._files["selections"].flush()
        return self.seq

    def sample(self, t_ms, x, y, valid, target):
        if self.closed or not self.samples_on:
            return
        self._writers["samples"].writerow([
            int(t_ms), "" if x is None else int(round(x)), "" if y is None else int(round(y)),
            1 if valid else 0, target or ""])
        if time.monotonic() - self._last_flush > 1.0:
            self._files["samples"].flush()
            self._last_flush = time.monotonic()

    def close(self):
        if self.closed:
            return
        self.closed = True
        for fh in self._files.values():
            try:
                fh.flush()
                fh.close()
            except Exception:
                pass
