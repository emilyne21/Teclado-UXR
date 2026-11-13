"""Comida y bebida."""
import math

from .draw import *          # noqa: F401,F403
from .draw import arc_pts, rrect_pts, crescent_pts
from .registry import icon


def _steam(c, x, y, h=14, col=GREY):
    c.path([(x, y), (x - 3, y - h * 0.35), (x + 3, y - h * 0.65), (x, y - h)], 2.4, col, smooth=True)


# ---------------------------------------------------------------- comida
@icon("manzana", "MANZANA", "una manzana")
def manzana(c):
    c.smooth([(50, 30), (66, 22), (84, 34), (86, 56), (74, 80), (58, 90), (50, 86), (42, 90), (26, 80), (14, 56),
              (16, 34), (34, 22)], RED, INK, 3)
    c.line((50, 30), (52, 12), 3.4, BROWN)
    c.poly([(54, 22), (66, 8), (80, 14), (70, 26)], GREEN, INK, 2.4)
    c.shine([(26, 40), (24, 54)], 3.2)


@icon("platano", "PLÁTANO", "un plátano")
def platano(c):
    c.smooth([(14, 30), (22, 58), (46, 78), (74, 76), (92, 56), (86, 50), (70, 62), (48, 62), (32, 46), (24, 26)],
             YELLOW, INK, 3)
    c.line((14, 30), (24, 26), 5, BROWN)
    c.circle((90, 53), 2.8, BROWN, None)
    c.path([(30, 36), (40, 56), (60, 66)], 1.8, ORANGE, smooth=True)


@icon("uvas", "UVAS", "uvas")
def uvas(c):
    rows = ((50, 30, 3), (36, 44, 2), (58, 44, 2), (28, 58, 1), (50, 58, 1), (72, 58, 1), (39, 72, 1), (61, 72, 1),
            (50, 85, 1))
    for (x, y, _) in rows:
        c.circle((x, y), 11, PURPLE, INK, 2.4)
        c.circle((x - 3.4, y - 3.4), 2.6, LPURPLE, None)
    c.line((50, 20), (52, 8), 3.4, BROWN)
    c.poly([(54, 14), (68, 4), (84, 12), (72, 24)], GREEN, INK, 2.4)


@icon("naranja", "NARANJA", "una naranja")
def naranja(c):
    c.circle((50, 56), 36, ORANGE, INK, 3)
    c.shine([(26, 44), (28, 34), (36, 28)], 3.2)
    c.poly([(50, 22), (62, 8), (78, 12), (68, 24)], GREEN, INK, 2.4)
    c.line((50, 22), (50, 16), 3.4, BROWN)
    c.circle((60, 66), 1.4, (210, 110, 20), None)
    c.circle((44, 72), 1.4, (210, 110, 20), None)
    c.circle((70, 52), 1.4, (210, 110, 20), None)


@icon("pan", "PAN", "pan")
def pan(c):
    c.smooth([(8, 62), (10, 40), (28, 26), (50, 22), (72, 26), (90, 40), (92, 62), (86, 78), (14, 78)], LBROWN, INK, 3)
    c.smooth([(14, 66), (16, 44), (32, 32), (50, 28), (68, 32), (84, 44), (86, 66), (82, 74), (18, 74)], (226, 176, 112),
             None)
    for x in (30, 50, 70):
        c.path([(x - 6, 50), (x, 42), (x + 6, 34)], 3, BROWN)


@icon("queso", "QUESO", "queso")
def queso(c):
    c.poly([(8, 56), (60, 30), (92, 46), (92, 76), (8, 76)], YELLOW, INK, 3)
    c.poly([(8, 56), (60, 30), (92, 46), (40, 70)], LYELLOW, INK, 3)
    c.line((40, 70), (40, 76), 3)
    c.ellipse((70, 58), 6, 4, YELLOW, INK, 2, rot=-24)
    c.ellipse((18, 66), 4, 3.4, ORANGE, INK, 2)
    c.ellipse((56, 40), 5, 3, YELLOW, INK, 1.6, rot=-24)
    c.ellipse((70, 68), 5, 4, ORANGE, INK, 2)


@icon("huevo", "HUEVO", "un huevo")
def huevo(c):
    c.smooth([(12, 52), (14, 30), (34, 14), (58, 18), (84, 22), (92, 44), (84, 70), (62, 84), (36, 84), (16, 74)],
             WHITE, INK, 3)
    c.circle((50, 52), 17, YELLOW, INK, 2.8)
    c.circle((44, 46), 4.4, LYELLOW, None)


@icon("pollo", "POLLO", "pollo")
def pollo(c):
    c.line((66, 62), (88, 84), 8, INK)
    c.line((66, 62), (88, 84), 4.4, WHITE)
    c.circle((88, 80), 6, WHITE, INK, 2.4)
    c.circle((84, 88), 6, WHITE, INK, 2.4)
    c.smooth([(10, 40), (22, 16), (50, 12), (74, 26), (76, 52), (62, 70), (38, 72), (16, 62)], (206, 120, 48), INK, 3)
    c.shine([(26, 30), (40, 24)], 3.2, (240, 180, 110))
    c.path([(30, 56), (46, 60), (60, 50)], 2, (150, 80, 30), smooth=True)


@icon("pescado", "PESCADO", "pescado")
def pescado(c):
    c.poly([(70, 52), (96, 28), (92, 52), (96, 76)], ORANGE, INK, 3)
    c.poly(arc_pts(40, 52, 36, 24, 0, 360, 36), BLUE, INK, 3)
    c.poly([(30, 30), (44, 16), (56, 32)], DBLUE, INK, 2.4)
    c.poly([(36, 72), (46, 86), (56, 70)], DBLUE, INK, 2.4)
    c.path([(54, 36), (60, 52), (54, 68)], 2.4, LBLUE, smooth=True)
    c.circle((20, 46), 4.6, WHITE, INK, 2)
    c.circle((19, 46), 1.8, INK, None)
    c.path([(8, 56), (12, 60)], 2.2, INK)


@icon("pasta", "PASTA", "pasta")
def pasta(c):
    c.ellipse((50, 66), 44, 20, WHITE, INK, 3)
    c.ellipse((50, 64), 32, 13, LGREY, INK, 1.8)
    for i in range(6):
        x = 28 + i * 8
        c.path([(x, 62), (x + 6, 50), (x - 2, 42), (x + 8, 36)], 3, YELLOW, smooth=True)
        c.path([(x, 62), (x + 6, 50), (x - 2, 42), (x + 8, 36)], 1.4, INK, smooth=True) if False else None
    c.smooth([(34, 52), (44, 40), (60, 40), (70, 52), (60, 62), (42, 62)], RED, INK, 2.4)
    c.circle((52, 48), 3, GREEN, None)
    c.circle((60, 54), 2.4, GREEN, None)
    c.line((84, 14), (70, 54), 3, DGREY)


@icon("sopa", "SOPA", "sopa")
def sopa(c):
    _steam(c, 36, 30, 18)
    _steam(c, 52, 26, 18)
    _steam(c, 68, 30, 18)
    c.poly(arc_pts(50, 44, 42, 42, 0, 180, 24) + [(8, 44)], ORANGE, INK, 3)
    c.ellipse((50, 44), 42, 10, LORANGE, INK, 3)
    c.circle((38, 44), 3, GREEN, None)
    c.circle((56, 46), 3, RED, None)
    c.circle((66, 42), 2.4, GREEN, None)
    c.rect(36, 86, 28, 6, ORANGE, INK, 2.6, 3)


@icon("pizza", "PIZZA", "pizza")
def pizza(c):
    c.poly([(50, 90), (8, 28)] + arc_pts(50, 70, 52, 52, 215, 325, 18)[1:-1][:0] + [(92, 28)], LYELLOW, INK, 3)
    c.poly([(50, 90), (12, 30), (22, 24), (50, 20), (78, 24), (88, 30)], YELLOW, None)
    c.poly([(50, 90), (8, 28), (92, 28)], None, INK, 3)
    c.path([(6, 28), (26, 18), (50, 14), (74, 18), (94, 28)], 9, (216, 150, 70), smooth=True)
    c.path([(6, 28), (26, 18), (50, 14), (74, 18), (94, 28)], 3.4, (236, 186, 120), smooth=True)
    for (x, y) in ((36, 38), (60, 40), (48, 58), (44, 74)):
        c.circle((x, y), 6.4 if y < 70 else 4.6, RED, INK, 2)
    c.circle((60, 56), 2.4, GREEN, None)


@icon("galleta", "GALLETA", "una galleta")
def galleta(c):
    c.circle((50, 52), 38, (222, 170, 100), INK, 3)
    c.circle((50, 52), 32, (236, 190, 120), None)
    for (x, y) in ((36, 38), (62, 36), (68, 58), (44, 64), (32, 56), (54, 50), (50, 76)):
        c.circle((x, y), 4.8, BROWN, INK, 1.4)


@icon("helado", "HELADO", "un helado")
def helado(c):
    c.poly([(30, 50), (70, 50), (50, 96)], (226, 176, 112), INK, 3)
    for i in range(4):
        c.line((34 + i * 3, 56 + i * 8), (66 - i * 3 + 4, 56 + i * 8 - 8), 1.6, LBROWN)
        c.line((66 - i * 3, 56 + i * 8), (34 + i * 3 + 4, 56 + i * 8 - 8), 1.6, LBROWN)
    c.circle((50, 44), 22, PINK, INK, 3)
    c.circle((50, 24), 16, (250, 236, 200), INK, 3)
    c.circle((50, 8), 5, RED, INK, 2)
    c.shine([(36, 40), (38, 34)], 2.2)


@icon("zanahoria", "ZANAHORIA", "zanahoria")
def zanahoria(c):
    c.poly([(30, 36), (74, 22), (88, 36), (24, 96)][:3] + [(14, 90)], ORANGE, INK, 3)
    for (a, b) in (((44, 44), (54, 52)), ((56, 34), (66, 40)), ((34, 66), (44, 72)), ((22, 80), (30, 84))):
        c.line(a, b, 2.2, (214, 110, 20))
    c.poly([(74, 22), (82, 6), (90, 18)], GREEN, INK, 2.4)
    c.poly([(70, 26), (66, 4), (78, 16)], DGREEN, INK, 2.4)
    c.poly([(80, 28), (96, 18), (96, 34)], GREEN, INK, 2.4)


@icon("tarta", "TARTA", "tarta")
def tarta(c):
    c.rect(12, 58, 76, 32, (240, 200, 150), INK, 3, 4)
    c.rect(16, 36, 68, 26, PINK, INK, 3, 4)
    c.path([(16, 52), (24, 58), (32, 52), (40, 58), (48, 52), (56, 58), (64, 52), (72, 58), (80, 52), (84, 52)], 3.6,
           WHITE, smooth=True)
    c.rect(48, 16, 4, 20, BLUE, INK, 1.6, 1)
    c.poly([(50, 4), (55, 12), (50, 16), (45, 12)], ORANGE, INK, 1.6)
    for x in (24, 40, 60, 76):
        c.circle((x, 76), 3.4, RED, INK, 1.4)
    c.circle((30, 44), 3, YELLOW, None)
    c.circle((70, 44), 3, LBLUE, None)


@icon("patatas", "PATATAS FRITAS", "patatas fritas")
def patatas(c):
    for (x, a, h) in ((22, -10, 40), (32, -4, 48), (42, 2, 52), (52, 0, 54), (62, 6, 50), (72, 10, 42)):
        with c.at(x + 4, 62, 1, a):
            c.rect(-4, -h, 8, h, YELLOW, INK, 2.2, 2)
    c.poly([(16, 56), (84, 56), (76, 94), (24, 94)], RED, INK, 3)
    c.poly([(30, 62), (70, 62), (66, 82), (34, 82)], YELLOW, None)
    c.star(50, 72, 8, 3.6, YELLOW, INK, 1.8)


@icon("yogur", "YOGUR", "yogur")
def yogur(c):
    c.poly([(22, 34), (78, 34), (70, 92), (30, 92)], WHITE, INK, 3)
    c.poly([(24, 50), (76, 50), (72, 78), (28, 78)], PINK, None)
    c.circle((50, 64), 8, RED, INK, 2)
    c.rect(18, 26, 64, 10, LGREY, INK, 3, 3)
    c.line((70, 16), (58, 60), 3.4, INK)
    c.line((70, 16), (58, 60), 2, DGREY)
    c.ellipse((72, 12), 6, 4, LGREY, INK, 2, rot=-70)


# ---------------------------------------------------------------- bebida
def _glass(c, x0, x1, y0, y1, liquid, level, lw=3):
    top_in = x0 + 2
    c.poly([(x0, y0), (x1, y0), (x1 - 6, y1), (x0 + 6, y1)], WHITE, INK, lw)
    t = (level - y0) / float(y1 - y0)
    xl = x0 + 6 * t
    xr = x1 - 6 * t
    c.poly([(xl + 1.4, level), (xr - 1.4, level), (x1 - 7.4, y1 - 1.4), (x0 + 7.4, y1 - 1.4)], liquid, None)
    c.line((x0 + 4, y0 + 8), (x0 + 7, y1 - 10), 2, WHITE)


@icon("agua", "AGUA", "agua")
def agua(c):
    _glass(c, 24, 66, 28, 92, LBLUE, 44)
    c.path([(26, 44), (34, 40), (44, 46), (54, 40), (64, 44)], 2.4, BLUE, smooth=True)
    c.drop(80, 40, 11, LBLUE, BLUE, 2.4)
    c.drop(86, 66, 6, LBLUE, BLUE, 1.8)
    c.shine([(78, 38), (76, 44)], 2, WHITE)


@icon("leche", "LECHE", "leche")
def leche(c):
    c.poly([(20, 30), (52, 30), (52, 94), (20, 94)], WHITE, INK, 3)
    c.poly([(52, 30), (72, 24), (72, 88), (52, 94)], LGREY, INK, 3)
    c.poly([(20, 30), (36, 8), (68, 8), (72, 24), (52, 30)], LBLUE, INK, 3)
    c.line((36, 8), (52, 30), 3)
    c.circle((36, 62), 11, LBLUE, INK, 2.4)
    c.drop(36, 62, 7, WHITE, None)
    c.ellipse((28, 44), 6, 4, DGREY, None)
    c.ellipse((44, 78), 6, 4, DGREY, None)
    c.rect(78, 56, 18, 36, WHITE, INK, 2.8, 3)
    c.rect(80, 60, 14, 16, (250, 250, 250), None)


@icon("zumo", "ZUMO", "zumo")
def zumo(c):
    c.line((58, 6), (46, 52), 4.4, INK)
    c.line((58, 6), (46, 52), 2.4, GREEN)
    _glass(c, 24, 70, 26, 92, ORANGE, 40)
    c.circle((74, 28), 14, ORANGE, INK, 2.6)
    c.circle((74, 28), 9.6, LORANGE, None)
    for a in range(0, 360, 60):
        r = math.radians(a)
        c.line((74, 28), (74 + 9 * math.cos(r), 28 + 9 * math.sin(r)), 1.4, WHITE)
    c.poly(arc_pts(74, 28, 14, 14, 0, 0, 2) + [(74, 28)], None, None, 1)


@icon("refresco", "REFRESCO", "un refresco")
def refresco(c):
    c.rect(26, 14, 48, 78, RED, INK, 3, 8)
    c.rect(26, 14, 48, 10, GREY, INK, 3, 4)
    c.rect(26, 82, 48, 10, GREY, INK, 3, 4)
    c.path([(26, 44), (38, 36), (50, 48), (62, 36), (74, 44)], 14, WHITE, smooth=True)
    c.path([(26, 44), (38, 36), (50, 48), (62, 36), (74, 44)], 4, RED, smooth=True)
    c.shine([(32, 26), (32, 78)], 2.6)
    for (x, y, r) in ((84, 30, 4), (90, 48, 3), (82, 62, 3.4), (12, 40, 3)):
        c.circle((x, y), r, LBLUE, BLUE, 1.4)


@icon("te", "TÉ", "té")
def te(c):
    _steam(c, 40, 34, 16)
    _steam(c, 56, 30, 16)
    c.poly(arc_pts(76, 56, 16, 14, -80, 80, 12), None, INK, 4.4, closed=False)
    c.poly([(14, 38), (78, 38), (72, 74), (56, 86), (36, 86), (20, 74)], WHITE, INK, 3)
    c.ellipse((46, 38), 32, 6, (190, 130, 60), INK, 2.6)
    c.ellipse((46, 94), 40, 6, LGREY, INK, 3)
    c.line((46, 40), (24, 22), 1.6, INK)
    c.rect(14, 12, 12, 14, LGREEN, INK, 1.8, 1)


@icon("cafe", "CAFÉ", "café")
def cafe(c):
    _steam(c, 38, 34, 18, GREY)
    _steam(c, 54, 30, 18, GREY)
    c.poly(arc_pts(78, 58, 14, 12, -85, 85, 12), None, INK, 4.4, closed=False)
    c.poly([(14, 40), (78, 40), (72, 76), (56, 88), (36, 88), (20, 76)], BROWN, INK, 3)
    c.ellipse((46, 40), 32, 6, (90, 54, 30), INK, 2.6)
    c.ellipse((46, 94), 42, 6, LGREY, INK, 3)
    c.shine([(22, 52), (26, 68)], 2.6, LBROWN)


@icon("cacao", "COLACAO", "colacao")
def cacao(c):
    c.poly(arc_pts(80, 58, 14, 12, -85, 85, 12), None, INK, 4.4, closed=False)
    c.poly([(14, 34), (78, 34), (74, 82), (68, 90), (24, 90), (18, 82)], BLUE, INK, 3)
    c.ellipse((46, 34), 32, 7, (92, 56, 34), INK, 2.6)
    c.rect(32, 20, 16, 14, WHITE, INK, 2.2, 3)
    c.rect(48, 22, 14, 12, WHITE, INK, 2.2, 3)
    c.heart(46, 62, 20, PINK, INK, 2)
    _steam(c, 36, 12, 8, GREY)


@icon("batido", "BATIDO", "un batido")
def batido(c):
    c.line((62, 4), (50, 36), 4.4, INK)
    c.line((62, 4), (50, 36), 2.4, WHITE)
    _glass(c, 22, 72, 30, 94, PINK, 40)
    c.path([(22, 38), (30, 28), (40, 36), (50, 24), (60, 34), (72, 28)], 12, WHITE, smooth=True)
    c.circle((52, 18), 6, RED, INK, 2)
    c.shine([(30, 54), (32, 80)], 2.4)
