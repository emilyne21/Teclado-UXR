from .draw import *          # noqa: F401,F403
from .draw import arc_pts
from .registry import icon


@icon("ui_hablar", "HABLAR", "")
def ui_hablar(c):
    c.poly([(10, 38), (28, 38), (50, 18), (50, 82), (28, 62), (10, 62)], WHITE, INK, 3.4)
    for r, w in ((16, 6), (28, 6), (40, 6)):
        c.arc((48, 50), r, -45, 45, w + 3, INK)
        c.arc((48, 50), r, -45, 45, w, WHITE)


@icon("ui_borrar", "BORRAR", "")
def ui_borrar(c):
    c.poly([(8, 50), (30, 22), (90, 22), (90, 78), (30, 78)], WHITE, INK, 3.4)
    c.line((44, 38), (72, 62), 9, INK)
    c.line((72, 38), (44, 62), 9, INK)
    c.line((44, 38), (72, 62), 5, RED)
    c.line((72, 38), (44, 62), 5, RED)


@icon("ui_limpiar", "LIMPIAR", "")
def ui_limpiar(c):
    c.rect(18, 26, 64, 8, WHITE, INK, 3.2, 3)
    c.rect(38, 16, 24, 10, WHITE, INK, 3.2, 3)
    c.poly([(24, 36), (76, 36), (70, 90), (30, 90)], WHITE, INK, 3.4)
    for x in (40, 50, 60):
        c.line((x, 46), (x - (x - 50) * 0.1, 80), 3, GREY)


@icon("ui_anterior", "ANTERIOR", "")
def ui_anterior(c):
    c.poly([(8, 50), (46, 12), (46, 34), (92, 34), (92, 66), (46, 66), (46, 88)], WHITE, INK, 3.4)


@icon("ui_siguiente", "SIGUIENTE", "")
def ui_siguiente(c):
    c.poly([(92, 50), (54, 12), (54, 34), (8, 34), (8, 66), (54, 66), (54, 88)], WHITE, INK, 3.4)
