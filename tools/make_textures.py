#!/usr/bin/env python3
"""Generate tileable material textures for the Nohara Hainan Villa."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "textures"
OUT.mkdir(exist_ok=True)
RNG = np.random.default_rng(20261103)
S = 1024


def periodic_value_noise(size, cells, seed=0):
    """Tileable bilinear value noise on a periodic lattice."""
    rng = np.random.default_rng(seed)
    grid = rng.random((cells, cells)).astype(np.float32)
    t = np.arange(size, dtype=np.float32) / size * cells
    i0 = np.floor(t).astype(np.int32) % cells
    i1 = (i0 + 1) % cells
    f = t - np.floor(t)
    f = f * f * (3 - 2 * f)
    # rows then cols
    a = grid[i0][:, i0]
    b = grid[i0][:, i1]
    c = grid[i1][:, i0]
    d = grid[i1][:, i1]
    fx = f[None, :]
    fy = f[:, None]
    top = a * (1 - fx) + b * fx
    bot = c * (1 - fx) + d * fx
    return top * (1 - fy) + bot * fy


def periodic_noise(size, components=8, scale=3.0, seed=0):
    """Natural-looking tileable fractal value noise."""
    field = np.zeros((size, size), np.float32)
    amp = 1.0
    total = 0.0
    cells = max(2, int(2 * scale))
    for o in range(components):
        field += amp * periodic_value_noise(size, cells, seed + o * 101)
        total += amp
        amp *= 0.58
        cells = min(size, cells * 2)
    field /= total
    field -= field.min()
    field /= max(field.max(), 1e-6)
    return field


def lerp(a, b, t):
    return a + (b - a) * t


def colorize(height, stops):
    """Map 0..1 height through (position, rgb) stops."""
    h, w = height.shape
    out = np.zeros((h, w, 3), np.float32)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        mask = (height >= p0) & (height <= p1)
        t = np.clip((height[mask] - p0) / max(p1 - p0, 1e-6), 0, 1)
        for k in range(3):
            out[..., k][mask] = lerp(c0[k], c1[k], t)
    return out


def save_rgb(arr, name, quality=95):
    arr = np.clip(arr, 0, 1)
    Image.fromarray((arr * 255 + 0.5).astype(np.uint8), "RGB").save(
        OUT / name, optimize=True
    )


def save_normal(height, name, strength=2.0):
    """Sobel normal map with wrapped edges."""
    gy, gx = np.gradient(height.astype(np.float32))
    nx = -gx * strength
    ny = -gy * strength
    nz = np.ones_like(nx)
    ln = np.sqrt(nx * nx + ny * ny + nz * nz)
    normal = np.stack([nx / ln, ny / ln, nz / ln], axis=-1)
    rgb = normal * 0.5 + 0.5
    save_rgb(rgb, name, quality=95)


def grain(shape, amount=0.03, seed=1):
    rng = np.random.default_rng(seed)
    return (rng.random(shape).astype(np.float32) - 0.5) * amount


# ---------------------------------------------------------------- roof tiles
def make_roof():
    size = S
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    cols, rows = 4, 4
    u = (xx / size * cols) % 1.0
    v = (yy / size * rows) % 1.0
    # barrel profile across each tile
    dome = np.sin(u * np.pi) ** 0.55
    # row overlap lip
    lip = np.exp(-((v - 0.86) / 0.055) ** 2)
    shadow = np.exp(-((v - 0.94) / 0.035) ** 2)
    base = 0.33 + 0.42 * dome
    base = base * (1.0 - 0.30 * (1 - v) * 0.25) + 0.075 * lip - 0.10 * shadow
    # per-tile variation
    tile_rng = np.random.default_rng(44)
    tv = tile_rng.normal(0, 0.035, (rows, cols)).astype(np.float32)
    ti = (np.floor(yy / size * rows).astype(int)) % rows
    tj = (np.floor(xx / size * cols).astype(int)) % cols
    base += tv[ti, tj]
    base += periodic_noise(size, 10, 2.0, 9) * 0.055
    base += grain((size, size), 0.035, 12)
    base = np.clip(base, 0.10, 0.95)
    stops = [
        (0.10, (0.16, 0.045, 0.025)),
        (0.28, (0.36, 0.105, 0.052)),
        (0.48, (0.60, 0.225, 0.115)),
        (0.68, (0.74, 0.345, 0.19)),
        (0.86, (0.82, 0.47, 0.29)),
        (1.00, (0.92, 0.62, 0.42)),
    ]
    rgb = colorize(base, stops)
    # sun-bleached flecks and dark weathering
    weather = periodic_noise(size, 14, 3.0, 31)
    m = weather > 0.86
    rgb[m] *= 0.82
    m2 = weather < 0.10
    rgb[m2] = rgb[m2] * 0.88 + np.array([0.10, 0.08, 0.055])
    save_rgb(rgb, "roof_tile.png")
    save_normal(base, "roof_tile_normal.png", 1.4)


# ------------------------------------------------------------------- plaster
def make_plaster():
    size = 768
    n1 = periodic_noise(size, 8, 2.0, 17)
    n2 = periodic_noise(size, 18, 24.0, 21)
    h = 0.55 + 0.11 * n1 + 0.035 * n2 + grain((size, size), 0.035, 23)
    h = np.clip(h, 0, 1)
    stops = [
        (0.0, (0.74, 0.69, 0.60)),
        (0.35, (0.83, 0.78, 0.69)),
        (0.65, (0.89, 0.85, 0.76)),
        (0.85, (0.93, 0.89, 0.81)),
        (1.0, (0.96, 0.93, 0.86)),
    ]
    rgb = colorize(h, stops)
    save_rgb(rgb, "plaster.png")
    save_normal(h, "plaster_normal.png", 0.35)


# ---------------------------------------------------------------------- wood
def make_wood():
    size = 768
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size
    # rings run along image Y (vertical grain)
    warp = 0.22 * np.sin(2 * np.pi * 2 * xx) + 0.10 * np.sin(2 * np.pi * 5 * yy)
    rings = 0.5 + 0.5 * np.sin(2 * np.pi * (12 * xx + 1.2 * np.sin(2 * np.pi * 2 * yy)) + warp * 5)
    fine = periodic_noise(size, 20, 32.0, 51)
    h = 0.35 + 0.38 * rings + 0.18 * fine
    h = np.clip(h, 0, 1)
    stops = [
        (0.0, (0.18, 0.085, 0.04)),
        (0.30, (0.33, 0.17, 0.085)),
        (0.55, (0.48, 0.28, 0.15)),
        (0.78, (0.60, 0.38, 0.22)),
        (1.0, (0.72, 0.50, 0.31)),
    ]
    rgb = colorize(h, stops)
    # long dark grain streaks
    streak = np.exp(-((np.sin(2 * np.pi * (xx * 18 + 0.12 * np.sin(yy * 8))) + 0.85) / 0.18) ** 2)
    rgb *= (1 - 0.18 * streak[..., None])
    save_rgb(rgb, "teak.png")
    save_normal(h, "teak_normal.png", 1.1)


# --------------------------------------------------------------------- stone
def make_stone():
    size = 768
    n = periodic_noise(size, 16, 3.0, 71)
    fine = periodic_noise(size, 24, 28.0, 73)
    h = 0.5 + 0.3 * n + 0.1 * fine + grain((size, size), 0.05, 77)
    h = np.clip(h, 0, 1)
    stops = [
        (0.0, (0.31, 0.30, 0.27)),
        (0.30, (0.48, 0.46, 0.41)),
        (0.55, (0.63, 0.61, 0.55)),
        (0.78, (0.76, 0.73, 0.66)),
        (1.0, (0.86, 0.83, 0.75)),
    ]
    rgb = colorize(h, stops)
    # hairline cracks
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size
    crack = np.abs(np.sin(2 * np.pi * (xx * 3 + 0.15 * np.sin(yy * 7))) + 0.18)
    rgb[crack < 0.012] *= 0.58
    save_rgb(rgb, "stone.png")
    save_normal(h, "stone_normal.png", 1.8)


# ------------------------------------------------------------------ pool tile
def make_pool_tile():
    size = 768
    tiles = 24
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size
    tx = (xx * tiles) % 1.0
    ty = (yy * tiles) % 1.0
    grout = np.minimum(np.minimum(tx, 1 - tx), np.minimum(ty, 1 - ty))
    teal = np.zeros((size, size, 3), np.float32)
    base = periodic_noise(size, 12, 4.0, 91)
    var = np.zeros((size, size), np.float32)
    rng = np.random.default_rng(92)
    colors = rng.uniform(-0.08, 0.08, (tiles, tiles)).astype(np.float32)
    ci = (np.floor(yy * tiles).astype(int)) % tiles
    cj = (np.floor(xx * tiles).astype(int)) % tiles
    var = colors[ci, cj]
    t = np.clip(0.5 + 0.25 * base + var, 0, 1)
    teal[..., 0] = lerp(0.10, 0.27, t)
    teal[..., 1] = lerp(0.42, 0.64, t)
    teal[..., 2] = lerp(0.43, 0.61, t)
    teal *= (1 - 0.35 * (grout < 0.035)[..., None])
    highlight = np.exp(-((grout - 0.07) / 0.04) ** 2) * 0.10
    teal += highlight[..., None]
    save_rgb(teal, "pool_tile.png")


# ---------------------------------------------------------------- linen, cane
def make_textiles():
    size = 512
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size
    weave = 0.5 + 0.5 * np.sin(2 * np.pi * xx * 96) * np.sin(2 * np.pi * yy * 96)
    n = periodic_noise(size, 10, 8.0, 101) * 0.15
    h = 0.62 + 0.12 * weave + n + grain((size, size), 0.03, 103)
    h = np.clip(h, 0, 1)
    rgb = colorize(h, [(0, (0.54, 0.49, 0.40)), (0.5, (0.77, 0.72, 0.63)), (1, (0.90, 0.86, 0.77))])
    save_rgb(rgb, "linen.png")
    save_normal(h, "linen_normal.png", 0.7)

    # rattan weave
    u = (xx * 18) % 1.0
    v = (yy * 18) % 1.0
    over = ((np.floor(xx * 18) + np.floor(yy * 18)) % 2).astype(np.float32)
    rib = 0.5 + 0.5 * np.cos(2 * np.pi * (u if True else v))
    h2 = 0.45 + 0.28 * rib + 0.12 * over + grain((size, size), 0.03, 111)
    h2 = np.clip(h2, 0, 1)
    rgb2 = colorize(h2, [(0, (0.28, 0.17, 0.08)), (0.5, (0.55, 0.38, 0.21)), (1, (0.76, 0.60, 0.38))])
    save_rgb(rgb2, "rattan.png")
    save_normal(h2, "rattan_normal.png", 1.0)


# ------------------------------------------------------------- ground / bark
def make_ground():
    size = 768
    n = periodic_noise(size, 18, 8.0, 121)
    fine = periodic_noise(size, 25, 45.0, 123)
    h = 0.5 + 0.3 * n + 0.16 * fine + grain((size, size), 0.12, 125)
    h = np.clip(h, 0, 1)
    rgb = colorize(h, [
        (0.0, (0.15, 0.22, 0.08)),
        (0.35, (0.26, 0.34, 0.12)),
        (0.60, (0.36, 0.43, 0.16)),
        (0.82, (0.46, 0.50, 0.22)),
        (1.0, (0.55, 0.56, 0.28)),
    ])
    save_rgb(rgb, "grass.png")
    save_normal(h, "grass_normal.png", 1.2)

    # gravel / decomposed granite driveway
    base_n = periodic_noise(size, 26, 60.0, 131)
    h2 = np.clip(0.5 + 0.35 * base_n + grain((size, size), 0.2, 133), 0, 1)
    rgb2 = colorize(h2, [(0, (0.40, 0.37, 0.31)), (0.5, (0.62, 0.58, 0.50)), (1, (0.79, 0.74, 0.64))])
    save_rgb(rgb2, "gravel.png")
    save_normal(h2, "gravel_normal.png", 1.8)

    # palm bark rings
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size
    rings = 0.5 + 0.5 * np.sin(2 * np.pi * yy * 28 + 0.5 * np.sin(2 * np.pi * xx * 4))
    h3 = np.clip(0.45 + 0.35 * rings + 0.08 * periodic_noise(size, 12, 30, 141), 0, 1)
    rgb3 = colorize(h3, [(0, (0.16, 0.12, 0.08)), (0.5, (0.33, 0.26, 0.17)), (1, (0.52, 0.43, 0.29))])
    save_rgb(rgb3, "palm_bark.png")
    save_normal(h3, "palm_bark_normal.png", 1.5)


# ----------------------------------------------------------- water normal map
def make_water_normal():
    size = 512
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size
    h = (
        0.5
        + 0.18 * np.sin(2 * np.pi * (3 * xx + 2 * yy) + 1.2 * np.sin(2 * np.pi * 2 * yy))
        + 0.10 * np.sin(2 * np.pi * (7 * xx - 3 * yy))
        + 0.06 * np.sin(2 * np.pi * (11 * xx + 9 * yy))
    )
    save_normal(h, "water_normal.png", 1.0)


if __name__ == "__main__":
    make_roof()
    make_plaster()
    make_wood()
    make_stone()
    make_pool_tile()
    make_textiles()
    make_ground()
    make_water_normal()
    print("Textures written to", OUT)
    for p in sorted(OUT.glob("*.png")):
        print(f"  {p.name:28s} {p.stat().st_size/1024:7.1f} KiB")
