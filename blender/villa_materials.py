"""Material library for the villa. Textures are embedded on glTF export."""
from __future__ import annotations
from pathlib import Path

import bpy

from villa_geometry import material, textured_material
from villa_config import PALETTE

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "textures"
_cache = {}


def image(filename, non_color=False):
    key = (filename, non_color)
    if key in _cache:
        return _cache[key]
    img = bpy.data.images.load(str(TEX / filename), check_existing=True)
    img.name = Path(filename).stem
    if non_color:
        img.colorspace_settings.name = "Non-Color"
    else:
        img.colorspace_settings.name = "sRGB"
    _cache[key] = img
    return img


def build():
    mats = {}
    p = PALETTE
    mats["plaster"] = textured_material(
        "Lime plaster", image("plaster.png"), image("plaster_normal.png", True),
        rough=0.88, tint=(1.0, 0.985, 0.95), bump_strength=0.45)
    mats["plaster_white"] = textured_material(
        "Lime plaster chalk", image("plaster.png"), image("plaster_normal.png", True),
        rough=0.9, tint=(1.10, 1.08, 1.04), bump_strength=0.35)
    mats["stone"] = textured_material(
        "Hainan basalt", image("stone.png"), image("stone_normal.png", True),
        rough=0.82, tint=(0.92, 0.92, 0.90), bump_strength=0.9)
    mats["stone_light"] = textured_material(
        "Pale granite", image("stone.png"), image("stone_normal.png", True),
        rough=0.75, tint=(1.22, 1.18, 1.10), bump_strength=0.6)
    mats["teak"] = textured_material(
        "Old teak", image("teak.png"), image("teak_normal.png", True),
        rough=0.62, tint=(0.95, 0.92, 0.88), bump_strength=0.55)
    mats["teak_light"] = textured_material(
        "New teak", image("teak.png"), image("teak_normal.png", True),
        rough=0.58, tint=(1.15, 1.08, 0.98), bump_strength=0.45)
    mats["teak_dark"] = material("Charred teak", (0.13, 0.075, 0.045), 0.62)
    mats["roof"] = textured_material(
        "Hainan red clay tile", image("roof_tile.png"), image("roof_tile_normal.png", True),
        rough=0.72, tint=(1.0, 0.97, 0.92), bump_strength=0.7)
    mats["roof_cap"] = material("Tile ridge", (0.29, 0.10, 0.055), 0.68)
    mats["roof_under"] = material("Roof soffit", (0.28, 0.16, 0.09), 0.8)
    mats["sage"] = material("Sage louver", (0.225, 0.33, 0.26), 0.55)
    mats["sage_light"] = material("Pale sage", (0.38, 0.47, 0.38), 0.6)
    mats["black"] = material("Blackened steel", (0.035, 0.037, 0.036), 0.38, 0.7)
    mats["bronze"] = material("Aged bronze", (0.16, 0.12, 0.075), 0.45, 0.75)
    mats["glass"] = material("Glass", (0.38, 0.55, 0.56), 0.08, 0.0, alpha=0.28)
    mats["glass_dark"] = material("Smoked glass", (0.10, 0.15, 0.15), 0.12, 0.1, alpha=0.55)
    mats["tile_floor"] = textured_material(
        "Hainan limestone tile", image("stone.png"), image("stone_normal.png", True),
        rough=0.55, tint=(1.28, 1.22, 1.10), bump_strength=0.2)
    mats["concrete"] = textured_material(
        "Board-formed concrete", image("stone.png"), image("stone_normal.png", True),
        rough=0.75, tint=(0.96, 0.94, 0.88), bump_strength=0.4)
    mats["deck"] = textured_material(
        "Teak deck", image("teak.png"), image("teak_normal.png", True),
        rough=0.62, tint=(1.02, 0.95, 0.84), bump_strength=0.7)
    mats["linen"] = textured_material(
        "Oatmeal linen", image("linen.png"), image("linen_normal.png", True),
        rough=0.92, tint=(1.0, 0.97, 0.91), bump_strength=0.5)
    mats["linen_white"] = textured_material(
        "White linen", image("linen.png"), image("linen_normal.png", True),
        rough=0.95, tint=(1.18, 1.16, 1.10), bump_strength=0.35)
    mats["rattan"] = textured_material(
        "Rattan", image("rattan.png"), image("rattan_normal.png", True),
        rough=0.78, tint=(1.0, 0.98, 0.94), bump_strength=0.8)
    mats["grass"] = textured_material(
        "Tropical lawn", image("grass.png"), image("grass_normal.png", True),
        rough=0.92, tint=(1.0, 1.0, 1.0), bump_strength=0.8)
    mats["gravel"] = textured_material(
        "Coral gravel", image("gravel.png"), image("gravel_normal.png", True),
        rough=0.9, tint=(1.05, 1.0, 0.92), bump_strength=1.0)
    mats["pool_tile"] = textured_material(
        "Pool mosaic", image("pool_tile.png"), None, rough=0.3,
        tint=(1.0, 1.0, 1.0))
    mats["water"] = material("Pool water", (0.025, 0.20, 0.22), 0.08, 0.12, alpha=0.55)
    mats["bark"] = textured_material(
        "Palm bark", image("palm_bark.png"), image("palm_bark_normal.png", True),
        rough=0.9, tint=(1.0, 0.98, 0.92), bump_strength=1.0)
    mats["bark_dark"] = material("Dark bark", (0.19, 0.14, 0.09), 0.9)
    mats["soil"] = material("Leaf litter", (0.18, 0.13, 0.075), 0.95)
    mats["terracotta"] = material("Terracotta pot", (0.48, 0.22, 0.11), 0.8)
    mats["ceramic"] = material("Glazed ceramic", (0.84, 0.82, 0.74), 0.32)
    mats["ceramic_dark"] = material("Tenmoku glaze", (0.08, 0.09, 0.08), 0.28)
    mats["paper"] = material("Shoji paper", (0.90, 0.86, 0.72), 0.95)
    mats["tv"] = material("Display black", (0.015, 0.017, 0.018), 0.18)
    mats["lamp"] = material("Warm lamp", (1.0, 0.76, 0.44), 0.4,
                            emission=(1.0, 0.58, 0.26), emission_strength=4.0)
    mats["lamp_soft"] = material("Paper lamp", (0.98, 0.86, 0.63), 0.85,
                                 emission=(1.0, 0.63, 0.31), emission_strength=2.0)
    mats["led"] = material("Cool LED", (0.8, 0.9, 0.95), 0.3,
                           emission=(0.62, 0.82, 0.92), emission_strength=2.5)
    mats["car_body"] = material("Kei car cream", (0.78, 0.76, 0.64), 0.32, 0.25)
    mats["car_glass"] = material("Car glass", (0.10, 0.14, 0.15), 0.08, 0.2, alpha=0.75)
    mats["rubber"] = material("Rubber", (0.025, 0.025, 0.025), 0.85)
    mats["chrome"] = material("Chrome", (0.75, 0.76, 0.75), 0.18, 1.0)
    mats["steel"] = material("Brushed steel", (0.54, 0.55, 0.54), 0.32, 0.9)
    mats["white_paint"] = material("Off white paint", (0.88, 0.86, 0.80), 0.55)
    mats["red_flower"] = material("Frangipani", (0.95, 0.82, 0.64), 0.62)
    mats["pink_flower"] = material("Bougainvillea", (0.82, 0.18, 0.36), 0.7)
    mats["orange_flower"] = material("Heliconia", (0.84, 0.22, 0.06), 0.65)
    mats["yellow_flower"] = material("Allamanda", (0.96, 0.72, 0.12), 0.6)
    for i, c in enumerate([
        (0.030, 0.075, 0.022), (0.045, 0.115, 0.028), (0.060, 0.150, 0.036),
        (0.085, 0.190, 0.050), (0.035, 0.095, 0.032), (0.055, 0.125, 0.026),
        (0.095, 0.170, 0.042), (0.022, 0.060, 0.020),
    ]):
        mats[f"leaf{i}"] = material(f"Foliage {i+1}", c, 0.72)
    mats["palm_leaf"] = material("Palm frond", (0.040, 0.110, 0.025), 0.60)
    mats["palm_leaf_back"] = material("Palm frond reverse", (0.060, 0.150, 0.035), 0.64)
    mats["palm_stem"] = material("Palm rachis", (0.13, 0.16, 0.05), 0.7)
    mats["palm_leaf_dry"] = material("Dry palm frond", (0.42, 0.32, 0.15), 0.88)
    mats["banana_leaf"] = material("Banana leaf", (0.055, 0.170, 0.035), 0.60)
    mats["turf"] = material("Turf edge", (0.24, 0.33, 0.11), 0.95)
    return mats
