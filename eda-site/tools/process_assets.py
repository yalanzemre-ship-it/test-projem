"""Builds the site's image kit and brand files inside the Higgsfield sandbox.

Usage: python3 process_assets.py <raw_dir> <repo_root> <fonts_dir>
raw_dir holds the downloaded generations: board0..7.png, a0..a13.png.
"""

import os
import sys

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

RAW, ROOT, FONTS = sys.argv[1], sys.argv[2], sys.argv[3]
PUB = os.path.join(ROOT, "app/public")
IMG = os.path.join(PUB, "assets/img")
BRAND = os.path.join(PUB, "assets/brand")
REFS = os.path.join(ROOT, "refs")
for d in (IMG, BRAND, REFS):
    os.makedirs(d, exist_ok=True)

INK, BONE, ACCENT, MUTE = (21, 16, 15), (242, 233, 230), (192, 115, 107), (154, 140, 135)
XW700 = os.path.join(FONTS, "Archivo-XW700.ttf")
MONO = os.path.join(FONTS, "PlexMono-Medium.ttf")

# Reference boards -> refs/ (working artifacts, not served)
for i in range(8):
    p = os.path.join(RAW, f"board{i}.png")
    if os.path.exists(p):
        im = Image.open(p).convert("RGB")
        im.thumbnail((1600, 1600))
        im.save(os.path.join(REFS, f"board-{i + 1}.jpg"), quality=82)

PLAN = {
    0: ("hero-a", [900, 1400, 2400]),
    1: ("hero-b", [1000, 2000]),
    2: ("day-1", [1000, 2000]),
    3: ("day-2", [1000, 2000]),
    4: ("day-3", [1000, 2000]),
    5: ("day-4", [1000, 2000]),
    6: ("svc-gelin", [500, 800]),
    7: ("svc-ozel", [500, 800]),
    8: ("svc-kalici", [500, 800]),
    9: ("svc-kas", [500, 800]),
    10: ("svc-kirpik", [500, 800]),
    11: ("svc-sac", [500, 800]),
    12: ("studio", [800, 1400]),
    13: ("silk", [1000, 2000]),
}
for k, (name, widths) in PLAN.items():
    im = Image.open(os.path.join(RAW, f"a{k}.png")).convert("RGB")
    for w in widths:
        c = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        c.save(os.path.join(IMG, f"{name}-{w}.webp"), quality=78, method=6)

# Favicon set from the EY monogram (Archivo, width 125, weight 700)
f = TTFont(XW700)
gs = f.getGlyphSet()
cmap = f.getBestCmap()
parts, x = [], 0
for ch in "EY":
    g = cmap[ord(ch)]
    parts.append((g, x))
    x += gs[g].width
bp = BoundsPen(gs)
for g, ox in parts:
    gs[g].draw(TransformPen(bp, (1, 0, 0, 1, ox, 0)))
xmin, ymin, xmax, ymax = bp.bounds
W, H = xmax - xmin, ymax - ymin
sp = SVGPathPen(gs)
for g, ox in parts:
    gs[g].draw(TransformPen(sp, (1, 0, 0, -1, ox - xmin, ymax)))
d = sp.getCommands()
S = max(W, H) / (1 - 2 * 0.22)
with open(os.path.join(PUB, "favicon.svg"), "w") as fh:
    fh.write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {round(S)} {round(S)}">'
        f'<rect width="100%" height="100%" fill="#15100F"/>'
        f'<path transform="translate({round((S - W) / 2)} {round((S - H) / 2)})" fill="#F2E9E6" d="{d}"/></svg>'
    )


def icon(size, pad, rule=True):
    big = size * 4
    im = Image.new("RGB", (big, big), INK)
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(XW700, int(big * (1 - 2 * pad) * 0.62))
    bb = dr.textbbox((0, 0), "EY", font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    dr.text(((big - tw) / 2 - bb[0], (big - th) / 2 - bb[1] - big * 0.02), "EY", font=font, fill=BONE)
    if rule and size >= 64:
        y = int((big + th) / 2 + big * 0.06)
        x0 = int((big - tw) / 2)
        dr.line([(x0, y), (x0 + tw, y)], fill=ACCENT, width=max(2, big // 90))
        for k in range(11):
            xx = x0 + int(tw * k / 10)
            dr.line([(xx, y), (xx, y - (big // 16 if k % 5 == 0 else big // 28))], fill=ACCENT, width=max(2, big // 140))
    return im.resize((size, size), Image.LANCZOS)


icon(16, 0.08, False).save(os.path.join(PUB, "favicon-16.png"))
icon(32, 0.12, False).save(os.path.join(PUB, "favicon-32.png"))
icon(48, 0.1, False).save(os.path.join(PUB, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
icon(180, 0.2).save(os.path.join(PUB, "apple-touch-icon.png"))
icon(192, 0.2).save(os.path.join(PUB, "icon-192.png"))
icon(512, 0.2).save(os.path.join(PUB, "icon-512.png"))
icon(512, 0.3).save(os.path.join(PUB, "icon-maskable-512.png"))

# Brand OG card 1200x630
hero = Image.open(os.path.join(RAW, "a0.png")).convert("RGB")
w, h = 1200, 630
s = max(w / hero.width, h / hero.height)
hero = hero.resize((round(hero.width * s), round(hero.height * s)), Image.LANCZOS)
left, top = (hero.width - w) // 2, (hero.height - h) // 2
og = hero.crop((left, top, left + w, top + h))
shade = Image.new("L", (w, h))
sd = ImageDraw.Draw(shade)
for xx in range(w):
    sd.line([(xx, 0), (xx, h)], fill=int(235 * max(0, 1 - xx / (w * 0.78))))
og = Image.composite(Image.new("RGB", (w, h), INK), og, shade)
dr = ImageDraw.Draw(og)
fT = ImageFont.truetype(XW700, 78)
fM = ImageFont.truetype(MONO, 20)
dr.text((64, 56), "EDA YALANIZ MAKEUP STUDIO", font=fM, fill=BONE)
dr.text((64, 300), "Her yüz", font=fT, fill=BONE)
dr.text((64, 390), "kendi ölçüsünde.", font=fT, fill=ACCENT)
dr.line([(64, 520), (600, 520)], fill=BONE, width=1)
for k in range(55):
    xx = 64 + k * 10
    dr.line([(xx, 520), (xx, 520 - (12 if k % 5 == 0 else 6))], fill=BONE, width=1)
dr.text((64, 540), "GELİN VE KALICI MAKYAJ · NİLÜFER, BURSA", font=fM, fill=MUTE)
og.save(os.path.join(BRAND, "og.jpg"), quality=86)

print("assets ok:", len(os.listdir(IMG)), "images")
