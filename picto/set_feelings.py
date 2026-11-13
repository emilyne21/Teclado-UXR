"""Emociones y estados."""
from .draw import *          # noqa: F401,F403
from .draw import arc_pts
from .registry import icon


def _emo(c, mood, fill, extra=None):
    c.circle((50, 52), 40, fill, INK, 3.6)
    face_features(c, 50, 52, 40, mood)
    if extra:
        extra(c)


@icon("feliz", "FELIZ", "feliz")
def feliz(c):
    _emo(c, 'happy', YELLOW)
    c.shine([(26, 34), (32, 26)], 3)


@icon("risa", "REÍR", "reír")
def risa(c):
    _emo(c, 'laugh', YELLOW)
    c.drop(14, 36, 7, LBLUE, BLUE, 2)
    c.drop(88, 36, 7, LBLUE, BLUE, 2)


@icon("triste", "TRISTE", "triste")
def triste(c):
    _emo(c, 'sad', LBLUE)


@icon("enfadado", "ENFADADO", "enfadado")
def enfadado(c):
    _emo(c, 'angry', (244, 120, 90))
    for (x, y, s) in ((82, 18, 8), (16, 20, 6)):
        c.path([(x - s, y), (x - s * 0.3, y), (x - s * 0.3, y - s)], 2.6, RED)
        c.path([(x + s, y), (x + s * 0.3, y), (x + s * 0.3, y - s)], 2.6, RED)
        c.path([(x - s, y + 2), (x - s * 0.3, y + 2), (x - s * 0.3, y + s + 2)], 2.6, RED)
        c.path([(x + s, y + 2), (x + s * 0.3, y + 2), (x + s * 0.3, y + s + 2)], 2.6, RED)


@icon("miedo", "MIEDO", "miedo")
def miedo(c):
    _emo(c, 'scared', LPURPLE)
    for x in (10, 90):
        c.path([(x, 40), (x + (3 if x < 50 else -3), 46), (x, 52), (x + (3 if x < 50 else -3), 58)], 2.4, PURPLE)


@icon("sorpresa", "SORPRESA", "sorpresa")
def sorpresa(c):
    _emo(c, 'surprised', YELLOW)
    c.line((84, 10), (92, 4), 2.8, ORANGE)
    c.line((88, 22), (97, 20), 2.8, ORANGE)
    c.line((16, 10), (8, 4), 2.8, ORANGE)
    c.line((12, 22), (3, 20), 2.8, ORANGE)


@icon("cansado", "CANSADO", "cansado")
def cansado(c):
    _emo(c, 'tired', (190, 200, 224))
    for (x, y, s) in ((78, 20, 5.4), (88, 10, 4)):
        c.path([(x - s, y - s), (x + s, y - s), (x - s, y + s), (x + s, y + s)], 2.4, PURPLE)


@icon("aburrido", "ABURRIDO", "aburrido")
def aburrido(c):
    _emo(c, 'bored', (232, 214, 176))
    c.path([(78, 12), (82, 10), (86, 12), (84, 16), (80, 18)], 2.2, DGREY, smooth=True)


@icon("carino", "CARIÑO", "cariño")
def carino(c):
    _emo(c, 'love', LPINK)
    c.heart(86, 14, 12, RED, INK, 1.8)
    c.heart(14, 18, 9, PINK, INK, 1.6)


@icon("enfermo", "ENFERMO", "me encuentro mal")
def enfermo(c):
    _emo(c, 'sick', (186, 224, 150))
    c.drop(18, 30, 6, LBLUE, BLUE, 1.6)


@icon("tranquilo", "TRANQUILO", "tranquilo")
def tranquilo(c):
    _emo(c, 'calm', (186, 232, 200))
    c.path([(12, 14), (20, 10), (28, 14)], 2.6, GREEN)
    c.path([(72, 10), (80, 6), (88, 10)], 2.6, GREEN)


@icon("nervioso", "NERVIOSO", "nervioso")
def nervioso(c):
    _emo(c, 'nervous', (250, 224, 150))
    c.path([(8, 70), (12, 66), (8, 62), (12, 58)], 2.4, ORANGE)
    c.path([(92, 70), (88, 66), (92, 62), (88, 58)], 2.4, ORANGE)


@icon("verguenza", "VERGÜENZA", "vergüenza")
def verguenza(c):
    _emo(c, 'shy', LPINK)
    c.path([(18, 26), (22, 22)], 2.2, RED)
    c.path([(82, 26), (78, 22)], 2.2, RED)
