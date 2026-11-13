"""Carga de config.json con valores por defecto."""
import copy
import json
import os

DEFAULTS = {
    "participant_id": "P01",
    "sessionID": 1,
    "input_mode": "mouse",          # "mouse" o "tobii"
    "dwell_time_ms": 800,
    "fullscreen": False,
    "window_size": [1440, 900],
    "fps": 60,
    "start_page": "necesidades",
    "grid": {"columns": 5, "rows": 4},
    "speech": {
        "enabled": True,
        "speak_on_select": True,    # decir cada pictograma al elegirlo
        "language": "es",
        "rate": 0,                  # -10 (lento) ... 10 (rapido), solo Windows
        "volume": 100,
    },
    "feedback": {
        "selection_flash_ms": 350,
        "hysteresis_px": 14,        # tolerancia al salir del borde de una tecla
        "sentence_max_items": 12,
    },
    "log_dir": "logs",
    "log_samples": True,
    "colors": {
        "background": "#ffffff",
        "ink": "#191919",
        "border": "#c7c7c7",
        "focus": "#795000",
        "focus_background": "#fff1c9",
        "progress_track": "#e2d8be",
        "selected": "#2e7d32",
        "panel": "#f2f2f2",
    },
    "tobii": {
        "launch_bridge": True,
        "bridge_executable": "sdk_bridge/windows/build/gaze_server.exe",
        "bridge_cwd": "sdk_bridge/windows",
        "udp_ip": "127.0.0.1",
        "udp_port": 5005,
        "source_screen_width_px": 1920,
        "source_screen_height_px": 1200,
        "sample_stale_after_ms": 150,
        "treat_zero_zero_as_invalid": True,
        "startup_wait_ms": 1200,
        "show_pointer": False,
    },
}


def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path):
    over = {}
    if path and os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as fh:
            over = json.load(fh)
    cfg = deep_merge(DEFAULTS, over)
    if cfg["input_mode"] not in ("mouse", "tobii"):
        raise ValueError("input_mode debe ser 'mouse' o 'tobii' (es %r)" % cfg["input_mode"])
    if cfg["dwell_time_ms"] < 100:
        raise ValueError("dwell_time_ms demasiado bajo")
    return cfg


def rgb(value):
    """'#rrggbb' -> (r, g, b)."""
    if isinstance(value, (tuple, list)):
        return tuple(int(v) for v in value[:3])
    v = value.lstrip("#")
    return (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16))
