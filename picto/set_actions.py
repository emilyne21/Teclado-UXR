"""Acciones (verbos)."""
import math

from .draw import *          # noqa: F401,F403
from .draw import arc_pts, rrect_pts
from .registry import icon


def _arrow(c, a, b, col=GREEN, w=6, head=11):
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    hx, hy = b[0] - math.cos(ang) * head * 0.6, b[1] - math.sin(ang) * head * 0.6
    c.line(a, (hx, hy), w, INK)
    c.line(a, (hx, hy), w - 3.2, col)
    p1 = (b[0] - math.cos(ang - 0.5) * head * 1.3, b[1] - math.sin(ang - 0.5) * head * 1.3)
    p2 = (b[0] - math.cos(ang + 0.5) * head * 1.3, b[1] - math.sin(ang + 0.5) * head * 1.3)
    c.poly([b, p1, p2], col, INK, 2.2)


def _walker(c, shirt=ORANGE):
    figure(c, (46, 24), 10, (46, 38), (44, 60),
           arms=[[(46, 40), (54, 50), (60, 58)]], back_arms=[[(46, 40), (38, 50), (34, 56)]],
           legs=[[(44, 60), (54, 72), (52, 86)], [(44, 60), (36, 74), (30, 84)]],
           shirt=shirt, pants=DBLUE, mood='happy')


@icon("ir", "IR", "ir")
def ir(c):
    _walker(c)
    _arrow(c, (62, 90), (94, 90), GREEN)


@icon("venir", "VENIR", "venir")
def venir(c):
    c.circle((14, 48), 11, WHITE, INK, 2.4)
    c.circle((14, 48), 6.5, RED, None)
    c.circle((14, 48), 2.6, WHITE, None)
    with c.at(100, 0, 1, 0, flip=True):
        _walker(c, BLUE)
    _arrow(c, (92, 90), (36, 90), GREEN)


@icon("ver", "VER", "ver")
def ver(c):
    pts = arc_pts(50, 66, 44, 36, 215, 325, 16) + arc_pts(50, 34, 44, 36, 145, 35, 16)[::-1][:0]
    top = arc_pts(50, 62, 44, 34, 205, 335, 18)
    bot = arc_pts(50, 38, 44, 34, 25, 155, 18)
    c.poly(top + bot, WHITE, INK, 3.2)
    c.circle((50, 50), 18, BLUE, INK, 2.6)
    c.circle((50, 50), 9, INK, None)
    c.circle((44, 44), 4, WHITE, None)
    for a in (-60, -30, 0, 30, 60):
        r = math.radians(a - 90)
        c.line((50 + 48 * math.cos(r), 50 + 38 * math.sin(r)), (50 + 58 * math.cos(r), 50 + 46 * math.sin(r)), 2.6, INK)
    c.sparkle(88, 18, 6, YELLOW)


@icon("escuchar", "ESCUCHAR", "escuchar")
def escuchar(c):
    ear = [(38, 14), (58, 10), (74, 22), (76, 42), (68, 58), (60, 70), (62, 84), (50, 92), (38, 86), (36, 72),
           (24, 66), (22, 50), (26, 28)]
    c.smooth(ear, SKIN, INK, 3)
    c.path([(40, 30), (54, 26), (62, 36), (60, 48), (52, 54), (46, 62), (48, 72)], 2.6, SKIN_D, smooth=True)
    for r, a in ((12, 1), (22, 1), (32, 1)):
        c.arc((10, 50), r, -50, 50, 3.2, BLUE)


@icon("dar", "DAR", "dar")
def dar(c):
    c.rect(24, 28, 40, 34, RED, INK, 2.8, 3)
    c.rect(20, 22, 48, 12, DRED, INK, 2.6, 3)
    c.rect(41, 22, 6, 40, YELLOW, INK, 1.8)
    c.path([(44, 22), (34, 10), (28, 16), (44, 22), (54, 10), (60, 16), (44, 22)], 2.4, YELLOW)
    hand_open(c, 34, 82, 1.7, 90)
    c.sparkle(82, 26, 6, YELLOW)
    c.sparkle(10, 40, 4, LBLUE)


@icon("abrir", "ABRIR", "abrir")
def abrir(c):
    c.rect(14, 8, 72, 86, DGREY, INK, 2.8, 3)
    c.rect(20, 14, 60, 80, YELLOW, None)
    c.poly([(20, 14), (50, 22), (50, 88), (20, 94)], BROWN, INK, 2.8)
    c.circle((44, 56), 2.6, YELLOW, INK, 1.4)
    c.line((62, 36), (74, 36), 2.2, WHITE)
    c.sparkle(70, 62, 7, WHITE, YELLOW)
    c.line((20, 94), (86, 94), 3, INK)


@icon("cerrar", "CERRAR", "cerrar")
def cerrar(c):
    c.rect(14, 8, 72, 86, DGREY, INK, 2.8, 3)
    c.rect(20, 14, 60, 80, BROWN, INK, 2.4, 2)
    c.rect(26, 22, 20, 28, LBROWN, INK, 1.8, 2)
    c.rect(54, 22, 20, 28, LBROWN, INK, 1.8, 2)
    c.rect(26, 58, 20, 28, LBROWN, INK, 1.8, 2)
    c.rect(54, 58, 20, 28, LBROWN, INK, 1.8, 2)
    c.rect(64, 48, 10, 4, YELLOW, INK, 1.6, 2)
    c.circle((52, 52), 4.4, YELLOW, INK, 1.8)
    c.line((20, 94), (86, 94), 3, INK)


@icon("esperar", "ESPERAR", "esperar")
def esperar(c):
    c.rect(20, 8, 60, 8, BROWN, INK, 2.6, 3)
    c.rect(20, 84, 60, 8, BROWN, INK, 2.6, 3)
    c.poly([(26, 16), (74, 16), (74, 24), (54, 50), (74, 76), (74, 84), (26, 84), (26, 76), (46, 50), (26, 24)],
           (232, 244, 255), INK, 3)
    c.poly([(32, 22), (68, 22), (52, 46), (48, 46)], YELLOW, None)
    c.poly([(48, 54), (52, 54), (68, 80), (32, 80)], YELLOW, None)
    c.line((50, 50), (50, 66), 1.6, YELLOW)
    c.shine([(32, 26), (34, 21)], 1.4)


@icon("parar", "PARAR", "parar")
def parar(c):
    pts = arc_pts(50, 50, 46, 46, 22.5, 382.5, 8)[:8]
    c.poly(pts, RED, INK, 3)
    c.poly([(50 + 40 * math.cos(math.radians(22.5 + i * 45)), 50 + 40 * math.sin(math.radians(22.5 + i * 45)))
            for i in range(8)], None, WHITE, 2)
    hand_open(c, 50, 56, 1.4, 0, WHITE)


@icon("escribir", "ESCRIBIR", "escribir")
def escribir(c):
    c.poly([(14, 14), (74, 14), (74, 90), (14, 90)], WHITE, INK, 2.8)
    for y in (28, 40, 52, 64):
        c.line((22, y), (66, y), 1.8, LBLUE)
    c.path([(22, 34), (30, 28), (38, 36), (46, 28), (54, 36)], 2.4, BLUE, smooth=True)
    with c.at(70, 56, 1, 40):
        c.poly([(-4.5, -30), (4.5, -30), (4.5, 16), (0, 26), (-4.5, 16)], YELLOW, INK, 2.4)
        c.rect(-4.5, -30, 9, 8, PINK, INK, 2.2, 2)
        c.poly([(-2.2, 20), (2.2, 20), (0, 26)], INK, INK, 1)
        c.line((0, -22), (0, 14), 1.4, ORANGE)


@icon("dibujar", "DIBUJAR", "dibujar")
def dibujar(c):
    c.smooth([(10, 52), (16, 30), (40, 14), (68, 14), (90, 30), (92, 52), (80, 62), (66, 56), (56, 66), (58, 82),
              (40, 90), (20, 80)], LBROWN, INK, 3)
    c.circle((30, 62), 5, WHITE, INK, 2)
    for (x, y, col) in ((30, 34, RED), (50, 24, YELLOW), (72, 28, GREEN), (82, 44, BLUE)):
        c.circle((x, y), 6, col, INK, 2)
    c.line((72, 86), (96, 52), 3.6, INK)
    c.line((72, 86), (96, 52), 2, BROWN)
    c.poly([(60, 98), (66, 86), (76, 90), (70, 98)], PURPLE, INK, 2)


@icon("cantar", "CANTAR", "cantar")
def cantar(c):
    bust(c, 36, 40, 19, shirt=RED, hair=HAIR_BLACK, style='short', mood='surprised')
    for (x, y, s) in ((74, 28, 1), (86, 52, 0.8), (70, 62, 0.7)):
        with c.at(x, y, s):
            c.line((6, -2), (6, -22), 3, INK)
            c.ellipse((0, 0), 7, 5, BLUE, INK, 2, rot=-20)
            c.path([(6, -22), (14, -18), (13, -10)], 3, INK)
    c.sparkle(88, 14, 5, YELLOW)


@icon("bailar", "BAILAR", "bailar")
def bailar(c):
    figure(c, (48, 24), 10, (48, 38), (50, 60),
           arms=[[(48, 40), (62, 34), (70, 18)]], back_arms=[[(48, 40), (36, 48), (26, 40)]],
           legs=[[(50, 60), (62, 70), (66, 86)], [(50, 60), (40, 74), (28, 84)]],
           shirt=PINK, pants=PURPLE, mood='happy', skirt=False)
    for (x, y, s) in ((16, 22, 0.9), (86, 52, 0.8)):
        with c.at(x, y, s):
            c.line((6, -2), (6, -20), 3, INK)
            c.ellipse((0, 0), 6, 4.4, ORANGE, INK, 2, rot=-20)
            c.path([(6, -20), (13, -16), (12, -9)], 3, INK)
    c.sparkle(86, 16, 5, YELLOW)


@icon("correr", "CORRER", "correr")
def correr(c):
    figure(c, (60, 24), 10, (54, 38), (46, 58),
           arms=[[(54, 40), (66, 46), (72, 36)]], back_arms=[[(54, 40), (42, 46), (32, 40)]],
           legs=[[(46, 58), (62, 62), (60, 80)], [(46, 58), (34, 70), (20, 76)]],
           shirt=RED, pants=DBLUE, mood='happy')
    for y, x0, x1 in ((36, 6, 22), (50, 2, 20), (64, 8, 18)):
        c.line((x0, y), (x1, y), 2.8, GREY)
    c.line((20, 88), (92, 88), 3, GREY)


@icon("lavar", "LAVAR LAS MANOS", "lavarme las manos")
def lavar(c):
    c.path([(78, 8), (78, 20), (54, 20), (54, 26)], 5, DGREY)
    c.rect(48, 24, 12, 8, GREY, INK, 2.2, 2)
    for i in range(4):
        c.line((54, 34 + i * 7), (54, 38 + i * 7), 2.6, BLUE)
    hand_open(c, 36, 84, 1.25, 28)
    hand_open(c, 66, 84, 1.25, -28)
    for (x, y, r) in ((20, 52, 6), (84, 52, 5), (46, 62, 4), (76, 70, 4), (14, 72, 3.4)):
        c.circle((x, y), r, (220, 240, 255), BLUE, 1.4)


@icon("vestirse", "VESTIRSE", "vestirme")
def vestirse(c):
    c.path([(50, 14), (50, 20)], 3, INK)
    c.arc((50, 12), 5, 180, 360, 3, INK)
    c.path([(50, 20), (14, 36)], 3, INK)
    c.path([(50, 20), (86, 36)], 3, INK)
    c.poly([(36, 24), (64, 24), (62, 30), (50, 36), (38, 30)], None, None, 1)
    c.poly([(36, 28), (50, 36), (64, 28), (90, 40), (82, 58), (70, 52), (70, 92), (30, 92), (30, 52), (18, 58), (10, 40)],
           RED, INK, 3)
    c.arc((50, 28), 9, 20, 160, 2.6, DRED)
    c.star(50, 66, 9, 4, YELLOW, INK, 1.8)


@icon("sentarse", "SENTARSE", "sentarme")
def sentarse(c):
    with c.at(10, 0):
        c.rect(54, 16, 8, 50, BROWN, INK, 2.6, 3)
        c.rect(24, 62, 42, 8, BROWN, INK, 2.6, 3)
        c.line((30, 70), (30, 94), 5, INK)
        c.line((30, 70), (30, 94), 2.6, BROWN)
        c.line((62, 70), (62, 94), 5, INK)
        c.line((62, 70), (62, 94), 2.6, BROWN)
        figure(c, (40, 22), 10, (40, 36), (42, 58),
               arms=[[(40, 38), (32, 50), (26, 56)]],
               legs=[[(42, 58), (20, 60), (14, 82)], [(42, 58), (10, 62), (6, 84)]],
               shirt=GREEN, pants=DBLUE, mood='happy', facing=-1)


@icon("abrazar", "ABRAZAR", "abrazar")
def abrazar(c):
    with c.at(30 - 50 * 0.82, 90 - 90 * 0.82, 0.82):
        bust(c, 50, 38, 19, shirt=BLUE, hair=HAIR, style='short', mood='calm')
    with c.at(70 - 50 * 0.82, 90 - 90 * 0.82, 0.82):
        bust(c, 50, 38, 19, shirt=PINK, hair=HAIR_BLACK, style='long', mood='calm')
    c.circle((60, 84), 4.6, SKIN, INK, 2)
    c.circle((40, 86), 4.6, SKIN, INK, 2)
    c.heart(50, 20, 18, RED, INK, 2.4)
