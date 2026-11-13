"""Respuestas y frases sociales."""
import math

from .draw import *          # noqa: F401,F403
from .draw import arc_pts
from .registry import icon


def qmark(c, x, y, s=1.0, col=BLUE, w=4.2):
    with c.at(x, y, s):
        c.arc((0, -8), 9, 150, 400, w + 2.4, INK)
        c.arc((0, -8), 9, 150, 400, w, col)
        c.line((6.4, -1.6), (0, 6), w + 2.4, INK)
        c.line((6.4, -1.6), (0, 6), w, col)
        c.line((0, 6), (0, 8), w + 2.4, INK)
        c.line((0, 6), (0, 8), w, col)
        c.circle((0, 17), 3.4, INK, None)
        c.circle((0, 17), 2.2, col, None)


@icon("si", "SÍ", "sí")
def si(c):
    c.circle((50, 50), 42, GREEN, INK, 3.6)
    c.path([(26, 52), (43, 69), (76, 32)], 11, INK)
    c.path([(26, 52), (43, 69), (76, 32)], 7, WHITE)


@icon("no", "NO", "no")
def no(c):
    c.circle((50, 50), 42, RED, INK, 3.6)
    c.line((31, 31), (69, 69), 11, INK)
    c.line((69, 31), (31, 69), 11, INK)
    c.line((31, 31), (69, 69), 7, WHITE)
    c.line((69, 31), (31, 69), 7, WHITE)


@icon("hola", "HOLA", "hola")
def hola(c):
    bust(c, 34, 44, 19, shirt=ORANGE, hair=HAIR_BLACK, style='short', mood='happy')
    hand_open(c, 76, 52, 1.5, 14)
    c.arc((76, 32), 18, 200, 340, 3, BLUE)
    c.arc((78, 28), 26, 215, 330, 3, LBLUE)
    c.sparkle(90, 78, 5, YELLOW)


@icon("adios", "ADIÓS", "adiós")
def adios(c):
    figure(c, (40, 28), 11, (40, 43), (40, 66),
           arms=[[(40, 45), (28, 40), (24, 24)]],
           legs=[[(40, 66), (46, 80), (46, 92)], [(40, 66), (34, 80), (32, 92)]],
           shirt=BLUE, pants=DBLUE, mood='happy')
    c.arc((18, 20), 8, 150, 270, 3, ORANGE)
    c.arc((14, 20), 15, 160, 270, 3, LORANGE)
    c.path([(62, 60), (84, 60)], 5, INK)
    c.path([(62, 60), (84, 60)], 2.6, GREEN)
    c.poly([(94, 60), (82, 52), (82, 68)], GREEN, INK, 2.2)


@icon("gracias", "GRACIAS", "gracias")
def gracias(c):
    c.heart(50, 40, 40, RED, INK, 3)
    c.shine([(32, 28), (38, 22)], 3)
    hand_open(c, 22, 78, 1.35, 52)
    hand_open(c, 78, 78, 1.35, -52)
    c.sparkle(88, 14, 6, YELLOW)
    c.sparkle(12, 16, 5, YELLOW)


@icon("porfavor", "POR FAVOR", "por favor")
def porfavor(c):
    bust(c, 50, 38, 19, shirt=TEAL, hair=HAIR, style='short', mood='shy')
    hand_open(c, 44, 92, 1.4, 14)
    hand_open(c, 56, 92, 1.4, -14)
    c.sparkle(86, 26, 5, YELLOW)
    c.sparkle(14, 30, 4, YELLOW)


@icon("perdon", "PERDÓN", "perdón")
def perdon(c):
    bust(c, 50, 44, 18, shirt=GREY, hair=HAIR_BLACK, style='short', mood='sad')
    c.heart(50, 12, 18, RED, INK, 2.2)
    c.path([(46, 4), (52, 10), (47, 14), (53, 20)], 2.4, WHITE)


@icon("mas", "MÁS", "más")
def mas(c):
    c.circle((50, 50), 42, BLUE, INK, 3.6)
    c.line((50, 26), (50, 74), 11, INK)
    c.line((26, 50), (74, 50), 11, INK)
    c.line((50, 26), (50, 74), 7, WHITE)
    c.line((26, 50), (74, 50), 7, WHITE)


@icon("acabado", "ACABADO", "he terminado")
def acabado(c):
    c.circle((50, 54), 32, WHITE, INK, 3)
    c.circle((50, 54), 21, LGREY, INK, 2)
    c.sparkle(42, 46, 6, WHITE, YELLOW, 1.4)
    c.sparkle(58, 62, 4, WHITE, LBLUE, 1.2)
    # tenedor
    c.rect(6, 28, 5, 14, DGREY, INK, 1.4, 2)
    c.rect(13, 28, 5, 14, DGREY, INK, 1.4, 2)
    c.rect(6, 38, 12, 8, DGREY, INK, 1.8, 3)
    c.rect(9, 44, 6, 44, DGREY, INK, 2, 3)
    # cuchillo
    c.poly([(86, 24), (94, 30), (94, 56), (86, 56)], LGREY, INK, 2)
    c.rect(86, 54, 8, 34, DGREY, INK, 2, 3)
    c.sparkle(80, 14, 6, YELLOW)


@icon("nose", "NO SÉ", "no sé")
def nose(c):
    bust(c, 50, 44, 18, shirt=PURPLE, hair=HAIR_BLOND, style='short', mood='neutral')
    hand_open(c, 18, 78, 1.1, -24)
    hand_open(c, 82, 78, 1.1, 24)
    qmark(c, 80, 20, 0.7, BLUE)
    qmark(c, 20, 18, 0.6, ORANGE)


def _thumb(c, cuff):
    c.rect(10, 48, 20, 40, cuff, INK, 2.8, 3)
    c.rect(28, 46, 54, 44, SKIN, INK, 3, 12)
    for y in (58, 68, 78):
        c.line((60, y), (80, y), 1.8, SKIN_D)
    c.rect(36, 14, 20, 42, SKIN, INK, 3, 10)
    c.rect(28, 48, 28, 12, SKIN, None)


@icon("bien", "BIEN", "bien")
def bien(c):
    _thumb(c, BLUE)
    c.sparkle(80, 22, 6, YELLOW)


@icon("mal", "MAL", "mal")
def mal(c):
    with c.at(0, 100, 1, 180, True):
        _thumb(c, RED)


@icon("ayuda", "AYUDA", "ayuda")
def ayuda(c):
    c.circle((50, 50), 42, WHITE, INK, 3.4)
    for a in (0, 90, 180, 270):
        pts = arc_pts(50, 50, 42, 42, a - 22, a + 22, 8) + arc_pts(50, 50, 20, 20, a + 22, a - 22, 6)
        c.poly(pts, RED, INK, 2.4)
    c.circle((50, 50), 20, None, INK, 3.4)


@icon("otravez", "OTRA VEZ", "otra vez")
def otravez(c):
    c.arc((50, 50), 32, 40, 330, 13, INK)
    c.arc((50, 50), 32, 40, 330, 8, BLUE)
    c.poly([(70, 14), (92, 34), (66, 42)], BLUE, INK, 3)
