"""Build the Kaze House in Blender and export a glTF binary.

Run:
  /Applications/Blender.app/Contents/MacOS/Blender -b --python blender/build_villa.py
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy
from mathutils import Vector

import villa_materials
import villa_architecture
import villa_landscape
import villa_outdoor
import villa_interior
import villa_details


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.unit_settings.system = "METRIC"
    return scene


def build():
    scene = reset_scene()
    print("BUILD materials", flush=True)
    mats = villa_materials.build()
    print("BUILD shell", flush=True)
    gf, f2, roof, trim = villa_architecture.build_shell(mats)
    print("BUILD site", flush=True)
    villa_landscape.build_site(mats)
    print("BUILD plants", flush=True)
    villa_landscape.build_plants(mats)
    print("BUILD veranda", flush=True)
    villa_outdoor.build_veranda(mats)
    print("BUILD pavilion", flush=True)
    villa_outdoor.build_pavilion(mats)
    print("BUILD interior", flush=True)
    villa_interior.build_interior(mats)
    print("BUILD details", flush=True)
    villa_details.build(mats)
    print("BUILD done", flush=True)
    return scene, mats


if __name__ == "__main__":
    scene, mats = build()
    out = ROOT / "blender" / "kaze_house.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    print("SAVED", out)
