"""Pictogramas originales dibujados con código (ver picto/draw.py).

Importar este paquete registra todos los pictogramas en `ICONS`.
"""
from .registry import ICONS, get, render, clear_cache, OVERRIDE_DIR     # noqa: F401
from . import (set_needs, set_people, set_actions, set_food,             # noqa: F401
               set_feelings, set_places, set_social, set_body, set_ui)
