"""Build, batch-merge and export the villa as a web-ready GLB.

Run:
  /Applications/Blender.app/Contents/MacOS/Blender -b --python blender/export_glb.py

Keeping the ten named groups separate preserves the roof / upper-floor toggles
and the animated pool water, while collapsing 2,000+ modelling objects into a
small number of draw calls for three.js.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.argv = ["blender"]

import bpy
import build_villa


def join_collection(coll_name, new_name, exclude=()):
    coll = bpy.data.collections.get(coll_name)
    if not coll:
        raise RuntimeError(f"Missing collection: {coll_name}")
    objs = [
        o for o in coll.objects
        if o.type == "MESH" and not any(o.name.startswith(p) for p in exclude)
    ]
    if not objs:
        raise RuntimeError(f"Empty collection: {coll_name}")
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = new_name
    print(f"JOINED {coll_name:14s} -> {new_name:16s} {len(obj.data.polygons):6d} polys",
          flush=True)
    return obj


def main():
    scene, _mats = build_villa.build()

    joins = [
        ("HOUSE_GF", "GF_House", ()),
        ("INTERIOR_GF", "GF_Interior", ()),
        ("HOUSE_TRIM", "GF_Trim", ()),
        ("HOUSE_F2", "F2_House", ()),
        ("INTERIOR_F2", "F2_Interior", ()),
        ("ROOF", "ROOF_All", ()),
        ("SITE", "SITE_All", ()),
        ("POOL", "POOL_All", ("POOL_Water",)),
        ("LANDSCAPE", "LANDSCAPE_All", ()),
    ]
    for coll, name, exclude in joins:
        join_collection(coll, name, exclude)

    world = bpy.data.worlds.new("Hainan sky")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.55, 0.70, 0.85, 1.0)
    bg.inputs[1].default_value = 0.8

    blend_path = ROOT / "blender" / "lanai_house.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    print("SAVED", blend_path, flush=True)

    glb_path = ROOT / "public" / "models" / "lanai_house.glb"
    glb_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(glb_path),
        export_format="GLB",
        export_apply=True,
        export_yup=True,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_extras=True,
        export_materials="EXPORT",
        export_image_format="AUTO",
        export_texcoords=True,
        export_normals=True,
        export_tangents=False,
        export_skins=False,
        export_morph=False,
    )
    print("EXPORTED", glb_path, round(os.path.getsize(glb_path) / 1024 / 1024, 2), "MiB",
          flush=True)


if __name__ == "__main__":
    main()
