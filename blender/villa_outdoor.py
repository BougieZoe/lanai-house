"""The deep rear engawa, shaded garden pavilion and outdoor life."""
from __future__ import annotations
import math

import bpy
from mathutils import Vector

from villa_config import *
from villa_geometry import box, cylinder, sphere, beam, sphere, get_collection
from villa_landscape import cone_between, shrub, heliconia


def build_veranda(mats):
    tr = get_collection("HOUSE_TRIM")
    # low teak engawa running the width of the living room
    x0, x1, y0, y1 = -3.35, 4.95, MAIN[3], 5.28
    box("GF_Engawa_Slab", x0, x1, y0, y1, 0.24, 0.34, mats["concrete"], tr)
    n = int((x1-x0)/0.16)
    for i in range(n):
        xx = x0 + 0.02 + i*0.16
        box(f"GF_Engawa_Board_{i:02d}", xx, xx+0.14, y0+0.02, y1-0.02,
            0.34, 0.395, mats["deck"], tr, bevel=0.005)
    # a step down to the garden
    for i in range(2):
        box(f"GF_Engawa_Step_{i}", 0.30, 2.80, y1+0.02+i*0.30, y1+0.28+i*0.30,
            0.395-0.12*(i+1), 0.395-0.12*i, mats["stone_light"], tr, bevel=0.01)
    # slim posts and a slatted pergola at the west end
    for xx in (-3.28, 0.05):
        cylinder(f"GF_Engawa_Post_{xx}", 0.055, 2.95, (xx, y1-0.18, 0.40+2.95/2),
                 mats["teak"], tr, vertices=12)
    box("GF_Engawa_Beam", -3.38, 0.15, y1-0.28, y1-0.12, 3.26, 3.38,
        mats["teak_dark"], tr)
    box("GF_Engawa_BeamWall", -3.38, 0.15, y0+0.02, y0+0.15, 3.26, 3.38,
        mats["teak_dark"], tr)
    for i in range(12):
        yy = y0 + 0.10 + i*(y1-y0-0.20)/11
        box(f"GF_Engawa_Slat_{i:02d}", -3.40, 0.18, yy-0.035, yy+0.035,
            3.38, 3.43, mats["teak"], tr)
    # tea bench under the pergola
    box("GF_Engawa_Bench", -2.65, -1.15, 4.45, 4.95, 0.42, 0.48,
        mats["teak"], tr, bevel=0.015)
    for xx in (-2.55, -1.25):
        box(f"GF_Engawa_BenchLeg_{xx}", xx, xx+0.06, 4.50, 4.90, 0.395, 0.42,
            mats["teak_dark"], tr)
    box("GF_Engawa_Table", -2.35, -1.45, 4.55, 4.95, 0.62, 0.66,
        mats["teak"], tr, bevel=0.01)
    cylinder("GF_Engawa_TablePost", 0.05, 0.22, (-1.90, 4.75, 0.51),
             mats["teak_dark"], tr, vertices=10)
    # hanging pendant and paper lantern
    cylinder("GF_Engawa_PendantCord", 0.006, 0.5, (-1.60, 4.35, 3.10),
             mats["black"], tr, vertices=8)
    sphere("GF_Engawa_Pendant", 0.13, (-1.60, 4.35, 2.83), mats["lamp_soft"],
           tr, segments=16, rings=10, scale=(1, 1, 0.9))
    # rain chain from the gutter to a stone basin
    for i in range(11):
        cylinder(f"GF_RainChain_{i}", 0.013, 0.18,
                 (4.62, MAIN[3]+0.55, EAVE-0.30-i*0.24), mats["bronze"], tr,
                 vertices=8)
    cylinder("GF_RainBasin", 0.32, 0.34, (4.62, MAIN[3]+0.55, 0.23),
             mats["stone"], tr, vertices=18)
    # planters on the engawa edge
    for i, (x, y) in enumerate(((-3.05, 4.75), (0.55, 4.95), (4.45, 4.95))):
        box(f"GF_Engawa_Planter_{i}", x-0.20, x+0.20, y-0.20, y+0.20,
            0.40, 0.64, mats["terracotta"], tr, bevel=0.02)
        shrub(mats, get_collection("LANDSCAPE"), f"GF_Engawa_Plant_{i}",
              x, y, 0.20, 0.84, mats["leaf3"], 300+i, 3)


def build_pavilion(mats):
    site = get_collection("SITE")
    garden = get_collection("LANDSCAPE")
    x0, x1, y0, y1 = 2.55, 6.75, 6.95, 11.15
    # stone pad
    box("PAV_Pad", x0-0.25, x1+0.25, y0-0.25, y1+0.25, 0.02, 0.12,
        mats["stone_light"], site, uv_scale=1.2)
    # posts
    for i, (xx, yy) in enumerate(((x0+0.12, y0+0.12), (x1-0.12, y0+0.12),
                                  (x0+0.12, y1-0.12), (x1-0.12, y1-0.12))):
        box(f"PAV_Post_{i}", xx-0.075, xx+0.075, yy-0.075, yy+0.075, 0.12, 2.78,
            mats["teak"], site, bevel=0.006)
    # beams
    for i, yy in enumerate((y0, y1)):
        box(f"PAV_Beam_{i}", x0-0.10, x1+0.10, yy-0.09, yy+0.09, 2.72, 2.90,
            mats["teak_dark"], site)
    for i, xx in enumerate((x0, x1)):
        box(f"PAV_BeamX_{i}", xx-0.09, xx+0.09, y0, y1, 2.78, 2.96,
            mats["teak_dark"], site)
    # slatted roof with a slight gap pattern
    n = 17
    for i in range(n):
        yy = y0 + 0.06 + i*(y1-y0-0.12)/(n-1)
        box(f"PAV_Slat_{i:02d}", x0-0.18, x1+0.18, yy-0.042, yy+0.042,
            2.96, 3.04, mats["teak"], site)
    # table
    tx, ty = 4.55, 9.05
    box("PAV_TableTop", tx-1.15, tx+1.15, ty-0.50, ty+0.50, 0.70, 0.76,
        mats["teak"], site, bevel=0.015)
    for i, (xx, yy) in enumerate(((tx-1.0, ty-0.38), (tx+1.0, ty-0.38),
                                  (tx-1.0, ty+0.38), (tx+1.0, ty+0.38))):
        box(f"PAV_TableLeg_{i}", xx-0.04, xx+0.04, yy-0.04, yy+0.04, 0.12, 0.70,
            mats["teak_dark"], site)
    # six simple rattan chairs
    for i, (xx, yy, rot) in enumerate((
            (tx-1.55, ty-0.30, 90), (tx-1.55, ty+0.65, 90),
            (tx+1.55, ty-0.30, -90), (tx+1.55, ty+0.65, -90),
            (tx-0.35, ty-0.95, 0), (tx+0.60, ty-0.95, 0))):
        chair(mats, site, f"PAV_Chair_{i}", xx, yy, rot)
    # bench along the east edge
    box("PAV_Bench", x1-0.55, x1-0.10, 7.55, 10.35, 0.42, 0.48,
        mats["teak"], site, bevel=0.015)
    for i, yy in enumerate((7.65, 8.55, 9.45, 10.25)):
        box(f"PAV_BenchLeg_{i}", x1-0.50, x1-0.15, yy-0.04, yy+0.04, 0.12, 0.42,
            mats["teak_dark"], site)
    # pendant lamp
    cylinder("PAV_PendantCord", 0.008, 0.62, (tx, ty, 2.62), mats["black"], site,
             vertices=8)
    sphere("PAV_Pendant", 0.16, (tx, ty, 2.28), mats["lamp_soft"], site,
           segments=16, rings=10, scale=(1, 1, 0.92))
    # ceiling fan (static, angled blades)
    cylinder("PAV_FanRod", 0.018, 0.35, (tx, ty, 2.76), mats["bronze"], site,
             vertices=10)
    cylinder("PAV_FanMotor", 0.12, 0.13, (tx, ty, 2.57), mats["bronze"], site,
             vertices=14)
    for i in range(3):
        ang = 2*math.pi*i/3
        box(f"PAV_FanBlade_{i}", tx-0.06, tx+0.06, ty-0.55, ty+0.55,
            2.50, 2.53, mats["teak"], site,
            rotation=(0, 0, ang), bevel=0.01)
    # potted tropical plants at the pavilion corners
    for i, (xx, yy) in enumerate(((x0+0.20, y0+0.22), (x1-0.25, y1-0.25))):
        cylinder(f"PAV_Pot_{i}", 0.27, 0.48, (xx, yy, 0.36),
                 mats["terracotta"], site, vertices=18)
        shrub(mats, garden, f"PAV_Plant_{i}", xx, yy, 0.34, 0.88,
              mats["leaf2"], 320+i, 4)
    # climbing bougainvillea on the southwest post
    for i in range(5):
        ang = i*0.7
        cone_between(f"PAV_Vine_{i}", (x0+0.14, y0+0.15, 0.1),
                     (x0-0.05+0.25*math.cos(ang), y0+0.05+0.20*math.sin(ang),
                      1.4+i*0.25), 0.018, 0.012, mats["bark"], garden, 6)
    for i in range(6):
        sphere(f"PAV_VineFlower_{i}", 0.12,
               (x0-0.10+0.25*math.cos(i), y0+0.08+0.2*math.sin(i), 1.4+i*0.22),
               mats["pink_flower"], garden, segments=8, rings=6,
               scale=(1, 1, 0.5))


def chair(mats, coll, name, x, y, rot_deg=0):
    import math
    r = math.radians(rot_deg)
    c, s = math.cos(r), math.sin(r)
    def rot(px, py):
        return (x + px*c - py*s, y + px*s + py*c)
    seat = [(-0.24, -0.24), (0.24, -0.24), (0.24, 0.24), (-0.24, 0.24)]
    pts = [rot(px, py) for px, py in seat]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    box(name+"_Seat", min(xs), max(xs), min(ys), max(ys), 0.43, 0.48,
        mats["rattan"], coll, bevel=0.02)
    # back
    back = [rot(-0.24, 0.24), rot(0.24, 0.24), rot(0.24, 0.32), rot(-0.24, 0.32)]
    xs = [p[0] for p in back]; ys = [p[1] for p in back]
    box(name+"_Back", min(xs), max(xs), min(ys), max(ys), 0.48, 1.02,
        mats["rattan"], coll, bevel=0.02)
    for i, (px, py) in enumerate(((-0.20,-0.20),(0.20,-0.20),(-0.20,0.20),(0.20,0.20))):
        qx, qy = rot(px, py)
        box(f"{name}_Leg{i}", qx-0.025, qx+0.025, qy-0.025, qy+0.025,
            0.12, 0.43, mats["teak_dark"], coll)
