"""Cuerpo y salud."""
import math

from .draw import *          # noqa: F401,F403
from .draw import arc_pts
from .registry import icon


def _ouch(c, x, y, s=1.0):
    """Estallido rojo que marca dónde duele."""
    with c.at(x, y, s):
        c.poly(star_pts(0, 0, 13, 6, 8, -90), RED, INK, 2.2)
        c.poly(star_pts(0, 0, 7, 3.4, 8, -60), YELLOW, None)


@icon("duele", "ME DUELE", "me duele")
def duele(c):
    figure(c, (50, 22), 12, (50, 40), (50, 66),
           arms=[[(50, 42), (36, 52), (30, 64)], [(50, 42), (64, 52), (70, 64)]],
           legs=[[(47, 66), (46, 80), (45, 93)], [(53, 66), (54, 80), (55, 93)]],
           shirt=ORANGE, pants=DBLUE, mood='sad', tw=16)
    _ouch(c, 82, 40, 1.1)
    _ouch(c, 24, 80, 0.8)
    c.line((16, 24), (24, 30), 2.6, RED)
    c.line((84, 22), (76, 28), 2.6, RED)


@icon("cabeza", "ME DUELE LA CABEZA", "me duele la cabeza")
def cabeza(c):
    bust(c, 50, 46, 21, shirt=GREEN, hair=HAIR, style='short', mood='sad')
    _ouch(c, 78, 20, 1.2)
    _ouch(c, 22, 18, 0.8)
    c.path([(32, 30), (36, 22)], 2.4, RED)


@icon("tripa", "ME DUELE LA TRIPA", "me duele la tripa")
def tripa(c):
    figure(c, (50, 22), 12, (50, 40), (50, 66),
           arms=[[(50, 42), (36, 52), (45, 60)], [(50, 42), (64, 52), (55, 60)]],
           legs=[[(47, 66), (46, 80), (45, 93)], [(53, 66), (54, 80), (55, 93)]],
           shirt=YELLOW, pants=DBLUE, mood='sad', tw=18)
    _ouch(c, 50, 54, 1.0)
    c.path([(24, 52), (20, 58), (24, 64)], 2.4, RED)
    c.path([(76, 52), (80, 58), (76, 64)], 2.4, RED)


@icon("garganta", "ME DUELE LA GARGANTA", "me duele la garganta")
def garganta(c):
    bust(c, 50, 42, 19, shirt=BLUE, hair=HAIR_BLACK, style='short', mood='sad')
    c.path([(36, 66), (50, 72), (64, 66)], 6, (230, 90, 90), smooth=True)
    _ouch(c, 50, 76, 1.0)
    hand_open(c, 80, 84, 0.9, -20)


@icon("fiebre", "FIEBRE", "tengo fiebre")
def fiebre(c):
    c.rect(40, 6, 20, 64, WHITE, INK, 3.2, 10)
    c.circle((50, 78), 16, RED, INK, 3.2)
    c.rect(46, 30, 8, 48, RED, None)
    c.circle((50, 78), 11, RED, None)
    for y in (18, 28, 38, 48, 58):
        c.line((60, y), (68, y), 2.4, INK)
    for y in (18, 28, 38, 48, 58):
        c.line((32, y), (40, y), 2.4, INK) if False else None
    c.path([(78, 28), (82, 22), (86, 28), (90, 22)], 2.4, ORANGE)
    c.path([(78, 44), (82, 38), (86, 44), (90, 38)], 2.4, ORANGE)


@icon("medicina", "MEDICINA", "la medicina")
def medicina(c):
    c.rect(52, 28, 38, 60, ORANGE, INK, 3, 6)
    c.rect(56, 14, 30, 16, WHITE, INK, 3, 4)
    c.rect(56, 44, 30, 28, WHITE, INK, 2.4, 2)
    c.rect(68, 48, 6, 20, RED, None)
    c.rect(61, 55, 20, 6, RED, None)
    with c.at(28, 70, 1, -30):
        c.rect(-17, -9, 34, 18, WHITE, INK, 3, 9)
        c.rect(0, -9, 17, 18, RED, INK, 3, 9)
        c.rect(0, -9, 8, 18, RED, None)
        c.line((0, -9), (0, 9), 2.4)
    c.circle((20, 30), 9, WHITE, INK, 2.6)
    c.line((14, 30), (26, 30), 1.8)


@icon("tos", "TOS", "tengo tos")
def tos(c):
    bust(c, 40, 44, 19, shirt=PURPLE, hair=HAIR, style='short', mood='sick')
    hand_open(c, 64, 62, 1.0, -75)
    for (x, y, s) in ((82, 28, 1), (90, 50, 0.8)):
        c.line((x - 4 * s, y - 8 * s), (x + 4 * s, y - 14 * s), 2.6, GREY)
        c.line((x - 4 * s, y + 2 * s), (x + 8 * s, y), 2.6, GREY)
        c.line((x - 4 * s, y + 12 * s), (x + 4 * s, y + 18 * s), 2.6, GREY)


@icon("frio", "FRÍO", "tengo frío")
def frio(c):
    bust(c, 46, 42, 19, shirt=BLUE, hair=HAIR_BLACK, style='short', mood='sad')
    c.circle((46, 42), 19, (176, 214, 250), None) if False else None
    c.rect(30, 62, 32, 10, RED, INK, 2.6, 5)
    c.rect(54, 66, 10, 22, RED, INK, 2.6, 3)
    for (x, y, s) in ((84, 22, 1.0), (14, 28, 0.8), (86, 62, 0.8)):
        for a in (0, 60, 120):
            r = math.radians(a)
            c.line((x - 9 * s * math.cos(r), y - 9 * s * math.sin(r)),
                   (x + 9 * s * math.cos(r), y + 9 * s * math.sin(r)), 2.6, LBLUE)
            c.line((x - 9 * s * math.cos(r), y - 9 * s * math.sin(r)),
                   (x + 9 * s * math.cos(r), y + 9 * s * math.sin(r)), 1.2, BLUE)


@icon("calor", "CALOR", "tengo calor")
def calor(c):
    c.circle((78, 22), 12, YELLOW, INK, 2.6)
    for a in range(0, 360, 45):
        r = math.radians(a)
        c.line((78 + 16 * math.cos(r), 22 + 16 * math.sin(r)), (78 + 22 * math.cos(r), 22 + 22 * math.sin(r)), 2.6,
               ORANGE)
    c.circle((40, 56), 31, (250, 150, 120), INK, 3.4)
    face_features(c, 40, 56, 31, 'tired')
    c.drop(14, 38, 7, LBLUE, BLUE, 1.8)
    c.drop(68, 64, 7, LBLUE, BLUE, 1.8)
    c.drop(60, 88, 6, LBLUE, BLUE, 1.8)


@icon("hambre", "HAMBRE", "tengo hambre")
def hambre(c):
    bust(c, 36, 46, 19, shirt=ORANGE, hair=HAIR, style='short', mood='eat')
    c.circle((74, 22), 20, WHITE, INK, 2.6)
    c.circle((58, 42), 4, WHITE, INK, 2)
    c.circle((52, 50), 2.4, WHITE, INK, 1.6)
    c.line((66, 12), (66, 32), 2.6, DGREY)
    c.line((64, 12), (64, 18), 2.4, DGREY)
    c.line((68, 12), (68, 18), 2.4, DGREY)
    c.line((82, 12), (82, 32), 2.6, DGREY)
    c.poly([(80, 12), (86, 12), (86, 24), (80, 24)], DGREY, None, 1)


@icon("sed", "SED", "tengo sed")
def sed(c):
    bust(c, 34, 46, 19, shirt=TEAL, hair=HAIR_BLACK, style='short', mood='tired')
    c.circle((74, 24), 20, WHITE, INK, 2.6)
    c.circle((58, 44), 4, WHITE, INK, 2)
    c.circle((52, 52), 2.4, WHITE, INK, 1.6)
    c.poly([(64, 12), (84, 12), (81, 34), (67, 34)], WHITE, INK, 2.4)
    c.poly([(65.4, 20), (82.6, 20), (80.6, 32.6), (68.4, 32.6)], LBLUE, None)


@icon("tirita", "ME HE HECHO DAÑO", "me he hecho daño")
def tirita(c):
    with c.at(50, 50, 1.25, -35):
        c.rect(-34, -12, 68, 24, (240, 200, 150), INK, 3, 12)
        c.rect(-12, -12, 24, 24, (252, 226, 190), INK, 2.4, 1)
        for (x, y) in ((-26, -4), (-26, 4), (-20, 0), (26, -4), (26, 4), (20, 0)):
            c.circle((x, y), 1.4, (200, 150, 100), None)
    _ouch(c, 82, 22, 0.8)
    c.sparkle(18, 80, 5, YELLOW)
