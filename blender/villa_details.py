"""Lived-in interior details: curtains, lamps, styling and joinery.

This module sits on top of villa_interior.py and only adds loose objects, so the
room planning stays readable. Everything is modelled at real scale for the GLB.
"""
from __future__ import annotations
import math
import random

from villa_config import GF, F2, EAVE
from villa_geometry import box, cylinder, sphere, beam, material, get_collection

MATS = {}


def _mats(mats):
    mats.setdefault("linen_sand", material("Sand linen", (0.66, 0.58, 0.45), 0.92))
    mats.setdefault("olive", material("Olive linen", (0.27, 0.30, 0.19), 0.92))
    mats.setdefault("clay_light", material("Pale clay", (0.74, 0.55, 0.40), 0.72))
    mats.setdefault("brass", material("Brushed brass", (0.55, 0.38, 0.19), 0.28, 0.8))
    mats.setdefault("curtain", material("Linen curtain", (0.86, 0.80, 0.69), 0.95))
    mats.setdefault("sheer", material("Sheer curtain", (0.92, 0.89, 0.82), 0.98, alpha=0.55))
    mats.setdefault("cork", material("Cork board", (0.48, 0.33, 0.20), 0.95))
    mats.setdefault("led_warm", material("Warm LED strip", (1.0, 0.72, 0.36), 0.4,
                                        emission=(1.0, 0.63, 0.25), emission_strength=5.0))
    mats.setdefault("lamp_warm", material("Warm lamp shade", (1.0, 0.80, 0.55), 0.8,
                                         emission=(1.0, 0.68, 0.34), emission_strength=2.5))
    return mats


def table_lamp(name, x, y, z, coll, h=0.48, shade=0.115):
    cylinder(name + "_Base", 0.075, 0.035, (x, y, z + 0.018), MATS["brass"], coll, vertices=18)
    cylinder(name + "_Stem", 0.012, h, (x, y, z + h / 2), MATS["black"], coll, vertices=8)
    cylinder(name + "_Shade", shade, 0.18, (x, y, z + h + 0.04), MATS["lamp_warm"], coll,
             vertices=18, radius_top=shade * 0.78)
    sphere(name + "_Glow", 0.032, (x, y, z + h + 0.03), MATS["lamp"], coll, segments=10, rings=8)


def downlight(name, x, y, z, coll):
    cylinder(name + "_Trim", 0.075, 0.008, (x, y, z), MATS["black"], coll, vertices=16)
    cylinder(name + "_Lens", 0.052, 0.006, (x, y, z - 0.008), MATS["lamp"], coll, vertices=16)


def curtain(name, x0, x1, y, z0, z1, coll, folds=7):
    w = (x1 - x0) / folds
    for i in range(folds):
        a = x0 + i * w + 0.004
        b = a + w - 0.008
        yy = y + (0.018 if i % 2 else -0.018)
        box(f"{name}_{i}", a, b, yy - 0.012, yy + 0.012, z0, z1,
            MATS["curtain"], coll, bevel=0.004)


def curtain_rod(name, x0, x1, y, z, coll):
    cylinder(name, 0.014, x1 - x0, ((x0 + x1) / 2, y, z), MATS["black"], coll,
             axis="X", vertices=10)
    for i, xx in enumerate((x0 + 0.04, x1 - 0.04)):
        cylinder(f"{name}_Bracket{i}", 0.038, 0.02, (xx, y, z), MATS["black"], coll, axis="Y", vertices=12)


def ceramic(name, x, y, z, coll, r=0.10, h=0.30, mat=None):
    mat = mat or MATS["ceramic_dark"]
    cylinder(name, r, h, (x, y, z + h / 2), mat, coll, vertices=16, radius_top=r * 0.72)


def books(name, x, y, z, coll, count=3, w=0.24, d=0.17, rot=0):
    rng = random.Random(int((x + y + z) * 100))
    for i in range(count):
        hh = 0.035 + 0.012 * rng.random()
        box(f"{name}_{i}", x - w / 2, x + w / 2, y - d / 2, y + d / 2,
            z + i * hh, z + (i + 1) * hh,
            MATS[rng.choice(["indigo", "rust", "olive", "linen_sand"])], coll,
            bevel=0.006, rotation=(0, 0, math.radians(rot + rng.uniform(-4, 4))))


def throw(name, x0, x1, y0, y1, z0, mat, coll):
    box(name, x0, x1, y0, y1, z0, z0 + 0.035, mat, coll, bevel=0.012)


def art(name, x, y, z, w, h, side, mat, coll):
    if side in ("N", "S"):
        box(name + "_Frame", x - w / 2, x + w / 2, y - 0.025, y + 0.025, z - h / 2, z + h / 2,
            MATS["teak_dark"], coll)
        box(name + "_Canvas", x - w / 2 + 0.045, x + w / 2 - 0.045, y - 0.035, y - 0.025,
            z - h / 2 + 0.045, z + h / 2 - 0.045, mat, coll)
    else:
        box(name + "_Frame", x - 0.025, x + 0.025, y - w / 2, y + w / 2, z - h / 2, z + h / 2,
            MATS["teak_dark"], coll)
        box(name + "_Canvas", x - 0.035, x - 0.025, y - w / 2 + 0.045, y + w / 2 - 0.045,
            z - h / 2 + 0.045, z + h / 2 - 0.045, mat, coll)


def slat_wall(name, x0, x1, y0, y1, z0, z1, coll, slats=12):
    for i in range(slats):
        t = i / max(1, slats - 1)
        yy = y0 + (y1 - y0) * t
        box(f"{name}_{i}", x0, x1, yy - 0.018, yy + 0.018, z0, z1,
            MATS["teak_dark"], coll, bevel=0.002)


def build(mats):
    MATS.clear()
    MATS.update(mats)
    _mats(MATS)
    gf = get_collection("INTERIOR_GF")
    f2 = get_collection("INTERIOR_F2")
    trim = get_collection("HOUSE_TRIM")
    site = get_collection("SITE")
    pool = get_collection("POOL")

    # ---------------------------------------------------------------- living
    # a low console behind the sofa, with two quiet objects
    # throw and table styling
    throw("GF_Living_Throw", 0.18, 0.88, -2.55, -1.20, GF + 0.44, MATS["olive"], gf)
    books("GF_Living_Table_Books", -0.82, -2.46, GF + 0.40, gf, 3, 0.28, 0.20, 8)
    ceramic("GF_Living_Table_Bowl", -0.48, -2.05, GF + 0.40, gf, 0.12, 0.10, MATS["clay_light"])
    cylinder("GF_Living_Table_Candle", 0.034, 0.18, (-1.15, -2.30, GF + 0.50),
             MATS["ceramic"], gf, vertices=12)
    # linen curtains at the south windows
    curtain("GF_Living_Curtain_L", -2.82, -2.36, -3.98, GF + 0.16, GF + 2.82, gf, 6)
    curtain("GF_Living_Curtain_R", 0.30, 0.79, -3.98, GF + 0.16, GF + 2.82, gf, 6)
    curtain_rod("GF_Living_CurtainRod", -2.84, 0.82, -3.98, GF + 2.86, gf)
    # ceiling slats and warm downlights; part of F2 so the cutaway hides them
    for i in range(7):
        yy = -3.46 + i * 0.45
        box(f"GF_Living_CeilingSlat{i}", -2.82, 0.95, yy - 0.025, yy + 0.025,
            3.12, 3.16, MATS["teak_dark"], f2)
    for i, (xx, yy) in enumerate(((-1.95, -3.15), (-0.95, -3.15), (0.05, -3.15),
                                  (-1.95, -1.35), (-0.95, -1.35), (0.05, -1.35))):
        downlight(f"GF_Living_Down{i}", xx, yy, 3.11, f2)
    # linear diffuser above the entry side
    box("GF_Living_AC", 1.45, 2.95, -3.42, -3.30, 3.13, 3.16, MATS["black"], f2)

    # ---------------------------------------------------------------- dining
    box("GF_Dining_Runner", -1.18, 0.78, 0.35, 0.66, GF + 0.765, GF + 0.772,
        MATS["olive"], gf, bevel=0.004)
    ceramic("GF_Dining_Bowl", -0.20, 0.50, GF + 0.775, gf, 0.19, 0.11, MATS["ceramic"])
    for i, xx in enumerate((-0.37, -0.20, -0.03)):
        sphere(f"GF_Dining_Fruit{i}", 0.055,
               (xx, 0.50 + (i % 2) * 0.05, GF + 0.86), MATS["clay_light"], gf,
               segments=10, rings=8)
    for i, xx in enumerate((-0.95, 0.55)):
        cylinder(f"GF_Dining_Candle{i}", 0.026, 0.28, (xx, 0.50, GF + 0.90),
                 MATS["brass"], gf, vertices=12)
        sphere(f"GF_Dining_Flame{i}", 0.018, (xx, 0.50, GF + 1.06), MATS["lamp"], gf,
               segments=8, rings=6)
    # chair cushions
    for i, (xx, yy) in enumerate(((-1.05, -0.50), (-0.20, -0.50), (0.65, -0.50),
                                    (-1.05, 1.50), (-0.20, 1.50), (0.65, 1.50))):
        box(f"GF_Dining_Cushion{i}", xx - 0.19, xx + 0.19, yy - 0.19, yy + 0.19,
            GF + 0.475, GF + 0.505, MATS["linen_sand"], gf, bevel=0.015)

    # ---------------------------------------------------------------- kitchen
    # slim extractor over the cooktop
    box("GF_Kitchen_Hood", -2.66, -2.12, 2.78, 3.36, GF + 2.02, GF + 2.16,
        MATS["steel"], gf, bevel=0.01)
    box("GF_Kitchen_HoodDuct", -2.48, -2.30, 2.94, 3.20, GF + 2.16, GF + 2.72,
        MATS["steel"], gf)
    cylinder("GF_Kitchen_Kettle", 0.11, 0.16, (-2.38, 2.96, GF + 1.03),
             MATS["black"], gf, vertices=16)
    box("GF_Kitchen_CuttingBoard", -2.58, -2.26, 2.28, 2.67, GF + 0.965, GF + 0.985,
        MATS["teak_light"], gf, bevel=0.008)
    cylinder("GF_Kitchen_HerbPot0", 0.06, 0.12, (-2.55, 1.78, GF + 1.42),
             MATS["terracotta"], gf, vertices=12)
    cylinder("GF_Kitchen_HerbPot1", 0.06, 0.12, (-2.40, 1.78, GF + 1.42),
             MATS["terracotta"], gf, vertices=12)
    for i in range(5):
        sphere(f"GF_Kitchen_Herb{i}", 0.07,
               (-2.55 + (i % 2) * 0.15, 1.78, GF + 1.57 + (i // 2) * 0.03),
               MATS["leaf2"], gf, segments=8, rings=6, scale=(1, 1, 0.8))
    box("GF_Kitchen_Towel", -2.74, -2.55, 2.18, 2.36, GF + 0.66, GF + 0.68,
        MATS["linen_sand"], gf, bevel=0.008)
    box("GF_Kitchen_IslandFruit", -1.12, -0.84, 2.27, 2.52, GF + 0.95, GF + 0.97,
        MATS["olive"], gf, bevel=0.03)
    for i in range(3):
        sphere(f"GF_Kitchen_IslandFruit{i}", 0.06,
               (-1.04 + i * 0.08, 2.38, GF + 1.03), MATS["clay_light"], gf,
               segments=8, rings=6)

    # ------------------------------------------------------------------- tea
    cylinder("GF_Tea_Pot", 0.12, 0.14, (-3.86, -2.00, GF + 0.38), MATS["ceramic_dark"],
             gf, vertices=16)
    cylinder("GF_Tea_PotLid", 0.045, 0.04, (-3.86, -2.00, GF + 0.47), MATS["ceramic_dark"],
             gf, vertices=12)
    for i, (xx, yy) in enumerate(((-4.05, -1.82), (-3.68, -1.82), (-3.88, -2.20))):
        cylinder(f"GF_Tea_Cup{i}", 0.045, 0.06, (xx, yy, GF + 0.345), MATS["ceramic"],
                 gf, vertices=12)
    ceramic("GF_Tea_Flower", -4.42, -2.50, GF + 0.31, gf, 0.055, 0.20, MATS["clay"])
    for i in range(3):
        beam(f"GF_Tea_FlowerStem{i}", (-4.42, -2.50, GF + 0.48),
             (-4.42 + (i - 1) * 0.10, -2.50 - 0.03, GF + 0.86 + i * 0.04),
             0.007, 0.007, MATS["bark_dark"], gf)
    sphere("GF_Tea_PaperLantern", 0.16, (-4.00, -1.10, GF + 2.44), MATS["lamp_soft"],
           gf, segments=16, rings=10, scale=(1, 1, 0.85))
    cylinder("GF_Tea_LanternCord", 0.006, 0.50, (-4.00, -1.10, GF + 2.82),
             MATS["black"], gf, vertices=8)

    # ----------------------------------------------------------------- entry
    box("GF_Entry_BenchCushion", 2.35, 2.92, -2.62, -2.30, GF + 0.36, GF + 0.405,
        MATS["linen_sand"], gf, bevel=0.018)
    cylinder("GF_Entry_UmbrellaStand", 0.12, 0.44, (2.20, -3.62, GF + 0.24),
             MATS["ceramic_dark"], gf, vertices=16)
    for i in range(2):
        cylinder(f"GF_Entry_Umbrella{i}", 0.018, 0.85,
                 (2.20 + (i - 0.5) * 0.05, -3.62, GF + 0.62),
                 MATS["black"] if i == 0 else MATS["olive"], gf, vertices=8)
    for i, (xx, yy) in enumerate(((1.28, -3.55), (1.62, -3.52))):
        box(f"GF_Entry_Slipper{i}", xx - 0.11, xx + 0.11, yy - 0.05, yy + 0.18,
            GF + 0.05, GF + 0.09, MATS["linen_sand"], gf, bevel=0.02)
    box("GF_Entry_Tray", 2.48, 2.82, -2.55, -2.36, GF + 0.37, GF + 0.39,
        MATS["teak_light"], gf, bevel=0.006)
    cylinder("GF_Entry_Keys", 0.03, 0.012, (2.65, -2.46, GF + 0.40), MATS["brass"],
             gf, vertices=12)
    downlight("GF_Entry_Down", 1.70, -3.10, 3.11, f2)

    # ---------------------------------------------------------------- master
    table_lamp("F2_Master_Lamp0", -4.03, -2.92, F2 + 0.55, f2)
    table_lamp("F2_Master_Lamp1", -4.03, -0.38, F2 + 0.55, f2)
    throw("F2_Master_Throw", -3.02, -2.55, -2.50, -0.80, F2 + 0.64, MATS["olive"], f2)
    books("F2_Master_Books", -3.72, -2.94, F2 + 0.72, f2, 3, 0.24, 0.18, 8)
    ceramic("F2_Master_Ceramic", -3.48, -0.40, F2 + 0.72, f2, 0.075, 0.22, MATS["clay_light"])
    # teak slat panel behind the bed
    slat_wall("F2_Master_Slat", -4.86, -4.83, -2.80, -0.52, F2 + 0.35, F2 + 2.45, f2, 18)
    # sheer curtains at the balcony door
    curtain("F2_Master_Curtain_L", -4.42, -3.95, -4.02, F2 + 0.18, F2 + 2.65, f2, 6)
    curtain("F2_Master_Curtain_R", -2.10, -1.64, -4.02, F2 + 0.18, F2 + 2.65, f2, 6)
    curtain_rod("F2_Master_CurtainRod", -4.44, -1.62, -4.02, F2 + 2.69, f2)
    for i, (xx, yy) in enumerate(((-3.90, -3.55), (-2.80, -3.55), (-1.70, -3.55))):
        downlight(f"F2_Master_Down{i}", xx, yy, F2 + 2.92, f2)
    box("F2_Master_AC", -4.40, -2.95, -0.28, -0.16, F2 + 2.90, F2 + 2.93, MATS["black"], f2)

    # ------------------------------------------------------------------ kids
    table_lamp("F2_Kids_DeskLamp", -1.30, 3.38, F2 + 0.76, f2, 0.38, 0.095)
    # two small plush toys on the beds
    for i, (xx, yy, col) in enumerate(((-3.10, 1.60, "rust"), (-3.10, 2.85, "indigo"))):
        sphere(f"F2_Kids_Plush{i}", 0.13, (xx, yy, F2 + 0.72), MATS[col], f2,
               segments=10, rings=8, scale=(1, 1, 1.15))
        sphere(f"F2_Kids_PlushEar{i}A", 0.055, (xx - 0.08, yy, F2 + 0.86), MATS[col], f2,
               segments=8, rings=6, scale=(1, 1, 1.2))
        sphere(f"F2_Kids_PlushEar{i}B", 0.055, (xx + 0.08, yy, F2 + 0.86), MATS[col], f2,
               segments=8, rings=6, scale=(1, 1, 1.2))
    books("F2_Kids_Books", -2.05, 0.38, F2 + 0.85, f2, 4, 0.24, 0.16, 4)
    box("F2_Kids_Pinboard", -2.62, -1.10, 3.72, 3.75, F2 + 1.05, F2 + 1.80,
        MATS["cork"], f2, bevel=0.008)
    for i in range(4):
        box(f"F2_Kids_Note{i}", -2.45 + i * 0.31, -2.25 + i * 0.31, 3.70, 3.71,
            F2 + 1.25 + (i % 2) * 0.22, F2 + 1.45 + (i % 2) * 0.22,
            MATS[["rust", "indigo", "olive", "clay_light"][i]], f2)
    box("F2_Kids_Basket", -4.55, -4.10, 3.15, 3.55, F2 + 0.06, F2 + 0.38,
        MATS["rattan"], f2, bevel=0.03)
    curtain("F2_Kids_Curtain_L", -4.45, -4.00, 3.72, F2 + 0.18, F2 + 2.55, f2, 5)
    curtain("F2_Kids_Curtain_R", -1.62, -1.17, 3.72, F2 + 0.18, F2 + 2.55, f2, 5)
    for i, (xx, yy) in enumerate(((-4.05, 1.25), (-2.75, 1.25), (-4.05, 3.10), (-2.75, 3.10))):
        downlight(f"F2_Kids_Down{i}", xx, yy, F2 + 2.92, f2)

    # ----------------------------------------------------------------- study
    table_lamp("F2_Study_DeskLamp", 2.12, -3.30, F2 + 0.76, f2, 0.42, 0.10)
    box("F2_Study_Papers", 0.55, 1.30, -3.42, -3.14, F2 + 0.765, F2 + 0.775,
        MATS["paper"], f2, bevel=0.002, rotation=(0, 0, math.radians(-6)))
    cylinder("F2_Study_PenCup", 0.055, 0.13, (1.65, -3.30, F2 + 0.83),
             MATS["ceramic"], f2, vertices=12)
    box("F2_Study_DaybedPillow", 0.18, 0.52, -2.40, -1.30, F2 + 0.62, F2 + 0.78,
        MATS["linen_sand"], f2, bevel=0.06, rotation=(0, 0, math.radians(8)))
    throw("F2_Study_Throw", 0.18, 0.92, -1.80, -1.10, F2 + 0.60, MATS["olive"], f2)
    art("F2_Study_Art", 0.55, -0.64, F2 + 1.55, 0.82, 0.95, "N", MATS["indigo"], f2)
    for i, (xx, yy) in enumerate(((0.80, -2.70), (2.10, -2.70), (0.80, -1.30), (2.10, -1.30))):
        downlight(f"F2_Study_Down{i}", xx, yy, F2 + 2.92, f2)
    box("F2_Study_AC", 1.15, 2.60, -0.72, -0.60, F2 + 2.90, F2 + 2.93, MATS["black"], f2)

    # ------------------------------------------------------------------ bath
    cylinder("F2_Bath_TowelRail", 0.012, 1.10, (2.23, 2.05, F2 + 1.25),
             MATS["brass"], f2, axis="Y", vertices=8)
    for i in range(2):
        box(f"F2_Bath_Towel{i}", 2.20, 2.26, 1.65 + i * 0.28, 1.95 + i * 0.28,
            F2 + 0.85, F2 + 1.55, MATS["linen_sand"], f2, bevel=0.02)
    box("F2_Bath_Stool", 0.45, 0.78, 2.65, 2.98, F2 + 0.02, F2 + 0.38,
        MATS["teak"], f2, bevel=0.03)
    cylinder("F2_Bath_Bucket", 0.12, 0.25, (0.42, 2.92, F2 + 0.14),
             MATS["clay_light"], f2, vertices=14)
    ceramic("F2_Bath_Plant", 1.90, 3.12, F2 + 0.02, f2, 0.13, 0.28, MATS["terracotta"])
    for i in range(4):
        sphere(f"F2_Bath_Leaf{i}", 0.10,
               (1.90 + 0.06 * (i - 1.5), 3.12, F2 + 0.42 + (i % 2) * 0.10),
               MATS["leaf2"], f2, segments=8, rings=6, scale=(0.8, 0.8, 1.4))

    # ------------------------------------------------------------------ wing
    table_lamp("GF_Wing_Lamp0", -7.62, -2.02, GF + 0.55, gf)
    table_lamp("GF_Wing_Lamp1", -7.62, -0.10, GF + 0.55, gf)
    throw("GF_Wing_Throw", -6.80, -6.25, -1.85, -0.15, GF + 0.64, MATS["olive"], gf)
    books("GF_Wing_Books", -6.00, 0.64, GF + 0.62, gf, 3, 0.20, 0.14, 10)
    ceramic("GF_Wing_Vase", -5.55, 0.66, GF + 0.62, gf, 0.07, 0.22, MATS["clay"])
    downlight("GF_Wing_Down", -6.70, 1.10, 3.10, f2)

    # --------------------------------------------------------------- engawa
    box("GF_Engawa_Cushion0", -2.48, -2.10, 4.52, 4.88, 0.48, 0.54,
        MATS["indigo"], trim, bevel=0.03)
    box("GF_Engawa_Cushion1", -1.88, -1.50, 4.52, 4.88, 0.48, 0.54,
        MATS["rust"], trim, bevel=0.03)
    box("GF_Engawa_Tray", -2.28, -1.72, 4.58, 4.82, 0.66, 0.68,
        MATS["teak_light"], trim, bevel=0.006)
    cylinder("GF_Engawa_Teapot", 0.075, 0.11, (-2.12, 4.70, 0.73),
             MATS["ceramic_dark"], trim, vertices=14)
    for i, xx in enumerate((-2.34, -1.94)):
        cylinder(f"GF_Engawa_Cup{i}", 0.04, 0.055, (xx, 4.70, 0.71),
                 MATS["ceramic"], trim, vertices=12)
    # wind chime
    cylinder("GF_Engawa_ChimeCord", 0.004, 0.55, (-2.95, 4.42, 2.60),
             MATS["black"], trim, vertices=6)
    for i in range(4):
        cylinder(f"GF_Engawa_Chime{i}", 0.018, 0.16,
                 (-2.95 + (i - 1.5) * 0.035, 4.42, 2.31 + (i % 2) * 0.04),
                 MATS["brass"], trim, vertices=8)

    # ------------------------------------------------------------- pavilion
    box("PAV_Runner", 3.55, 5.55, 8.82, 9.28, 0.76, 0.767, MATS["olive"], site, bevel=0.004)
    cylinder("PAV_Bowl", 0.20, 0.10, (4.55, 9.05, 0.87), MATS["ceramic"], site, vertices=18)
    for i in range(3):
        sphere(f"PAV_Fruit{i}", 0.055, (4.50 + i * 0.06, 9.05, 0.96),
               MATS["clay_light"], site, segments=8, rings=6)
    for i, xx in enumerate((4.05, 5.05)):
        cylinder(f"PAV_Candle{i}", 0.03, 0.22, (xx, 9.05, 0.99), MATS["brass"], site, vertices=10)
        sphere(f"PAV_Flame{i}", 0.018, (xx, 9.05, 1.12), MATS["lamp"], site, segments=8, rings=6)

    # ---------------------------------------------------------------- pool
    for i, (xx, yy) in enumerate(((-6.15, 6.20), (-1.95, 6.20))):
        box(f"POOL_Towel{i}", xx - 0.28, xx + 0.28, yy - 0.12, yy + 0.12,
            0.38, 0.41, MATS["linen_sand"] if i == 0 else MATS["olive"], pool, bevel=0.02)
    cylinder("POOL_Tray", 0.17, 0.025, (-4.05, 6.15, 0.40), MATS["teak_light"], pool,
             vertices=16)
    for i in range(2):
        cylinder(f"POOL_Glass{i}", 0.035, 0.09, (-4.12 + i * 0.14, 6.15, 0.46),
                 MATS["glass"], pool, vertices=12)

    print("  details: interiors styled", flush=True)
