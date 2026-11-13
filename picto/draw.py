import math
from contextlib import contextmanager

import pygame

# --------------------------------------------------------------------------
# Paleta (colores planos con buen contraste)
# --------------------------------------------------------------------------
INK = (38, 40, 52)
WHITE = (255, 255, 255)
PAPER = (251, 247, 238)
LGREY = (228, 232, 238)
GREY = (176, 184, 196)
DGREY = (104, 112, 128)
RED = (226, 72, 64)
DRED = (160, 44, 48)
PINK = (246, 150, 172)
LPINK = (253, 214, 224)
ORANGE = (247, 150, 48)
LORANGE = (253, 205, 140)
YELLOW = (252, 208, 60)
LYELLOW = (255, 238, 160)
GREEN = (84, 176, 84)
LGREEN = (166, 216, 122)
DGREEN = (46, 124, 68)
BLUE = (66, 140, 222)
LBLUE = (164, 210, 248)
DBLUE = (38, 84, 168)
PURPLE = (146, 98, 196)
LPURPLE = (206, 184, 238)
BROWN = (140, 92, 56)
LBROWN = (204, 154, 104)
BEIGE = (242, 216, 172)
SKIN = (248, 206, 168)
SKIN_D = (222, 172, 132)
HAIR = (104, 68, 44)
HAIR_BLACK = (52, 42, 44)
HAIR_BLOND = (234, 192, 92)
HAIR_GREY = (196, 198, 206)
HAIR_RED = (196, 96, 52)
TEAL = (52, 170, 170)


# --------------------------------------------------------------------------
# Geometría
# --------------------------------------------------------------------------
def arc_pts(cx, cy, rx, ry, a0, a1, n=24, rot=0.0):
    """Puntos de un arco elíptico. Ángulos en grados, 0 = derecha, 90 = abajo."""
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        x, y = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + x * cr - y * sr, cy + x * sr + y * cr))
    return pts


def rrect_pts(x, y, w, h, r):
    r = min(r, w / 2.0, h / 2.0)
    if r <= 0.01:
        return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0),
                       (x + r, y + h - r, 90), (x + r, y + r, 180)):
        pts += arc_pts(cx, cy, r, r, a0, a0 + 90, 6)
    return pts


def spline_pts(points, closed=True, per=8):
    """Catmull-Rom: curva suave que pasa por los puntos dados."""
    n = len(points)
    out = []
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = points[(i - 1) % n] if (closed or i > 0) else points[0]
        p1 = points[i]
        p2 = points[(i + 1) % n]
        p3 = points[(i + 2) % n] if (closed or i + 2 < n) else points[-1]
        for k in range(per):
            t = k / float(per)
            t2, t3 = t * t, t * t * t
            out.append(tuple(
                0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t +
                       (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 +
                       (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3)
                for j in (0, 1)))
    if not closed:
        out.append(points[-1])
    return out


def crescent_pts(cx, cy, R, d=0.45, r=0.82, rot=0.0):
    """Media luna: círculo de radio R menos otro círculo desplazado d*R."""
    d, r = d * R, r * R
    x = (d * d + R * R - r * r) / (2 * d)
    y = math.sqrt(max(0.0, R * R - x * x))
    al = math.degrees(math.atan2(-y, x)) % 360
    be = math.degrees(math.atan2(y, x - d))
    # arco exterior: de la intersección superior, por la izquierda, a la inferior
    outer = arc_pts(0, 0, R, R, al, 360 - al, 22)
    inner = [(d + p[0], p[1]) for p in arc_pts(0, 0, r, r, be, 360 - be, 18)]
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return [(cx + px * cr - py * sr, cy + px * sr + py * cr) for px, py in outer + inner]


def heart_pts(cx, cy, s):
    pts = []
    for i in range(40):
        t = 2 * math.pi * i / 40
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s / 17.0, cy + y * s / 17.0 + s * 0.05))
    return pts


def star_pts(cx, cy, big, small, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = big if i % 2 == 0 else small
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# --------------------------------------------------------------------------
# Lienzo
# --------------------------------------------------------------------------
class Canvas:
    def __init__(self, size=400):
        self.size = size
        self.k = size / 100.0
        self.surf = pygame.Surface((size, size), pygame.SRCALPHA)
        self._m = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
        self._sc = 1.0
        self._stack = []

    # -- transformaciones --------------------------------------------------
    def push(self, tx=0.0, ty=0.0, scale=1.0, rot=0.0, flip=False):
        a, b, c, d, e, f = self._m
        r = math.radians(rot)
        co, si = math.cos(r) * scale, math.sin(r) * scale
        fx = -1.0 if flip else 1.0
        la, lb, lc, ld, le, lf = co * fx, si * fx, -si, co, tx, ty
        self._stack.append((self._m, self._sc))
        self._m = (a * la + c * lb, b * la + d * lb,
                   a * lc + c * ld, b * lc + d * ld,
                   a * le + c * lf + e, b * le + d * lf + f)
        self._sc *= scale

    def pop(self):
        self._m, self._sc = self._stack.pop()

    @contextmanager
    def at(self, tx=0.0, ty=0.0, scale=1.0, rot=0.0, flip=False):
        self.push(tx, ty, scale, rot, flip)
        try:
            yield self
        finally:
            self.pop()

    def _pt(self, p):
        a, b, c, d, e, f = self._m
        x, y = p
        return ((a * x + c * y + e) * self.k, (b * x + d * y + f) * self.k)

    def _w(self, w):
        return max(1.0, w * self._sc * self.k)

    # -- trazos ------------------------------------------------------------
    def _stroke_px(self, P, wpx, col, closed=False):
        r = wpx / 2.0
        pairs = list(zip(P, P[1:]))
        if closed and len(P) > 2:
            pairs.append((P[-1], P[0]))
        surf = self.surf
        for (ax, ay), (bx, by) in pairs:
            dx, dy = bx - ax, by - ay
            ln = math.hypot(dx, dy)
            if ln < 1e-6:
                continue
            nx, ny = -dy / ln * r, dx / ln * r
            pygame.draw.polygon(surf, col, ((ax + nx, ay + ny), (bx + nx, by + ny),
                                            (bx - nx, by - ny), (ax - nx, ay - ny)))
        if r >= 1.2:
            for x, y in P:
                pygame.draw.circle(surf, col, (x, y), r)

    def path(self, pts, w=3, col=INK, smooth=False, closed=False):
        if smooth:
            pts = spline_pts(pts, closed=closed)
        self._stroke_px([self._pt(p) for p in pts], self._w(w), col, closed)

    def line(self, a, b, w=3, col=INK):
        self.path([a, b], w, col)

    def curve(self, p0, p1, p2, w=3, col=INK, n=16):
        pts = []
        for i in range(n + 1):
            t = i / float(n)
            pts.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                        (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
        self.path(pts, w, col)

    def arc(self, c, r, a0, a1, w=3, col=INK, ry=None, rot=0.0):
        n = max(8, int(abs(a1 - a0) / 8))
        self.path(arc_pts(c[0], c[1], r, ry if ry is not None else r, a0, a1, n, rot), w, col)

    # -- formas rellenas ---------------------------------------------------
    def poly(self, pts, fill=None, line=INK, w=3, closed=True):
        P = [self._pt(p) for p in pts]
        if fill is not None and len(P) >= 3:
            pygame.draw.polygon(self.surf, fill, P)
        if line is not None:
            self._stroke_px(P, self._w(w), line, closed)

    def smooth(self, pts, fill=None, line=INK, w=3, per=8):
        self.poly(spline_pts(pts, True, per), fill, line, w)

    def ellipse(self, c, rx, ry, fill=None, line=INK, w=3, rot=0.0):
        n = int(max(20, min(110, (rx + ry) * self.k * self._sc * 0.55)))
        self.poly(arc_pts(c[0], c[1], rx, ry, 0, 360, n, rot), fill, line, w)

    def circle(self, c, r, fill=None, line=INK, w=3):
        self.ellipse(c, r, r, fill, line, w)

    def rect(self, x, y, w, h, fill=None, line=INK, lw=3, r=0):
        self.poly(rrect_pts(x, y, w, h, r), fill, line, lw)

    def heart(self, cx, cy, s, fill=RED, line=INK, w=2.4):
        self.poly(heart_pts(cx, cy, s), fill, line, w)

    def star(self, cx, cy, big, small=None, fill=YELLOW, line=INK, w=2.4, n=5, rot=-90):
        self.poly(star_pts(cx, cy, big, small if small else big * 0.46, n, rot), fill, line, w)

    def drop(self, cx, cy, s, fill=BLUE, line=INK, w=1.8):
        body = arc_pts(cx, cy + s * 0.38, s * 0.66, s * 0.66, -38, 218, 20)
        self.poly([(cx, cy - s)] + body, fill, line, w)

    def shine(self, pts, w=1.6, col=WHITE):
        self.path(pts, w, col, smooth=True)

    def sparkle(self, cx, cy, s, col=YELLOW, line=INK, w=1.4):
        self.poly([(cx, cy - s), (cx + s * 0.28, cy - s * 0.28), (cx + s, cy),
                   (cx + s * 0.28, cy + s * 0.28), (cx, cy + s), (cx - s * 0.28, cy + s * 0.28),
                   (cx - s, cy), (cx - s * 0.28, cy - s * 0.28)], col, line, w)

    def save(self, path):
        pygame.image.save(self.surf, path)


# --------------------------------------------------------------------------
# Piezas reutilizables: caras, cabezas, personas, manos
# --------------------------------------------------------------------------
def limb(c, pts, w, col, outline=1.6):
    c.path(pts, w + 2 * outline, INK)
    c.path(pts, w, col)


def face_features(c, cx, cy, r, mood):
    """Ojos, cejas y boca según el estado de ánimo (sin dibujar el óvalo)."""
    lw = max(1.5, r * 0.11)
    ex, ey, er = r * 0.38, cy - r * 0.12, r * 0.10

    def eyes_dots(dy=0.0, rr=er):
        c.circle((cx - ex, ey + dy), rr, INK, None)
        c.circle((cx + ex, ey + dy), rr, INK, None)

    def mouth(p0, p1, p2, w=lw, col=INK):
        c.curve((cx + p0[0] * r, cy + p0[1] * r), (cx + p1[0] * r, cy + p1[1] * r),
                (cx + p2[0] * r, cy + p2[1] * r), w, col)

    if mood == 'happy':
        eyes_dots()
        mouth((-0.46, 0.28), (0, 0.9), (0.46, 0.28))
    elif mood == 'laugh':
        for s in (-1, 1):
            c.arc((cx + s * ex, ey + er * 1.4), er * 1.9, 200, 340, lw)
        c.poly(arc_pts(cx, cy + r * 0.2, r * 0.5, r * 0.5, 0, 180, 14), (150, 42, 54), INK, lw * 0.8)
        c.ellipse((cx, cy + r * 0.62), r * 0.24, r * 0.12, (240, 110, 120), None)
    elif mood == 'sad':
        eyes_dots(r * 0.05)
        c.line((cx - ex - r * 0.22, cy - r * 0.28), (cx - ex + r * 0.2, cy - r * 0.44), lw * 0.9)
        c.line((cx + ex + r * 0.22, cy - r * 0.28), (cx + ex - r * 0.2, cy - r * 0.44), lw * 0.9)
        mouth((-0.4, 0.62), (0, 0.22), (0.4, 0.62))
        c.drop(cx - ex - r * 0.05, cy + r * 0.2, r * 0.22, LBLUE, BLUE, 1.0)
    elif mood == 'angry':
        eyes_dots(r * 0.06, er * 1.1)
        c.line((cx - ex - r * 0.28, cy - r * 0.46), (cx - ex + r * 0.2, cy - r * 0.2), lw * 1.2)
        c.line((cx + ex + r * 0.28, cy - r * 0.46), (cx + ex - r * 0.2, cy - r * 0.2), lw * 1.2)
        c.path([(cx - 0.42 * r, cy + 0.62 * r), (cx - 0.2 * r, cy + 0.45 * r), (cx, cy + 0.62 * r),
                (cx + 0.2 * r, cy + 0.45 * r), (cx + 0.42 * r, cy + 0.62 * r)], lw)
    elif mood == 'scared':
        for s in (-1, 1):
            c.circle((cx + s * ex, ey), r * 0.2, WHITE, INK, lw * 0.8)
            c.circle((cx + s * ex, ey + r * 0.03), r * 0.07, INK, None)
        c.arc((cx - ex, cy - r * 0.5), r * 0.22, 200, 340, lw * 0.8)
        c.arc((cx + ex, cy - r * 0.5), r * 0.22, 200, 340, lw * 0.8)
        c.ellipse((cx, cy + r * 0.55), r * 0.26, r * 0.2, (150, 42, 54), INK, lw * 0.8)
        c.drop(cx + r * 0.78, cy - r * 0.35, r * 0.2, LBLUE, BLUE, 1.0)
    elif mood == 'surprised':
        c.arc((cx - ex, cy - r * 0.5), r * 0.22, 200, 340, lw * 0.9)
        c.arc((cx + ex, cy - r * 0.5), r * 0.22, 200, 340, lw * 0.9)
        eyes_dots(0, er * 1.25)
        c.ellipse((cx, cy + r * 0.55), r * 0.2, r * 0.27, (150, 42, 54), INK, lw * 0.8)
    elif mood == 'tired':
        for s in (-1, 1):
            c.arc((cx + s * ex, ey), er * 1.8, 20, 160, lw)
            c.line((cx + s * ex - er * 1.8, ey + er * 0.3), (cx + s * ex + er * 1.8, ey + er * 0.3), lw * 0.7)
        c.ellipse((cx, cy + r * 0.52), r * 0.2, r * 0.26, (150, 42, 54), INK, lw * 0.8)
        c.path([(cx - 0.95 * r, cy + 0.15 * r), (cx - 0.7 * r, cy + 0.38 * r)], lw * 0.7, DGREY)
    elif mood == 'bored':
        for s in (-1, 1):
            c.circle((cx + s * ex, ey + er * 0.4), er * 1.5, WHITE, INK, lw * 0.7)
            c.circle((cx + s * ex + er * 0.5, ey + er * 0.6), er * 0.8, INK, None)
            c.line((cx + s * ex - er * 1.9, ey - er * 0.4), (cx + s * ex + er * 1.9, ey - er * 0.4), lw)
        c.line((cx - r * 0.3, cy + r * 0.58), (cx + r * 0.3, cy + r * 0.58), lw)
    elif mood == 'love':
        for s in (-1, 1):
            c.heart(cx + s * ex, ey, r * 0.34, RED, None)
        mouth((-0.42, 0.3), (0, 0.85), (0.42, 0.3))
        for s in (-1, 1):
            c.ellipse((cx + s * r * 0.68, cy + r * 0.3), r * 0.16, r * 0.1, (255, 150, 160), None)
    elif mood == 'calm':
        for s in (-1, 1):
            c.arc((cx + s * ex, ey + er * 0.4), er * 1.8, 20, 160, lw)
        mouth((-0.3, 0.42), (0, 0.7), (0.3, 0.42))
        for s in (-1, 1):
            c.ellipse((cx + s * r * 0.66, cy + r * 0.28), r * 0.16, r * 0.1, (255, 170, 160), None)
    elif mood == 'shy':
        for s in (-1, 1):
            c.circle((cx + s * ex - r * 0.06, ey + r * 0.12), er, INK, None)
            c.arc((cx + s * ex, ey - r * 0.08), er * 2.2, 200, 340, lw * 0.8)
        mouth((-0.2, 0.55), (0, 0.45), (0.2, 0.55))
        for s in (-1, 1):
            c.ellipse((cx + s * r * 0.64, cy + r * 0.22), r * 0.22, r * 0.14, (255, 120, 140), None)
    elif mood == 'nervous':
        eyes_dots(0, er * 1.1)
        c.line((cx - ex - r * 0.2, cy - r * 0.42), (cx - ex + r * 0.2, cy - r * 0.34), lw * 0.9)
        c.line((cx + ex + r * 0.2, cy - r * 0.42), (cx + ex - r * 0.2, cy - r * 0.34), lw * 0.9)
        c.path([(cx - 0.42 * r, cy + 0.55 * r), (cx - 0.21 * r, cy + 0.4 * r), (cx, cy + 0.55 * r),
                (cx + 0.21 * r, cy + 0.4 * r), (cx + 0.42 * r, cy + 0.55 * r)], lw * 0.9)
        c.drop(cx + r * 0.8, cy - r * 0.45, r * 0.2, LBLUE, BLUE, 1.0)
        c.drop(cx - r * 0.85, cy - r * 0.1, r * 0.16, LBLUE, BLUE, 1.0)
    elif mood == 'sick':
        for s in (-1, 1):
            c.arc((cx + s * ex, ey), er * 1.7, 20, 160, lw)
        c.path([(cx - 0.4 * r, cy + 0.6 * r), (cx - 0.2 * r, cy + 0.5 * r), (cx, cy + 0.62 * r),
                (cx + 0.2 * r, cy + 0.5 * r), (cx + 0.4 * r, cy + 0.6 * r)], lw * 0.9)
        # termómetro en la boca
        c.push(cx + r * 0.3, cy + r * 0.55, 1, 24)
        c.rect(0, -r * 0.07, r * 0.8, r * 0.14, WHITE, INK, lw * 0.6, r * 0.07)
        c.rect(0, -r * 0.07, r * 0.28, r * 0.14, RED, INK, lw * 0.5, r * 0.07)
        c.pop()
    elif mood == 'eat':
        eyes_dots()
        c.ellipse((cx, cy + r * 0.52), r * 0.3, r * 0.24, (150, 42, 54), INK, lw * 0.8)
        c.ellipse((cx, cy + r * 0.62), r * 0.16, r * 0.1, (240, 110, 120), None)
    elif mood == 'sleep':
        for s in (-1, 1):
            c.arc((cx + s * ex, ey), er * 1.8, 20, 160, lw)
        mouth((-0.2, 0.55), (0, 0.7), (0.2, 0.55))
    else:  # neutral
        eyes_dots()
        c.line((cx - r * 0.3, cy + r * 0.52), (cx + r * 0.3, cy + r * 0.52), lw)


def head(c, cx, cy, r, skin=SKIN, hair=HAIR, style='short', mood='happy',
         glasses=False, beard=False, fill=None, outline=None):
    """Cabeza con pelo. `fill` fuerza el color del óvalo (para caritas de emoción)."""
    lw = outline if outline else max(1.8, r * 0.13)
    if style in ('long', 'pigtails'):
        if style == 'long':
            c.ellipse((cx - r * 0.9, cy + r * 0.55), r * 0.42, r * 1.15, hair, INK, lw, rot=8)
            c.ellipse((cx + r * 0.9, cy + r * 0.55), r * 0.42, r * 1.15, hair, INK, lw, rot=-8)
        else:
            c.circle((cx - r * 1.05, cy + r * 0.15), r * 0.4, hair, INK, lw)
            c.circle((cx + r * 1.05, cy + r * 0.15), r * 0.4, hair, INK, lw)
    if style == 'bun':
        c.circle((cx, cy - r * 1.08), r * 0.42, hair, INK, lw)
    if style != 'none':
        c.circle((cx - r * 0.98, cy + r * 0.08), r * 0.2, skin, INK, lw * 0.8)
        c.circle((cx + r * 0.98, cy + r * 0.08), r * 0.2, skin, INK, lw * 0.8)
    c.circle((cx, cy), r, fill if fill else skin, INK, lw)
    if beard:
        pts = arc_pts(cx, cy, r * 1.0, r * 1.0, 20, 160, 16) + \
              [(cx - r * 0.5, cy + r * 0.38), (cx, cy + r * 0.28), (cx + r * 0.5, cy + r * 0.38)]
        c.poly(pts, hair, INK, lw * 0.8)
    face_features(c, cx, cy, r, mood)
    if style in ('short', 'long', 'bun', 'pigtails', 'cap'):
        pts = arc_pts(cx, cy - r * 0.02, r * 1.03, r * 1.03, 183, 357, 14)
        pts += [(cx + r * 0.84, cy - r * 0.26), (cx + r * 0.32, cy - r * 0.62),
                (cx - r * 0.32, cy - r * 0.4), (cx - r * 0.84, cy - r * 0.3)]
        c.poly(pts, hair, INK, lw)
    if glasses:
        for s in (-1, 1):
            c.circle((cx + s * r * 0.4, cy - r * 0.1), r * 0.27, None, INK, lw * 0.8)
        c.line((cx - r * 0.13, cy - r * 0.1), (cx + r * 0.13, cy - r * 0.1), lw * 0.8)


def bust(c, cx=50, cy=38, r=19, shirt=BLUE, skin=SKIN, **kw):
    """Retrato (cabeza y hombros)."""
    c.ellipse((cx, cy + r + 33), 29, 23, shirt, INK, 2.6)
    c.rect(cx - r * 0.3, cy + r * 0.7, r * 0.6, r * 0.9, skin, INK, 2.0, 2)
    c.poly([(cx - r * 0.3, cy + r * 1.4), (cx, cy + r * 1.85), (cx + r * 0.3, cy + r * 1.4)], skin, INK, 2.0)
    head(c, cx, cy, r, skin=skin, **kw)


def figure(c, head_pos, hr, shoulder, hip, arms=(), legs=(), back_arms=(), shirt=BLUE,
           pants=DBLUE, skin=SKIN, hair=HAIR, style='short', mood='happy', shoe=INK,
           tw=15, facing=1, skirt=False, glasses=False, beard=False):
    """Persona de cuerpo entero. arms/legs: listas de puntos (hombro-codo-mano, cadera-rodilla-pie)."""
    for a in back_arms:
        limb(c, a[:2], 6.2, shirt)
        limb(c, a[1:], 5.2, skin)
        c.circle(a[-1], 3.0, skin, INK, 1.4)
    for lg in legs:
        limb(c, lg[:2], 8.4, pants)
        limb(c, lg[1:], 7.6, pants)
        fx, fy = lg[-1]
        c.ellipse((fx + 2.6 * facing, fy + 1.2), 5.4, 3.0, shoe, INK, 1.4)
    limb(c, [shoulder, hip], tw, shirt, 1.6)
    if skirt:
        c.poly([(hip[0] - 7, hip[1] - 4), (hip[0] + 7, hip[1] - 4), (hip[0] + 13, hip[1] + 11), (hip[0] - 13, hip[1] + 11)],
               pants, INK, 1.8)
    for a in arms:
        limb(c, a[:2], 6.2, shirt)
        limb(c, a[1:], 5.2, skin)
        c.circle(a[-1], 3.0, skin, INK, 1.4)
    head(c, head_pos[0], head_pos[1], hr, skin=skin, hair=hair, style=style, mood=mood,
         glasses=glasses, beard=beard)


def hand_open(c, x, y, s=1.0, rot=0.0, skin=SKIN):
    """Mano abierta; los dedos apuntan hacia arriba antes de rotar."""
    with c.at(x, y, s, rot):
        for fx, fh in ((-6, 11), (-2, 13.5), (2, 12.5), (6, 9.5)):
            c.rect(fx - 1.9, -4 - fh, 3.8, fh + 3, skin, INK, 1.4, 1.9)
        with c.at(-9, 2, 1, -38):
            c.rect(-2.2, -9, 4.4, 11, skin, INK, 1.4, 2.2)
        c.rect(-8, -5, 16, 15, skin, INK, 1.6, 4)


def sparkles(c, pts, col=YELLOW):
    for (x, y, s) in pts:
        c.sparkle(x, y, s, col)
