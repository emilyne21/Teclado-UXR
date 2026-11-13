"""Imágenes de vista previa del tablero (sin abrir ventana)."""
import os
import tempfile

import pygame

import picto
from . import pages


def make_previews(cfg, base_dir, out_dir, size=None):
    from .app import App
    from .logger import SessionLogger
    os.makedirs(out_dir, exist_ok=True)
    cfg = dict(cfg)
    cfg["input_mode"] = "mouse"
    cfg["fullscreen"] = False
    cfg["speech"] = dict(cfg["speech"], enabled=False)
    tmp = tempfile.mkdtemp(prefix="picto_prev_")
    logger = SessionLogger(dict(cfg, log_samples=False), base_dir, log_dir=tmp)
    app = App(cfg, base_dir, headless=True, size=size, logger=logger)
    files = []
    try:
        # 1) cada página, y la de necesidades con una tecla en foco y una frase de ejemplo
        for i, cat in enumerate(pages.CATEGORIES, 1):
            app.board.set_category(cat.id)
            app.board.sentence = []
            path = os.path.join(out_dir, "%02d_%s.png" % (i, cat.id))
            app.save_preview(path)
            files.append(path)
        app.board.set_category("necesidades")
        app.board.sentence = ["yo", "quiero", "beber", "agua"][:3]
        path = os.path.join(out_dir, "10_ejemplo_frase_y_dwell.png")
        app.save_preview(path, focus_uid="picto:beber", progress=0.6, overlay=False)
        files.append(path)
        files.append(save_catalog(os.path.join(out_dir, "todos_los_pictogramas.png")))
    finally:
        app.close()
    return files


def save_catalog(path, cols=10, cell=150):
    """Hoja con todos los pictogramas y su nombre."""
    ids = [i for i in picto.ICONS if not i.startswith("ui_")]
    rows = (len(ids) + cols - 1) // cols
    pad, lab = 10, 26
    W = cols * (cell + pad) + pad
    H = rows * (cell + lab + pad) + pad
    sheet = pygame.Surface((W, H))
    sheet.fill((255, 255, 255))
    font = pygame.font.SysFont("segoeui,arial,dejavusans", 15, bold=True)
    for n, pid in enumerate(ids):
        r, c = divmod(n, cols)
        x, y = pad + c * (cell + pad), pad + r * (cell + lab + pad)
        pygame.draw.rect(sheet, (244, 244, 244), (x, y, cell, cell), border_radius=10)
        sheet.blit(picto.render(pid, cell - 10), (x + 5, y + 5))
        t = font.render(picto.ICONS[pid].label, True, (25, 25, 25))
        if t.get_width() > cell:
            t = pygame.transform.smoothscale(t, (cell, t.get_height()))
        sheet.blit(t, (x + (cell - t.get_width()) // 2, y + cell + 3))
    pygame.image.save(sheet, path)
    return path
