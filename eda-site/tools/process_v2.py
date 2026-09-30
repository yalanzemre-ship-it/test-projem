"""Light-theme asset pass, run inside the Higgsfield sandbox.

Usage: python3 process_v2.py <assets.json> <repo_root> <fonts_dir>
assets.json maps an output name to {"url": ..., "widths": [...]}; every listed
image is downloaded and written as app/public/assets/img/<name>-<w>.webp.
Also rebuilds the favicon set (light, no ruler) and the brand OG card from hero-a.
"""

import io
import json
import os
import sys
import urllib.request

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

MANIFEST, ROOT, FONTS = sys.argv[1], sys.argv[2], sys.argv[3]
PUB = os.path.join(ROOT, "app/public")
IMG = os.path.join(PUB, "assets/img")
BRAND = os.path.join(PUB, "assets/brand")
os.makedirs(IMG, exist_ok=True)
os.makedirs(BRAND, exist_ok=True)

BG, FG, ACCENT, MUTE = (247, 241, 239), (28, 22, 20), (156, 84, 78), (107, 95, 90)
XW700 = os.path.join(FONTS, "Archivo-XW700.ttf")
MONO = os.path.join(FONTS, "PlexMono-Medium.ttf")

with open(MANIFEST) as fh:
    assets = json.load(fh)
for name, spec in assets.items():
    raw = urllib.request.urlopen(spec["url"]).read()
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    for w in spec["widths"]:
        c = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        c.save(os.path.join(IMG, f"{name}-{w}.webp"), quality=80, method=6)
    print(name, im.size)

# favicon set: ink "EY" on the blush ground
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
S = max(W, H) / (1 - 2 * 0.22)
with open(os.path.join(PUB, "favicon.svg"), "w") as fh:
    fh.write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {round(S)} {round(S)}">'
        f'<rect width="100%" height="100%" fill="#F7F1EF"/>'
        f'<path transform="translate({round((S - W) / 2)} {round((S - H) / 2)})" fill="#1C1614" d="{sp.getCommands()}"/></svg>'
    )


def icon(size, pad):
    big = size * 4
    im = Image.new("RGB", (big, big), BG)
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(XW700, int(big * (1 - 2 * pad) * 0.62))
    bb = dr.textbbox((0, 0), "EY", font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    dr.text(((big - tw) / 2 - bb[0], (big - th) / 2 - bb[1]), "EY", font=font, fill=FG)
    return im.resize((size, size), Image.LANCZOS)


icon(16, 0.08).save(os.path.join(PUB, "favicon-16.png"))
icon(32, 0.12).save(os.path.join(PUB, "favicon-32.png"))
icon(48, 0.1).save(os.path.join(PUB, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
icon(180, 0.2).save(os.path.join(PUB, "apple-touch-icon.png"))
icon(192, 0.2).save(os.path.join(PUB, "icon-192.png"))
icon(512, 0.2).save(os.path.join(PUB, "icon-512.png"))
icon(512, 0.3).save(os.path.join(PUB, "icon-maskable-512.png"))

# brand OG card 1200x630 from the current hero
hero = Image.open(os.path.join(IMG, "hero-a-2400.webp")).convert("RGB")
w, h = 1200, 630
s = max(w / hero.width, h / hero.height)
hero = hero.resize((round(hero.width * s), round(hero.height * s)), Image.LANCZOS)
left, top = (hero.width - w) // 2, (hero.height - h) // 2
og = hero.crop((left, top, left + w, top + h))
shade = Image.new("L", (w, h))
sd = ImageDraw.Draw(shade)
for xx in range(w):
    sd.line([(xx, 0), (xx, h)], fill=int(240 * max(0, 1 - xx / (w * 0.72))))
og = Image.composite(Image.new("RGB", (w, h), BG), og, shade)
dr = ImageDraw.Draw(og)
fT = ImageFont.truetype(XW700, 78)
fM = ImageFont.truetype(MONO, 20)
dr.text((64, 56), "EDA YALANIZ MAKEUP STUDIO", font=fM, fill=FG)
dr.text((64, 300), "Her yüz", font=fT, fill=FG)
dr.text((64, 390), "kendi ölçüsünde.", font=fT, fill=ACCENT)
dr.text((64, 540), "GELİN VE KALICI MAKYAJ · NİLÜFER, BURSA", font=fM, fill=MUTE)
og.save(os.path.join(BRAND, "og.jpg"), quality=86)
print("brand ok")
