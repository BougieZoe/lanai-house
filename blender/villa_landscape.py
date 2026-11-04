"""Tropical site, planting, pool, carport and the small domestic details."""
from __future__ import annotations
import math
import random

import bpy
from mathutils import Vector, Euler

from villa_config import *
from villa_geometry import (
    box, cylinder, sphere, beam, plane, text_mesh,
    get_collection, _new_mesh_obj, RNG,
)

C = math.cos
S = math.sin


# ------------------------------------------------------------------ utilities
def cone_between(name, p0, p1, r0, r1, mat, coll, vertices=8):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    length = d.length
    if length < 1e-6:
        return None
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r0, radius2=r1,
                                    depth=length, location=(p0+p1)/2)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = d.to_track_quat("Z", "Y")
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    coll.objects.link(obj)
    obj.data.materials.append(mat)
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def add_quad(verts, faces, uvs, a, b, c, d):
    base = len(verts)
    verts.extend([a, b, c, d])
    faces.append((base, base+1, base+2, base+3))
    uvs.extend([(0,0), (1,0), (1,1), (0,1)])


def palm_tree(mats, coll, name, base, height=9.0, lean=(0.8, 0.2),
              fronds=14, scale=1.0, seed=1):
    """A coconut palm with a tapered, gently leaning trunk and feather fronds."""
    rng = random.Random(seed)
    x0, y0, z0 = base
    segs, sides = 14, 12
    verts, faces, uvs = [], [], []
    rings = []
    for j in range(segs+1):
        t = j/segs
        cx = x0 + lean[0]*(t**1.7)
        cy = y0 + lean[1]*(t**1.7)
        cz = z0 + height*t
        r = (0.32 - 0.18*t) * scale
        ring = []
        for i in range(sides):
            a = 2*math.pi*i/sides
            ring.append(len(verts))
            verts.append((cx + r*math.cos(a), cy + r*math.sin(a), cz))
            uvs.append((i/sides*2.0, t*height/1.6))
        rings.append(ring)
    for j in range(segs):
        for i in range(sides):
            a = rings[j][i]
            b = rings[j][(i+1) % sides]
            c = rings[j+1][(i+1) % sides]
            d = rings[j+1][i]
            faces.append((a, b, c, d))
    trunk = _new_mesh_obj(name+"_Trunk", verts, faces, mats["bark"], coll,
                          uvs=uvs, smooth=True)
    top = Vector((x0 + lean[0], y0 + lean[1], z0 + height))
    cylinder(name+"_Crownshaft", 0.14*scale, 1.0*scale,
             (top.x, top.y, top.z-0.45*scale), mats["leaf1"], coll, vertices=12)

    fv, ff, fu, fmat = [], [], [], []
    dry_v, dry_f, dry_uv = [], [], []

    def add_face(vlist, flist, uvlist, matlist, a, b, c, d, mi=0):
        i0 = len(vlist)
        vlist.extend([a, b, c, d])
        flist.append((i0, i0+1, i0+2, i0+3))
        uvlist.extend([(0,0), (1,0), (1,1), (0,1)])
        if matlist is not None:
            matlist.append(mi)

    for k in range(fronds):
        ang = 2*math.pi*k/fronds + rng.uniform(-0.18, 0.18)
        dirx, diry = math.cos(ang), math.sin(ang)
        sidex, sidey = -diry, dirx
        L = (3.1 + rng.uniform(-0.35, 0.55)) * scale
        droop = rng.uniform(0.55, 1.15)
        dry = k < 3
        vv = dry_v if dry else fv
        ffl = dry_f if dry else ff
        uu = dry_uv if dry else fu
        mm = None if dry else fmat
        nleaf = 19
        for j in range(nleaf):
            s0 = 0.02 + 0.96*j/nleaf
            s1 = 0.02 + 0.96*(j+1)/nleaf
            p0x = top.x + dirx*L*s0
            p0y = top.y + diry*L*s0
            p0z = top.z + 0.70*math.sin(math.pi*s0*0.85) - droop*s0*s0
            p1x = top.x + dirx*L*s1
            p1y = top.y + diry*L*s1
            p1z = top.z + 0.70*math.sin(math.pi*s1*0.85) - droop*s1*s1
            w = 0.032*scale
            add_face(vv, ffl, uu, mm,
                     (p0x-sidex*w, p0y-sidey*w, p0z),
                     (p0x+sidex*w, p0y+sidey*w, p0z),
                     (p1x+sidex*w, p1y+sidey*w, p1z),
                     (p1x-sidex*w, p1y-sidey*w, p1z), 1)
            s = (s0+s1)/2
            px, py, pz = (p0x+p1x)/2, (p0y+p1y)/2, (p0z+p1z)/2
            ll = L*0.35*(0.28 + 1.05*math.sin(math.pi*s)**0.65)
            ll *= rng.uniform(0.90, 1.08)
            for sgn in (-1, 1):
                sx, sy = sidex*sgn, sidey*sgn
                b0 = (px - dirx*0.035, py - diry*0.035, pz)
                b1 = (px + dirx*0.035, py + diry*0.035, pz)
                mx = px + sx*ll*0.52 + dirx*ll*0.10
                my = py + sy*ll*0.52 + diry*ll*0.10
                mz = pz + 0.05*ll*(1-s) - 0.02*ll
                m0 = (mx - dirx*0.070, my - diry*0.070, mz)
                m1 = (mx + dirx*0.070, my + diry*0.070, mz)
                tipx = px + sx*ll + dirx*ll*0.15
                tipy = py + sy*ll + diry*ll*0.15
                tipz = pz - 0.16*ll*(0.3+s)
                add_face(vv, ffl, uu, mm, b0, b1, m1, m0, 0)
                add_face(vv, ffl, uu, mm, m0, m1,
                         (tipx-dirx*0.015, tipy-diry*0.015, tipz),
                         (tipx+dirx*0.015, tipy+diry*0.015, tipz), 0)
    _new_mesh_obj(name+"_Fronds", fv, ff, [mats["palm_leaf"], mats["palm_stem"]],
                  coll, uvs=fu, face_materials=fmat)
    _new_mesh_obj(name+"_DryFronds", dry_v, dry_f, mats["palm_leaf_dry"], coll,
                  uvs=dry_uv)
    for i in range(4):
        a = rng.uniform(0, 2*math.pi)
        rr = rng.uniform(0.16, 0.38)
        sphere(f"{name}_Coconut{i}", 0.12*scale,
               (top.x + rr*math.cos(a), top.y + rr*math.sin(a), top.z-0.28),
               mats["bark_dark"], coll, segments=12, rings=8,
               scale=(1, 1, 1.18))
    return trunk


def frangipani(mats, coll, name, base, height=4.4, seed=4):
    rng = random.Random(seed)
    x, y, z = base
    trunk_top = (x+0.18, y+0.12, z+height*0.38)
    cone_between(name+"_Trunk", (x,y,z), trunk_top, 0.20, 0.12, mats["bark"], coll, 10)
    tips = []
    for i in range(4):
        a = 2*math.pi*i/4 + rng.uniform(-0.4, 0.4)
        p1 = (trunk_top[0]+0.82*math.cos(a), trunk_top[1]+0.82*math.sin(a),
              z+height*(0.66+rng.uniform(-0.08,0.08)))
        cone_between(f"{name}_Branch{i}", trunk_top, p1, 0.11, 0.06, mats["bark"], coll, 8)
        for j in range(2):
            a2 = a + rng.uniform(-0.7, 0.7)
            p2 = (p1[0]+0.72*math.cos(a2), p1[1]+0.72*math.sin(a2),
                  z+height*(0.84+rng.uniform(-0.06,0.08)))
            cone_between(f"{name}_Twig{i}_{j}", p1, p2, 0.06, 0.025, mats["bark"], coll, 7)
            tips.append(p2)
    lv, lf, lu = [], [], []
    for tip in tips:
        for i in range(7):
            a = 2*math.pi*i/7 + rng.uniform(-0.2, 0.2)
            length = rng.uniform(0.30, 0.42)
            w = length*0.34
            dx, dy = math.cos(a), math.sin(a)
            sx, sy = -dy, dx
            p0 = Vector(tip) + Vector((0,0,-0.08))
            p1 = Vector(tip) + Vector((dx*length*0.45+sx*w, dy*length*0.45+sy*w, 0.01))
            p2 = Vector(tip) + Vector((dx*length, dy*length, -0.02))
            p3 = Vector(tip) + Vector((dx*length*0.45-sx*w, dy*length*0.45-sy*w, 0.01))
            add_quad(lv, lf, lu, tuple(p0), tuple(p1), tuple(p2), tuple(p3))
    _new_mesh_obj(name+"_Leaves", lv, lf, mats["leaf4"], coll, uvs=lu)
    fv, ff, fu = [], [], []
    for tip in tips:
        for i in range(3):
            cen = Vector(tip) + Vector((rng.uniform(-0.18,0.18), rng.uniform(-0.18,0.18),
                                        rng.uniform(-0.05,0.12)))
            for petal in range(5):
                a = 2*math.pi*petal/5
                p0 = cen
                p1 = cen + Vector((0.055*math.cos(a-0.35), 0.055*math.sin(a-0.35), 0.01))
                p2 = cen + Vector((0.095*math.cos(a), 0.095*math.sin(a), 0.02))
                p3 = cen + Vector((0.055*math.cos(a+0.35), 0.055*math.sin(a+0.35), 0.01))
                add_quad(fv, ff, fu, tuple(p0), tuple(p1), tuple(p2), tuple(p3))
    _new_mesh_obj(name+"_Flowers", fv, ff, mats["red_flower"], coll, uvs=fu)


def banana(mats, coll, name, base, seed=9):
    rng = random.Random(seed)
    x, y, z = base
    for i in range(6):
        a = 2*math.pi*i/6 + rng.uniform(-0.2, 0.2)
        h = rng.uniform(1.2, 2.0)
        p1 = (x+0.35*math.cos(a), y+0.35*math.sin(a), z+h)
        cone_between(f"{name}_Stem{i}", (x,y,z), p1, 0.055, 0.035, mats["leaf2"], coll, 7)
        lv, lf, lu = [], [], []
        dx, dy = math.cos(a), math.sin(a)
        sx, sy = -dy, dx
        L = rng.uniform(1.25, 1.75)
        W = L*0.34
        p0 = Vector(p1)
        for j in range(5):
            t = j/5
            c = p0 + Vector((dx*L*t, dy*L*t, 0.42*math.sin(math.pi*t) - 0.30*t*t))
            w = W*math.sin(math.pi*min(1, t*1.1))**0.6
            t2 = (j+1)/5
            c2 = p0 + Vector((dx*L*t2, dy*L*t2, 0.42*math.sin(math.pi*t2) - 0.30*t2*t2))
            w2 = W*math.sin(math.pi*min(1, t2*1.1))**0.6
            add_quad(lv, lf, lu,
                     tuple(c - Vector((sx*w, sy*w, 0))),
                     tuple(c + Vector((sx*w, sy*w, 0))),
                     tuple(c2 + Vector((sx*w2, sy*w2, 0))),
                     tuple(c2 - Vector((sx*w2, sy*w2, 0))))
        _new_mesh_obj(f"{name}_Leaf{i}", lv, lf, mats["banana_leaf"], coll, uvs=lu)
        beam(f"{name}_Rib{i}", tuple(p0), tuple(p0 + Vector((dx*L, dy*L, -0.18))),
             0.02, 0.02, mats["leaf1"], coll)


def shrub(mats, coll, name, x, y, r=0.65, h=0.85, mat=None, seed=0, blobs=4):
    rng = random.Random(seed)
    mat = mat or mats[f"leaf{rng.randint(0,6)}"]
    for i in range(blobs):
        a = rng.uniform(0, 2*math.pi)
        rr = rng.uniform(0, r*0.55)
        sphere(f"{name}_Blob{i}", r*rng.uniform(0.55,0.95),
               (x+math.cos(a)*rr, y+math.sin(a)*rr, h*0.45 + rng.uniform(-0.08,0.12)),
               mat, coll, segments=12, rings=8,
               scale=(1.0, 1.0, rng.uniform(0.6, 0.95)))


def heliconia(mats, coll, name, base, seed=0):
    rng = random.Random(seed)
    x, y, z = base
    for i in range(5):
        a = rng.uniform(0, 2*math.pi)
        h = rng.uniform(0.8, 1.4)
        p1 = (x+0.22*math.cos(a), y+0.22*math.sin(a), z+h)
        cone_between(f"{name}_Stem{i}", (x,y,z), p1, 0.022, 0.014, mats["leaf2"], coll, 6)
        for j in range(2):
            ang = a + (j-0.5)*0.8
            dx, dy = math.cos(ang), math.sin(ang)
            sx, sy = -dy, dx
            L, W = 0.62, 0.18
            lv, lf, lu = [], [], []
            p0 = Vector(p1)
            for k in range(3):
                t0, t1 = k/3, (k+1)/3
                c0 = p0 + Vector((dx*L*t0, dy*L*t0, 0.22*math.sin(math.pi*t0)-0.18*t0))
                c1 = p0 + Vector((dx*L*t1, dy*L*t1, 0.22*math.sin(math.pi*t1)-0.18*t1))
                w0 = W*math.sin(math.pi*min(1,t0*1.15))
                w1 = W*math.sin(math.pi*min(1,t1*1.15))
                add_quad(lv, lf, lu,
                         tuple(c0-Vector((sx*w0, sy*w0,0))), tuple(c0+Vector((sx*w0, sy*w0,0))),
                         tuple(c1+Vector((sx*w1, sy*w1,0))), tuple(c1-Vector((sx*w1, sy*w1,0))))
            _new_mesh_obj(f"{name}_Leaf{i}_{j}", lv, lf, mats["banana_leaf"], coll, uvs=lu)
        for j in range(3):
            sphere(f"{name}_Bract{i}_{j}", 0.055, (p1[0], p1[1], p1[2]+0.08+j*0.10),
                   mats["orange_flower"], coll, segments=8, rings=6, scale=(0.45,1.0,0.35))


def fern(mats, coll, name, base, seed=0):
    rng = random.Random(seed)
    x, y, z = base
    lv, lf, lu = [], [], []
    for i in range(9):
        a = 2*math.pi*i/9 + rng.uniform(-0.2,0.2)
        dx, dy = math.cos(a), math.sin(a)
        sx, sy = -dy, dx
        L = rng.uniform(0.45, 0.75)
        for j in range(5):
            t = 0.15 + 0.8*j/5
            c = Vector((x+dx*L*t, y+dy*L*t, z+0.18*math.sin(math.pi*t)))
            w = 0.11*(1-t*0.55)
            add_quad(lv, lf, lu,
                     tuple(c-Vector((sx*w, sy*w,0))), tuple(c+Vector((sx*w, sy*w,0))),
                     tuple(c+Vector((sx*w*0.4+dx*0.05, sy*w*0.4+dy*0.05, 0.02))),
                     tuple(c+Vector((dx*0.02, dy*0.02, 0.01))))
    _new_mesh_obj(name+"_Fronds", lv, lf, mats["leaf0"], coll, uvs=lu)


# --------------------------------------------------------------------- site
def build_site(mats):
    print("  site: start", flush=True)
    site = get_collection("SITE")
    px0, px1, py0, py1 = POOL
    pieces = [
        (SITE_X[0], SITE_X[1], SITE_Y[0], py0),
        (SITE_X[0], px0, py0, py1),
        (px1, SITE_X[1], py0, py1),
        (SITE_X[0], SITE_X[1], py1, SITE_Y[1]),
    ]
    for i, (x0, x1, y0, y1) in enumerate(pieces):
        print(f"  site: lawn {i}", flush=True)
        plane(f"SITE_Lawn_{i}", x0, x1, y0, y1, 0.02, mats["grass"], site,
              uv_scale=3.0, subdiv=12)
    box("SITE_Road", -15, 15, -19.4, -15.45, -0.16, 0.01, mats["concrete"], site,
        uv_scale=4)
    box("SITE_Curb", -13.2, 13.2, -15.45, -15.22, -0.02, 0.11, mats["stone_light"], site)
    plane("SITE_Sidewalk", -13.2, 13.2, -15.22, -14.65, 0.115, mats["stone_light"], site,
          uv_scale=1.5)
    for i in range(10):
        box(f"SITE_RoadDash_{i}", -12+i*2.6, -11.4+i*2.6, -17.6, -17.45,
            0.012, 0.018, mats["white_paint"], site)
    plane("SITE_Drive", 6.85, 11.65, -15.0, 1.95, 0.055, mats["gravel"], site,
          uv_scale=1.4, subdiv=8)
    box("SITE_CarportPad", 6.95, 11.55, -4.2, 1.9, 0.03, 0.12,
        mats["concrete"], site)
    rng = random.Random(18)
    for i in range(11):
        yy = -14.2 + i*0.80
        xx = 1.32 + math.sin(i*0.85)*0.16
        box(f"SITE_Step_{i:02d}", xx-0.43, xx+0.43, yy-0.27, yy+0.27,
            0.02, 0.085, mats["stone_light"], site, bevel=0.012,
            rotation=(0, 0, math.radians(rng.uniform(-8, 8))))
    box("SITE_EntryLanding", 0.20, 3.05, -5.90, -4.15, 0.02, 0.22,
        mats["stone_light"], site, bevel=0.015)
    beds = [
        (-12.6, -10.3, -13.8, -8.4), (-9.4, -4.6, -14.5, -11.9),
        (4.2, 7.0, -13.5, -8.2), (11.2, 12.7, -8.0, 4.5),
        (-12.7, -9.9, 4.0, 14.6), (3.2, 12.7, 11.9, 15.4),
        (-2.0, 2.9, 4.9, 6.7),
    ]
    for i, (x0, x1, y0, y1) in enumerate(beds):
        box(f"SITE_Bed_{i}", x0, x1, y0, y1, 0.025, 0.12,
            mats["soil"], site, bevel=0.03)
    for i in range(4):
        box(f"SITE_HerbBox_{i}", -1.7+i*0.62, -1.25+i*0.62, 5.02, 5.55,
            0.10, 0.34, mats["teak"], site)
    print("  site: pool", flush=True)
    build_pool(mats)
    print("  site: boundary", flush=True)
    build_boundary(mats)
    print("  site: carport", flush=True)
    build_carport(mats)
    print("  site: done", flush=True)
    return site


def build_pool(mats):
    pool = get_collection("POOL")
    px0, px1, py0, py1 = POOL
    dx0, dx1, dy0, dy1 = POOL_DECK
    deck = [
        (dx0, px0, dy0, dy1),
        (px1, dx1, dy0, dy1),
        (px0, px1, dy0, py0),
        (px0, px1, py1, dy1),
    ]
    for i, (x0, x1, y0, y1) in enumerate(deck):
        box(f"POOL_Deck_{i}", x0, x1, y0, y1, -0.10, 0.10,
            mats["stone_light"], pool, uv_scale=1.4)
    box("POOL_TeakDeck", px1+0.02, dx1-0.05, 6.30, 12.0, 0.10, 0.145,
        mats["deck"], pool, uv_scale=0.7)
    copings = [
        (px0-0.30, px0, py0-0.30, py1+0.30),
        (px1, px1+0.30, py0-0.30, py1+0.30),
        (px0-0.30, px1+0.30, py0-0.30, py0),
        (px0-0.30, px1+0.30, py1, py1+0.30),
    ]
    for i, (x0, x1, y0, y1) in enumerate(copings):
        box(f"POOL_Coping_{i}", x0, x1, y0, y1, 0.10, 0.16,
            mats["stone"], pool, bevel=0.012)
    box("POOL_BasinFloor", px0, px1, py0, py1, -POOL_DEPTH, -POOL_DEPTH+0.10,
        mats["pool_tile"], pool, uv_scale=0.7)
    for side, (x0,x1,y0,y1) in enumerate([
        (px0, px0+0.12, py0, py1), (px1-0.12, px1, py0, py1),
        (px0, px1, py0, py0+0.12), (px0, px1, py1-0.12, py1),
    ]):
        box(f"POOL_BasinWall_{side}", x0, x1, y0, y1, -POOL_DEPTH, 0.10,
            mats["pool_tile"], pool, uv_scale=0.7)
    plane("POOL_Water", px0+0.10, px1-0.10, py0+0.10, py1-0.10,
          -0.10, mats["water"], pool)
    for i in range(3):
        box(f"POOL_Step_{i}", px0+0.3, px0+1.15, py0+0.3+i*0.32,
            py0+1.85+i*0.32, -POOL_DEPTH+0.10, -0.55+i*0.20,
            mats["pool_tile"], pool, bevel=0.02)
    for xx in (px1-0.55, px1-0.30):
        cylinder(f"POOL_Ladder_{xx}", 0.025, 1.15, (xx, py0+1.15, 0.22),
                 mats["chrome"], pool, vertices=10)
    for zz in (0.12, 0.48, 0.84):
        cylinder(f"POOL_LadderStep_{zz}", 0.022, 0.40,
                 (px1-0.425, py0+1.15, zz), mats["chrome"], pool, axis="X", vertices=10)
    sx, sy = -8.7, 6.25
    box("POOL_ShowerBase", sx-0.55, sx+0.55, sy-0.55, sy+0.55, 0.10, 0.24,
        mats["stone"], pool, bevel=0.02)
    for i in range(7):
        cylinder(f"POOL_ShowerScreenPost_{i}", 0.035, 2.05,
                 (sx-0.85+i*0.20, sy-0.55, 0.10+1.025), mats["bark"], pool,
                 vertices=8)
    for j in range(5):
        cylinder(f"POOL_ShowerScreenRail_{j}", 0.018, 1.35,
                 (sx-0.25, sy-0.56, 0.35+j*0.36), mats["rattan"], pool,
                 axis="X", vertices=8)
    cylinder("POOL_ShowerPipe", 0.025, 2.2, (sx, sy-0.30, 1.2), mats["bronze"],
             pool, vertices=10)
    cylinder("POOL_ShowerHead", 0.13, 0.025, (sx, sy-0.06, 2.25), mats["bronze"],
             pool, axis="Y", vertices=18)
    for i, yy in enumerate((7.6, 9.5)):
        lx = 0.55
        box(f"POOL_LoungerBase_{i}", lx-0.45, lx+0.75, yy-0.32, yy+0.32,
            0.22, 0.36, mats["teak"], pool, bevel=0.03)
        box(f"POOL_LoungerCushion_{i}", lx-0.40, lx+0.55, yy-0.30, yy+0.30,
            0.36, 0.48, mats["linen_white"], pool, bevel=0.045)
        box(f"POOL_LoungerBack_{i}", lx-0.45, lx-0.05, yy-0.30, yy+0.30,
            0.38, 0.95, mats["linen_white"], pool, bevel=0.05,
            rotation=(0, math.radians(-38), 0))
    cylinder("POOL_SideTable", 0.25, 0.45, (1.55, 8.55, 0.32), mats["teak"],
             pool, vertices=18)
    cylinder("POOL_Cup1", 0.045, 0.10, (1.50, 8.50, 0.60), mats["ceramic"], pool,
             vertices=12)
    cylinder("POOL_UmbrellaPole", 0.035, 2.5, (1.45, 7.2, 1.3), mats["bronze"],
             pool, vertices=12)
    cylinder("POOL_UmbrellaArm", 0.03, 1.7, (0.75, 7.2, 2.55), mats["bronze"],
             pool, axis="X", vertices=10)
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=1.55, radius2=0.03,
                                    depth=0.22, location=(0.05, 7.2, 2.55))
    um = bpy.context.object; um.name="POOL_UmbrellaCanopy"
    for c in list(um.users_collection): c.objects.unlink(um)
    pool.objects.link(um)
    um.data.materials.append(mats["linen"])
    for p in um.data.polygons: p.use_smooth = True


def build_boundary(mats):
    site = get_collection("SITE")
    segs = [(-13.0, 0.25), (2.05, 7.30), (11.45, 13.0)]
    for si, (a, b) in enumerate(segs):
        box(f"SITE_FrontWall_{si}", a, b, WALL_FRONT_Y-0.14, WALL_FRONT_Y+0.14,
            0.02, 0.58, mats["plaster"], site, uv_scale=2)
        box(f"SITE_FrontCoping_{si}", a, b, WALL_FRONT_Y-0.18, WALL_FRONT_Y+0.18,
            0.58, 0.65, mats["stone_light"], site, bevel=0.01)
        n = int((b-a)/0.16)
        for i in range(n):
            xx = a + 0.10 + i*0.16
            box(f"SITE_FrontSlat_{si}_{i:03d}", xx, xx+0.055,
                WALL_FRONT_Y-0.03, WALL_FRONT_Y+0.03, 0.65, 1.38,
                mats["teak"], site)
        box(f"SITE_FrontRail_{si}", a, b, WALL_FRONT_Y-0.04, WALL_FRONT_Y+0.04,
            1.34, 1.42, mats["teak_dark"], site)
    for xx in (0.25, 2.05, 7.30, 11.45):
        box(f"SITE_GatePier_{xx}", xx-0.13, xx+0.13, WALL_FRONT_Y-0.20,
            WALL_FRONT_Y+0.20, 0.02, 1.62, mats["plaster"], site, bevel=0.008)
        box(f"SITE_GatePierCap_{xx}", xx-0.18, xx+0.18, WALL_FRONT_Y-0.24,
            WALL_FRONT_Y+0.24, 1.62, 1.70, mats["stone"], site, bevel=0.01)
    for i in range(10):
        xx = 0.42 + i*0.15
        box(f"SITE_PedGateSlat_{i}", xx, xx+0.05, WALL_FRONT_Y+0.05,
            WALL_FRONT_Y+0.10, 0.08, 1.50, mats["teak"], site)
    box("SITE_PedGateRail", 0.38, 1.90, WALL_FRONT_Y+0.04, WALL_FRONT_Y+0.12,
        1.44, 1.53, mats["teak_dark"], site)
    for i in range(22):
        xx = 7.55 + i*0.165
        box(f"SITE_CarGateSlat_{i}", xx, xx+0.06, WALL_FRONT_Y+0.01,
            WALL_FRONT_Y+0.06, 0.08, 1.50, mats["teak"], site)
    box("SITE_CarGateRailT", 7.50, 11.25, WALL_FRONT_Y-0.01, WALL_FRONT_Y+0.08,
        1.44, 1.54, mats["teak_dark"], site)
    box("SITE_CarGateRailB", 7.50, 11.25, WALL_FRONT_Y-0.01, WALL_FRONT_Y+0.08,
        0.10, 0.18, mats["teak_dark"], site)
    for xx in (SITE_X[0], SITE_X[1]):
        box(f"SITE_SideWall_{xx}", xx-0.14, xx+0.14, -14.6, 15.6, 0.02, 1.78,
            mats["plaster"], site, uv_scale=2)
        box(f"SITE_SideCoping_{xx}", xx-0.19, xx+0.19, -14.6, 15.6, 1.78, 1.88,
            mats["stone"], site, bevel=0.01)
        for i in range(5):
            zz = 0.30 + i*0.30
            box(f"SITE_SideShadow_{xx}_{i}", xx-0.17, xx+0.17, -14.6, 15.6,
                zz, zz+0.018, mats["stone"], site)
    box("SITE_RearWall", -13.0, 13.0, 15.45, 15.75, 0.02, 1.55,
        mats["plaster"], site, uv_scale=2)
    box("SITE_RearCoping", -13.1, 13.1, 15.40, 15.80, 1.55, 1.66,
        mats["stone"], site, bevel=0.01)
    cylinder("SITE_MailBoxPost", 0.045, 1.15, (0.55, -14.45, 0.58),
             mats["black"], site, vertices=10)
    box("SITE_MailBox", 0.35, 0.75, -14.58, -14.20, 1.05, 1.29,
        mats["black"], site, bevel=0.02)
    text_mesh("SITE_HouseNumber", "01", (2.35, WALL_FRONT_Y-0.17, 0.92), 0.22,
              mats["teak_dark"], site, rot=(math.pi/2, 0, 0), extrude=0.004)
    dx, dy = -3.65, -8.95
    box("SITE_DogBase", dx-0.85, dx+0.85, dy-0.75, dy+0.75, 0.02, 0.15,
        mats["stone"], site, bevel=0.02)
    box("SITE_DogHouse", dx-0.68, dx+0.68, dy-0.55, dy+0.55, 0.15, 1.05,
        mats["plaster_white"], site, bevel=0.02)
    box("SITE_DogDoor", dx-0.25, dx+0.25, dy-0.58, dy-0.53, 0.18, 0.78,
        mats["teak_dark"], site)
    box("SITE_DogRoofL", dx-0.80, dx+0.03, dy-0.72, dy+0.72, 1.02, 1.12,
        mats["roof"], site, rotation=(0, math.radians(24), 0), bevel=0.01)
    box("SITE_DogRoofR", dx-0.03, dx+0.80, dy-0.72, dy+0.72, 1.02, 1.12,
        mats["roof"], site, rotation=(0, math.radians(-24), 0), bevel=0.01)
    text_mesh("SITE_DogSign", "SHIRO", (dx, dy-0.58, 1.32), 0.11,
              mats["teak_dark"], site, rot=(math.pi/2, 0, 0), extrude=0.003)
    cylinder("SITE_DogBowl", 0.10, 0.06, (dx+0.95, dy+0.15, 0.18),
             mats["steel"], site, vertices=16)
    cylinder("SITE_LanternPost", 0.035, 1.2, (0.10, -13.6, 0.60),
             mats["black"], site, vertices=10)
    box("SITE_LanternHead", -0.10, 0.30, -13.80, -13.40, 1.18, 1.38,
        mats["lamp"], site, bevel=0.01)


def build_carport(mats):
    site = get_collection("SITE")
    x0, x1, y0, y1 = 6.95, 11.55, -4.15, 1.85
    print("    cp: posts", flush=True)
    for pi, (xx, yy) in enumerate(((x0+0.10, y0+0.10), (x0+0.10, y1-0.10),
                   (x1-0.10, y0+0.10), (x1-0.10, y1-0.10))):
        print(f"      post {pi} at {xx},{yy}", flush=True)
        box(f"SITE_CarportPost_{pi}", xx-0.075, xx+0.075, yy-0.075, yy+0.075,
            0.10, 2.78, mats["teak"], site)
    print("    cp: beams", flush=True)
    for bi, yy in enumerate((y0+0.10, y1-0.10)):
        box(f"SITE_CarportBeam_{bi}", x0, x1, yy-0.09, yy+0.09, 2.70, 2.88,
            mats["teak_dark"], site)
    for bi, xx in enumerate((x0, x1)):
        box(f"SITE_CarportBeamX_{bi}", xx-0.09, xx+0.09, y0, y1, 2.78, 2.94,
            mats["teak_dark"], site)
    print("    cp: slats", flush=True)
    n = 18
    for i in range(n):
        yy = y0 + 0.08 + i*(y1-y0-0.16)/(n-1)
        box(f"SITE_CarportSlat_{i:02d}", x0-0.12, x1+0.12, yy-0.045, yy+0.045,
            2.94, 3.04, mats["teak"], site)
    print("    cp: store", flush=True)
    box("SITE_CarportStore", x1-0.25, x1+0.05, -1.2, 1.4, 0.10, 2.70,
        mats["plaster_white"], site, uv_scale=2)
    print("    cp: ev", flush=True)
    box("SITE_EVCharger", x1-0.33, x1-0.25, -0.25, 0.10, 1.10, 1.50,
        mats["black"], site, bevel=0.01)
    print("    cp: light", flush=True)
    cylinder("SITE_EVLight", 0.025, 0.015, (x1-0.34, -0.08, 1.42),
             mats["led"], site, axis="X", vertices=10)
    print("    carport: car", flush=True)
    car(mats, site, 9.1, -1.35, 0.10)
    print("    carport: bike", flush=True)
    bicycle(mats, site, 7.55, 1.30)
    print("    carport: done", flush=True)


def car(mats, coll, x, y, z):
    box("CAR_Body", x-0.74, x+0.74, y-1.55, y+1.55, z+0.30, z+0.82,
        mats["car_body"], coll, bevel=0.16)
    box("CAR_Cabin", x-0.66, x+0.66, y-1.02, y+0.78, z+0.78, z+1.38,
        mats["car_body"], coll, bevel=0.14)
    box("CAR_Windshield", x-0.58, x+0.58, y-1.08, y-0.92, z+0.88, z+1.30,
        mats["car_glass"], coll, rotation=(math.radians(18),0,0))
    box("CAR_RearGlass", x-0.58, x+0.58, y+0.70, y+0.82, z+0.88, z+1.30,
        mats["car_glass"], coll)
    for sx in (-1, 1):
        box(f"CAR_SideGlass_{sx}", x+sx*0.67-0.01, x+sx*0.67+0.01, y-0.82,
            y+0.60, z+0.92, z+1.28, mats["car_glass"], coll)
    box("CAR_BumperF", x-0.70, x+0.70, y-1.62, y-1.50, z+0.28, z+0.48,
        mats["rubber"], coll, bevel=0.05)
    box("CAR_BumperR", x-0.70, x+0.70, y+1.50, y+1.62, z+0.28, z+0.48,
        mats["rubber"], coll, bevel=0.05)
    for sx in (-1, 1):
        cylinder(f"CAR_Headlight_{sx}", 0.10, 0.03,
                 (x+sx*0.50, y-1.58, z+0.62), mats["lamp_soft"], coll,
                 axis="Y", vertices=14)
        cylinder(f"CAR_Taillight_{sx}", 0.085, 0.03,
                 (x+sx*0.50, y+1.57, z+0.60), mats["roof_cap"], coll,
                 axis="Y", vertices=14)
        for sy in (-1, 1):
            cylinder(f"CAR_Wheel_{sx}_{sy}", 0.28, 0.18,
                     (x+sx*0.70, y+sy*0.95, z+0.33), mats["rubber"], coll,
                     axis="X", vertices=18)
            cylinder(f"CAR_Hub_{sx}_{sy}", 0.12, 0.19,
                     (x+sx*0.70, y+sy*0.95, z+0.33), mats["chrome"], coll,
                     axis="X", vertices=14)
    box("CAR_RoofRack", x-0.42, x+0.42, y-0.35, y+0.35, z+1.38, z+1.43,
        mats["black"], coll)


def bicycle(mats, coll, x, y):
    for sy in (-0.55, 0.55):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.32, minor_radius=0.025,
                                         major_segments=20, minor_segments=8,
                                         location=(x, y+sy, 0.44))
        o = bpy.context.object; o.name=f"BIKE_Wheel_{sy}"
        for c in list(o.users_collection): c.objects.unlink(o)
        coll.objects.link(o)
        o.rotation_euler[1] = math.pi/2
        o.data.materials.append(mats["rubber"])
    beam("BIKE_Frame1", (x, y-0.55, 0.44), (x, y+0.10, 0.78), 0.035, 0.035,
         mats["roof_cap"], coll)
    beam("BIKE_Frame2", (x, y-0.55, 0.44), (x, y-0.05, 0.42), 0.035, 0.035,
         mats["roof_cap"], coll)
    beam("BIKE_Frame3", (x, y+0.10, 0.78), (x, y+0.55, 0.44), 0.035, 0.035,
         mats["roof_cap"], coll)
    beam("BIKE_SeatPost", (x, y-0.02, 0.42), (x, y-0.02, 0.86), 0.03, 0.03,
         mats["steel"], coll)
    box("BIKE_Seat", x-0.08, x+0.08, y-0.16, y+0.08, 0.86, 0.91,
        mats["linen_white"], coll, bevel=0.02)
    beam("BIKE_Handle", (x, y+0.10, 0.78), (x, y+0.22, 0.98), 0.03, 0.03,
         mats["steel"], coll)
    box("BIKE_Basket", x-0.18, x+0.18, y-0.72, y-0.48, 0.66, 0.80,
        mats["rattan"], coll, bevel=0.01)


def build_plants(mats):
    plants = get_collection("LANDSCAPE")
    palm_tree(mats, plants, "PALM_West", (-11.3, -7.2, 0.0), 8.8, (0.9, -0.3), 14, 1.05, 12)
    palm_tree(mats, plants, "PALM_RearWest", (-12.3, 14.8, 0.0), 10.0, (0.8, 0.5), 15, 1.12, 7)
    palm_tree(mats, plants, "PALM_RearEast", (6.0, 13.7, 0.0), 8.3, (-0.5, 0.3), 13, 0.95, 31)
    palm_tree(mats, plants, "PALM_East", (12.4, 6.4, 0.0), 7.8, (-0.9, 0.1), 13, 0.92, 22)
    palm_tree(mats, plants, "PALM_Front", (-7.6, -10.2, 0.0), 6.8, (0.5, 0.2), 12, 0.82, 44)
    frangipani(mats, plants, "FRANGIPANI_Front", (-3.0, -7.0, 0.0), 4.6, 3)
    frangipani(mats, plants, "FRANGIPANI_Pool", (-10.6, 14.1, 0.0), 3.8, 8)
    banana(mats, plants, "BANANA_Pool", (4.8, 12.0, 0.0), 5)
    banana(mats, plants, "BANANA_East", (11.2, 8.4, 0.0), 6)
    for i in range(18):
        xx = -12.2 + i*1.42
        if -1.0 < xx < 3.2:
            continue
        shrub(mats, plants, f"HEDGE_Front_{i}", xx, -14.15, 0.72, 0.95,
              mats["leaf4" if i % 3 else "leaf1"], 50+i, 3)
    for i in range(15):
        yy = -13.2 + i*1.75
        shrub(mats, plants, f"HEDGE_West_{i}", -12.2, yy, 0.75, 1.0,
              mats["leaf5" if i % 2 else "leaf0"], 70+i, 3)
        shrub(mats, plants, f"HEDGE_East_{i}", 12.2, yy, 0.75, 1.0,
              mats["leaf6" if i % 2 else "leaf2"], 90+i, 3)
    for i, (x, y, r, h) in enumerate([
        (4.2, -4.9, 0.55, 0.75), (5.0, -3.7, 0.45, 0.65),
        (-4.9, -5.2, 0.5, 0.7), (-2.2, -5.1, 0.42, 0.6),
        (5.6, 4.9, 0.55, 0.75), (-0.2, 4.9, 0.5, 0.7),
        (3.8, 5.2, 0.6, 0.85), (-8.9, -3.3, 0.6, 0.8),
    ]):
        shrub(mats, plants, f"FOUNDATION_{i}", x, y, r, h,
              mats[f"leaf{(i+2)%7}"], 120+i, 4)
    for i in range(9):
        x = -9.0 + i*1.3
        if -7.5 < x < -1.6:
            continue
        shrub(mats, plants, f"POOLBED_{i}", x, 11.75, 0.55, 0.72,
              mats[f"leaf{(i+1)%7}"], 150+i, 3)
    for i, (x, y) in enumerate([(-9.1, 10.8), (-9.0, 12.0), (1.6, 11.0),
                                 (2.1, 7.0), (-0.3, 6.2)]):
        heliconia(mats, plants, f"HELICONIA_{i}", (x, y, 0.10), 180+i)
    for i, (x, y) in enumerate([(-5.9, -7.5), (-2.0, -12.0), (5.8, -7.0),
                                (-10.5, 5.8), (3.2, 12.9)]):
        fern(mats, plants, f"FERN_{i}", (x, y, 0.10), 200+i)
    for i in range(5):
        xx = 7.15 + i*0.08
        cone_between(f"BOUGAINVILLEA_Vine{i}", (xx, 1.7, 0.1),
                     (xx+0.5, 1.2, 2.8), 0.02, 0.015, mats["bark"], plants, 6)
        for j in range(3):
            sphere(f"BOUGAINVILLEA_Flower{i}_{j}", 0.12,
                   (xx+0.35+j*0.12, 1.25+j*0.1, 2.55+j*0.1),
                   mats["pink_flower"], plants, segments=8, rings=6,
                   scale=(1, 1, 0.55))
    for i in range(8):
        shrub(mats, plants, f"HERB_{i}", -1.55+ (i%4)*0.62, 5.28,
              0.16, 0.22, mats["leaf3"], 230+i, 2)
    for i, (x, y) in enumerate([(3.15, -4.85), (0.55, -5.35)]):
        cylinder(f"POT_Entry_{i}", 0.32, 0.55, (x, y, 0.375),
                 mats["terracotta"], plants, vertices=18)
        shrub(mats, plants, f"POT_Plant_{i}", x, y, 0.34, 0.95,
              mats["leaf2"], 250+i, 4)
