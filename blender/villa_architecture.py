"""House envelope, timber work, roofs and custom joinery."""
from __future__ import annotations
import math
import random

import bpy
import bmesh
from mathutils import Vector

from villa_config import *
from villa_geometry import (
    box, cylinder, sphere, beam, triangle_wall, plane, text_mesh,
    get_collection, _new_mesh_obj, RNG,
)

T = 0.24          # exterior wall thickness
TI = 0.12         # interior partition thickness


def wall_x(prefix, y_center, x0, x1, z0, z1, openings, mat, coll, t=T):
    """Wall running along X with rectangular openings (x0,x1,z0,z1)."""
    pieces = []
    cursor = x0
    for (a0, a1, b0, b1) in sorted(openings):
        if a0 > cursor + 1e-5:
            pieces.append((cursor, a0, z0, z1))
        if b0 > z0 + 1e-5:
            pieces.append((a0, a1, z0, b0))
        if b1 < z1 - 1e-5:
            pieces.append((a0, a1, b1, z1))
        cursor = max(cursor, a1)
    if cursor < x1 - 1e-5:
        pieces.append((cursor, x1, z0, z1))
    for i, (a0, a1, b0, b1) in enumerate(pieces):
        box(f"{prefix}_{i:02d}", a0, a1, y_center - t/2, y_center + t/2,
            b0, b1, mat, coll, uv_scale=2.2)
    return pieces


def wall_y(prefix, x_center, y0, y1, z0, z1, openings, mat, coll, t=T):
    pieces = []
    cursor = y0
    for (a0, a1, b0, b1) in sorted(openings):
        if a0 > cursor + 1e-5:
            pieces.append((cursor, a0, z0, z1))
        if b0 > z0 + 1e-5:
            pieces.append((a0, a1, z0, b0))
        if b1 < z1 - 1e-5:
            pieces.append((a0, a1, b1, z1))
        cursor = max(cursor, a1)
    if cursor < y1 - 1e-5:
        pieces.append((cursor, y1, z0, z1))
    for i, (a0, a1, b0, b1) in enumerate(pieces):
        box(f"{prefix}_{i:02d}", x_center - t/2, x_center + t/2, a0, a1,
            b0, b1, mat, coll, uv_scale=2.2)
    return pieces


def louver_panel_x(name, x0, x1, y, z0, z1, mat, coll, depth=0.075, slats=18):
    """A shutter panel on an X-facing wall, with horizontal tilted slats."""
    frame = 0.045
    box(name + "_top", x0, x1, y-depth/2, y+depth/2, z1-frame, z1,
        mat, coll, bevel=0.006)
    box(name + "_bottom", x0, x1, y-depth/2, y+depth/2, z0, z0+frame,
        mat, coll, bevel=0.006)
    box(name + "_left", x0, x0+frame, y-depth/2, y+depth/2, z0, z1,
        mat, coll, bevel=0.006)
    box(name + "_right", x1-frame, x1, y-depth/2, y+depth/2, z0, z1,
        mat, coll, bevel=0.006)
    inner_h = z1 - z0 - 2*frame
    for i in range(slats):
        zz = z0 + frame + (i + 0.5) * inner_h / slats
        box(f"{name}_slat_{i:02d}", x0+frame, x1-frame,
            y-0.035, y+0.035, zz-0.013, zz+0.013,
            mat, coll, rotation=(math.radians(28), 0, 0))


def louver_panel_y(name, x, y0, y1, z0, z1, mat, coll, depth=0.075, slats=18):
    frame = 0.045
    box(name + "_top", x-depth/2, x+depth/2, y0, y1, z1-frame, z1,
        mat, coll, bevel=0.006)
    box(name + "_bottom", x-depth/2, x+depth/2, y0, y1, z0, z0+frame,
        mat, coll, bevel=0.006)
    box(name + "_left", x-depth/2, x+depth/2, y0, y0+frame, z0, z1,
        mat, coll, bevel=0.006)
    box(name + "_right", x-depth/2, x+depth/2, y1-frame, y1, z0, z1,
        mat, coll, bevel=0.006)
    inner_h = z1 - z0 - 2*frame
    for i in range(slats):
        zz = z0 + frame + (i + 0.5) * inner_h / slats
        box(f"{name}_slat_{i:02d}", x-0.035, x+0.035,
            y0+frame, y1-frame, zz-0.013, zz+0.013,
            mat, coll, rotation=(0, math.radians(28), 0))


def window_x(name, y_face, x0, x1, z0, z1, mats, coll, outward=-1,
             mullions=2, shutters=True, sill=True, louver=True,
             transom=False):
    """Window in a wall that runs along X. outward=-1 south, +1 north."""
    fm, gm, sm = mats["black"], mats["glass"], mats["stone_light"]
    ft, fd = 0.055, 0.11
    yc = y_face + outward * 0.015
    box(f"{name}_frame_l", x0, x0+ft, yc-fd/2, yc+fd/2, z0, z1, fm, coll)
    box(f"{name}_frame_r", x1-ft, x1, yc-fd/2, yc+fd/2, z0, z1, fm, coll)
    box(f"{name}_frame_t", x0, x1, yc-fd/2, yc+fd/2, z1-ft, z1, fm, coll)
    box(f"{name}_frame_b", x0, x1, yc-fd/2, yc+fd/2, z0, z0+ft, fm, coll)
    box(f"{name}_glass", x0+ft, x1-ft, yc-0.006, yc+0.006,
        z0+ft, z1-ft, gm, coll)
    for i in range(1, mullions + 1):
        xx = x0 + (x1-x0) * i / (mullions+1)
        box(f"{name}_mullion_{i}", xx-0.022, xx+0.022,
            yc-fd/2, yc+fd/2, z0, z1, fm, coll)
    if transom:
        zz = z0 + (z1-z0)*0.72
        box(f"{name}_transom", x0, x1, yc-fd/2+0.005, yc+fd/2-0.005,
            zz-0.025, zz+0.025, fm, coll)
    if sill:
        box(f"{name}_sill", x0-0.10, x1+0.10, y_face, y_face+outward*0.18,
            z0-0.085, z0+0.01, sm, coll, bevel=0.008)
    if shutters:
        pw = min(0.62, max(0.42, (x1-x0)*0.30))
        if louver:
            louver_panel_x(f"{name}_shutter_l", x0-pw-0.055, x0-0.055,
                           y_face+outward*0.055, z0, z1, mats["sage"], coll)
            louver_panel_x(f"{name}_shutter_r", x1+0.055, x1+pw+0.055,
                           y_face+outward*0.055, z0, z1, mats["sage"], coll)
        else:
            box(f"{name}_shutter_l", x0-pw-0.055, x0-0.055,
                y_face+outward*0.03, y_face+outward*0.09, z0, z1,
                mats["sage"], coll, bevel=0.008)
            box(f"{name}_shutter_r", x1+0.055, x1+pw+0.055,
                y_face+outward*0.03, y_face+outward*0.09, z0, z1,
                mats["sage"], coll, bevel=0.008)


def window_y(name, x_face, y0, y1, z0, z1, mats, coll, outward=-1,
             mullions=1, shutters=False, sill=True):
    fm, gm, sm = mats["black"], mats["glass"], mats["stone_light"]
    ft, fd = 0.055, 0.11
    xc = x_face + outward * 0.015
    box(f"{name}_frame_l", xc-fd/2, xc+fd/2, y0, y0+ft, z0, z1, fm, coll)
    box(f"{name}_frame_r", xc-fd/2, xc+fd/2, y1-ft, y1, z0, z1, fm, coll)
    box(f"{name}_frame_t", xc-fd/2, xc+fd/2, y0, y1, z1-ft, z1, fm, coll)
    box(f"{name}_frame_b", xc-fd/2, xc+fd/2, y0, y1, z0, z0+ft, fm, coll)
    box(f"{name}_glass", xc-0.006, xc+0.006, y0+ft, y1-ft,
        z0+ft, z1-ft, gm, coll)
    for i in range(1, mullions+1):
        yy = y0 + (y1-y0)*i/(mullions+1)
        box(f"{name}_mullion_{i}", xc-fd/2, xc+fd/2, yy-0.022, yy+0.022,
            z0, z1, fm, coll)
    if sill:
        box(f"{name}_sill", x_face, x_face+outward*0.18, y0-0.10, y1+0.10,
            z0-0.085, z0+0.01, sm, coll, bevel=0.008)
    if shutters:
        louver_panel_y(f"{name}_shutter_l", x_face+outward*0.055,
                       y0-0.58, y0-0.055, z0, z1, mats["sage"], coll)
        louver_panel_y(f"{name}_shutter_r", x_face+outward*0.055,
                       y1+0.055, y1+0.58, z0, z1, mats["sage"], coll)


def entry_door(name, y_face, x0, x1, z0, z1, mats, coll, outward=-1):
    fm, dm = mats["black"], mats["teak_dark"]
    ft = 0.06
    yc = y_face + outward*0.02
    box(name+"_frame_l", x0, x0+ft, yc-0.055, yc+0.055, z0, z1, fm, coll)
    box(name+"_frame_r", x1-ft, x1, yc-0.055, yc+0.055, z0, z1, fm, coll)
    box(name+"_frame_t", x0, x1, yc-0.055, yc+0.055, z1-ft, z1, fm, coll)
    box(name+"_door", x0+ft, x1-ft, yc-0.045, yc+0.045, z0, z1-ft,
        dm, coll, bevel=0.006)
    # vertical glazed slot
    gx0, gx1 = x0+(x1-x0)*0.60, x1-ft-0.06
    box(name+"_slot_glass", gx0, gx1, yc-0.05, yc-0.035,
        z0+0.35, z1-0.45, mats["glass"], coll)
    # handle
    cylinder(name+"_handle", 0.018, 0.22, (x0+(x1-x0)*0.46, yc+outward*0.075,
             z0+1.0), fm, coll, axis="Z", vertices=12)
    # stone threshold
    box(name+"_threshold", x0-0.12, x1+0.12, y_face-0.12, y_face+0.18,
        z0-0.04, z0+0.02, mats["stone_light"], coll)


def sliding_x(name, y_face, x0, x1, z0, z1, mats, coll, panels=4, outward=-1):
    fm, gm = mats["black"], mats["glass"]
    fd = 0.10
    yc = y_face + outward*0.015
    box(name+"_track_t", x0, x1, yc-fd/2, yc+fd/2, z1-0.06, z1, fm, coll)
    box(name+"_track_b", x0, x1, yc-fd/2, yc+fd/2, z0, z0+0.035, fm, coll)
    for i in range(panels):
        px0 = x0 + (x1-x0)*i/panels
        px1 = x0 + (x1-x0)*(i+1)/panels
        yy = yc + (0.025 if i % 2 else -0.025)
        box(f"{name}_p{i}_l", px0, px0+0.045, yy-0.035, yy+0.035, z0, z1, fm, coll)
        box(f"{name}_p{i}_r", px1-0.045, px1, yy-0.035, yy+0.035, z0, z1, fm, coll)
        box(f"{name}_p{i}_t", px0, px1, yy-0.035, yy+0.035, z1-0.05, z1, fm, coll)
        box(f"{name}_p{i}_b", px0, px1, yy-0.035, yy+0.035, z0, z0+0.05, fm, coll)
        box(f"{name}_p{i}_glass", px0+0.045, px1-0.045, yy-0.006, yy+0.006,
            z0+0.05, z1-0.05, gm, coll)


def sliding_x_wood(name, y_face, x0, x1, z0, z1, mats, coll, panels=2, outward=-1):
    """Slatted timber sliding screens."""
    fm = mats["teak"]
    fd = 0.075
    yc = y_face + outward*0.02
    for i in range(panels):
        px0 = x0 + (x1-x0)*i/panels
        px1 = x0 + (x1-x0)*(i+1)/panels
        yy = yc + (0.02 if i % 2 else -0.02)
        box(f"{name}_p{i}_frame_t", px0, px1, yy-fd/2, yy+fd/2, z1-0.055, z1, fm, coll)
        box(f"{name}_p{i}_frame_b", px0, px1, yy-fd/2, yy+fd/2, z0, z0+0.055, fm, coll)
        box(f"{name}_p{i}_frame_l", px0, px0+0.045, yy-fd/2, yy+fd/2, z0, z1, fm, coll)
        box(f"{name}_p{i}_frame_r", px1-0.045, px1, yy-fd/2, yy+fd/2, z0, z1, fm, coll)
        for j in range(12):
            zz = z0 + (j+0.5)*(z1-z0)/12
            box(f"{name}_p{i}_slat{j:02d}", px0+0.05, px1-0.05,
                yy-0.015, yy+0.015, zz-0.018, zz+0.018, fm, coll, bevel=0.003)


# --------------------------------------------------------------------- roofs
def tiled_slope_x(name, x0, x1, y_ridge, y_eave, z_ridge, z_eave,
                  mat, coll, thickness=0.14, ribs=True):
    """Roof slope running down along Y, corrugation across X."""
    nx = max(48, int((x1-x0)/0.055))
    nt = 10
    verts, uvs, faces = [], [], []
    slope = math.hypot(y_eave-y_ridge, z_eave-z_ridge)
    for j in range(nt+1):
        t = j/nt
        y = y_ridge + (y_eave-y_ridge)*t
        z = z_ridge + (z_eave-z_ridge)*t
        for i in range(nx+1):
            x = x0 + (x1-x0)*i/nx
            rib = 0.016 + 0.022*(0.5+0.5*math.cos(2*math.pi*(x-x0)/0.285)) if ribs else 0
            verts.append((x, y, z + rib))
            uvs.append(((x-x0)/1.2, t*slope/1.2))
    for j in range(nt):
        for i in range(nx):
            a = j*(nx+1)+i
            faces.append((a, a+1, a+nx+2, a+nx+1))
    obj = _new_mesh_obj(name, verts, faces, mat, coll, uvs=uvs)
    # underside, slightly below, as a separate shell
    verts2, faces2 = [], []
    for j in range(nt+1):
        t = j/nt
        y = y_ridge + (y_eave-y_ridge)*t
        z = z_ridge + (z_eave-z_ridge)*t - thickness
        for i in range(nx+1):
            x = x0 + (x1-x0)*i/nx
            verts2.append((x, y, z))
    for j in range(nt):
        for i in range(nx):
            a = j*(nx+1)+i
            faces2.append((a+nx+1, a+nx+2, a+1, a))
    _new_mesh_obj(name+"_soffit", verts2, faces2, coll and mat, coll)
    return obj


def tiled_slope_y(name, y0, y1, x_ridge, x_eave, z_ridge, z_eave,
                  mat, coll, thickness=0.14, ribs=True):
    """Roof slope running down along X, corrugation across Y."""
    ny = max(48, int((y1-y0)/0.055))
    nt = 10
    verts, uvs, faces = [], [], []
    slope = math.hypot(x_eave-x_ridge, z_eave-z_ridge)
    for j in range(nt+1):
        t = j/nt
        x = x_ridge + (x_eave-x_ridge)*t
        z = z_ridge + (z_eave-z_ridge)*t
        for i in range(ny+1):
            y = y0 + (y1-y0)*i/ny
            rib = 0.016 + 0.022*(0.5+0.5*math.cos(2*math.pi*(y-y0)/0.285)) if ribs else 0
            verts.append((x, y, z + rib))
            uvs.append(((y-y0)/1.2, t*slope/1.2))
    for j in range(nt):
        for i in range(ny):
            a = j*(ny+1)+i
            faces.append((a, a+1, a+ny+2, a+ny+1))
    obj = _new_mesh_obj(name, verts, faces, mat, coll, uvs=uvs)
    verts2, faces2 = [], []
    for j in range(nt+1):
        t = j/nt
        x = x_ridge + (x_eave-x_ridge)*t
        z = z_ridge + (z_eave-z_ridge)*t - thickness
        for i in range(ny+1):
            y = y0 + (y1-y0)*i/ny
            verts2.append((x, y, z))
    for j in range(nt):
        for i in range(ny):
            a = j*(ny+1)+i
            faces2.append((a+ny+1, a+ny+2, a+1, a))
    _new_mesh_obj(name+"_soffit", verts2, faces2, mat, coll)
    return obj


def build_roof(mats, roof_coll):
    # main gable
    tiled_slope_x("ROOF_Main_South", ROOF_X[0], ROOF_X[1], ROOF_RIDGE_Y, ROOF_Y[0],
                  ROOF_RIDGE_Z, ROOF_EAVE_Z, mats["roof"], roof_coll)
    tiled_slope_x("ROOF_Main_North", ROOF_X[0], ROOF_X[1], ROOF_RIDGE_Y, ROOF_Y[1],
                  ROOF_RIDGE_Z, ROOF_EAVE_Z, mats["roof"], roof_coll)
    # ridge
    cylinder("ROOF_Main_Ridge", 0.16, ROOF_X[1]-ROOF_X[0],
             ((ROOF_X[0]+ROOF_X[1])/2, ROOF_RIDGE_Y, ROOF_RIDGE_Z+0.02),
             mats["roof_cap"], roof_coll, axis="X", vertices=16)
    box("ROOF_Main_RidgeBoard", ROOF_X[0], ROOF_X[1], ROOF_RIDGE_Y-0.13,
        ROOF_RIDGE_Y+0.13, ROOF_RIDGE_Z-0.18, ROOF_RIDGE_Z-0.02,
        mats["teak_dark"], roof_coll)
    # gable infill
    triangle_wall("ROOF_Gable_West", MAIN[0], MAIN[2], MAIN[3], EAVE, RIDGE,
                  T, mats["plaster"], roof_coll, uv_scale=2.0)
    triangle_wall("ROOF_Gable_East", MAIN[1], MAIN[2], MAIN[3], EAVE, RIDGE,
                  T, mats["plaster"], roof_coll, uv_scale=2.0)
    # gable battens
    for sgn, xx in ((-1, MAIN[0]), (1, MAIN[1])):
        for i in range(6):
            t = i/5
            yy = MAIN[2] + (MAIN[3]-MAIN[2])*t
            # height of triangle at this y
            zz = EAVE + (RIDGE-EAVE)*(1-abs((yy-(MAIN[2]+MAIN[3])/2)/((MAIN[3]-MAIN[2])/2)))
            if zz > EAVE+0.3:
                box(f"ROOF_Gable_Batten_{sgn}_{i}", xx-T/2-0.018, xx+T/2+0.018,
                    yy-0.025, yy+0.025, EAVE, zz-0.08, mats["teak"], roof_coll)
        # circular vent
        cylinder(f"ROOF_Gable_Vent_{sgn}", 0.24, 0.06,
                 (xx+sgn*0.15, (MAIN[2]+MAIN[3])/2, 7.85),
                 mats["teak_dark"], roof_coll, axis="X", vertices=24)
    # fascia / gutters / eaves
    for yy, out in ((ROOF_Y[0], -1), (ROOF_Y[1], 1)):
        box(f"ROOF_Fascia_{out}", ROOF_X[0], ROOF_X[1], yy-0.06, yy+0.06,
            ROOF_EAVE_Z-0.24, ROOF_EAVE_Z-0.02, mats["teak_dark"], roof_coll)
        cylinder(f"ROOF_Gutter_{out}", 0.075, ROOF_X[1]-ROOF_X[0],
                 ((ROOF_X[0]+ROOF_X[1])/2, yy+out*0.10, ROOF_EAVE_Z-0.06),
                 mats["bronze"], roof_coll, axis="X", vertices=12)
        # rafter tails
        for i in range(26):
            xx = ROOF_X[0]+0.28 + i*(ROOF_X[1]-ROOF_X[0]-0.56)/25
            beam(f"ROOF_Rafter_{out}_{i:02d}",
                 (xx, MAIN[2] if out < 0 else MAIN[3], ROOF_EAVE_Z-0.33),
                 (xx, yy+out*0.04, ROOF_EAVE_Z-0.10),
                 0.075, 0.10, mats["teak"], roof_coll)
    # bargeboards along gable edges
    for xx in (ROOF_X[0]+0.03, ROOF_X[1]-0.03):
        for yy in (ROOF_Y[0], ROOF_Y[1]):
            pass
    # wing roof (lower cross volume, ridge along X)
    tiled_slope_x("ROOF_Wing_South", WING_ROOF[0], WING_ROOF[1], 0.35, WING_ROOF[2],
                  WING_RIDGE_Z, WING_EAVE_Z, mats["roof"], roof_coll)
    tiled_slope_x("ROOF_Wing_North", WING_ROOF[0], WING_ROOF[1], 0.35, WING_ROOF[3],
                  WING_RIDGE_Z, WING_EAVE_Z, mats["roof"], roof_coll)
    cylinder("ROOF_Wing_Ridge", 0.14, WING_ROOF[1]-WING_ROOF[0],
             ((WING_ROOF[0]+WING_ROOF[1])/2, 0.35, WING_RIDGE_Z+0.02),
             mats["roof_cap"], roof_coll, axis="X", vertices=14)
    triangle_wall("ROOF_Wing_Gable_West", WING_ROOF[0], WING_ROOF[2], WING_ROOF[3],
                  WING_EAVE_Z, WING_RIDGE_Z, T, mats["plaster_white"], roof_coll,
                  uv_scale=2.0)
    for yy, out in ((WING_ROOF[2], -1), (WING_ROOF[3], 1)):
        box(f"ROOF_Wing_Fascia_{out}", WING_ROOF[0], WING_ROOF[1], yy-0.06, yy+0.06,
            WING_EAVE_Z-0.22, WING_EAVE_Z-0.02, mats["teak_dark"], roof_coll)
        cylinder(f"ROOF_Wing_Gutter_{out}", 0.065, WING_ROOF[1]-WING_ROOF[0],
                 ((WING_ROOF[0]+WING_ROOF[1])/2, yy+out*0.095, WING_EAVE_Z-0.06),
                 mats["bronze"], roof_coll, axis="X", vertices=12)
    # solar hot-water panels on the wing's north pitch
    tilt = math.atan2(WING_RIDGE_Z-WING_EAVE_Z, WING_ROOF[3]-0.35)
    for i in range(3):
        xpos = WING_ROOF[0]+0.55+i*0.72
        yc = 2.55
        zc = WING_RIDGE_Z - (yc-0.35)*(WING_RIDGE_Z-WING_EAVE_Z)/(WING_ROOF[3]-0.35) + 0.10
        box(f"ROOF_Solar_{i}", xpos, xpos+0.55, yc-0.50, yc+0.50,
            zc-0.03, zc+0.03, mats["glass_dark"], roof_coll,
            rotation=(-tilt, 0, 0))
    # downpipes, fixed to the wall corners rather than floating at the eave
    for i, (xx, yy) in enumerate(((MAIN[0]-0.17, MAIN[2]-0.17),
                                  (MAIN[1]+0.17, MAIN[2]-0.17),
                                  (MAIN[0]-0.17, MAIN[3]+0.17),
                                  (MAIN[1]+0.17, MAIN[3]+0.17))):
        cylinder(f"ROOF_Downpipe_{i}", 0.055, EAVE-0.14,
                 (xx, yy, (EAVE-0.14)/2+0.1), mats["bronze"], roof_coll,
                 axis="Z", vertices=12)
        for j in range(4):
            zz = 1.1 + j*1.5
            if zz < EAVE-0.4:
                box(f"ROOF_DownpipeBracket_{i}_{j}", xx-0.09, xx+0.09,
                    yy-0.09, yy+0.09, zz, zz+0.045,
                    mats["bronze"], roof_coll)


def build_shell(mats):
    gf = get_collection("HOUSE_GF")
    f2 = get_collection("HOUSE_F2")
    roof = get_collection("ROOF")
    trim = get_collection("HOUSE_TRIM")

    # ---------------------------------------------------------- foundations
    box("GF_Plinth_Main", MAIN[0]-0.22, MAIN[1]+0.22, MAIN[2]-0.22, MAIN[3]+0.22,
        -0.05, GF, mats["stone"], gf, uv_scale=1.2, bevel=0.02)
    box("GF_Plinth_Wing", WING[0]-0.20, WING[1]+0.10, WING[2]-0.20, WING[3]+0.20,
        -0.05, GF, mats["stone"], gf, uv_scale=1.2, bevel=0.02)
    # ground slab / finished floor
    box("GF_Slab", MAIN[0], MAIN[1], MAIN[2], MAIN[3], GF-0.09, GF,
        mats["concrete"], gf)
    plane("GF_Floor_Main", MAIN[0]+0.12, MAIN[1]-0.12, MAIN[2]+0.12, MAIN[3]-0.12,
          GF+0.003, mats["tile_floor"], gf, uv_scale=0.9)
    plane("GF_Floor_Wing", WING[0]+0.12, WING[1]-0.02, WING[2]+0.12, WING[3]-0.12,
          GF+0.004, mats["deck"], gf, uv_scale=0.6)

    # ---------------------------------------------------------- ground walls
    south_open = [
        (-4.05, -1.25, 0.93, 2.92),
        (1.02, 2.16, GF, 2.72),
        (3.15, 4.62, 0.95, 2.55),
    ]
    wall_x("GF_Wall_S", MAIN[2]+T/2, MAIN[0], MAIN[1], GF, F2, south_open,
           mats["plaster"], gf)
    north_open = [(-2.72, 3.18, GF, 3.06)]
    wall_x("GF_Wall_N", MAIN[3]-T/2, MAIN[0], MAIN[1], GF, F2, north_open,
           mats["plaster"], gf, t=T)
    west_open = [(-3.86, -2.84, 0.95, 2.62), (-1.78, -0.98, GF, 2.55)]
    wall_y("GF_Wall_W", MAIN[0]+T/2, MAIN[2], MAIN[3], GF, F2, west_open,
           mats["plaster"], gf)
    east_open = [(-1.45, 0.92, 1.18, 2.72)]
    wall_y("GF_Wall_E", MAIN[1]-T/2, MAIN[2], MAIN[3], GF, F2, east_open,
           mats["plaster"], gf)

    # wing walls
    wing_s_open = [(-7.95, -5.65, 0.90, 2.70)]
    wall_x("GF_Wing_S", WING[2]+T/2, WING[0], WING[1], GF, WING_EAVE_Z-0.25,
           wing_s_open, mats["plaster"], gf)
    wing_n_open = [(-7.95, -5.85, GF, 2.72)]
    wall_x("GF_Wing_N", WING[3]-T/2, WING[0], WING[1], GF, WING_EAVE_Z-0.25,
           wing_n_open, mats["plaster"], gf)
    wing_w_open = [(0.95, 2.18, 1.62, 2.85)]
    wall_y("GF_Wing_W", WING[0]+T/2, WING[2], WING[3], GF, WING_EAVE_Z-0.25,
           wing_w_open, mats["plaster"], gf)
    # the east side of the wing is the main house wall, already built above

    # ------------------------------------------------------------ upper walls
    f2s_open = [
        (-4.42, -1.62, F2, 5.92),
        (-0.52, 0.92, 4.22, 5.78),
        (2.38, 4.58, 4.08, 5.90),
    ]
    wall_x("F2_Wall_S", MAIN[2]+T/2, MAIN[0], MAIN[1], F2, EAVE, f2s_open,
           mats["plaster_white"], f2)
    f2n_open = [
        (-4.22, -2.38, 4.18, 5.82),
        (0.42, 1.82, 4.85, 6.08),
        (2.52, 3.38, F2, 5.72),
    ]
    wall_x("F2_Wall_N", MAIN[3]-T/2, MAIN[0], MAIN[1], F2, EAVE, f2n_open,
           mats["plaster_white"], f2)
    f2w_open = [(-3.56, -2.90, 4.35, 5.72)]
    wall_y("F2_Wall_W", MAIN[0]+T/2, MAIN[2], MAIN[3], F2, EAVE, f2w_open,
           mats["plaster_white"], f2)
    f2e_open = [(-2.72, -1.10, 4.30, 5.72)]
    wall_y("F2_Wall_E", MAIN[1]-T/2, MAIN[2], MAIN[3], F2, EAVE, f2e_open,
           mats["plaster_white"], f2)

    # ------------------------------------------------ F2 slab around stair void
    slab_parts = [
        (MAIN[0]+0.0, 3.45, MAIN[2]+0.0, MAIN[3]-0.0),
        (3.45, MAIN[1], MAIN[2], -2.80),
        (3.45, MAIN[1], 1.80, MAIN[3]),
        (4.95, MAIN[1], -2.80, 1.80),
    ]
    for i, (x0, x1, y0, y1) in enumerate(slab_parts):
        box(f"F2_Slab_{i}", x0, x1, y0, y1, F2-0.18, F2,
            mats["concrete"], f2)
        plane(f"F2_Floor_{i}", x0+0.03, x1-0.03, y0+0.03, y1-0.03,
              F2+0.003, mats["deck"], f2, uv_scale=0.7)
    # dark steel edge around the stair void
    box("F2_StairVoidTrim", 3.45, 4.95, -2.82, -2.78, F2-0.20, F2+0.02,
        mats["black"], f2)
    box("F2_StairVoidTrimN", 3.45, 4.95, 1.78, 1.82, F2-0.20, F2+0.02,
        mats["black"], f2)

    # --------------------------------------------------------------- openings
    window_x("GF_Win_Living", MAIN[2], -4.05, -1.25, 0.93, 2.92, mats, gf,
             outward=-1, mullions=3, shutters=True)
    entry_door("GF_EntryDoor", MAIN[2], 1.02, 2.16, GF, 2.72, mats, gf)
    window_x("GF_Win_East", MAIN[2], 3.15, 4.62, 0.95, 2.55, mats, gf,
             outward=-1, mullions=2, shutters=False)
    sliding_x("GF_Glass_North", MAIN[3], -2.72, 3.18, GF, 3.06, mats, gf,
              panels=4, outward=1)
    window_y("GF_Win_West", MAIN[0], -3.86, -2.84, 0.95, 2.62, mats, gf,
             outward=-1, mullions=1, shutters=False)
    window_y("GF_Win_EastSide", MAIN[1], -1.45, 0.92, 1.18, 2.72, mats, gf,
             outward=1, mullions=2, shutters=False)
    window_x("GF_Wing_Win_S", WING[2], -7.95, -5.65, 0.90, 2.70, mats, gf,
             outward=-1, mullions=2, shutters=True)
    sliding_x("GF_Wing_Glass_N", WING[3], -7.95, -5.85, GF, 2.72, mats, gf,
              panels=2, outward=1)
    window_y("GF_Wing_Win_W", WING[0], 0.95, 2.18, 1.62, 2.85, mats, gf,
             outward=-1, mullions=1, shutters=False)

    sliding_x("F2_Glass_Master", MAIN[2], -4.42, -1.62, F2, 5.92, mats, f2,
              panels=3, outward=-1)
    window_x("F2_Win_Kids", MAIN[2], -0.52, 0.92, 4.22, 5.78, mats, f2,
             outward=-1, mullions=1, shutters=True)
    window_x("F2_Win_Study", MAIN[2], 2.38, 4.58, 4.08, 5.90, mats, f2,
             outward=-1, mullions=2, shutters=True)
    window_x("F2_Win_North1", MAIN[3], -4.22, -2.38, 4.18, 5.82, mats, f2,
             outward=1, mullions=2, shutters=False)
    window_x("F2_Win_Bath", MAIN[3], 0.42, 1.82, 4.85, 6.08, mats, f2,
             outward=1, mullions=1, shutters=False)
    sliding_x("F2_Door_Balcony", MAIN[3], 2.52, 3.38, F2, 5.72, mats, f2,
              panels=2, outward=1)
    window_y("F2_Win_West", MAIN[0], -3.56, -2.90, 4.35, 5.72, mats, f2,
             outward=-1, mullions=1, shutters=False)
    window_y("F2_Win_East", MAIN[1], -2.72, -1.10, 4.30, 5.72, mats, f2,
             outward=1, mullions=2, shutters=False)

    # --------------------------------------------------------------- trim bands
    # horizontal shadow band at the floor line
    box("GF_Band_S", MAIN[0]-0.02, MAIN[1]+0.02, MAIN[2]-0.035, MAIN[2]+0.02,
        F2-0.22, F2-0.10, mats["teak_dark"], trim)
    box("GF_Band_N", MAIN[0]-0.02, MAIN[1]+0.02, MAIN[3]-0.02, MAIN[3]+0.035,
        F2-0.22, F2-0.10, mats["teak_dark"], trim)
    box("GF_Band_W", MAIN[0]-0.035, MAIN[0]+0.02, MAIN[2]-0.02, MAIN[3]+0.02,
        F2-0.22, F2-0.10, mats["teak_dark"], trim)
    box("GF_Band_E", MAIN[1]-0.02, MAIN[1]+0.035, MAIN[2]-0.02, MAIN[3]+0.02,
        F2-0.22, F2-0.10, mats["teak_dark"], trim)
    # vertical battens near entry / stair
    for i in range(11):
        xx = 2.35 + i*0.075
        box(f"TRIM_EntryBatten_{i:02d}", xx, xx+0.025, MAIN[2]-0.05, MAIN[2]-0.02,
            GF, 3.25, mats["teak"], trim)
    # entry canopy
    box("GF_Canopy_Slab", 0.35, 2.95, -5.75, -4.16, 3.23, 3.38,
        mats["teak_dark"], trim, bevel=0.01)
    for i in range(16):
        yy = -5.68 + i*0.092
        box(f"TRIM_CanopySlat_{i:02d}", 0.38, 2.92, yy, yy+0.045,
            3.38, 3.42, mats["teak"], trim)
    for xx in (0.48, 2.82):
        cylinder(f"TRIM_CanopyPost_{xx}", 0.055, 2.95, (xx, -5.62, 0.35+2.95/2),
                 mats["black"], trim, vertices=12)
    cylinder("TRIM_CanopyLight", 0.09, 0.08, (1.66, -5.3, 3.30),
             mats["lamp"], trim, vertices=16)
    # house plaque
    box("TRIM_Plaque", 2.32, 2.92, MAIN[2]-0.045, MAIN[2]-0.015, 1.58, 2.06,
        mats["teak_dark"], trim, bevel=0.006)
    text_mesh("TRIM_PlaqueText", "KAZE 01", (2.62, MAIN[2]-0.06, 1.82), 0.075,
              mats["stone_light"], trim, rot=(math.pi/2, 0, 0), extrude=0.003)
    # downlights at entry
    for xx in (0.55, 2.75):
        cylinder(f"TRIM_EntryLight_{xx}", 0.07, 0.06, (xx, -5.34, 3.22),
                 mats["lamp"], trim, vertices=14)

    # ------------------------------------------------------------- balconies
    # front balcony: master bedroom
    bx0, bx1 = -4.48, -1.56
    by0, by1 = -5.72, MAIN[2]
    box("F2_Balcony_Slab", bx0, bx1, by0, by1, F2-0.17, F2+0.02,
        mats["concrete"], f2, bevel=0.01)
    # deck boards
    nboards = int((bx1-bx0)/0.155)
    for i in range(nboards):
        xx = bx0 + 0.04 + i*0.155
        box(f"F2_Balcony_Board_{i:02d}", xx, xx+0.135, by0+0.04, by1-0.03,
            F2+0.02, F2+0.065, mats["deck"], f2)
    # support brackets
    for xx in (bx0+0.2, bx1-0.2):
        beam(f"F2_Balcony_Bracket_{xx}", (xx, MAIN[2]-0.2, F2-0.2),
             (xx, MAIN[2]-1.15, F2-0.75), 0.09, 0.12, mats["teak"], f2)
    # railing
    rail_z0, rail_z1 = F2+0.06, F2+1.04
    box("F2_Balcony_RailTop", bx0, bx1, by0+0.01, by0+0.10, rail_z1-0.055, rail_z1,
        mats["teak"], f2)
    box("F2_Balcony_RailBottom", bx0, bx1, by0+0.01, by0+0.08, rail_z0+0.10, rail_z0+0.16,
        mats["teak"], f2)
    for side_x in (bx0, bx1-0.06):
        box(f"F2_Balcony_RailPost_{side_x}", side_x, side_x+0.06, by0+0.01, by0+0.10,
            rail_z0, rail_z1, mats["teak"], f2)
    n = int((bx1-bx0)/0.12)
    for i in range(1, n):
        xx = bx0 + i*(bx1-bx0)/n
        box(f"F2_Balcony_Slat_{i:02d}", xx-0.018, xx+0.018, by0+0.03, by0+0.065,
            rail_z0+0.16, rail_z1-0.055, mats["teak"], f2)
    # planters on balcony
    for j, (px, pw) in enumerate(((-4.3, 0.5), (-1.85, 0.42))):
        box(f"F2_Balcony_Planter_{j}", px, px+pw, by0+0.12, by0+0.46,
            F2+0.07, F2+0.36, mats["terracotta"], f2, bevel=0.02)
    # laundry pole (a small domestic detail)
    cylinder("F2_Balcony_LaundryPole", 0.022, 1.9,
             ((bx0+bx1)/2, by0+0.28, F2+1.68), mats["steel"], f2,
             axis="X", vertices=10)
    for xx in (bx0+0.28, bx1-0.28):
        cylinder(f"F2_Balcony_LaundryPost_{xx}", 0.022, 0.7,
                 (xx, by0+0.28, F2+1.34), mats["steel"], f2, vertices=8)
    # two hanging linen towels
    box("F2_Balcony_Towel1", -3.45, -2.95, by0+0.285, by0+0.31,
        F2+0.95, F2+1.62, mats["linen_white"], f2)
    box("F2_Balcony_Towel2", -2.35, -1.95, by0+0.285, by0+0.31,
        F2+1.02, F2+1.62, mats["linen"], f2)

    # rear balcony / route to pool
    rx0, rx1 = -0.7, 3.5
    ry0, ry1 = MAIN[3], MAIN[3]+1.18
    box("F2_RearDeck_Slab", rx0, rx1, ry0, ry1, F2-0.16, F2+0.02,
        mats["concrete"], f2)
    nb = int((rx1-rx0)/0.155)
    for i in range(nb):
        xx = rx0 + 0.04 + i*0.155
        box(f"F2_RearDeck_Board_{i:02d}", xx, xx+0.135, ry0+0.03, ry1-0.03,
            F2+0.02, F2+0.06, mats["deck"], f2)
    box("F2_RearRail_Top", rx0, rx1, ry1-0.1, ry1-0.02, F2+0.98, F2+1.04,
        mats["teak"], f2)
    for i in range(int((rx1-rx0)/0.12)):
        xx = rx0 + i*0.12
        box(f"F2_RearRail_Slat_{i:02d}", xx, xx+0.022, ry1-0.075, ry1-0.045,
            F2+0.10, F2+0.98, mats["teak"], f2)

    # --------------------------------------------------------------- roof
    build_roof(mats, roof)
    return gf, f2, roof, trim
