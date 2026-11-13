import os

import pygame

from .draw import Canvas

ICONS = {}          # id -> Icon
_CACHE = {}         # (id, size) -> Surface
MASTER = 400        # tamaño del lienzo maestro antes de reducir

# Carpeta donde se pueden dejar PNG propios (p. ej. de ARASAAC) con el nombre <id>.png
OVERRIDE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "assets", "pictograms")


class Icon:
    __slots__ = ("id", "label", "speech", "fn")

    def __init__(self, id, label, speech, fn):
        self.id, self.label, self.speech, self.fn = id, label, speech, fn


def icon(id, label, speech=None):
    """Decorador: registra la función de dibujo de un pictograma."""
    def deco(fn):
        if id in ICONS:
            raise ValueError("pictograma duplicado: %s" % id)
        ICONS[id] = Icon(id, label, speech if speech else label.lower(), fn)
        return fn
    return deco


def get(id):
    return ICONS[id]


def _load_override(id, size):
    path = os.path.join(OVERRIDE_DIR, id + ".png")
    if not os.path.isfile(path):
        return None
    try:
        img = pygame.image.load(path).convert_alpha()
    except Exception:
        return None
    w, h = img.get_size()
    k = min(size / float(w), size / float(h))
    img = pygame.transform.smoothscale(img, (max(1, int(w * k)), max(1, int(h * k))))
    out = pygame.Surface((size, size), pygame.SRCALPHA)
    out.blit(img, ((size - img.get_width()) // 2, (size - img.get_height()) // 2))
    return out


def render(id, size):
    """Superficie cuadrada con el pictograma a `size` píxeles (con caché)."""
    key = (id, int(size))
    surf = _CACHE.get(key)
    if surf is not None:
        return surf
    surf = _load_override(id, int(size))
    if surf is None:
        cv = Canvas(MASTER)
        ICONS[id].fn(cv)
        surf = cv.surf
        if int(size) != MASTER:
            surf = pygame.transform.smoothscale(surf, (int(size), int(size)))
    _CACHE[key] = surf
    return surf


def clear_cache():
    _CACHE.clear()
