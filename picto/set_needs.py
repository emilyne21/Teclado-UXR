"""Necesidades básicas (el tablero de elección original)."""
from .draw import *          # noqa: F401,F403
from .draw import (arc_pts, rrect_pts, crescent_pts)
from .registry import icon


@icon("yo", "YO", "yo")
def yo(c):
    bust(c, 50, 36, 19, shirt=BLUE, hair=HAIR, style='short', mood='happy')
    hand_open(c, 50, 88, 0.95, -18)
    c.heart(50, 76, 7, RED, INK, 1.6)


@icon("quiero", "QUIERO", "quiero")
def quiero(c):
    figure(c, (28, 28), 11, (28, 42), (28, 66),
           arms=[[(28, 44), (42, 46), (56, 38)], [(28, 46), (22, 58), (24, 66)]],
           legs=[[(25, 66), (24, 80), (23, 92)], [(31, 66), (32, 80), (35, 92)]],
           shirt=GREEN, pants=DBLUE, mood='happy')
    c.star(76, 28, 15, 7, YELLOW, INK, 2.4)
    for a, b in (((76, 6), (76, 10)), ((95, 22), (91, 24)), ((57, 22), (61, 24)), ((90, 44), (87, 41))):
        c.line(a, b, 2.4, ORANGE)
    c.path([(60, 38), (64, 36)], 2.4, ORANGE)


@icon("comer", "COMER", "comer")
def comer(c):
    c.ellipse((66, 86), 30, 9, WHITE, INK, 2.6)
    c.ellipse((66, 85), 21, 5.5, LGREY, INK, 1.6)
    c.smooth([(50, 83), (54, 74), (64, 70), (74, 72), (80, 79), (74, 85), (58, 86)], LORANGE, INK, 2.2)
    c.circle((60, 79), 3.4, RED, INK, 1.3)
    c.circle((71, 78), 3.4, GREEN, INK, 1.3)
    bust(c, 32, 34, 18, shirt=ORANGE, hair=HAIR_BLACK, style='short', mood='eat')
    c.line((84, 74), (58, 52), 3.6, DGREY)
    c.ellipse((50, 46), 8, 5.6, LGREY, INK, 2.0, rot=-35)
    c.ellipse((50, 46), 4.8, 3, LORANGE, None, rot=-35)


@icon("beber", "BEBER", "beber")
def beber(c):
    bust(c, 32, 38, 18, shirt=TEAL, hair=HAIR, style='short', mood='happy')
    with c.at(58, 52, 1, -28):
        c.poly([(-12, -20), (12, -20), (9, 20), (-9, 20)], WHITE, INK, 2.6)
        c.poly([(-10.6, -8), (10.6, -8), (8.6, 18.5), (-8.6, 18.5)], LBLUE, None)
        c.line((-8, -3), (-6.5, 12), 1.6, WHITE)
    c.drop(84, 40, 5.5, LBLUE, BLUE)
    c.drop(90, 56, 4, LBLUE, BLUE)


@icon("bano", "IR AL BAÑO", "ir al baño")
def bano(c):
    c.rect(22, 16, 40, 28, WHITE, INK, 2.8, 5)
    c.rect(32, 10, 20, 8, LGREY, INK, 2.4, 3)
    c.circle((70, 22), 3.4, BLUE, INK, 1.6)
    c.poly([(16, 52), (84, 52), (80, 66), (68, 78), (68, 88), (34, 88), (34, 78), (22, 68)], WHITE, INK, 2.8)
    c.ellipse((50, 52), 36, 7, LBLUE, INK, 2.4)
    c.ellipse((50, 52), 28, 4.2, BLUE, None)
    c.rect(28, 88, 44, 6, LGREY, INK, 2.4, 3)
    c.line((26, 60), (40, 70), 1.8, GREY)


@icon("dormir", "DORMIR", "dormir")
def dormir(c):
    c.rect(8, 62, 84, 14, BROWN, INK, 2.6, 3)
    c.rect(8, 40, 8, 48, BROWN, INK, 2.6, 3)
    c.rect(84, 52, 8, 36, BROWN, INK, 2.6, 3)
    c.rect(16, 50, 68, 20, LBLUE, INK, 2.6, 6)
    c.rect(18, 42, 22, 14, WHITE, INK, 2.4, 6)
    head(c, 28, 45, 9.6, hair=HAIR, style='short', mood='sleep')
    c.rect(30, 52, 56, 22, BLUE, INK, 2.6, 7)
    for x in (44, 58, 72):
        c.circle((x, 63), 2.2, LBLUE, None)
    c.poly(crescent_pts(80, 22, 15, 0.5, 0.84, -20), YELLOW, INK, 2.4)
    for (x, y, s) in ((34, 26, 6.5), (46, 14, 5), (55, 6, 3.6)):
        c.path([(x - s, y - s), (x + s, y - s), (x - s, y + s), (x + s, y + s)], 2.6, PURPLE)


@icon("duchar", "DUCHAR", "ducharme")
def duchar(c):
    c.path([(18, 6), (18, 18), (44, 18)], 4, DGREY)
    with c.at(52, 20, 1, 20):
        c.ellipse((0, 0), 16, 6.5, GREY, INK, 2.4)
        c.rect(-4, -8, 8, 6, DGREY, INK, 2)
    for i in range(7):
        x = 38 + i * 6
        c.line((x, 34 + (i % 2) * 3), (x - 3, 46 + (i % 2) * 3), 2.4, BLUE)
    bust(c, 56, 60, 14, shirt=SKIN, hair=HAIR, style='bun', mood='calm')
    for (x, y, r) in ((30, 62, 5), (80, 56, 4), (74, 82, 6), (24, 80, 4)):
        c.circle((x, y), r, (214, 236, 255), BLUE, 1.4)


@icon("musica", "OÍR MÚSICA", "oír música")
def musica(c):
    c.arc((50, 56), 30, 188, 352, 6, INK)
    c.arc((50, 56), 30, 188, 352, 3.6, GREY)
    for x in (18, 82):
        c.rect(x - 8, 52, 16, 28, RED, INK, 2.6, 7)
        c.rect(x - 4, 57, 8, 18, DRED, None, 1, 4)
    for (x, y, s) in ((46, 56, 1), (62, 40, 0.8)):
        with c.at(x, y, s):
            c.line((6, -2), (6, -26), 3, INK)
            c.ellipse((0, 0), 7, 5, INK, INK, 1, rot=-20)
            c.path([(6, -26), (14, -22), (13, -14)], 3, INK)
    c.sparkle(90, 22, 6, YELLOW)
    c.sparkle(12, 24, 5, LBLUE)


@icon("tele", "VER LA TELE", "ver la tele")
def tele(c):
    c.line((40, 18), (30, 6), 2.6, DGREY)
    c.line((60, 18), (70, 6), 2.6, DGREY)
    c.rect(8, 18, 84, 58, DGREY, INK, 2.8, 8)
    c.rect(14, 24, 60, 46, LBLUE, INK, 2.2, 4)
    c.circle((32, 38), 6, YELLOW, INK, 1.6)
    c.poly([(14, 70), (34, 48), (48, 62), (58, 52), (74, 70)], LGREEN, INK, 1.8)
    c.circle((83, 36), 3.4, RED, INK, 1.2)
    c.circle((83, 48), 3.4, GREEN, INK, 1.2)
    c.line((79, 60), (87, 60), 1.8, GREY)
    c.line((79, 64), (87, 64), 1.8, GREY)
    c.rect(26, 76, 12, 8, DGREY, INK, 2, 2)
    c.rect(62, 76, 12, 8, DGREY, INK, 2, 2)
    c.rect(18, 84, 64, 5, DGREY, INK, 2, 2)


@icon("pasear", "PASEAR", "pasear")
def pasear(c):
    c.circle((80, 16), 8, YELLOW, INK, 2.2)
    c.rect(0, 84, 100, 20, LGREEN, INK, 2.2)
    c.rect(14, 56, 6, 28, BROWN, INK, 2.2, 2)
    c.circle((17, 44), 15, GREEN, INK, 2.4)
    c.circle((9, 52), 9, GREEN, INK, 2.4)
    c.circle((26, 53), 9, GREEN, INK, 2.4)
    figure(c, (54, 26), 10, (54, 40), (52, 62),
           arms=[[(54, 42), (62, 52), (68, 60)]], back_arms=[[(54, 42), (46, 52), (42, 58)]],
           legs=[[(52, 62), (62, 74), (60, 86)], [(52, 62), (44, 76), (38, 86)]],
           shirt=ORANGE, pants=DBLUE, mood='happy')


@icon("jugar", "JUGAR", "jugar")
def jugar(c):
    # pelota
    c.circle((38, 56), 26, WHITE, INK, 2.8)
    c.poly(arc_pts(38, 56, 26, 26, -90, 0, 10) + [(38, 56)], RED, None)
    c.poly(arc_pts(38, 56, 26, 26, 90, 180, 10) + [(38, 56)], BLUE, None)
    c.poly(arc_pts(38, 56, 26, 26, 0, 90, 10) + [(38, 56)], YELLOW, None)
    c.circle((38, 56), 26, None, INK, 2.8)
    c.line((38, 30), (38, 82), 2.4)
    c.line((12, 56), (64, 56), 2.4)
    c.circle((38, 56), 5, WHITE, INK, 2)
    # cubos
    c.rect(64, 66, 24, 24, GREEN, INK, 2.8, 3)
    c.rect(68, 44, 22, 22, ORANGE, INK, 2.8, 3)
    c.circle((79, 55), 4.5, WHITE, INK, 1.6)
    c.circle((76, 78), 3, WHITE, None)
    c.circle((82, 78), 3, WHITE, None)


@icon("hablar", "HABLAR", "hablar")
def hablar(c):
    bust(c, 32, 46, 18, shirt=PURPLE, hair=HAIR_BLACK, style='long', mood='laugh')
    c.poly(rrect_pts(52, 8, 44, 32, 9) , WHITE, INK, 2.6)
    c.poly([(60, 38), (56, 52), (72, 39)], WHITE, INK, 2.6)
    c.rect(54, 10, 40, 28, WHITE, None, 1, 8)
    for (x, y, r) in ((64, 24, 3.4), (74, 24, 3.4), (84, 24, 3.4)):
        c.circle((x, y), r, BLUE, None)


@icon("leer", "LEER", "leer")
def leer(c):
    c.poly([(50, 30), (50, 84), (8, 78), (8, 24)], WHITE, INK, 2.8)
    c.poly([(50, 30), (50, 84), (92, 78), (92, 24)], PAPER, INK, 2.8)
    c.poly([(8, 78), (50, 84), (92, 78), (92, 84), (50, 90), (8, 84)], BLUE, INK, 2.4)
    for i in range(5):
        y = 38 + i * 8
        c.line((16, y - 1.5 + i * 0.6), (42, y + 2 + i * 0.5), 2.2, GREY)
        c.line((58, y + 2 + i * 0.5), (84, y - 1.5 + i * 0.6), 2.2, GREY)
    c.heart(72, 14, 10, RED, INK, 2)
    c.star(24, 14, 8, 3.6, YELLOW, INK, 2)


@icon("ordenador", "ORDENADOR", "el ordenador")
def ordenador(c):
    c.rect(12, 10, 76, 52, DGREY, INK, 2.8, 6)
    c.rect(18, 16, 64, 40, LBLUE, INK, 2.2, 3)
    c.rect(24, 22, 24, 6, WHITE, None, 1, 2)
    c.rect(24, 32, 40, 4, WHITE, None, 1, 2)
    c.rect(24, 40, 32, 4, WHITE, None, 1, 2)
    c.circle((70, 44), 6, ORANGE, INK, 1.6)
    c.rect(42, 62, 16, 12, GREY, INK, 2.4, 2)
    c.rect(32, 72, 36, 5, GREY, INK, 2.4, 2)
    c.rect(10, 80, 60, 14, LGREY, INK, 2.6, 4)
    for r in range(2):
        for i in range(9):
            c.rect(14 + i * 6.2, 83 + r * 5, 4.4, 3.2, WHITE, INK, 1, 1)
    c.rect(76, 80, 12, 14, LGREY, INK, 2.4, 6)
    c.line((82, 80), (82, 86), 1.6)


@icon("videojuegos", "VIDEOJUEGOS", "jugar a los videojuegos")
def videojuegos(c):
    c.poly(rrect_pts(8, 32, 84, 44, 18), PURPLE, INK, 2.8)
    c.poly([(8, 56), (8, 66), (14, 78), (28, 78), (34, 66), (34, 56)], PURPLE, INK, 2.6)
    c.poly([(92, 56), (92, 66), (86, 78), (72, 78), (66, 66), (66, 56)], PURPLE, INK, 2.6)
    c.rect(12, 38, 76, 32, PURPLE, None, 1, 14)
    # cruceta
    c.rect(22, 47, 20, 7, INK, None, 1, 2)
    c.rect(28.5, 40.5, 7, 20, INK, None, 1, 2)
    # botones
    for (x, y, col) in ((72, 42, GREEN), (82, 51, RED), (72, 60, YELLOW), (62, 51, BLUE)):
        c.circle((x, y), 4.8, col, INK, 1.8)
    # sticks
    c.circle((44, 66), 5, LGREY, INK, 2)
    c.circle((58, 66), 5, LGREY, INK, 2)
    c.rect(36, 14, 28, 14, LBLUE, INK, 2.4, 3)
    c.sparkle(50, 21, 4.5, YELLOW)
