"""Kaze House — dimensions and palette.

Blender axes: X east, Y north, Z up. The street is south (-Y), the pool is north (+Y).
All dimensions in metres.
"""
from __future__ import annotations

# ------------------------------------------------------------------ site
SITE_X = (-13.0, 13.0)
SITE_Y = (-15.0, 16.0)
STREET_Y = -16.2
WALL_FRONT_Y = -15.0

# ----------------------------------------------------------------- house
GF = 0.35                     # ground-floor finished level
F2 = 3.55                     # upper-floor finished level
EAVE = 7.15                   # top of upper wall / roof eave
RIDGE = 9.45                  # main roof ridge

MAIN = (-5.0, 5.4, -4.2, 3.8)  # x0, x1, y0, y1
WING = (-8.4, -5.0, -2.6, 3.4)

# roof
ROOF_X = (-5.9, 6.3)
ROOF_Y = (-5.3, 4.9)
ROOF_RIDGE_Y = -0.2
ROOF_EAVE_Z = 7.12
ROOF_RIDGE_Z = 9.45

WING_ROOF = (-9.15, -4.35, -3.3, 4.1)
WING_RIDGE_X = -6.72
WING_EAVE_Z = 3.88
WING_RIDGE_Z = 5.15

# ------------------------------------------------------------------ pool
POOL = (-7.4, -1.8, 7.0, 10.6)   # x0, x1, y0, y1
POOL_DEPTH = 1.45
POOL_DECK = (-9.25, 2.10, 5.65, 12.3)

# --------------------------------------------------------------- palette
PALETTE = {
    "plaster": (0.88, 0.84, 0.75),
    "plaster_warm": (0.91, 0.86, 0.75),
    "stone": (0.55, 0.52, 0.46),
    "teak": (0.40, 0.24, 0.13),
    "teak_dark": (0.20, 0.11, 0.06),
    "roof": (0.58, 0.22, 0.12),
    "sage": (0.26, 0.36, 0.28),
    "sage_light": (0.40, 0.49, 0.39),
    "black": (0.045, 0.045, 0.04),
    "bronze": (0.19, 0.14, 0.09),
    "glass": (0.62, 0.76, 0.74),
    "tile_floor": (0.72, 0.68, 0.59),
    "concrete": (0.62, 0.60, 0.54),
    "linen": (0.83, 0.78, 0.68),
    "linen_white": (0.92, 0.90, 0.84),
    "rattan": (0.63, 0.46, 0.27),
    "grass": (0.31, 0.39, 0.15),
    "water": (0.10, 0.52, 0.53),
}
