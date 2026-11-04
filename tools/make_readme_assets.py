from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "renders"
SERIF = "/System/Library/Fonts/Supplemental/Songti.ttc"
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GEORGIA_IT = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
MONO = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size)

def tracking(draw, xy, text, fnt, fill, tracking_px=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        w = draw.textlength(ch, font=fnt)
        x += w + tracking_px

def cover():
    im = Image.open(OUT / "hero_front.png").convert("RGB")
    im = ImageOps_fit(im, (1600, 900))
    # gentle overall contrast, then a left-side cinematic gradient
    im = ImageEnhance.Contrast(im).enhance(1.04)
    grad = Image.new("L", (1600, 900), 0)
    gd = ImageDraw.Draw(grad)
    for x in range(0, 1000):
        v = int(210 * max(0, (1 - x / 1000) ** 1.35))
        gd.line([(x, 0), (x, 900)], fill=v)
    black = Image.new("RGB", im.size, (10, 16, 12))
    im = Image.composite(black, im, grad)
    d = ImageDraw.Draw(im)
    # subtle texture line
    d.rectangle([(92, 156), (148, 160)], fill=(180, 85, 45))
    tracking(d, (92, 182), "HAINAN  /  ARCHITECTURAL STUDY", font(MONO, 15), (226, 215, 196), 3)
    d.text((80, 258), "LANAI", font=font(GEORGIA, 108), fill=(248, 242, 229))
    tracking(d, (96, 402), "HAINAN / 2026", font(MONO, 15), (214, 203, 184), 4)
    d.text((96, 448), "A tropical courtyard villa, written for the Hainan light.", font=font(GEORGIA_IT, 25), fill=(214, 203, 184))
    d.text((96, 500), "Deep eaves · cross ventilation · engawa · water", font=font(GEORGIA, 18), fill=(176, 164, 145))
    d.line([(96, 560), (500, 560)], fill=(120, 108, 91), width=1)
    tracking(d, (96, 584), "26 × 31 M SITE   /   190 M²   /   3 BEDROOMS", font(MONO, 13), (190, 178, 158), 2)
    d.text((96, 780), "2026", font=font(GEORGIA, 18), fill=(160, 146, 126))
    im.save(OUT / "lanai-cover.jpg", quality=92, optimize=True, progressive=True)

def ImageOps_fit(im, size):
    from PIL import ImageOps
    return ImageOps.fit(im, size, method=Image.Resampling.LANCZOS, centering=(0.52, 0.50))

def poster():
    im = Image.open(OUT / "poster_exterior.png").convert("RGB")
    im = ImageOps_fit(im, (1600, 900))
    im = ImageEnhance.Contrast(im).enhance(1.03)
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([(0, 0), (1600, 900)], fill=(6, 12, 8, 35))
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(im)
    # bottom gradient, not a hard band
    grad = Image.new("L", (1600, 900), 0)
    gd = ImageDraw.Draw(grad)
    for y in range(560, 900):
        gd.line([(0, y), (1600, y)], fill=int(190 * ((y - 560) / 340) ** 1.3))
    im = Image.composite(Image.new("RGB", im.size, (7, 13, 9)), im, grad)
    d = ImageDraw.Draw(im)
    # play button
    cx, cy, r = 800, 400, 55
    d.ellipse([(cx-r, cy-r), (cx+r, cy+r)], outline=(245, 236, 219), width=2)
    d.polygon([(cx-15, cy-22), (cx-15, cy+22), (cx+24, cy)], fill=(245, 236, 219))
    tracking(d, (72, 760), "WATCH THE FILM  /  2K", font(MONO, 16), (245, 236, 219), 4)
    d.text((72, 800), "LANAI · HAINAN", font=font(GEORGIA, 26), fill=(245, 236, 219))
    im.save(OUT / "lanai-poster.jpg", quality=92, optimize=True, progressive=True)

def palette():
    im = Image.new("RGB", (1600, 560), (240, 233, 221))
    d = ImageDraw.Draw(im)
    d.text((72, 62), "MATERIAL PALETTE", font=font(MONO, 14), fill=(96, 87, 72))
    d.text((70, 100), "A quiet tropical warmth.", font=font(GEORGIA_IT, 34), fill=(40, 45, 36))
    swatches = [
        ("HAINAN RED CLAY", "#B4552D", "roof tile"),
        ("LIME PLASTER", "#E8DFCF", "walls"),
        ("TEAK", "#6F4A32", "joinery"),
        ("BASALT", "#7D7A70", "stone"),
        ("SAGE", "#5B6E59", "louvers"),
        ("POOL", "#2B8F92", "water"),
    ]
    x = 72
    for name, hexv, sub in swatches:
        rgb = tuple(int(hexv[i:i+2], 16) for i in (1, 3, 5))
        d.rectangle([(x, 205), (x+210, 330)], fill=rgb)
        d.text((x, 354), name, font=font(MONO, 12), fill=(54, 49, 40))
        d.text((x, 375), sub, font=font(GEORGIA_IT, 18), fill=(117, 105, 88))
        d.text((x, 412), hexv, font=font(MONO, 12), fill=(146, 131, 111))
        x += 242
    d.line([(72, 475), (1528, 475)], fill=(198, 186, 168), width=1)
    d.text((72, 496), "All finishes are procedural textures generated in Blender and packed into the glTF.", font=font(GEORGIA, 17), fill=(96, 88, 75))
    im.save(OUT / "palette.jpg", quality=94, optimize=True, progressive=True)

cover()
poster()
palette()
print("assets written")
