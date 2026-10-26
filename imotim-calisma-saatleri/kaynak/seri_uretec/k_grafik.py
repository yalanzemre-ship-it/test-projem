"""Grafik/çizim temalı konseptler: iki duvar saati, mimari çizim (blueprint), güneş yayı."""

import math
from string import Template

from .temel import P, logo, tam


def t(css, **kw):
    return Template(css).substitute(**kw)


# --- İki duvar saati ----------------------------------------------------------

def kadran(saat, cap, yuz, cizgi, akrep, vurgu):
    r = cap / 2
    parca = [f'<circle cx="{r}" cy="{r}" r="{r - 8}" fill="{yuz}" stroke="{cizgi}" stroke-width="14"/>']
    for i in range(60):
        a = math.radians(i * 6)
        uzun = i % 5 == 0
        r1, r2 = r - (52 if uzun else 38), r - 26
        parca.append(f'<line x1="{r + r1 * math.sin(a):.1f}" y1="{r - r1 * math.cos(a):.1f}" x2="{r + r2 * math.sin(a):.1f}" '
                     f'y2="{r - r2 * math.cos(a):.1f}" stroke="{cizgi}" stroke-width="{7 if uzun else 2.5}" stroke-linecap="round"/>')
    for n in (12, 3, 6, 9):
        a = math.radians(n * 30)
        rr = r - 98
        parca.append(f'<text x="{r + rr * math.sin(a):.1f}" y="{r - rr * math.cos(a) + 20:.1f}" text-anchor="middle" '
                     f'font-family="Bodoni" font-weight="600" font-size="58" fill="{cizgi}">{n}</text>')

    def el(aci, uzunluk, kalinlik, renk):
        a = math.radians(aci)
        return (f'<line x1="{r - 24 * math.sin(a):.1f}" y1="{r + 24 * math.cos(a):.1f}" x2="{r + uzunluk * math.sin(a):.1f}" '
                f'y2="{r - uzunluk * math.cos(a):.1f}" stroke="{renk}" stroke-width="{kalinlik}" stroke-linecap="round"/>')
    parca.append(el((saat % 12) * 30, r * .5, 16, akrep))
    parca.append(el(0, r * .74, 10, akrep))
    parca.append(f'<circle cx="{r}" cy="{r}" r="16" fill="{vurgu}"/>')
    return (f'<svg width="{cap}" height="{cap}" viewBox="0 0 {cap} {cap}" style="filter:drop-shadow(0 20px 30px rgba(0,0,0,.25))">'
            + "".join(parca) + "</svg>")


def iki_saat(v):
    tema = [
        dict(bg="#efe6d6", fg="#1b1b1b", yuz="#ffffff", cizgi="#1b1b1b", akrep="#1b1b1b", vurgu="#8a1b2b", ince="#7a6e62"),
        dict(bg="#8a1b2b", fg="#ffffff", yuz="#efe6d6", cizgi="#3a1015", akrep="#3a1015", vurgu="#8a1b2b", ince="rgba(255,255,255,.7)"),
        dict(bg="#121110", fg="#f3ead9", yuz="#1c1a17", cizgi="#d9c39b", akrep="#f3ead9", vurgu="#d9c39b", ince="rgba(243,234,217,.6)"),
    ][v]
    css = t("""
.story { background:$bg; color:$fg; }
.logo { position:absolute; top:200px; left:50%; transform:translateX(-50%); }
.baslik { position:absolute; top:420px; left:0; right:0; text-align:center; font-family:"DMSerif"; font-size:100px; line-height:1; }
.saatler { position:absolute; top:600px; left:60px; right:60px; display:flex; justify-content:space-between; }
.saatler .k { display:flex; flex-direction:column; align-items:center; }
.saatler .ne { font-family:"Montserrat"; font-weight:700; font-size:24px; letter-spacing:.4em; padding-left:.4em; color:$ince; margin-top:34px; }
.saatler .s { font-family:"DMSerif"; font-size:110px; line-height:1; margin-top:8px; }
.alt { position:absolute; top:1330px; left:0; right:0; text-align:center; font-family:"DMSerif"; font-style:italic; font-size:64px; }
.alt small { display:block; font-family:"Montserrat"; font-style:normal; font-weight:600; font-size:24px; letter-spacing:.42em;
  padding-left:.42em; color:$ince; margin-top:22px; }
""", **tema)
    a = dict(yuz=tema["yuz"], cizgi=tema["cizgi"], akrep=tema["akrep"], vurgu=tema["vurgu"])
    govde = f"""{logo(380, tema["fg"])}
<div class="baslik">Çalışma Saatleri</div>
<div class="saatler">
  <div class="k">{kadran(10, 450, **a)}<div class="ne">AÇILIŞ</div><div class="s">10:00</div></div>
  <div class="k">{kadran(19, 450, **a)}<div class="ne">KAPANIŞ</div><div class="s">19:00</div></div>
</div>
<div class="alt">Haftanın her günü<small>PAZARTESİ – PAZAR</small></div>"""
    return css, govde


# --- Mimari çizim (blueprint) -------------------------------------------------

def blueprint(v):
    tema = [
        dict(bg="#1f4f8a", cizgi="#ffffff", ince="rgba(255,255,255,.14)", kalin="rgba(255,255,255,.28)"),
        dict(bg="#0b1626", cizgi="#7fe3ff", ince="rgba(127,227,255,.10)", kalin="rgba(127,227,255,.22)"),
        dict(bg="#efe3c8", cizgi="#5a3b22", ince="rgba(90,59,34,.10)", kalin="rgba(90,59,34,.22)"),
    ][v]
    c = tema["cizgi"]
    css = t("""
.story { background-color:$bg; color:$cizgi; font-family:"SpaceMono";
  background-image: linear-gradient($kalin 2px, transparent 2px), linear-gradient(90deg, $kalin 2px, transparent 2px),
    linear-gradient($ince 1px, transparent 1px), linear-gradient(90deg, $ince 1px, transparent 1px);
  background-size: 120px 120px, 120px 120px, 24px 24px, 24px 24px; background-position: -2px -2px; }
.logo { position:absolute; top:205px; left:80px; }
.sag-ust { position:absolute; top:212px; right:80px; text-align:right; font-weight:700; font-size:24px; line-height:1.5; letter-spacing:.1em; }
.cizim { position:absolute; top:430px; left:80px; }
.not { position:absolute; font-size:24px; letter-spacing:.08em; }
.antet { position:absolute; top:1300px; left:80px; right:80px; border:3px solid $cizgi; display:grid; grid-template-columns: 1fr 1fr; }
.antet div { border:1.5px solid $cizgi; padding:14px 18px; font-size:22px; letter-spacing:.06em; }
.antet b { display:block; font-size:34px; margin-top:4px; letter-spacing:.02em; }
.antet .tam { grid-column:1 / -1; }
""", **tema)
    # Basit bina cephesi: alçak gövde + giriş kulesi + pencere bantları, ölçü çizgileri
    cizim = f"""<svg class="cizim" width="920" height="760" viewBox="0 0 920 760" fill="none" stroke="{c}" stroke-width="3">
<rect x="40" y="170" width="840" height="230"/>
<rect x="330" y="110" width="200" height="290"/>
<line x1="40" y1="230" x2="880" y2="230"/>
{"".join(f'<rect x="{x}" y="260" width="70" height="110"/>' for x in (70, 160, 250, 570, 660, 750))}
<rect x="380" y="250" width="100" height="150"/>
<line x1="0" y1="400" x2="920" y2="400" stroke-width="4"/>
<g stroke-width="2"><line x1="40" y1="60" x2="880" y2="60"/><line x1="40" y1="45" x2="40" y2="160"/><line x1="880" y1="45" x2="880" y2="160"/>
<path d="M40 60 l18 -8 v16z M880 60 l-18 -8 v16z" fill="{c}"/></g>
<text x="460" y="44" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="24" fill="{c}" stroke="none">İMOTİM MOBİLYA AVM — ÖN CEPHE</text>
<g stroke-width="2">
<line x1="60" y1="560" x2="860" y2="560"/>
{"".join(f'<line x1="{60 + i * 800 / 9:.1f}" y1="{548 if i % 3 else 536}" x2="{60 + i * 800 / 9:.1f}" y2="{572 if i % 3 else 584}"/>' for i in range(10))}
<path d="M60 560 l22 -10 v20z M860 560 l-22 -10 v20z" fill="{c}"/></g>
<text x="60" y="640" font-family="SpaceMono" font-weight="700" font-size="56" fill="{c}" stroke="none">10:00</text>
<text x="860" y="640" text-anchor="end" font-family="SpaceMono" font-weight="700" font-size="56" fill="{c}" stroke="none">19:00</text>
<text x="460" y="520" text-anchor="middle" font-family="SpaceMono" font-weight="700" font-size="28" fill="{c}" stroke="none">HER GÜN AÇIK · 9 SAAT</text>
<text x="60" y="690" font-family="SpaceMono" font-size="22" fill="{c}" stroke="none">AÇILIŞ</text>
<text x="860" y="690" text-anchor="end" font-family="SpaceMono" font-size="22" fill="{c}" stroke="none">KAPANIŞ</text>
</svg>"""
    govde = f"""{logo(340, c)}
<div class="sag-ust">PAFTA 7/7<br>REV. HER GÜN</div>
{cizim}
<div class="antet">
  <div class="tam">PROJE<b>ÇALIŞMA SAATLERİ</b></div>
  <div>AÇILIŞ<b>10:00</b></div><div>KAPANIŞ<b>19:00</b></div>
  <div>GÜNLER<b>PZT – PAZ</b></div><div>ÖLÇEK<b>7/7</b></div>
</div>"""
    return css, govde


# --- Güneş yayı ---------------------------------------------------------------

def gunes(v):
    if v == 0:
        zemin, cx, cy, r = tam("gb"), 540, 760, 400
    elif v == 1:
        zemin, cx, cy, r = tam("yaz"), 540, 860, 420
    else:
        cx, cy, r = 540, 940, 420
        zemin = """<div class="katman" style="background:linear-gradient(180deg,#f7c59f 0%,#f4dcc0 45%,#efe6d6 70%)"></div>
<svg class="katman" width="1080" height="1920" style="position:absolute;inset:0">
<path d="M0 960 C 180 880, 330 900, 520 950 S 860 880, 1080 930 V 1920 H 0Z" fill="#c98b6b"/>
<path d="M0 1040 C 220 980, 420 1020, 640 1060 S 940 1000, 1080 1040 V 1920 H 0Z" fill="#a4573f"/>
<path d="M0 1160 C 260 1110, 520 1170, 760 1180 S 980 1140, 1080 1150 V 1920 H 0Z" fill="#8a1b2b"/></svg>"""
    # Gün içi konum: 10:00 sol uç (180°), 19:00 sağ uç (0°); güneş ~14:30'da tepede
    css = """
.ust-g { background: linear-gradient(180deg, rgba(0,0,0,.30), rgba(0,0,0,0) 30%); }
.alt-g { background: linear-gradient(0deg, rgba(0,0,0,.62), rgba(0,0,0,.25) 26%, rgba(0,0,0,0) 40%); }
.uc { position:absolute; font-family:"Montserrat"; color:#fff; text-shadow:0 2px 14px rgba(0,0,0,.35); }
.uc .s { font-weight:800; font-size:76px; line-height:1; }
.uc .n { font-weight:700; font-size:22px; letter-spacing:.35em; margin-top:8px; }
.alt { position:absolute; top:1440px; left:0; right:0; display:flex; flex-direction:column; align-items:center; color:#fff; }
.alt .k { font-family:"Fraunces"; font-style:italic; font-size:76px; margin-top:24px; text-shadow:0 2px 14px rgba(0,0,0,.35); }
"""
    if v == 2:
        css = css.replace(".uc { position:absolute; font-family:\"Montserrat\"; color:#fff;", ".uc { position:absolute; font-family:\"Montserrat\"; color:#5c111c;")
    noktalar = "".join(
        f'<circle cx="{cx + r * math.cos(math.radians(180 - i * 6)):.1f}" cy="{cy - r * math.sin(math.radians(180 - i * 6)):.1f}" r="5" fill="#fff" opacity=".9"/>'
        for i in range(31))
    gx, gy = cx, cy - r
    yay = f"""<svg class="katman" width="1080" height="1920" style="position:absolute;inset:0;overflow:visible">
<defs><radialGradient id="gunes"><stop offset="0" stop-color="#fff7d6"/><stop offset=".45" stop-color="#ffd36b"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient></defs>
{noktalar}
<circle cx="{gx}" cy="{gy}" r="120" fill="url(#gunes)"/><circle cx="{gx}" cy="{gy}" r="48" fill="#fff4cf"/>
<circle cx="{cx - r}" cy="{cy}" r="16" fill="#fff"/><circle cx="{cx + r}" cy="{cy}" r="16" fill="#fff"/></svg>"""
    govde = f"""{zemin}
<div class="katman ust-g"></div><div class="katman alt-g"></div>
{yay}
<div class="uc" style="top:{cy + 34}px;left:{cx - r - 40}px"><div class="s">10:00</div><div class="n">AÇILIŞ</div></div>
<div class="uc" style="top:{cy + 34}px;right:{1080 - cx - r - 40}px;text-align:right"><div class="s">19:00</div><div class="n">KAPANIŞ</div></div>
<div class="alt">{logo(420)}<div class="k">Haftanın her günü</div></div>"""
    return css, govde


KAVRAMLAR = [
    ("iki-duvar-saati", iki_saat, 3),
    ("mimari-cizim", blueprint, 3),
    ("gunes-yayi", gunes, 3),
]
