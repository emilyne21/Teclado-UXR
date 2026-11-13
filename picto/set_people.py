"""Personas."""
from .draw import *          # noqa: F401,F403
from .draw import arc_pts
from .registry import icon


def small_bust(c, cx, s, **kw):
    """Busto reducido; el centro de los hombros queda siempre en y = 90."""
    with c.at(cx - 50 * s, 90 - 90 * s, s):
        bust(c, 50, 38, 19, **kw)


@icon("tu", "TÚ", "tú")
def tu(c):
    bust(c, 66, 36, 19, shirt=GREEN, hair=HAIR_BLACK, style='short', mood='happy')
    # mano que señala al otro
    c.rect(8, 62, 22, 22, SKIN, INK, 2.2, 8)
    c.rect(24, 66, 30, 8, SKIN, INK, 2.2, 4)
    c.rect(10, 56, 16, 9, SKIN, INK, 2.2, 4)
    for y in (72, 78):
        c.line((12, y), (24, y), 1.4, SKIN_D)


@icon("mama", "MAMÁ", "mamá")
def mama(c):
    bust(c, 50, 38, 19, shirt=PINK, hair=HAIR, style='long', mood='happy')
    for s in (-1, 1):
        c.circle((50 + s * 18.6, 46), 2.2, YELLOW, INK, 1.2)


@icon("papa", "PAPÁ", "papá")
def papa(c):
    bust(c, 50, 38, 19, shirt=BLUE, hair=HAIR_BLACK, style='short', mood='happy', beard=True)


@icon("hermano", "HERMANOS", "mis hermanos")
def hermano(c):
    small_bust(c, 30, 0.86, shirt=GREEN, hair=HAIR, style='short', mood='happy')
    small_bust(c, 72, 0.64, shirt=ORANGE, hair=HAIR_BLOND, style='pigtails', mood='happy')


@icon("abuelo", "ABUELO", "abuelo")
def abuelo(c):
    bust(c, 50, 38, 19, shirt=BROWN, hair=HAIR_GREY, style='short', mood='happy', glasses=True)
    c.path([(40, 54), (46, 51), (54, 51), (60, 54)], 2.6, HAIR_GREY)


@icon("abuela", "ABUELA", "abuela")
def abuela(c):
    bust(c, 50, 38, 19, shirt=PURPLE, hair=HAIR_GREY, style='bun', mood='happy', glasses=True)
    c.path([(38, 66), (50, 76), (62, 66)], 2.2, YELLOW)
    c.circle((50, 77), 2.6, WHITE, INK, 1.2)


@icon("amigo", "AMIGO", "amigo")
def amigo(c):
    small_bust(c, 28, 0.72, shirt=BLUE, hair=HAIR_BLACK, style='short', mood='happy')
    small_bust(c, 72, 0.72, shirt=PINK, hair=HAIR_RED, style='bun', mood='happy')
    c.heart(50, 26, 24, RED, INK, 2.6)
    c.shine([(40, 18), (44, 14)], 1.8)


@icon("profe", "PROFE", "el profe")
def profe(c):
    c.rect(40, 6, 56, 42, BROWN, INK, 2.6, 4)
    c.rect(44, 10, 48, 34, DGREEN, None, 1, 2)
    c.path([(50, 20), (58, 20)], 2.2, WHITE)
    c.path([(54, 16), (54, 24)], 2.2, WHITE)
    c.path([(64, 20), (72, 20)], 2.2, WHITE)
    c.path([(50, 34), (84, 34)], 2.2, WHITE)
    c.path([(50, 39), (70, 39)], 2.2, WHITE)
    bust(c, 32, 44, 18, shirt=TEAL, hair=HAIR, style='bun', mood='happy', glasses=True)
    c.line((54, 80), (80, 54), 2.6, LBROWN)


@icon("medico", "MÉDICO", "el médico")
def medico(c):
    bust(c, 50, 38, 19, shirt=WHITE, hair=HAIR_BLACK, style='short', mood='happy')
    c.poly([(40, 64), (50, 90), (60, 64)], LBLUE, INK, 1.8)
    c.path([(37, 64), (36, 78), (46, 88), (54, 88), (64, 78), (63, 64)], 2.4, DGREY, smooth=True)
    c.circle((50, 91), 4.2, GREY, INK, 1.8)
    c.rect(66, 80, 14, 14, RED, INK, 1.6, 2)
    c.rect(71.4, 82, 3.2, 10, WHITE, None)
    c.rect(68, 85.4, 10, 3.2, WHITE, None)
    c.poly(arc_pts(50, 28, 17, 11, 185, 355, 14), GREEN, INK, 2.2)
    c.rect(33, 27, 34, 5, GREEN, INK, 2.0, 2)


@icon("nino", "NIÑO", "el niño")
def nino(c):
    bust(c, 50, 38, 19, shirt=BLUE, hair=HAIR, style='short', mood='happy')


@icon("nina", "NIÑA", "la niña")
def nina(c):
    bust(c, 50, 38, 19, shirt=PINK, hair=HAIR_BLACK, style='pigtails', mood='happy')
    for s in (-1, 1):
        c.rect(50 + s * 26 - 2, 22, 4, 8, RED, INK, 1.2, 1)


@icon("bebe", "BEBÉ", "el bebé")
def bebe(c):
    c.ellipse((50, 96), 28, 20, LYELLOW, INK, 2.6)
    c.circle((50, 44), 24, SKIN, INK, 2.8)
    c.circle((26.5, 46), 4.5, SKIN, INK, 1.6)
    c.circle((73.5, 46), 4.5, SKIN, INK, 1.6)
    c.path([(46, 21), (48, 14), (55, 12), (58, 17), (53, 20)], 2.6, HAIR, smooth=True)
    c.circle((38, 42), 2.8, INK, None)
    c.circle((62, 42), 2.8, INK, None)
    c.ellipse((31, 52), 4.2, 2.6, (255, 160, 160), None)
    c.ellipse((69, 52), 4.2, 2.6, (255, 160, 160), None)
    c.circle((50, 56), 5.4, LBLUE, INK, 2.0)
    c.circle((50, 56), 2.2, WHITE, None)
    c.arc((50, 64), 7, 20, 160, 2.2, LBLUE)
