"""Lugares y transportes."""
import math

from .draw import *          # noqa: F401,F403
from .draw import arc_pts, rrect_pts
from .registry import icon


def _ground(c, col=LGREEN, y=86):
    c.rect(-4, y, 108, 24, col, INK, 2.6)


@icon("casa", "CASA", "casa")
def casa(c):
    _ground(c)
    c.rect(66, 14, 10, 24, RED, INK, 2.6, 1)
    c.rect(18, 42, 64, 44, BEIGE, INK, 3, 2)
    c.poly([(10, 46), (50, 12), (90, 46)], RED, INK, 3)
    c.rect(42, 58, 18, 28, BROWN, INK, 2.6, 2)
    c.circle((55, 73), 1.8, YELLOW, None)
    c.rect(24, 52, 14, 14, LBLUE, INK, 2.4, 1)
    c.rect(66, 52, 12, 14, LBLUE, INK, 2.4, 1)
    c.line((31, 52), (31, 66), 1.6)
    c.line((24, 59), (38, 59), 1.6)


@icon("colegio", "COLEGIO", "el colegio")
def colegio(c):
    _ground(c)
    c.rect(8, 44, 84, 42, (236, 160, 90), INK, 3, 2)
    c.rect(34, 24, 32, 22, (236, 160, 90), INK, 3, 2)
    c.poly([(30, 26), (50, 8), (70, 26)], RED, INK, 3)
    c.circle((50, 34), 6, WHITE, INK, 2)
    c.line((50, 34), (50, 30), 1.6)
    c.line((50, 34), (53, 35), 1.6)
    c.rect(42, 62, 16, 24, BROWN, INK, 2.6, 2)
    for x in (14, 70):
        c.rect(x, 54, 12, 12, LBLUE, INK, 2.4, 1)
    c.line((50, 8), (50, 0), 2.4)
    c.poly([(50, 0), (62, 3), (50, 6)], YELLOW, INK, 1.4)


@icon("parque", "PARQUE", "el parque")
def parque(c):
    c.circle((84, 14), 8, YELLOW, INK, 2.2)
    _ground(c, LGREEN, 88)
    for s in (-1, 1):
        c.line((50 + s * 34, 88), (50 + s * 22, 22), 5, INK)
        c.line((50 + s * 34, 88), (50 + s * 22, 22), 2.6, ORANGE)
    c.line((26, 22), (74, 22), 6, INK)
    c.line((26, 22), (74, 22), 3.4, ORANGE)
    c.line((40, 24), (40, 62), 2, INK)
    c.line((60, 24), (60, 62), 2, INK)
    c.rect(34, 62, 32, 7, BLUE, INK, 2.4, 3)


@icon("supermercado", "SUPERMERCADO", "el supermercado")
def supermercado(c):
    c.path([(6, 16), (22, 16), (30, 64), (80, 64), (90, 30), (26, 30)], 5, INK)
    c.poly([(26, 30), (90, 30), (80, 64), (30, 64)], LBLUE, None)
    c.path([(6, 16), (22, 16), (30, 64), (80, 64), (90, 30), (26, 30)], 2.4, DGREY)
    for i in range(4):
        c.line((38 + i * 11, 32), (40 + i * 10, 62), 1.4, DGREY)
    c.circle((44, 24), 9, RED, INK, 2.2)
    c.circle((64, 22), 7, ORANGE, INK, 2.2)
    c.rect(50, 8, 14, 18, GREEN, INK, 2, 3)
    c.circle((38, 82), 7, DGREY, INK, 2.6)
    c.circle((72, 82), 7, DGREY, INK, 2.6)
    c.circle((38, 82), 2, WHITE, None)
    c.circle((72, 82), 2, WHITE, None)


@icon("hospital", "HOSPITAL", "el hospital")
def hospital(c):
    _ground(c, LGREY)
    c.rect(12, 26, 76, 60, WHITE, INK, 3, 2)
    c.rect(36, 8, 28, 28, RED, INK, 3, 3)
    c.rect(48, 12, 4, 20, WHITE, None)
    c.rect(40, 20, 20, 4, WHITE, None)
    c.rect(42, 62, 16, 24, LBLUE, INK, 2.6, 2)
    for (x, y) in ((18, 40), (68, 40), (18, 62), (68, 62)):
        c.rect(x, y, 14, 14, LBLUE, INK, 2.4, 1)


@icon("playa", "PLAYA", "la playa")
def playa(c):
    c.circle((80, 18), 10, YELLOW, INK, 2.4)
    c.rect(-4, 50, 108, 26, BLUE, INK, 2.6)
    c.path([(0, 58), (10, 54), (20, 58), (30, 54), (40, 58), (50, 54), (60, 58), (70, 54), (80, 58), (90, 54), (100, 58)],
           2.4, LBLUE, smooth=True)
    c.rect(-4, 76, 108, 30, (244, 214, 140), INK, 2.6)
    c.line((36, 84), (46, 38), 3.4, BROWN)
    c.poly(arc_pts(40, 40, 28, 22, 180, 360, 18), RED, INK, 2.8)
    c.poly(arc_pts(40, 40, 28, 22, 180, 360, 18)[6:13], WHITE, None, 1)
    c.circle((70, 84), 5, ORANGE, INK, 2)


@icon("piscina", "PISCINA", "la piscina")
def piscina(c):
    c.rect(6, 46, 88, 46, LBLUE, INK, 3, 6)
    for y in (58, 72, 84):
        c.path([(14, y), (24, y - 4), (34, y), (44, y - 4), (54, y), (64, y - 4), (74, y), (84, y - 4)], 2.2, BLUE,
               smooth=True)
    for x in (66, 80):
        c.path([(x, 48), (x, 18), (x - 8, 12)], 4.4, INK)
        c.path([(x, 48), (x, 18), (x - 8, 12)], 2.2, LGREY)
    c.line((66, 24), (80, 24), 2.4, GREY)
    c.line((66, 34), (80, 34), 2.4, GREY)
    c.ellipse((30, 62), 16, 8, WHITE, INK, 2.8)
    c.ellipse((30, 62), 8, 3.4, LBLUE, INK, 2)
    c.path([(16, 58), (22, 54)], 4, RED)
    c.path([(38, 54), (44, 58)], 4, RED)


@icon("cocina", "COCINA", "la cocina")
def cocina(c):
    _steam(c, 36, 28, 14)
    _steam(c, 52, 24, 14)
    c.rect(18, 32, 56, 30, DGREY, INK, 3, 5)
    c.rect(14, 28, 64, 8, GREY, INK, 3, 3)
    c.line((78, 40), (94, 36), 5, INK)
    c.line((78, 40), (94, 36), 2.6, BROWN)
    c.rect(10, 64, 80, 28, LGREY, INK, 3, 3)
    for x in (24, 50, 76):
        c.circle((x, 76), 5.4, WHITE, INK, 2.2)
        c.line((x, 76), (x + 3, 73), 1.8)
    c.path([(30, 64), (30, 56)], 1, INK)


def _steam(c, x, y, h=14, col=GREY):
    c.path([(x, y), (x - 3, y - h * 0.35), (x + 3, y - h * 0.65), (x, y - h)], 2.4, col, smooth=True)


@icon("habitacion", "HABITACIÓN", "mi habitación")
def habitacion(c):
    c.rect(0, 0, 100, 74, (212, 232, 248), None)
    c.rect(-4, 74, 108, 30, (214, 170, 120), INK, 2.6)
    c.rect(54, 10, 34, 36, LBLUE, INK, 3, 2)
    c.line((71, 10), (71, 46), 2.2)
    c.line((54, 28), (88, 28), 2.2)
    c.star(63, 19, 4.4, 2, YELLOW, None, 1)
    c.rect(6, 52, 62, 12, BROWN, INK, 2.6, 3)
    c.rect(6, 44, 6, 40, BROWN, INK, 2.6, 2)
    c.rect(62, 56, 6, 28, BROWN, INK, 2.6, 2)
    c.rect(12, 42, 18, 12, WHITE, INK, 2.4, 5)
    c.rect(14, 52, 50, 16, ORANGE, INK, 2.6, 4)
    c.rect(78, 64, 14, 20, BROWN, INK, 2.4, 2)
    c.poly([(76, 54), (94, 54), (90, 44), (80, 44)], YELLOW, INK, 2.2)
    c.line((85, 54), (85, 64), 2.4)


@icon("salon", "SALÓN", "el salón")
def salon(c):
    c.rect(0, 0, 100, 72, (250, 232, 214), None)
    c.rect(-4, 72, 108, 30, (214, 170, 120), INK, 2.6)
    c.rect(10, 44, 80, 30, PURPLE, INK, 3, 8)
    c.rect(4, 50, 16, 28, PURPLE, INK, 3, 7)
    c.rect(80, 50, 16, 28, PURPLE, INK, 3, 7)
    c.rect(22, 30, 56, 24, (170, 132, 214), INK, 3, 7)
    c.rect(26, 52, 48, 20, LPURPLE, INK, 2.4, 4)
    c.line((50, 54), (50, 70), 1.6, PURPLE)
    c.rect(10, 74, 4, 8, BROWN, INK, 1.6)
    c.rect(86, 74, 4, 8, BROWN, INK, 1.6)
    c.circle((88, 14), 8, YELLOW, INK, 2.2)
    c.rect(10, 8, 30, 20, LBLUE, INK, 2.6, 2)
    c.poly([(12, 26), (22, 16), (30, 22), (38, 14), (38, 26)], LGREEN, None)


@icon("coche", "COCHE", "el coche")
def coche(c):
    c.rect(-4, 86, 108, 20, LGREY, INK, 2.6)
    c.poly([(6, 68), (6, 54), (24, 50), (36, 32), (66, 32), (80, 50), (94, 56), (94, 68)], RED, INK, 3)
    c.poly([(30, 50), (40, 37), (50, 37), (50, 50)], LBLUE, INK, 2.4)
    c.poly([(54, 50), (54, 37), (64, 37), (74, 50)], LBLUE, INK, 2.4)
    c.rect(86, 58, 8, 6, YELLOW, INK, 1.6, 2)
    c.rect(6, 60, 6, 5, ORANGE, INK, 1.4, 2)
    for x in (28, 74):
        c.circle((x, 72), 12, INK, INK, 1)
        c.circle((x, 72), 7, GREY, None)
        c.circle((x, 72), 2.4, DGREY, None)


@icon("autobus", "AUTOBÚS", "el autobús")
def autobus(c):
    c.rect(-4, 86, 108, 20, LGREY, INK, 2.6)
    c.rect(6, 22, 88, 56, YELLOW, INK, 3, 8)
    c.rect(6, 62, 88, 10, ORANGE, None, 1)
    for x in (12, 32, 52):
        c.rect(x, 30, 16, 16, LBLUE, INK, 2.4, 3)
    c.rect(72, 30, 16, 36, LBLUE, INK, 2.4, 3)
    c.line((80, 30), (80, 66), 1.8)
    c.rect(6, 54, 6, 6, RED, INK, 1.4, 2)
    c.rect(86, 66, 8, 6, WHITE, INK, 1.4, 2)
    for x in (24, 70):
        c.circle((x, 78), 11, INK, INK, 1)
        c.circle((x, 78), 6.4, GREY, None)
        c.circle((x, 78), 2.2, DGREY, None)
