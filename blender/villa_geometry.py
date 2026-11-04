"""Small, dependency-free modelling helpers for the Blender scene."""
from __future__ import annotations
import math
import random
from typing import Iterable, Sequence

import bpy
import bmesh
from mathutils import Vector, Euler, Matrix

RNG = random.Random(20261103)


# ------------------------------------------------------------------ collections
def get_collection(name: str, parent: bpy.types.Collection | None = None):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(c)
    return c


def move_to_collection(obj, coll):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    coll.objects.link(obj)


# --------------------------------------------------------------------- materials
def set_input(node, name, value):
    if name in node.inputs:
        node.inputs[name].default_value = value


def material(name, color, rough=0.6, metallic=0.0, alpha=1.0, emission=None,
             emission_strength=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*color, alpha)
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    set_input(bsdf, "Base Color", (*color, 1.0))
    set_input(bsdf, "Roughness", rough)
    set_input(bsdf, "Metallic", metallic)
    set_input(bsdf, "Alpha", alpha)
    if emission:
        set_input(bsdf, "Emission Color", (*emission, 1.0))
        set_input(bsdf, "Emission Strength", emission_strength)
    if alpha < 1.0:
        m.blend_method = "BLEND"
        m.surface_render_method = "DITHERED"
        m.use_transparency_overlap = False
    return m


def textured_material(name, image, normal_image=None, rough=0.7, metallic=0.0,
                      tint=(1, 1, 1), alpha=1.0, emission=None,
                      emission_strength=0.0, bump_strength=1.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*tint, alpha)
    nt = m.node_tree
    nodes, links = nt.nodes, nt.links
    bsdf = nodes.get("Principled BSDF")
    set_input(bsdf, "Roughness", rough)
    set_input(bsdf, "Metallic", metallic)
    set_input(bsdf, "Base Color", (*tint, 1.0))
    set_input(bsdf, "Alpha", alpha)
    if emission:
        set_input(bsdf, "Emission Color", (*emission, 1.0))
        set_input(bsdf, "Emission Strength", emission_strength)
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = image
    tex.extension = "REPEAT"
    tex.interpolation = "Linear"
    tint_node = nodes.new("ShaderNodeMixRGB")
    tint_node.blend_type = "MULTIPLY"
    tint_node.inputs[0].default_value = 1.0
    tint_node.inputs[2].default_value = (*tint, 1.0)
    links.new(tex.outputs["Color"], tint_node.inputs[1])
    links.new(tint_node.outputs["Color"], bsdf.inputs["Base Color"])
    if normal_image:
        nm = nodes.new("ShaderNodeNormalMap")
        nm.inputs["Strength"].default_value = bump_strength
        ntex = nodes.new("ShaderNodeTexImage")
        ntex.image = normal_image
        ntex.extension = "REPEAT"
        ntex.image.colorspace_settings.name = "Non-Color"
        links.new(ntex.outputs["Color"], nm.inputs["Color"])
        links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    if alpha < 1.0:
        m.blend_method = "BLEND"
        m.surface_render_method = "DITHERED"
        m.use_transparency_overlap = False
    return m


# ------------------------------------------------------------------- primitives
def _new_mesh_obj(name, verts, faces, mat, coll, uvs=None, smooth=False,
                  material_slots=None, face_materials=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    coll.objects.link(obj)
    if isinstance(mat, (list, tuple)):
        for m in mat:
            mesh.materials.append(m)
    else:
        mesh.materials.append(mat)
    if uvs is not None:
        layer = mesh.uv_layers.new(name="UVMap")
        for i, uv in enumerate(uvs):
            if i < len(layer.data):
                layer.data[i].uv = uv
    if face_materials is not None:
        for p, mi in zip(mesh.polygons, face_materials):
            p.material_index = mi
    if smooth:
        for p in mesh.polygons:
            p.use_smooth = True
    return obj


def box(name, x0, x1, y0, y1, z0, z1, mat, coll, uv_scale=1.0,
        bevel=0.0, rotation=None, smooth=False):
    """Axis-aligned box with UVs measured in metres."""
    x0, x1 = sorted((float(x0), float(x1)))
    y0, y1 = sorted((float(y0), float(y1)))
    z0, z1 = sorted((float(z0), float(z1)))
    dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
    cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
    verts = [
        (-dx/2, -dy/2, -dz/2), ( dx/2, -dy/2, -dz/2),
        ( dx/2,  dy/2, -dz/2), (-dx/2,  dy/2, -dz/2),
        (-dx/2, -dy/2,  dz/2), ( dx/2, -dy/2,  dz/2),
        ( dx/2,  dy/2,  dz/2), (-dx/2,  dy/2,  dz/2),
    ]
    faces = [(0,1,2,3), (4,7,6,5), (0,4,5,1), (1,5,6,2), (2,6,7,3), (3,7,4,0)]
    uvs = []
    s = max(float(uv_scale), 1e-5)
    for fi, f in enumerate(faces):
        for vi in f:
            x, y, z = verts[vi]
            if fi in (0, 1):
                u, v = x / s, y / s
            elif fi in (2, 3):
                u, v = y / s, z / s
            else:
                u, v = x / s, z / s
            uvs.append((u, v))
    obj = _new_mesh_obj(name, verts, faces, mat, coll, uvs=uvs, smooth=smooth)
    obj.location = (cx, cy, cz)
    if rotation:
        obj.rotation_euler = Euler(rotation, "XYZ")
    if bevel > 0:
        mod = obj.modifiers.new("soft edges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        mod.limit_method = "ANGLE"
        mod.angle_limit = math.radians(40)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception:
            pass
        obj.select_set(False)
    return obj


def cylinder(name, radius, depth, loc, mat, coll, axis="Z", vertices=24,
             bevel=0.0, smooth=True, radius_top=None):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth,
        end_fill_type="NGON", location=loc,
    )
    obj = bpy.context.object
    obj.name = name
    move_to_collection(obj, coll)
    if radius_top is not None:
        # scale the top ring for a tapered form
        zmax = max(v.co.z for v in obj.data.vertices)
        for v in obj.data.vertices:
            if abs(v.co.z - zmax) < 1e-5:
                v.co.x *= radius_top / radius
                v.co.y *= radius_top / radius
    if axis == "X":
        obj.rotation_euler[1] = math.pi / 2
    elif axis == "Y":
        obj.rotation_euler[0] = math.pi / 2
    obj.data.materials.append(mat)
    if smooth:
        for p in obj.data.polygons:
            p.use_smooth = True
    if bevel > 0:
        mod = obj.modifiers.new("soft edges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception:
            pass
        obj.select_set(False)
    return obj


def sphere(name, radius, loc, mat, coll, segments=20, rings=12, scale=(1,1,1)):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=rings, radius=radius, location=loc
    )
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to_collection(obj, coll)
    obj.data.materials.append(mat)
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def beam(name, p0, p1, width, height, mat, coll, up=(0, 0, 1)):
    """A rectangular timber between two points."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    length = d.length
    if length < 1e-6:
        return None
    mid = (p0 + p1) / 2
    obj = box(name, -width/2, width/2, -length/2, length/2,
              -height/2, height/2, mat, coll)
    obj.location = mid
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = d.to_track_quat("Y", "Z")
    return obj


def triangle_wall(name, x, y0, y1, z0, z1, thickness, mat, coll, uv_scale=2.0):
    """A gable infill triangle extruded along X at plane x."""
    verts = [
        (x - thickness/2, y0, z0), (x - thickness/2, y1, z0),
        (x - thickness/2, (y0+y1)/2, z1),
        (x + thickness/2, y0, z0), (x + thickness/2, y1, z0),
        (x + thickness/2, (y0+y1)/2, z1),
    ]
    faces = [(0,1,2), (5,4,3), (0,3,4,1), (1,4,5,2), (2,5,3,0)]
    uvs = [(v[1]/uv_scale, v[2]/uv_scale) for v in verts]
    return _new_mesh_obj(name, verts, faces, mat, coll, uvs=uvs)


def plane(name, x0, x1, y0, y1, z, mat, coll, uv_scale=1.0, subdiv=1, smooth=False):
    nx = max(1, subdiv)
    ny = max(1, subdiv)
    verts = []
    uvs = []
    for j in range(ny + 1):
        for i in range(nx + 1):
            x = x0 + (x1-x0) * i / nx
            y = y0 + (y1-y0) * j / ny
            verts.append((x, y, z))
            uvs.append(((x-x0)/uv_scale, (y-y0)/uv_scale))
    faces = []
    for j in range(ny):
        for i in range(nx):
            a = j*(nx+1)+i
            faces.append((a, a+1, a+nx+2, a+nx+1))
    return _new_mesh_obj(name, verts, faces, mat, coll, uvs=uvs, smooth=smooth)


def text_mesh(name, body, loc, size, mat, coll, rot=(math.pi/2, 0, 0), extrude=0.006):
    curve = bpy.data.curves.new(name + "Curve", type="FONT")
    curve.body = body
    curve.size = size
    curve.extrude = extrude
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    obj = bpy.data.objects.new(name, curve)
    coll.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = Euler(rot, "XYZ")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target="MESH")
    obj.select_set(False)
    obj.data.materials.append(mat)
    return obj


def lerp(a, b, t):
    return a + (b - a) * t


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)
