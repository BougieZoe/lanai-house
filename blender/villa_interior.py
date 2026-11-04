"""Interior partitions, joinery, furniture and the lived-in details."""
from __future__ import annotations
import math

import bpy
from mathutils import Vector

from villa_config import *
from villa_geometry import (
    box, cylinder, sphere, beam, plane, material,
    get_collection, text_mesh,
)
from villa_architecture import wall_x, wall_y, sliding_x_wood

mats = {}


def _mats(mats):
    if "tatami" not in mats:
        mats["tatami"] = material("Tatami", (0.44, 0.43, 0.24), 0.9)
        mats["indigo"] = material("Indigo linen", (0.10, 0.17, 0.24), 0.9)
        mats["rust"] = material("Rust linen", (0.45, 0.18, 0.10), 0.9)
        mats["mustard"] = material("Mustard linen", (0.62, 0.46, 0.12), 0.9)
        mats["clay"] = material("Clay ceramic", (0.55, 0.32, 0.24), 0.62)
        mats["mirror"] = material("Mirror", (0.82, 0.84, 0.83), 0.03, 1.0)
        mats["rattan_dark"] = material("Dark rattan", (0.35, 0.24, 0.12), 0.8)
        mats["linen_sand"] = material("Sand linen", (0.66, 0.58, 0.45), 0.92)
        mats["olive"] = material("Olive linen", (0.27, 0.30, 0.19), 0.92)
        mats["clay_light"] = material("Pale clay", (0.74, 0.55, 0.40), 0.72)
        mats["brass"] = material("Brushed brass", (0.55, 0.38, 0.19), 0.28, 0.8)
        mats["curtain"] = material("Linen curtain", (0.86, 0.80, 0.69), 0.95)
        mats["cork"] = material("Cork board", (0.48, 0.33, 0.20), 0.95)
        mats["led_warm"] = material("Warm LED strip", (1.0, 0.72, 0.36), 0.4,
                                    emission=(1.0, 0.63, 0.25), emission_strength=5.0)
        mats["lamp_warm"] = material("Warm lamp shade", (1.0, 0.80, 0.55), 0.8,
                                     emission=(1.0, 0.68, 0.34), emission_strength=2.5)
    return mats


def rug(name, x0, x1, y0, y1, z, mat, coll, border=True):
    box(name, x0, x1, y0, y1, z, z+0.018, mat, coll, bevel=0.006)
    if border:
        w = 0.035
        for i, (a,b,c,d) in enumerate(((x0,x1,y0,y0+w),(x0,x1,y1-w,y1),
                                       (x0,x0+w,y0,y1),(x1-w,x1,y0,y1))):
            box(f"{name}_Border{i}", a, b, c, d, z+0.018, z+0.024,
                mats_border, coll) if False else None


def sofa(name, x0, x1, y0, y1, z, mat, coll, back="E", cushions=3):
    base_h = 0.22
    seat_h = 0.20
    back_t = 0.24
    box(name+"_Base", x0, x1, y0, y1, z+0.06, z+base_h, mat, coll, bevel=0.035)
    if back == "E":
        bx0, bx1 = x1-back_t, x1
        sy0, sy1 = y0, y1
        seat_x0, seat_x1 = x0, x1-back_t
        for i in range(cushions):
            a = sy0 + (sy1-sy0)*i/cushions + 0.02
            b = sy0 + (sy1-sy0)*(i+1)/cushions - 0.02
            box(f"{name}_Seat{i}", seat_x0+0.04, seat_x1-0.02, a, b,
                z+base_h, z+base_h+seat_h, mat, coll, bevel=0.04)
        box(name+"_Back", bx0, bx1, y0, y1, z+base_h, z+0.83, mat, coll, bevel=0.04)
        for i in range(2):
            box(f"{name}_Arm{i}", x0, x1, y0 if i==0 else y1-0.16,
                y0+0.16 if i==0 else y1, z+base_h, z+0.55, mat, coll, bevel=0.03)
    elif back == "W":
        bx0, bx1 = x0, x0+back_t
        for i in range(cushions):
            a = y0 + (y1-y0)*i/cushions + 0.02
            b = y0 + (y1-y0)*(i+1)/cushions - 0.02
            box(f"{name}_Seat{i}", bx1, x1-0.04, a, b,
                z+base_h, z+base_h+seat_h, mat, coll, bevel=0.04)
        box(name+"_Back", bx0, bx1, y0, y1, z+base_h, z+0.83, mat, coll, bevel=0.04)
        for i in range(2):
            box(f"{name}_Arm{i}", x0, x1, y0 if i==0 else y1-0.16,
                y0+0.16 if i==0 else y1, z+base_h, z+0.55, mat, coll, bevel=0.03)
    else:  # back N or S
        if back == "N":
            by0, by1 = y1-back_t, y1
            seat_y0, seat_y1 = y0, y1-back_t
            for i in range(cushions):
                a = x0 + (x1-x0)*i/cushions + 0.02
                b = x0 + (x1-x0)*(i+1)/cushions - 0.02
                box(f"{name}_Seat{i}", a, b, seat_y0+0.04, seat_y1-0.02,
                    z+base_h, z+base_h+seat_h, mat, coll, bevel=0.04)
            box(name+"_Back", x0, x1, by0, by1, z+base_h, z+0.83, mat, coll, bevel=0.04)
        else:
            by0, by1 = y0, y0+back_t
            seat_y0, seat_y1 = y0+back_t, y1
            for i in range(cushions):
                a = x0 + (x1-x0)*i/cushions + 0.02
                b = x0 + (x1-x0)*(i+1)/cushions - 0.02
                box(f"{name}_Seat{i}", a, b, seat_y0+0.02, seat_y1-0.04,
                    z+base_h, z+base_h+seat_h, mat, coll, bevel=0.04)
            box(name+"_Back", x0, x1, by0, by1, z+base_h, z+0.83, mat, coll, bevel=0.04)
    # little legs
    for i, (xx, yy) in enumerate(((x0+0.06,y0+0.06),(x1-0.06,y0+0.06),
                                   (x0+0.06,y1-0.06),(x1-0.06,y1-0.06))):
        box(f"{name}_Leg{i}", xx-0.025, xx+0.025, yy-0.025, yy+0.025,
            z, z+0.06, mats["teak_dark"], coll)
    # throw pillows
    for i in range(2):
        if back in ("E","W"):
            yy = y0 + (y1-y0)*(0.24+0.42*i)
            xx = (x1-0.32 if back=="E" else x0+0.06)
            box(f"{name}_Pillow{i}", xx, xx+0.24, yy, yy+0.34,
                z+base_h+seat_h, z+0.63, mats["indigo" if i==0 else "rust"], coll,
                bevel=0.05, rotation=(0,0,math.radians(8 if i==0 else -6)))
        else:
            xx = x0 + (x1-x0)*(0.24+0.42*i)
            yy = (y1-0.32 if back=="N" else y0+0.06)
            box(f"{name}_Pillow{i}", xx, xx+0.34, yy, yy+0.24,
                z+base_h+seat_h, z+0.63, mats["indigo" if i==0 else "rust"], coll,
                bevel=0.05, rotation=(0,0,math.radians(8 if i==0 else -6)))


def armchair(name, x, y, z, mat, coll, rot=0):
    r = math.radians(rot)
    box(name+"_Base", x-0.36, x+0.36, y-0.36, y+0.36, z+0.12, z+0.40,
        mat, coll, bevel=0.08)
    box(name+"_Back", x-0.34, x+0.34, y+0.20, y+0.38, z+0.34, z+0.92,
        mat, coll, bevel=0.07, rotation=(0,0,r))
    for i in range(2):
        box(f"{name}_Arm{i}", x-0.38+i*0.70, x-0.26+i*0.70, y-0.36, y+0.34,
            z+0.40, z+0.62, mat, coll, bevel=0.05)
    for i, (xx, yy) in enumerate(((x-0.28,y-0.28),(x+0.28,y-0.28),
                                   (x-0.28,y+0.28),(x+0.28,y+0.28))):
        box(f"{name}_Leg{i}", xx-0.02, xx+0.02, yy-0.02, yy+0.02, z, z+0.12,
            mats["teak_dark"], coll)


def dining_table(name, x0, x1, y0, y1, z, mat, coll):
    box(name+"_Top", x0, x1, y0, y1, z+0.72, z+0.76, mat, coll, bevel=0.01)
    for i, (xx, yy) in enumerate(((x0+0.10,y0+0.10),(x1-0.10,y0+0.10),
                                   (x0+0.10,y1-0.10),(x1-0.10,y1-0.10))):
        box(f"{name}_Leg{i}", xx-0.04, xx+0.04, yy-0.04, yy+0.04,
            z, z+0.72, mats["teak_dark"], coll)


def dining_chair(name, x, y, z, mat, coll, rot=0):
    r = math.radians(rot)
    box(name+"_Seat", x-0.22, x+0.22, y-0.22, y+0.22, z+0.42, z+0.47,
        mat, coll, bevel=0.02)
    # back on +y side, rotate the box around its centre
    box(name+"_Back", x-0.22, x+0.22, y+0.17, y+0.26, z+0.47, z+0.94,
        mat, coll, bevel=0.02, rotation=(0,0,r))
    for i, (px, py) in enumerate(((-0.18,-0.18),(0.18,-0.18),(-0.18,0.18),(0.18,0.18))):
        box(f"{name}_Leg{i}", x+px-0.02, x+px+0.02, y+py-0.02, y+py+0.02,
            z, z+0.42, mats["teak_dark"], coll)


def bed(name, x0, x1, y0, y1, z, head, coll, lin=None, accent=None):
    lin = lin or mats["linen_white"]
    accent = accent or mats["indigo"]
    box(name+"_Frame", x0, x1, y0, y1, z+0.12, z+0.34, mats["teak"], coll,
        bevel=0.03)
    box(name+"_Mattress", x0+0.04, x1-0.04, y0+0.04, y1-0.04, z+0.34, z+0.56,
        lin, coll, bevel=0.08)
    # duvet
    box(name+"_Duvet", x0+0.06, x1-0.06, y0+0.06, y1-0.32, z+0.54, z+0.64,
        accent, coll, bevel=0.06)
    # pillows at head
    if head == "W":
        for i in range(2):
            yy = y0 + (y1-y0)*(0.25+0.38*i)
            box(f"{name}_Pillow{i}", x0+0.10, x0+0.58, yy, yy+0.48,
                z+0.56, z+0.72, lin, coll, bevel=0.09)
        box(name+"_Headboard", x0-0.10, x0+0.03, y0-0.04, y1+0.04,
            z+0.12, z+1.10, mats["rattan"], coll, bevel=0.04)
    elif head == "E":
        for i in range(2):
            yy = y0 + (y1-y0)*(0.25+0.38*i)
            box(f"{name}_Pillow{i}", x1-0.58, x1-0.10, yy, yy+0.48,
                z+0.56, z+0.72, lin, coll, bevel=0.09)
        box(name+"_Headboard", x1-0.03, x1+0.10, y0-0.04, y1+0.04,
            z+0.12, z+1.10, mats["rattan"], coll, bevel=0.04)
    # bench at foot
    if head == "W":
        box(name+"_Bench", x1+0.10, x1+0.50, y0+0.20, y1-0.20,
            z+0.28, z+0.42, mats["mustard"], coll, bevel=0.03)
    else:
        box(name+"_Bench", x0-0.50, x0-0.10, y0+0.20, y1-0.20,
            z+0.28, z+0.42, mats["mustard"], coll, bevel=0.03)


def side_table(name, x, y, z, coll, r=0.22):
    cylinder(name+"_Top", r, 0.035, (x,y,z+0.52), mats["teak"], coll, vertices=18)
    cylinder(name+"_Post", 0.035, 0.50, (x,y,z+0.26), mats["black"], coll, vertices=10)


def wardrobe(name, x0, x1, y0, y1, z, coll, doors=3):
    box(name, x0, x1, y0, y1, z, z+2.30, mats["teak"], coll, bevel=0.02)
    for i in range(doors):
        a = x0 + (x1-x0)*i/doors + 0.01
        b = x0 + (x1-x0)*(i+1)/doors - 0.01
        box(f"{name}_Door{i}", a, b, y0-0.02, y0+0.01, z+0.05, z+2.25,
            mats["teak_light"], coll, bevel=0.006)
        cylinder(f"{name}_Handle{i}", 0.012, 0.18,
                 ((a+b)/2, y0-0.04, z+1.1), mats["black"], coll, vertices=8)


def desk(name, x0, x1, y0, y1, z, coll, chair_side="N"):
    box(name+"_Top", x0, x1, y0, y1, z+0.72, z+0.76, mats["teak"], coll, bevel=0.01)
    for i, (xx, yy) in enumerate(((x0+0.05,y0+0.05),(x1-0.05,y0+0.05),
                                   (x0+0.05,y1-0.05),(x1-0.05,y1-0.05))):
        box(f"{name}_Leg{i}", xx-0.025, xx+0.025, yy-0.025, yy+0.025,
            z, z+0.72, mats["black"], coll)
    # small drawer block
    box(name+"_Drawer", x0+0.05, x0+0.55, y0+0.08, y1-0.08, z+0.45, z+0.72,
        mats["teak_dark"], coll, bevel=0.01)


def bookshelf(name, x0, x1, y0, y1, z, coll, shelves=4):
    box(name+"_Back", x0, x1, y0, y0+0.05, z, z+1.95, mats["teak_dark"], coll)
    for side in (0,1):
        xx = x0 if side==0 else x1-0.05
        box(f"{name}_Side{side}", xx, xx+0.05, y0, y1, z, z+1.95,
            mats["teak"], coll)
    for i in range(shelves+1):
        zz = z + i*1.95/shelves
        box(f"{name}_Shelf{i}", x0, x1, y0, y1, zz, zz+0.04, mats["teak"], coll)
    # books
    rng = __import__("random").Random(int(x0*10))
    for i in range(shelves):
        for j in range(7):
            bw = rng.uniform(0.03, 0.06)
            bh = rng.uniform(0.22, 0.34)
            bx = x0+0.10+j*0.10
            box(f"{name}_Book{i}_{j}", bx, bx+bw, y0+0.06, y1-0.08,
                z+i*1.95/shelves+0.04, z+i*1.95/shelves+0.04+bh,
                mats[rng.choice(["indigo","rust","mustard","sage"])], coll)


def pendant(name, x, y, z, coll, drop=0.55, r=0.16):
    cylinder(name+"_Cord", 0.006, drop, (x,y,z-drop/2), mats["black"], coll,
             vertices=6)
    cylinder(name+"_Shade", r, 0.18, (x,y,z-drop), mats["lamp_soft"], coll,
             vertices=18)
    sphere(name+"_Bulb", 0.045, (x,y,z-drop-0.06), mats["lamp"], coll,
           segments=10, rings=8)


def floor_lamp(name, x, y, z, coll):
    cylinder(name+"_Base", 0.16, 0.035, (x,y,z+0.02), mats["black"], coll,
             vertices=18)
    cylinder(name+"_Stem", 0.018, 1.45, (x,y,z+0.75), mats["black"], coll,
             vertices=8)
    cylinder(name+"_Shade", 0.20, 0.24, (x,y,z+1.52), mats["lamp_soft"], coll,
             vertices=18)


def ceiling_fan(name, x, y, z, coll, span=0.75):
    cylinder(name+"_Rod", 0.015, 0.20, (x,y,z-0.10), mats["bronze"], coll,
             vertices=8)
    cylinder(name+"_Motor", 0.10, 0.12, (x,y,z-0.25), mats["bronze"], coll,
             vertices=14)
    for i in range(3):
        a = 2*math.pi*i/3
        box(f"{name}_Blade{i}", x-0.06, x+0.06, y-span, y+span,
            z-0.30, z-0.275, mats["teak"], coll, bevel=0.01,
            rotation=(0,0,a))


def plant(name, x, y, z, coll, pot_r=0.20, h=0.55):
    cylinder(name+"_Pot", pot_r, 0.40, (x,y,z+0.20), mats["terracotta"],
             coll, vertices=16)
    for i in range(4):
        a = 2*math.pi*i/4
        sphere(f"{name}_Leaf{i}", 0.90,
               (x+0.10*math.cos(a), y+0.10*math.sin(a), z+h),
               mats[f"leaf{i%4}"], coll, segments=10, rings=6,
               scale=(0.16, 0.16, 0.38))


def wall_art(name, x, y, z, w, h, coll, side="S", art=None):
    art = art or mats["indigo"]
    if side in ("S", "N"):
        yy0 = y if side == "S" else y-0.035
        yy1 = y+0.035 if side == "S" else y
        box(name+"_Frame", x-w/2, x+w/2, yy0, yy1, z-h/2, z+h/2,
            mats["teak_dark"], coll)
        box(name+"_Canvas", x-w/2+0.035, x+w/2-0.035, yy0-0.006, yy1+0.006,
            z-h/2+0.035, z+h/2-0.035, art, coll)
    else:
        xx0 = x if side == "W" else x-0.035
        xx1 = x+0.035 if side == "W" else x
        box(name+"_Frame", xx0, xx1, y-w/2, y+w/2, z-h/2, z+h/2,
            mats["teak_dark"], coll)
        box(name+"_Canvas", xx0-0.006, xx1+0.006, y-w/2+0.035, y+w/2-0.035,
            z-h/2+0.035, z+h/2-0.035, art, coll)


def toilet(mats, coll, prefix, x, y, z, rot=0):
    box(prefix+"_Base", x-0.20, x+0.20, y-0.28, y+0.28, z+0.10, z+0.38,
        mats["ceramic"], coll, bevel=0.07)
    box(prefix+"_Seat", x-0.22, x+0.22, y-0.30, y+0.26, z+0.38, z+0.43,
        mats["ceramic"], coll, bevel=0.04)
    box(prefix+"_Tank", x-0.20, x+0.20, y+0.22, y+0.42, z+0.38, z+0.78,
        mats["ceramic"], coll, bevel=0.04)


def basin(mats, coll, prefix, x, y, z):
    cylinder(prefix+"_Pedestal", 0.10, 0.55, (x, y, z+0.28), mats["ceramic"],
             coll, vertices=14)
    cylinder(prefix+"_Bowl", 0.20, 0.12, (x, y, z+0.60), mats["ceramic"],
             coll, vertices=18)
    cylinder(prefix+"_Faucet", 0.015, 0.22, (x, y+0.18, z+0.72), mats["chrome"],
             coll, vertices=8)


def powder_fixtures(mats, coll, prefix, x0, x1, y0, y1, z):
    toilet(mats, coll, prefix+"_Toilet", x0+0.40, y1-0.34, z)
    basin(mats, coll, prefix+"_Basin", x1-0.26, y0+0.34, z)


def bathroom_fixtures(mats, coll, prefix, x0, x1, y0, y1, z):
    # Japanese soaking tub along the north wall
    tx0, tx1 = x0+0.10, x1-0.18
    ty0, ty1 = y1-0.90, y1-0.10
    box(prefix+"_Tub", tx0, tx1, ty0, ty1, z+0.05, z+0.62, mats["ceramic"],
        coll, bevel=0.10)
    box(prefix+"_TubInner", tx0+0.13, tx1-0.13, ty0+0.13, ty1-0.13,
        z+0.46, z+0.58, mats["water"], coll)
    box(prefix+"_TubRim", tx0-0.03, tx1+0.03, ty0-0.03, ty1+0.03,
        z+0.58, z+0.66, mats["teak"], coll, bevel=0.02)
    # vanity along the east wall
    box(prefix+"_Vanity", x1-0.62, x1-0.02, y0+0.08, y0+0.78,
        z+0.55, z+0.86, mats["teak"], coll, bevel=0.01)
    cylinder(prefix+"_Basin", 0.15, 0.10, (x1-0.32, y0+0.43, z+0.90),
             mats["ceramic"], coll, vertices=18)
    cylinder(prefix+"_Faucet", 0.018, 0.26, (x1-0.32, y0+0.22, z+0.98),
             mats["chrome"], coll, vertices=8)
    box(prefix+"_Mirror", x1-0.60, x1-0.04, y0+0.075, y0+0.095,
        z+1.10, z+1.80, mats["mirror"], coll)
    # toilet
    toilet(mats, coll, prefix+"_Toilet", x0+0.38, y0+0.43, z)
    # wet-room shower in the south-west corner
    box(prefix+"_ShowerTray", x0+0.02, x0+0.92, y0+0.92, y1-1.02,
        z+0.01, z+0.08, mats["stone"], coll, bevel=0.01)
    box(prefix+"_ShowerGlass", x0+0.92, x0+0.95, y0+0.92, y1-1.02,
        z+0.08, z+1.85, mats["glass"], coll)
    cylinder(prefix+"_ShowerHead", 0.10, 0.02, (x0+0.48, y0+1.00, z+2.08),
             mats["chrome"], coll, vertices=16)
    cylinder(prefix+"_ShowerPipe", 0.018, 0.55, (x0+0.48, y0+0.98, z+1.82),
             mats["chrome"], coll, vertices=8)


def stair(mats):
    gf = get_collection("INTERIOR_GF")
    f2 = get_collection("INTERIOR_F2")
    x0, x1 = 3.62, 4.88
    y0 = -2.70
    rise = (F2-GF)/16
    run = 0.28
    for i in range(16):
        yy = y0 + i*run
        zt = GF + (i+1)*rise
        box(f"GF_Stair_Tread{i:02d}", x0, x1, yy, yy+run+0.035, zt-0.055, zt,
            mats["deck"], gf, bevel=0.008)
        # slim riser in black steel, set back to keep the stair light
        box(f"GF_Stair_Riser{i:02d}", x0+0.05, x1-0.05, yy-0.012, yy+0.012,
            zt-rise, zt-0.055, mats["black"], gf)
    # steel stringers
    for si, xx in enumerate((x0-0.02, x1+0.02)):
        beam(f"GF_Stair_Stringer_{si}", (xx, y0, GF+0.05),
             (xx, y0+16*run, F2+0.05), 0.06, 0.22, mats["black"], gf)
    # handrail on the west side
    for i in range(0, 16, 4):
        yy = y0 + i*run
        zt = GF + (i+1)*rise
        cylinder(f"GF_Stair_Post{i}", 0.018, 1.0, (x0-0.06, yy, zt+0.5),
                 mats["black"], gf, vertices=8)
    beam("GF_Stair_Handrail", (x0-0.06, y0, GF+1.0),
         (x0-0.06, y0+16*run, F2+1.0), 0.045, 0.045, mats["teak"], gf)
    # floor guard at the top
    rx = 3.45
    for i in range(8):
        yy = -2.75 + i*0.58
        box(f"F2_StairGuardPost{i}", rx-0.02, rx+0.02, yy-0.02, yy+0.02,
            F2, F2+1.02, mats["teak"], f2)
    box("F2_StairGuardTop", rx-0.025, rx+0.025, -2.80, 1.80,
        F2+0.98, F2+1.04, mats["teak"], f2)
    for i in range(7):
        yy = -2.65 + i*0.62
        box(f"F2_StairGuardGlass{i}", rx-0.008, rx+0.008, yy, yy+0.55,
            F2+0.10, F2+0.96, mats["glass"], f2)


def build_wing(mats):
    """Guest suite in the low west wing, with a compact ensuite."""
    gf = get_collection("INTERIOR_GF")
    x0, x1, y0, y1 = WING
    # doorway from the tea room through the main west wall
    dy0, dy1 = -1.78, -0.98
    box("GF_Wing_DoorFrameT", -5.035, -4.965, dy0-0.05, dy1+0.05, 2.52, 2.57,
        mats["teak"], gf)
    box("GF_Wing_DoorFrameL", -5.035, -4.965, dy0-0.05, dy0, GF, 2.57,
        mats["teak"], gf)
    box("GF_Wing_DoorFrameR", -5.035, -4.965, dy1, dy1+0.05, GF, 2.57,
        mats["teak"], gf)
    for i in range(2):
        yy = dy0+0.02 + i*0.38
        box(f"GF_Wing_DoorPanel{i}_Frame", -5.02, -4.98, yy, yy+0.36,
            GF+0.04, 2.46, mats["teak"], gf)
        box(f"GF_Wing_DoorPanel{i}_Paper", -5.015, -4.985, yy+0.04, yy+0.32,
            GF+0.12, 2.38, mats["paper"], gf)
    # a quiet guest room under the lower wing roof
    rug("GF_Wing_Rug", -8.05, -5.35, -2.10, 0.55, GF+0.012, mats["linen"], gf)
    bed("GF_Wing_Bed", -8.10, -6.25, -1.90, -0.10, GF, "W", gf,
        lin=mats["linen_white"], accent=mats["rust"])
    side_table("GF_Wing_Night0", -7.98, -2.15, GF, gf)
    side_table("GF_Wing_Night1", -7.98, -0.02, GF, gf)
    desk("GF_Wing_Desk", -7.65, -6.05, -2.52, -2.05, GF, gf)
    dining_chair("GF_Wing_Chair", -6.80, -2.35, GF, mats["teak"], gf, rot=180)
    # low chest and a reading corner
    box("GF_Wing_Chest", -5.70, -5.20, 0.35, 0.95, GF+0.05, GF+0.62,
        mats["teak"], gf, bevel=0.02)
    armchair("GF_Wing_Armchair", -7.10, 2.10, GF+0.02, mats["rattan"], gf, 45)
    side_table("GF_Wing_TeaTable", -7.90, 2.10, GF, gf, r=0.18)
    plant("GF_Wing_Plant", -5.55, 2.95, GF+0.02, gf, 0.18, 0.55)
    ceiling_fan("GF_Wing_Fan", -6.70, 0.40, GF+3.10, gf)
    wall_art("GF_Wing_Art", -6.95, -2.58, GF+1.65, 0.90, 0.70, gf, side="N",
             art=mats["indigo"])
    # ensuite: a compact wet room in the south-east corner
    bx0, bx1, by0, by1 = -6.55, -5.15, 1.00, 2.68
    wall_y("GF_Wing_BathW", bx0, by0, by1, GF, WING_EAVE_Z-0.30,
           [(1.65,2.25,GF,2.25)], mats["plaster_white"], gf, t=0.09)
    wall_x("GF_Wing_BathS", by0, bx0, bx1, GF, WING_EAVE_Z-0.30, [],
           mats["plaster_white"], gf, t=0.09)
    wall_x("GF_Wing_BathN", by1, bx0, bx1, GF, WING_EAVE_Z-0.30, [],
           mats["plaster_white"], gf, t=0.09)
    box("GF_Wing_BathFloor", bx0, bx1, by0, by1, GF, GF+0.03,
        mats["pool_tile"], gf, uv_scale=0.6)
    # toilet / basin / shower, laid out for the 1.4 x 1.7 m room
    toilet(mats, gf, "GF_Wing_Toilet", -5.42, 2.37, GF)
    basin(mats, gf, "GF_Wing_Basin", -5.42, 1.28, GF)
    box("GF_Wing_ShowerTray", -6.45, -5.90, 1.10, 1.95, GF+0.03, GF+0.09,
        mats["stone"], gf, bevel=0.01)
    box("GF_Wing_ShowerGlass", -5.92, -5.89, 1.10, 1.95, GF+0.09, GF+1.90,
        mats["glass"], gf)
    cylinder("GF_Wing_ShowerHead", 0.09, 0.02, (-6.15, 1.12, GF+2.05),
             mats["chrome"], gf, vertices=14)
    return gf


def build_interior(mats):
    globals()["mats"] = mats
    _mats(mats)
    gf = get_collection("INTERIOR_GF")
    f2 = get_collection("INTERIOR_F2")

    print("  int: GF partitions", flush=True)
    # ---------------------------------------------------------- GF partitions
    wall_y("GF_Part_TeaE", -2.95, -4.10, -0.25, GF, F2, [(-3.95,-3.15,GF,2.55)],
           mats["plaster_white"], gf, t=0.10)
    wall_x("GF_Part_TeaN", -0.25, -4.88, -2.95, GF, F2, [],
           mats["plaster_white"], gf, t=0.10)
    wall_y("GF_Part_PowderW", -3.70, 0.0, 1.35, GF, F2, [(0.35,1.00,GF,2.25)],
           mats["plaster_white"], gf, t=0.10)
    wall_x("GF_Part_PowderS", 0.0, -4.88, -3.70, GF, F2, [],
           mats["plaster_white"], gf, t=0.10)
    wall_x("GF_Part_PowderN", 1.35, -4.88, -3.70, GF, F2, [],
           mats["plaster_white"], gf, t=0.10)
    wall_y("GF_Part_LaundryE", -2.95, 1.55, 3.55, GF, F2, [(2.35,3.05,GF,2.2)],
           mats["plaster_white"], gf, t=0.10)
    wall_x("GF_Part_LaundryS", 1.55, -4.88, -2.95, GF, F2, [],
           mats["plaster_white"], gf, t=0.10)
    wall_x("GF_Part_WC_S", 2.00, 3.50, 4.95, GF, F2, [],
           mats["plaster_white"], gf, t=0.10)
    wall_y("GF_Part_WC_W", 3.50, 2.00, 3.55, GF, F2, [(2.20,2.85,GF,2.2)],
           mats["plaster_white"], gf, t=0.10)

    print("  int: tea room", flush=True)
    # tea room tatami, low table, tokonoma
    box("GF_Tea_TatamiBase", -4.84, -3.02, -3.98, -0.40, GF, GF+0.06,
        mats["teak_dark"], gf)
    for i in range(2):
        for j in range(2):
            x0 = -4.82 + i*0.90
            y0 = -3.95 + j*1.75
            box(f"GF_Tea_Mat{i}_{j}", x0, x0+0.88, y0, y0+1.72,
                GF+0.06, GF+0.09, mats["tatami"], gf, bevel=0.004)
            box(f"GF_Tea_MatEdge{i}_{j}", x0, x0+0.88, y0, y0+0.035,
                GF+0.09, GF+0.095, mats["indigo"], gf)
    box("GF_Tea_Table", -4.30, -3.45, -2.35, -1.70, GF+0.26, GF+0.31,
        mats["teak"], gf, bevel=0.01)
    for i, (xx,yy) in enumerate(((-4.20,-2.25),(-3.55,-2.25),(-4.20,-1.80),(-3.55,-1.80))):
        cylinder(f"GF_Tea_Cushion{i}", 0.19, 0.06, (xx,yy,GF+0.12),
                 mats["indigo" if i%2 else "rust"], gf, vertices=18)
    # tokonoma at north
    box("GF_Tea_Tokonoma", -4.80, -3.35, -0.80, -0.32, GF+0.06, GF+0.22,
        mats["teak"], gf, bevel=0.01)
    box("GF_Tea_Scroll", -4.50, -3.70, -0.34, -0.31, GF+0.55, GF+1.65,
        mats["paper"], gf)
    cylinder("GF_Tea_Vase", 0.10, 0.34, (-4.10, -0.55, GF+0.38),
             mats["ceramic_dark"], gf, vertices=14)
    for i in range(3):
        beam(f"GF_Tea_Branch{i}", (-4.10,-0.55,GF+0.5),
             (-4.10+(i-1)*0.18, -0.55-0.06, GF+1.15+i*0.12), 0.012, 0.012,
             mats["bark_dark"], gf)
    text_mesh("GF_Tea_Calligraphy", "WA", (-4.10, -0.345, GF+1.30), 0.24,
              mats["teak_dark"], gf, rot=(math.pi/2,0,0), extrude=0.002)
    # shoji screens on the east side, two open panels
    for i in range(2):
        yy = -3.95 + i*0.40
        box(f"GF_Tea_ShojiFrameL{i}", -2.955, -2.93, yy, yy+0.04, GF, GF+2.2,
            mats["teak"], gf)
        box(f"GF_Tea_ShojiFrameT{i}", -2.955, -2.93, yy, yy+0.38, GF+2.16,
            GF+2.20, mats["teak"], gf)
        box(f"GF_Tea_ShojiPaper{i}", -2.95, -2.94, yy+0.04, yy+0.38,
            GF+0.10, GF+2.12, mats["paper"], gf)
        for j in range(4):
            box(f"GF_Tea_ShojiMullion{i}_{j}", -2.956, -2.928,
                yy+0.04+j*0.085, yy+0.05+j*0.085, GF+0.10, GF+2.12,
                mats["teak"], gf)

    print("  int: powder", flush=True)
    # powder room
    powder_fixtures(mats, gf, "GF_Powder", -4.75, -3.82, 0.15, 1.28, GF)

    print("  int: laundry", flush=True)
    # laundry
    box("GF_Laundry_Washer", -4.70, -4.10, 2.95, 3.50, GF+0.05, GF+0.88,
        mats["white_paint"], gf, bevel=0.03)
    cylinder("GF_Laundry_Drum", 0.24, 0.05, (-4.40, 2.98, GF+0.48),
             mats["glass_dark"], gf, axis="Y", vertices=20)
    box("GF_Laundry_Counter", -4.75, -4.10, 1.60, 2.35, GF+0.82, GF+0.86,
        mats["teak"], gf)
    box("GF_Laundry_Storage", -4.75, -4.10, 1.60, 2.35, GF+0.05, GF+0.82,
        mats["white_paint"], gf)
    for i in range(3):
        box(f"GF_Laundry_Shelf{i}", -4.75, -3.05, 3.30, 3.38, GF+1.2+i*0.4,
            GF+1.24+i*0.4, mats["teak"], gf)
    for i in range(4):
        box(f"GF_Laundry_Towel{i}", -4.65+i*0.12, -4.55+i*0.12, 3.28, 3.40,
            GF+1.26, GF+1.55, mats["linen"], gf)
    # water heater
    cylinder("GF_Laundry_Heater", 0.24, 0.80, (-3.35, 3.10, GF+1.25),
             mats["white_paint"], gf, vertices=16)

    print("  int: living", flush=True)
    # living room
    rug("GF_Living_Rug", -2.45, 0.65, -3.65, -0.95, GF+0.012, mats["linen"], gf)
    sofa("GF_Living_Sofa", 0.15, 0.92, -3.10, -1.05, GF+0.02, mats["linen_sand"],
         gf, back="E", cushions=3)
    box("GF_Living_Coffee", -1.30, -0.10, -2.80, -1.70, GF+0.34, GF+0.40,
        mats["stone_light"], gf, bevel=0.02)
    for i, (xx,yy) in enumerate(((-1.20,-2.68),(-0.18,-2.68),(-1.20,-1.82),(-0.18,-1.82))):
        cylinder(f"GF_Living_CoffeeLeg{i}", 0.025, 0.32, (xx,yy,GF+0.17),
                 mats["black"], gf, vertices=8)
    armchair("GF_Living_Chair0", -2.15, -3.15, GF+0.02, mats["rattan"], gf, 105)
    armchair("GF_Living_Chair1", -2.15, -2.05, GF+0.02, mats["rattan"], gf, 75)
    # TV / console on the tea-room wall
    box("GF_Living_TVConsole", -2.80, -2.55, -3.55, -1.15, GF+0.10, GF+0.42,
        mats["teak"], gf, bevel=0.01)
    box("GF_Living_TV", -2.815, -2.80, -3.25, -1.55, GF+0.65, GF+1.42,
        mats["tv"], gf, bevel=0.01)
    floor_lamp("GF_Living_Lamp", -2.30, -0.95, GF+0.02, gf)
    plant("GF_Living_Plant", -2.33, -3.45, GF+0.02, gf, 0.18, 0.62)
    ceiling_fan("GF_Living_Fan", -0.55, -2.15, GF+3.05, gf)
    wall_art("GF_Living_Art", -2.70, -0.70, GF+1.65, 0.75, 1.05, gf, side="E" if False else "W", art=mats["rust"])

    print("  int: dining", flush=True)
    # dining
    rug("GF_Dining_Rug", -1.45, 1.05, -0.35, 1.45, GF+0.010, mats["rattan"], gf)
    dining_table("GF_Dining_Table", -1.35, 0.95, -0.20, 1.20, GF, mats["teak"], gf)
    for i, (xx, yy) in enumerate(((-1.05,-0.50),(-0.20,-0.50),(0.65,-0.50),
                                    (-1.05,1.50),(-0.20,1.50),(0.65,1.50))):
        dining_chair(f"GF_Dining_Chair{i}", xx, yy, GF, mats["teak"], gf,
                     rot=0 if i<3 else 180)
    for i, xx in enumerate((-0.95, -0.20, 0.55)):
        pendant(f"GF_Dining_Pendant{i}", xx, 0.50, GF+3.15, gf, drop=0.55, r=0.13)
    # table setting
    for i, xx in enumerate((-0.85, -0.20, 0.45)):
        cylinder(f"GF_Dining_Plate{i}", 0.14, 0.015, (xx, 0.20, GF+0.765),
                 mats["ceramic"], gf, vertices=18)
        cylinder(f"GF_Dining_Cup{i}", 0.04, 0.08, (xx+0.22, 0.28, GF+0.80),
                 mats["ceramic_dark"], gf, vertices=12)

    print("  int: kitchen", flush=True)
    # kitchen
    box("GF_Kitchen_Counter", -2.70, -2.12, 1.60, 3.48, GF+0.05, GF+0.90,
        mats["teak"], gf, bevel=0.01)
    box("GF_Kitchen_Top", -2.74, -2.08, 1.56, 3.50, GF+0.90, GF+0.95,
        mats["stone_light"], gf, bevel=0.01)
    # sink
    box("GF_Kitchen_Sink", -2.56, -2.26, 2.05, 2.55, GF+0.90, GF+0.96,
        mats["steel"], gf, bevel=0.02)
    cylinder("GF_Kitchen_Faucet", 0.018, 0.36, (-2.62, 2.58, GF+1.10),
             mats["chrome"], gf, vertices=8)
    # cooktop
    box("GF_Kitchen_Cooktop", -2.56, -2.22, 2.85, 3.30, GF+0.95, GF+0.965,
        mats["black"], gf, bevel=0.005)
    for i in range(4):
        cylinder(f"GF_Kitchen_Burner{i}", 0.085, 0.01,
                 (-2.52+0.15*(i%2), 2.96+0.15*(i//2), GF+0.97),
                 mats["steel"], gf, vertices=14)
    # tall fridge
    box("GF_Kitchen_Fridge", -2.68, -2.12, 0.98, 1.55, GF+0.05, GF+1.95,
        mats["white_paint"], gf, bevel=0.03)
    box("GF_Kitchen_FridgeDoor", -2.66, -2.14, 0.96, 0.98, GF+0.10, GF+1.90,
        mats["white_paint"], gf)
    # island and stools
    box("GF_Kitchen_Island", -1.55, -0.18, 2.02, 2.72, GF+0.05, GF+0.90,
        mats["teak"], gf, bevel=0.01)
    box("GF_Kitchen_IslandTop", -1.62, -0.10, 1.96, 2.78, GF+0.90, GF+0.95,
        mats["stone_light"], gf, bevel=0.01)
    for i, yy in enumerate((2.12, 2.55)):
        cylinder(f"GF_Kitchen_Stool{i}_Seat", 0.17, 0.06, (0.08, yy, GF+0.69),
                 mats["rattan"], gf, vertices=16)
        for j in range(3):
            a = 2*math.pi*j/3
            box(f"GF_Kitchen_Stool{i}_Leg{j}", 0.08+0.11*math.cos(a)-0.012,
                0.08+0.11*math.cos(a)+0.012, yy+0.11*math.sin(a)-0.012,
                yy+0.11*math.sin(a)+0.012, GF+0.05, GF+0.69,
                mats["black"], gf)
    # open shelving on the west wall
    for i in range(3):
        box(f"GF_Kitchen_Shelf{i}", -2.80, -2.68, 1.55, 3.45, GF+1.3+i*0.36,
            GF+1.34+i*0.36, mats["teak"], gf)
    for i in range(7):
        cylinder(f"GF_Kitchen_Jar{i}", 0.06, 0.12, (-2.74, 1.70+i*0.22, GF+1.42),
                 mats["ceramic" if i%2 else "clay"], gf, vertices=12)
    print("  int: entry", flush=True)
    # entry
    box("GF_Entry_Stone", 0.92, 3.30, -4.05, -2.55, GF, GF+0.028,
        mats["stone_light"], gf, bevel=0.01)
    box("GF_Entry_Shoe", 2.58, 3.27, -3.95, -3.05, GF+0.05, GF+0.92,
        mats["teak"], gf, bevel=0.01)
    for i in range(3):
        box(f"GF_Entry_ShoeDoor{i}", 2.60, 3.25, -3.90+0.01, -3.89,
            GF+0.10+i*0.27, GF+0.32+i*0.27, mats["teak_light"], gf)
    box("GF_Entry_Bench", 2.35, 2.92, -2.62, -2.30, GF+0.30, GF+0.36,
        mats["teak"], gf, bevel=0.01)
    for i, xx in enumerate((2.42, 2.84)):
        box(f"GF_Entry_BenchLeg{i}", xx-0.02, xx+0.02, -2.58, -2.34,
            GF+0.02, GF+0.30, mats["black"], gf)
    box("GF_Entry_Mirror", 3.275, 3.295, -3.95, -3.10, GF+0.90, GF+2.15,
        mats["mirror"], gf)
    for i in range(3):
        cylinder(f"GF_Entry_Hook{i}", 0.025, 0.10, (3.27, -2.62+i*0.22, GF+1.75),
                 mats["black"], gf, axis="X", vertices=8)
    box("GF_Entry_Mat", 1.10, 2.05, -3.80, -3.10, GF+0.028, GF+0.042,
        mats["rattan_dark"], gf, bevel=0.005)
    print("  int: stair/WC", flush=True)
    # stair and WC
    stair(mats)
    wall_x("GF_Part_WC_N", 3.55, 3.50, 4.95, GF, F2, [], mats["plaster_white"], gf, t=0.10)
    box("GF_WC_Toilet", 4.30, 4.75, 3.12, 3.50, GF+0.10, GF+0.75,
        mats["ceramic"], gf, bevel=0.06)
    box("GF_WC_Vanity", 3.56, 4.10, 2.10, 2.55, GF+0.55, GF+0.84,
        mats["teak"], gf, bevel=0.01)
    cylinder("GF_WC_Basin", 0.13, 0.10, (3.83, 2.32, GF+0.88),
             mats["ceramic"], gf, vertices=16)
    box("GF_WC_Mirror", 3.55, 3.57, 2.12, 2.55, GF+1.10, GF+1.75,
        mats["mirror"], gf)
    # corridor light
    pendant("GF_Corridor_Pendant", 4.14, 2.78, GF+3.0, gf, drop=0.45, r=0.11)

    print("  int: F2 partitions", flush=True)
    # ---------------------------------------------------------- F2 partitions
    wall_y("F2_Part_Central", -0.95, -4.15, 3.75, F2, EAVE,
           [(-3.30,-2.35,F2,5.55),(0.95,1.90,F2,5.55)],
           mats["plaster_white"], f2, t=0.10)
    wall_x("F2_Part_MasterKids", 0.08, -4.95, -0.95, F2, EAVE, [],
           mats["plaster_white"], f2, t=0.10)
    wall_x("F2_Part_StudyN", -0.58, -0.95, 3.45, F2, EAVE,
           [(1.65,2.45,F2,5.5)], mats["plaster_white"], f2, t=0.10)
    wall_y("F2_Part_BathW", 0.10, 1.35, 3.52, F2, EAVE,
           [(1.55,2.20,F2,5.3)], mats["plaster_white"], f2, t=0.10)
    wall_x("F2_Part_BathS", 1.35, 0.10, 2.38, F2, EAVE, [],
           mats["plaster_white"], f2, t=0.10)
    wall_y("F2_Part_BathE", 2.38, 1.35, 3.52, F2, EAVE, [],
           mats["plaster_white"], f2, t=0.10)
    wall_x("F2_Part_LinenS", 2.10, 2.45, 3.45, F2, EAVE,
           [(2.55,3.10,F2,5.2)], mats["plaster_white"], f2, t=0.10)
    wall_y("F2_Part_LinenW", 2.45, 2.10, 3.45, F2, EAVE, [],
           mats["plaster_white"], f2, t=0.10)

    print("  int: master", flush=True)
    # master bedroom
    rug("F2_Master_Rug", -4.55, -1.15, -3.55, -0.25, F2+0.014,
        mats["linen"], f2)
    bed("F2_Master_Bed", -4.55, -2.55, -2.55, -0.75, F2, "W", f2,
        lin=mats["linen_white"], accent=mats["indigo"])
    side_table("F2_Master_Night0", -4.30, -2.92, F2, f2)
    side_table("F2_Master_Night1", -4.30, -0.38, F2, f2)
    wardrobe("F2_Master_Wardrobe", -4.85, -2.35, -0.62, -0.02, F2, f2, doors=4)
    armchair("F2_Master_Chair", -1.55, -3.30, F2, mats["rattan"], f2, 45)
    floor_lamp("F2_Master_Lamp", -4.55, -0.42, F2, f2)
    ceiling_fan("F2_Master_Fan", -2.85, -1.75, F2+2.95, f2)
    wall_art("F2_Master_Art", -1.02, -1.55, F2+1.55, 0.85, 1.05, f2, side="E",
             art=mats["rust"])
    print("  int: kids", flush=True)
    # kids room
    rug("F2_Kids_Rug", -4.45, -1.35, 1.00, 3.35, F2+0.014, mats["mustard"], f2)
    # two low beds with playful colours
    bed("F2_Kids_Bed0", -4.62, -2.70, 1.05, 1.95, F2, "W", f2,
        lin=mats["linen_white"], accent=mats["rust"])
    bed("F2_Kids_Bed1", -4.62, -2.70, 2.30, 3.20, F2, "W", f2,
        lin=mats["linen_white"], accent=mats["indigo"])
    # desk under the north window
    desk("F2_Kids_Desk", -2.55, -1.05, 3.10, 3.55, F2, f2)
    dining_chair("F2_Kids_Chair", -1.80, 2.80, F2, mats["teak"], f2, rot=180)
    # low shelf and toy box
    box("F2_Kids_Shelf", -2.80, -1.55, 0.20, 0.55, F2+0.05, F2+0.85,
        mats["teak"], f2, bevel=0.01)
    for i in range(5):
        box(f"F2_Kids_Book{i}", -2.72+i*0.18, -2.62+i*0.18, 0.22, 0.52,
            F2+0.52, F2+0.80, mats[["rust","indigo","mustard","sage"][i%4]], f2)
    box("F2_Kids_ToyBox", -2.30, -1.55, 0.62, 0.95, F2+0.05, F2+0.42,
        mats["teak_light"], f2, bevel=0.02)
    ceiling_fan("F2_Kids_Fan", -2.60, 1.55, F2+2.95, f2)
    print("  int: study", flush=True)
    # study
    rug("F2_Study_Rug", 0.20, 3.05, -3.40, -1.10, F2+0.014,
        mats["indigo"], f2)
    desk("F2_Study_Desk", 0.15, 2.45, -3.55, -3.05, F2, f2)
    dining_chair("F2_Study_Chair", 1.30, -2.70, F2, mats["teak"], f2, rot=0)
    bookshelf("F2_Study_Shelf", 2.90, 3.35, -3.90, -1.00, F2, f2, shelves=5)
    box("F2_Study_Daybed", 0.15, 0.95, -2.55, -1.05, F2+0.10, F2+0.62,
        mats["linen"], f2, bevel=0.06)
    box("F2_Study_DaybedBack", 0.10, 0.20, -2.55, -1.05, F2+0.30, F2+1.10,
        mats["teak"], f2, bevel=0.03)
    floor_lamp("F2_Study_Lamp", 2.72, -3.75, F2, f2)
    ceiling_fan("F2_Study_Fan", 1.65, -2.25, F2+2.95, f2)
    print("  int: bath", flush=True)
    # bath
    bathroom_fixtures(mats, f2, "F2_Bath", 0.18, 2.28, 1.48, 3.42, F2)
    ceiling_fan("F2_Bath_Fan", 1.2, 2.3, F2+2.85, f2, span=0.35)
    print("  int: hall", flush=True)
    # hall, stair guard, console
    rug("F2_Hall_Rug", 0.10, 3.30, -0.40, 1.30, F2+0.014, mats["linen"], f2)
    box("F2_Hall_Console", 0.15, 1.35, 0.82, 1.12, F2+0.05, F2+0.82,
        mats["teak"], f2, bevel=0.01)
    plant("F2_Hall_Plant", 2.95, 0.30, F2+0.02, f2, 0.18, 0.55)
    wall_art("F2_Hall_Art", 1.95, -0.52, F2+1.55, 0.75, 0.95, f2, side="N",
             art=mats["rust"])
    pendant("F2_Hall_Pendant", 1.55, 0.35, F2+2.85, f2, drop=0.5, r=0.12)
    # rear balcony cafe table
    cylinder("F2_Balcony_Table", 0.30, 0.04, (1.85, 4.30, F2+0.70),
             mats["teak"], f2, vertices=18)
    cylinder("F2_Balcony_TablePost", 0.035, 0.60, (1.85, 4.30, F2+0.40),
             mats["black"], f2, vertices=8)
    for i, (xx, yy) in enumerate(((1.25,4.30),(2.45,4.30))):
        dining_chair(f"F2_Balcony_Chair{i}", xx, yy, F2, mats["rattan"], f2,
                     rot=90 if i==0 else -90)
    # linen closet
    for i in range(4):
        box(f"F2_Linen_Shelf{i}", 2.50, 3.40, 2.15, 3.40, F2+0.15+i*0.42,
            F2+0.19+i*0.42, mats["teak"], f2)
    for i in range(3):
        box(f"F2_Linen_Towel{i}", 2.60, 3.30, 2.25, 2.65, F2+0.20+i*0.42,
            F2+0.33+i*0.42, mats["linen"], f2, bevel=0.02)
    build_wing(mats)
    return gf, f2
