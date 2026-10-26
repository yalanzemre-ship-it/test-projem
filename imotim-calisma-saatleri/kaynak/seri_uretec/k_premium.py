"""Açık tema, yalnızca drone: referans paylaşımların daha işlenmiş halleri.

Konseptler: saten (ipek kıvrımlı kumaş), kağıt kesim pencere, kağıt dalgalar,
kart (yılbaşı paylaşımı dili), editoryal menü, madalyon davetiye, açık cam.
Altın detaylar SVG folyo gradyanı + kabartma (specular lighting) filtresiyle,
kağıt yüzeyler ince grenli dokuyla verilir; fotoğraflara doku/filtre uygulanmaz.
"""

from string import Template

from .temel import BINA, KISA, TAM, kirp, logo

SAAT = "10:00 – 19:00"
WEB = "imotim.com.tr"

ALTIN = [("0", "#8a6a35"), (".18", "#c9a865"), (".36", "#f6e6bd"), (".54", "#b8915a"), (".72", "#ead39f"), ("1", "#8d6a3a")]
ALTIN_CSS = "linear-gradient(100deg, " + ", ".join(f"{c} {float(o) * 100:g}%" for o, c in ALTIN) + ")"
# HTML metinlerde (açık zemin üstünde) kullanılan, okunurluk için daha koyu folyo
ALTIN_KOYU = [("0", "#76571f"), (".2", "#a9844a"), (".38", "#d9bd85"), (".56", "#957038"), (".74", "#c4a266"), ("1", "#77582a")]
ALTIN_KOYU_CSS = "linear-gradient(100deg, " + ", ".join(f"{c} {float(o) * 100:g}%" for o, c in ALTIN_KOYU) + ")"

# Tam ekran (1080x1920) fotoğrafta binanın dikey merkezi
BINA_TAM_Y = {"gb": 1027, "yaz": 1008}


def t(css, **kw):
    return Template(css).substitute(**kw)


# --- Ortak parçalar -----------------------------------------------------------

ORTAK_CSS = """
.story { font-family:"Montserrat"; color:$yazi; background:$zemin; }
.zemin-svg { position:absolute; inset:0; }
.folyo { background:%s; -webkit-background-clip:text; background-clip:text; color:transparent;
  filter: drop-shadow(0 2px 1.5px rgba(110,80,35,.28)); }
.altin-bg { background:%s; }
.etiket { display:flex; align-items:center; justify-content:center; gap:24px; font-weight:600; font-size:23px;
  letter-spacing:.42em; color:$ince; white-space:nowrap; }
.etiket span { margin-right:-.42em; }
.etiket::before, .etiket::after { content:""; width:84px; height:1.5px; background:linear-gradient(90deg, rgba(184,145,90,0), #b8915a); }
.etiket::after { transform:scaleX(-1); }
.gunler-hap { display:flex; gap:12px; justify-content:center; }
.gunler-hap span { width:104px; height:62px; border-radius:999px; display:flex; align-items:center; justify-content:center;
  background:linear-gradient(180deg, #ffffff, $hap2); color:$yazi; font-weight:600; font-size:23px;
  box-shadow: 0 8px 18px rgba(60,40,10,.10), inset 0 0 0 1.5px rgba(184,145,90,.38), inset 0 2px 0 rgba(255,255,255,.9); }
.web { font-weight:500; font-size:23px; letter-spacing:.14em; color:$ince; text-align:center; }
""" % (ALTIN_KOYU_CSS, ALTIN_CSS)

PALET = {
    "gumus": dict(zemin="#eceef1", yazi="#1c1c1e", ince="#5b5b60", hap2="#f1f1f3",
                  z1="#fcfcfd", z2="#e4e5e9", k1="#ffffff", k2="#dfe0e4", on="#f8f8f9", golge=.2,
                  katman=["#fdfdfd", "#f6f6f7", "#efeff1", "#e7e8eb", "#dfe0e4"]),
    "inci": dict(zemin="#f3f1ed", yazi="#1b1a18", ince="#5e5a54", hap2="#f5f3ef",
                 z1="#fffefc", z2="#ebe7e0", k1="#ffffff", k2="#e6e1d9", on="#fbfaf7", golge=.18,
                 katman=["#fefdfb", "#f8f5f0", "#f1ede6", "#eae4da", "#e2dbcf"]),
    "sampanya": dict(zemin="#efe5d4", yazi="#2b2118", ince="#6b5845", hap2="#f6efe3",
                     z1="#fdf9f2", z2="#eadcc5", k1="#fffaf3", k2="#e5d6bd", on="#f8f1e6", golge=.18,
                     katman=["#fdf9f2", "#f7efe2", "#f0e4d2", "#e9d9c2", "#e1cdb1"]),
    "kum": dict(zemin="#ede5d8", yazi="#2c241c", ince="#6a5d4e", hap2="#f4eee4",
                z1="#fbf7f1", z2="#e3d7c5", k1="#fdf9f3", k2="#dfd2bf", on="#f6f0e7", golge=.18,
                katman=["#fbf7f1", "#f4ede3", "#ece3d5", "#e4d8c7", "#dbcdb8"]),
}


def defs():
    """Altın folyo gradyanı, kabartma ve doku filtreleri (her sayfada bir kez)."""
    duraklar = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in ALTIN)
    return f"""<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="folyo" x1="0" y1="0" x2="1" y2=".35">{duraklar}</linearGradient>
<filter id="kabart" x="-5%" y="-20%" width="110%" height="150%" color-interpolation-filters="sRGB">
 <feGaussianBlur in="SourceAlpha" stdDeviation="1.4" result="b"/>
 <feSpecularLighting in="b" surfaceScale="2.2" specularConstant=".85" specularExponent="22" lighting-color="#ffffff" result="s">
  <feDistantLight azimuth="235" elevation="50"/></feSpecularLighting>
 <feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>
 <feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k1="0" k2="1" k3=".6" k4="0" result="p"/>
 <feDropShadow in="p" dx="0" dy="2.5" stdDeviation="2.5" flood-color="#5a3f15" flood-opacity=".28"/>
</filter>
<filter id="doku" x="0" y="0" width="100%" height="100%">
 <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" stitchTiles="stitch"/>
 <feColorMatrix type="saturate" values="0"/>
</filter>
<filter id="parla" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="parla-ince" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9"/></filter>
</defs></svg>"""


def yazi_svg(*parcalar):
    """Mutlak koordinatlı, tam sayfa yazı katmanı (el yazısı başlıklar vb.)."""
    return f'<svg class="zemin-svg" width="1080" height="1920" viewBox="0 0 1080 1920" style="overflow:visible">{"".join(parcalar)}</svg>'


def el_yazisi(metin, x, y, font, boyut, aci=-5):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{font}" font-size="{boyut}" fill="url(#folyo)" '
            f'filter="url(#kabart)" transform="rotate({aci} {x} {y - boyut * .3:.0f})">{metin}</text>')


def doku(clip_id, opaklik=.05):
    return (f'<rect width="1080" height="1920" filter="url(#doku)" clip-path="url(#{clip_id})" '
            f'style="mix-blend-mode:multiply;opacity:{opaklik}"/>')


def gunler_hap():
    return '<div class="gunler-hap">' + "".join(f"<span>{g}</span>" for g in KISA) + "</div>"


def altin_ikon(w):
    return f'<div class="logo-ikon altin-bg" style="width:{w}px"></div>'


def tam_foto_svg(k, y):
    return f'<image href="../assets/{TAM[k]}" x="0" y="{y}" width="1080" height="1920"/>'


# ============================================================================
# 1) SATEN
# ============================================================================

def saten(cfg):
    p = PALET[cfg["tema"]]
    k = cfg["foto"]
    sayfa = "M0 0 H1080 V1110 C 860 1180, 540 1080, 300 1140 C 170 1172, 70 1180, 0 1165 Z"
    on = "M0 1550 C 300 1480, 720 1600, 1080 1485 V1920 H0 Z"
    ra = "M0 0 H820 C 700 210, 470 430, 0 600 Z"
    rb = "M1080 0 V1250 C 950 1030, 860 760, 900 480 C 930 280, 1000 130, 1062 0 Z"
    g = p["golge"]
    zemin = f"""<svg class="zemin-svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs>
<linearGradient id="sz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p['z1']}"/><stop offset="1" stop-color="{p['z2']}"/></linearGradient>
<linearGradient id="sa" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="560" y2="430"><stop offset="0" stop-color="{p['k2']}"/><stop offset=".72" stop-color="{p['k1']}"/><stop offset="1" stop-color="{p['k1']}"/></linearGradient>
<linearGradient id="sb" gradientUnits="userSpaceOnUse" x1="1080" y1="0" x2="880" y2="0"><stop offset="0" stop-color="{p['k2']}"/><stop offset=".75" stop-color="{p['k1']}"/></linearGradient>
<linearGradient id="so" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p['k1']}"/><stop offset=".5" stop-color="{p['on']}"/></linearGradient>
<filter id="g-sayfa" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="18" stdDeviation="20" flood-color="#000" flood-opacity="{g * 1.5}"/></filter>
<filter id="g-serit" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="14" stdDeviation="22" flood-color="#000" flood-opacity="{g}"/></filter>
<filter id="g-on" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="-10" stdDeviation="18" flood-color="#000" flood-opacity="{g * 1.3}"/></filter>
<clipPath id="c-sayfa"><path d="{sayfa}"/></clipPath>
<clipPath id="c-ra"><path d="{ra}"/></clipPath>
<clipPath id="c-rb"><path d="{rb}"/></clipPath>
<clipPath id="c-on"><path d="{on}"/></clipPath>
<clipPath id="c-kagit"><path d="{sayfa}"/><path d="{on}"/><path d="{rb}"/></clipPath>
</defs>
{tam_foto_svg(k, cfg.get("kaydir", 310))}
<path d="{sayfa}" fill="url(#sz)" filter="url(#g-sayfa)"/>
<g clip-path="url(#c-sayfa)">
 <path d="M0 1132 C 70 1147, 170 1139, 300 1107 C 540 1047, 860 1147, 1080 1077" stroke="#fff" stroke-width="40" fill="none" filter="url(#parla-ince)" opacity=".9"/>
</g>
<path d="{ra}" fill="url(#sa)" filter="url(#g-serit)"/>
<g clip-path="url(#c-ra)">
 <path d="M-30 470 C 400 330, 620 150, 720 -20" stroke="#000" stroke-width="26" fill="none" filter="url(#parla)" opacity=".05"/>
 <path d="M-30 560 C 440 400, 680 200, 800 -20" stroke="#fff" stroke-width="50" fill="none" filter="url(#parla)" opacity=".9"/>
</g>
<path d="{rb}" fill="url(#sb)" filter="url(#g-serit)"/>
<g clip-path="url(#c-rb)">
 <path d="M1110 -20 C 1050 140, 1000 300, 990 480 C 975 760, 1030 1000, 1110 1180" stroke="#000" stroke-width="24" fill="none" filter="url(#parla)" opacity=".05"/>
 <path d="M1090 -20 C 1025 130, 960 290, 935 480 C 905 760, 985 1030, 1100 1220" stroke="#fff" stroke-width="44" fill="none" filter="url(#parla)" opacity=".9"/>
</g>
<path d="{on}" fill="url(#so)" filter="url(#g-on)"/>
<g clip-path="url(#c-on)">
 <path d="M0 1574 C 300 1504, 720 1624, 1080 1509" stroke="#fff" stroke-width="34" fill="none" filter="url(#parla-ince)" opacity=".95"/>
</g>
{doku("c-kagit")}
</svg>"""

    ince, script, h1, h2 = cfg["baslik"]
    if cfg.get("icerik") == "seridi":
        icerik = f'<div class="buyuk folyo">{SAAT}</div><div style="height:30px"></div>{gunler_hap()}'
    else:
        icerik = '<div class="satirlar">' + "".join(
            f'<div class="satir"><span class="hap">{a}</span><span class="dik"></span><span class="sag">{SAAT}</span></div>'
            for a in ("PZT – CUMA", "CUMARTESİ", "PAZAR")) + "</div>"
    css = t(ORTAK_CSS, **p) + t("""
.ince { position:absolute; top:168px; left:0; right:0; text-align:center; font-weight:200; font-size:150px; line-height:1; }
.ayrac { position:absolute; top:500px; left:0; right:0; display:flex; align-items:center; justify-content:center; gap:28px; }
.ayrac i { width:130px; height:1.5px; background:linear-gradient(90deg, rgba(184,145,90,0), #b8915a); }
.ayrac i:last-child { transform:scaleX(-1); }
.blok { position:absolute; top:564px; left:0; right:0; display:flex; flex-direction:column; align-items:center; }
.h1 { font-weight:500; font-size:44px; letter-spacing:.08em; }
.h2 { font-weight:300; font-size:30px; letter-spacing:.5em; margin-right:-.5em; margin-top:10px; color:$ince; }
.satirlar { margin-top:40px; display:flex; flex-direction:column; gap:16px; }
.satir { display:flex; align-items:center; }
.hap { width:296px; height:74px; border-radius:999px; display:flex; align-items:center; justify-content:center;
  background:linear-gradient(180deg, #ffffff, $hap2); font-weight:500; font-size:27px; letter-spacing:.09em;
  box-shadow: 0 10px 22px rgba(60,40,10,.11), inset 0 0 0 1.5px rgba(184,145,90,.38), inset 0 2px 0 rgba(255,255,255,.9); }
.dik { width:1.5px; height:54px; background:linear-gradient(180deg, rgba(184,145,90,0), #b8915a, rgba(184,145,90,0)); margin:0 34px; }
.sag { width:320px; font-weight:600; font-size:33px; letter-spacing:.04em; }
.buyuk { margin-top:34px; font-weight:300; font-size:104px; line-height:1.05; letter-spacing:-.01em; }
.not { margin-top:26px; text-align:center; font-style:italic; font-size:27px; line-height:1.45; color:$ince; }
.not b { font-weight:700; color:$yazi; }
.alt { position:absolute; top:1594px; left:0; right:0; display:flex; flex-direction:column; align-items:center; gap:12px; }
""", **p)
    govde = f"""{defs()}{zemin}
<div class="ince">{ince}</div>
{yazi_svg(el_yazisi(script, 560, cfg.get("script_y", 432), cfg["font"], cfg["boyut"]))}
<div class="ayrac"><i></i>{altin_ikon(70)}<i></i></div>
<div class="blok"><div class="h1">{h1}</div><div class="h2">{h2}</div>{icerik}
<div class="not"><b>Pazar dahil</b> her gün kapılarımızı siz değerli<br>misafirlerimize açıyoruz.</div></div>
<div class="alt">{logo(300, p["yazi"])}<div class="web">{WEB}</div></div>"""
    return css, govde


# ============================================================================
# 2) KAĞIT KESİM PENCERE
# ============================================================================

def delik(sekil, x0, y0, x1, y1):
    r = (x1 - x0) / 2
    if sekil == "kapsul":
        return f"M{x0} {y0 + r} A{r} {r} 0 0 1 {x1} {y0 + r} V{y1 - r} A{r} {r} 0 0 1 {x0} {y1 - r} Z"
    return f"M{x0} {y1} V{y0 + r} A{r} {r} 0 0 1 {x1} {y0 + r} V{y1} Z"


def pencere(cfg):
    p = PALET[cfg["tema"]]
    k = cfg["foto"]
    sekil = cfg["sekil"]
    x0, y0, x1, y1 = (120, 350, 960, 1240) if sekil == "kemer" else (170, 340, 910, 1250)
    n, adim = 5, 24
    ic = (x0 + adim * (n - 1), y0 + adim * (n - 1), x1 - adim * (n - 1), y1 - adim * (n - 1))
    fw, fh = ic[2] - ic[0], ic[3] - ic[1]
    katmanlar = ""
    for i in reversed(range(n)):
        d = i * adim
        katmanlar += (f'<path d="M0 0 H1080 V1920 H0 Z {delik(sekil, x0 + d, y0 + d, x1 - d, y1 - d)}" fill="{p["katman"][i]}" '
                      f'fill-rule="evenodd" filter="url(#g-katman)"/>')
    en_ic = f"M0 0 H1080 V1920 H0 Z {delik(sekil, *ic)}"
    zemin = f"""<svg class="zemin-svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs>
<filter id="g-katman" x="-5%" y="-5%" width="110%" height="110%"><feDropShadow dx="0" dy="12" stdDeviation="15" flood-color="#3a2a10" flood-opacity=".2"/></filter>
<clipPath id="c-kagit"><path d="{en_ic}" clip-rule="evenodd"/></clipPath>
</defs>
<image href="{kirp(k, fw, fh, *BINA[k], s=cfg.get("s", .78))}" x="{ic[0]}" y="{ic[1]}" width="{fw}" height="{fh}"/>
{katmanlar}
<path d="{delik(sekil, x0, y0, x1, y1)}" fill="none" stroke="url(#folyo)" stroke-width="2.5"/>
{doku("c-kagit")}
</svg>"""
    css = t(ORTAK_CSS, **p) + """
.logo-u { position:absolute; top:186px; left:50%; transform:translateX(-50%); }
.alt { position:absolute; top:1282px; left:0; right:0; display:flex; flex-direction:column; align-items:center; }
.saat { margin-top:162px; font-weight:300; font-size:94px; line-height:1; letter-spacing:-.01em; }
.saat b { font-weight:300; }
.alt .gunler-hap { margin-top:32px; }
.alt .web { margin-top:34px; }
"""
    govde = f"""{defs()}{zemin}
<div class="logo-u">{logo(300, p["yazi"])}</div>
<div class="alt"><div class="etiket"><span>ÇALIŞMA SAATLERİ</span></div>
<div class="saat">10:00 <b class="folyo">–</b> 19:00</div>{gunler_hap()}<div class="web">{WEB}</div></div>
{yazi_svg(el_yazisi(cfg["script"], 540, 1420, cfg["font"], cfg["boyut"], aci=-4))}"""
    return css, govde


# ============================================================================
# 3) KAĞIT DALGALAR
# ============================================================================

DALGALAR = [
    "M0 1010 C 240 930, 520 1060, 760 990 S 1000 930, 1080 960 V1920 H0 Z",
    "M0 1080 C 300 1160, 560 1020, 820 1090 S 1020 1130, 1080 1100 V1920 H0 Z",
    "M0 1160 C 220 1100, 480 1210, 740 1150 S 980 1090, 1080 1140 V1920 H0 Z",
    "M0 1230 C 260 1300, 600 1170, 860 1240 S 1040 1260, 1080 1240 V1920 H0 Z",
    "M0 1310 C 300 1250, 640 1340, 1080 1270 V1920 H0 Z",
]


def dalga(cfg):
    p = PALET[cfg["tema"]]
    k = cfg["foto"]
    renkler = list(reversed(p["katman"]))  # arkadan öne: koyudan açığa
    katmanlar = "".join(f'<path d="{d}" fill="{renkler[i]}" filter="url(#g-dalga)"/>' for i, d in enumerate(DALGALAR))
    zemin = f"""<svg class="zemin-svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs>
<linearGradient id="ust-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".32"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
<filter id="g-dalga" x="-5%" y="-10%" width="110%" height="120%"><feDropShadow dx="0" dy="-6" stdDeviation="16" flood-color="#2a1d08" flood-opacity=".24"/></filter>
<clipPath id="c-kagit"><path d="{DALGALAR[0]}"/></clipPath>
</defs>
{tam_foto_svg(k, 697 - BINA_TAM_Y[k])}
<rect width="1080" height="440" fill="url(#ust-g)"/>
{katmanlar}
<path d="{DALGALAR[-1]}" fill="none" stroke="url(#folyo)" stroke-width="2" transform="translate(0 1)" opacity=".8"/>
{doku("c-kagit")}
</svg>"""
    css = t(ORTAK_CSS, **p) + """
.logo-u { position:absolute; top:200px; left:50%; transform:translateX(-50%); filter: drop-shadow(0 4px 16px rgba(0,0,0,.3)); }
.alt { position:absolute; top:1352px; left:0; right:0; display:flex; flex-direction:column; align-items:center; }
.saat { margin-top:152px; font-weight:300; font-size:96px; line-height:1; letter-spacing:-.01em; }
.saat b { font-weight:300; }
.alt .web { margin-top:30px; }
"""
    govde = f"""{defs()}{zemin}
<div class="logo-u">{logo(400)}</div>
<div class="alt"><div class="etiket"><span>{cfg["etiket"]}</span></div><div class="saat">10:00 <b class="folyo">–</b> 19:00</div>
<div class="web">PAZARTESİ – PAZAR · {WEB}</div></div>
{yazi_svg(el_yazisi(cfg["script"], 540, 1484, cfg["font"], cfg["boyut"], aci=-4))}"""
    return css, govde


# ============================================================================
# 4) KART (yılbaşı paylaşımı dili)
# ============================================================================

def kart(cfg):
    p = PALET[cfg["tema"]]
    k = cfg["foto"]
    halkalar = ""
    for i, (rx, ry) in enumerate(((1180, 1380), (1000, 1180), (820, 980), (650, 780))):
        cx, cy = 760 + i * 60, 760 + i * 80
        dolgu = "url(#h1)" if i % 2 == 0 else "url(#h2)"
        halkalar += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{dolgu}" filter="url(#g-halka)"/>'
                     f'<ellipse cx="{cx}" cy="{cy}" rx="{rx - 26}" ry="{ry - 26}" fill="none" stroke="#fff" stroke-width="22" '
                     f'opacity=".75" filter="url(#parla)"/>')
    zemin = f"""<svg class="zemin-svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs>
<linearGradient id="h1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p['k1']}"/><stop offset="1" stop-color="{p['k2']}"/></linearGradient>
<linearGradient id="h2" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p['z1']}"/><stop offset="1" stop-color="{p['z2']}"/></linearGradient>
<filter id="g-halka" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="0" stdDeviation="26" flood-color="#2a1d08" flood-opacity="{p['golge'] * .8}"/></filter>
<clipPath id="c-kagit"><rect width="1080" height="1920"/></clipPath>
</defs>
<rect width="1080" height="1920" fill="{p['zemin']}"/>
{halkalar}
<ellipse cx="300" cy="1900" rx="760" ry="560" fill="{p['zemin']}" filter="url(#g-halka)"/>
{doku("c-kagit", .045)}
</svg>"""
    hafta_sonu = cfg.get("metin") == "hafta-sonu"
    if hafta_sonu:
        metin = ('<div class="s1">Hafta sonu da</div><div class="s2 folyo" style="font-size:150px">açığız!</div>'
                 '<div class="cizgi altin-bg"></div><div class="p">Cumartesi ve Pazar dahil her gün<br>10:00 – 19:00 arası kapılarımız açık.</div>')
    else:
        metin = (f'<div class="s1">AVM\'miz her gün</div><div class="s2 folyo">{SAAT}</div><div class="s3">arası açıktır.</div>'
                 '<div class="cizgi altin-bg"></div><div class="p">Pazartesi\'den Pazar\'a, haftanın her günü<br>sizleri ağırlamaktan mutluluk duyarız.</div>')
    css = t(ORTAK_CSS, **p) + t("""
.kart { position:absolute; top:290px; left:96px; width:888px; height:1100px; border-radius:50px;
  background:linear-gradient(180deg, #ffffff, $hap2); box-shadow: 0 40px 90px rgba(50,35,10,.18), inset 0 0 0 1.5px rgba(255,255,255,.9); }
.kart::after { content:""; position:absolute; inset:16px; border-radius:38px; box-shadow: inset 0 0 0 1px rgba(184,145,90,.32); }
.metin { position:absolute; top:348px; left:136px; right:136px; display:flex; flex-direction:column; align-items:center; text-align:center; }
.metin .etiket { margin-top:20px; font-size:21px; }
.s1 { margin-top:34px; font-weight:700; font-size:68px; line-height:1.08; letter-spacing:-.01em; }
.s2 { font-weight:800; font-size:110px; line-height:1.1; letter-spacing:-.02em; }
.s3 { font-weight:700; font-size:68px; line-height:1.08; color:$ince; }
.cizgi { width:96px; height:4px; border-radius:2px; margin:28px 0 26px; }
.p { font-weight:500; font-size:33px; line-height:1.4; color:$ince; }
.foto-k { position:absolute; top:880px; left:96px; width:984px; height:700px;
  -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000 34%), radial-gradient(ellipse 128% 152% at 100% 0%, #000 69.6%, transparent 70%);
  -webkit-mask-composite: source-in; mask-composite: intersect; }
.logo-a { position:absolute; top:1610px; left:50%; transform:translateX(-50%); }
""", **p)
    govde = f"""{defs()}{zemin}
<div class="kart"></div>
<div class="metin">{altin_ikon(64)}<div class="etiket"><span>ÇALIŞMA SAATLERİ</span></div>{metin}</div>
<div class="foto-k"><img src="{kirp(k, 984, 700, *BINA[k])}" width="984" height="700" style="display:block" alt=""></div>
<div class="logo-a">{logo(330, p["yazi"])}</div>"""
    return css, govde


# ============================================================================
# 5) EDİTORYAL MENÜ
# ============================================================================

def menu(cfg):
    p = PALET[cfg["tema"]]
    k = cfg["foto"]
    y = 520 - BINA_TAM_Y[k]
    css = t(ORTAK_CSS, **p) + t("""
.foto-u { position:absolute; inset:0; -webkit-mask-image: linear-gradient(180deg, #000 0, #000 640px, transparent 900px); }
.foto-u img { position:absolute; left:0; top:${y}px; }
.ust-g { position:absolute; left:0; right:0; top:0; height:420px; background:linear-gradient(180deg, rgba(0,0,0,.3), transparent); }
.logo-u { position:absolute; top:196px; left:50%; transform:translateX(-50%); filter: drop-shadow(0 4px 16px rgba(0,0,0,.3)); }
.baslik { position:absolute; top:868px; left:0; right:0; text-align:center; font-family:"Bodoni"; line-height:.98; }
.baslik .a { font-weight:500; font-size:138px; letter-spacing:-.01em; }
.baslik .b { font-style:italic; font-weight:500; font-size:138px; padding:0 20px; }
.sus { position:absolute; top:1184px; left:0; right:0; display:flex; align-items:center; justify-content:center; gap:22px; }
.sus i { width:150px; height:1.5px; background:linear-gradient(90deg, rgba(184,145,90,0), #b8915a); }
.sus i:last-child { transform:scaleX(-1); }
.sus b { font-size:22px; }
.tablo { position:absolute; top:1236px; left:110px; right:110px; }
.tablo .s { display:flex; align-items:baseline; height:78px; }
.tablo .g { font-family:"Bodoni"; font-style:italic; font-size:44px; }
.tablo .n { flex:1; margin:0 18px; border-bottom:3px dotted rgba(184,145,90,.7); transform:translateY(-10px); }
.tablo .z { font-weight:500; font-size:33px; letter-spacing:.03em; }
.not { position:absolute; top:1490px; left:0; right:0; text-align:center; font-family:"Bodoni"; font-style:italic; font-size:34px; color:$ince; }
.alt { position:absolute; top:1568px; left:0; right:0; display:flex; flex-direction:column; align-items:center; gap:12px; }
""", y=y, **p)
    satirlar = "".join(f'<div class="s"><span class="g">{g}</span><span class="n"></span><span class="z">{SAAT}</span></div>'
                       for g in ("Pazartesi – Cuma", "Cumartesi", "Pazar"))
    zemin = f"""<svg class="zemin-svg" width="1080" height="1920"><defs><clipPath id="c-kagit"><rect y="700" width="1080" height="1220"/></clipPath></defs>
{doku("c-kagit", .045)}</svg>"""
    govde = f"""{defs()}
<div class="foto-u"><img src="../assets/{TAM[k]}" width="1080" height="1920" alt=""></div>{zemin}
<div class="ust-g"></div>
<div class="logo-u">{logo(380)}</div>
<div class="baslik"><div class="a">Çalışma</div><div class="b folyo">Saatleri</div></div>
<div class="sus"><i></i><b class="folyo">✦</b><i></i></div>
<div class="tablo">{satirlar}</div>
<div class="not">Haftanın her günü sizleri bekliyoruz.</div>
<div class="alt">{logo(290, p["yazi"])}<div class="web">{WEB}</div></div>"""
    return css, govde


# ============================================================================
# 6) MADALYON DAVETİYE
# ============================================================================

def madalyon(cfg):
    p = PALET[cfg["tema"]]
    k = cfg["foto"]
    cx, cy, r = 540, 720, 280
    yazi = "İMOTİM MOBİLYA AVM  ✦  HAFTANIN HER GÜNÜ AÇIK  ✦  "
    cerceve = f"""<svg class="zemin-svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs>
<radialGradient id="vinyet" cx=".5" cy=".42" r=".75"><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#7a5a2a" stop-opacity=".12"/></radialGradient>
<filter id="g-mad" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#3a2a10" flood-opacity=".25"/></filter>
<clipPath id="c-kagit"><rect width="1080" height="1920"/></clipPath>
<clipPath id="c-daire"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
<path id="yazi-yolu" d="M{cx} {cy} m-{r + 52} 0 a{r + 52} {r + 52} 0 1 1 {2 * (r + 52)} 0 a{r + 52} {r + 52} 0 1 1 -{2 * (r + 52)} 0"/>
</defs>
{doku("c-kagit", .045)}
<rect width="1080" height="1920" fill="url(#vinyet)"/>
<rect x="56" y="56" width="968" height="1808" fill="none" stroke="url(#folyo)" stroke-width="3"/>
<rect x="70" y="70" width="940" height="1780" fill="none" stroke="url(#folyo)" stroke-width="1.2" opacity=".8"/>
<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="#fff" filter="url(#g-mad)"/>
<image href="{kirp(k, 2 * r, 2 * r, *BINA[k], s=.72)}" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" clip-path="url(#c-daire)"/>
<circle cx="{cx}" cy="{cy}" r="{r + 2}" fill="none" stroke="url(#folyo)" stroke-width="9" filter="url(#kabart)"/>
<circle cx="{cx}" cy="{cy}" r="{r + 20}" fill="none" stroke="url(#folyo)" stroke-width="1.5"/>
<circle cx="{cx}" cy="{cy}" r="{r + 86}" fill="none" stroke="url(#folyo)" stroke-width="1.5"/>
<text font-family="Montserrat" font-weight="600" font-size="22" letter-spacing="5" fill="url(#folyo)">
<textPath href="#yazi-yolu" textLength="{2 * 3.14159 * (r + 52) - 30:.0f}" lengthAdjust="spacing">{yazi * 2}</textPath></text>
</svg>"""
    css = t(ORTAK_CSS, **p) + """
.logo-u { position:absolute; top:176px; left:50%; transform:translateX(-50%); }
.alt { position:absolute; top:1350px; left:0; right:0; display:flex; flex-direction:column; align-items:center; }
.saat { margin-top:26px; font-weight:300; font-size:96px; line-height:1; letter-spacing:-.01em; }
.saat b { font-weight:300; }
.alt .gunler-hap { margin-top:32px; }
.alt .web { margin-top:40px; }
"""
    css = css.replace("$ince", p["ince"])
    govde = f"""{defs()}{cerceve}
<div class="logo-u">{logo(250, p["yazi"])}</div>
{yazi_svg(el_yazisi(cfg["script"], 540, 1272, cfg["font"], cfg["boyut"], aci=-4))}
<div class="alt"><div class="etiket"><span>ÇALIŞMA SAATLERİ</span></div><div class="saat">10:00 <b class="folyo">–</b> 19:00</div>
{gunler_hap()}<div class="web">{WEB}</div></div>"""
    return css, govde


# ============================================================================
# 7) AÇIK CAM
# ============================================================================

def cam(cfg):
    p = PALET[cfg["tema"]]
    k = cfg["foto"]
    css = t(ORTAK_CSS, **p) + t("""
.ust-g { position:absolute; left:0; right:0; top:0; height:760px; background:linear-gradient(180deg, rgba(10,20,40,.34), rgba(10,20,40,0)); }
.logo-u { position:absolute; top:196px; left:50%; transform:translateX(-50%); filter: drop-shadow(0 4px 16px rgba(0,0,0,.3)); }
.gok { position:absolute; top:400px; left:0; right:0; text-align:center; color:#fff; }
.gok .a { font-weight:200; font-size:118px; line-height:1; text-shadow:0 4px 24px rgba(0,0,0,.28); }
.kart { position:absolute; top:1196px; left:64px; width:952px; padding:34px 60px 30px; border-radius:46px;
  background:linear-gradient(180deg, rgba(255,255,255,.78), rgba(255,255,255,.66));
  backdrop-filter: blur(26px) saturate(1.35); -webkit-backdrop-filter: blur(26px) saturate(1.35);
  box-shadow: 0 30px 70px rgba(0,0,0,.28), inset 0 0 0 1.5px rgba(255,255,255,.95); }
.kart .ust { display:flex; align-items:center; justify-content:space-between; }
.kart .ust .ne { font-weight:600; font-size:22px; letter-spacing:.34em; color:$ince; }
.kart .ust .acik { display:flex; align-items:center; gap:12px; font-weight:700; font-size:22px; letter-spacing:.2em; color:#1d7a45; }
.kart .ust .acik i { width:12px; height:12px; border-radius:50%; background:#2fb463; box-shadow:0 0 0 5px rgba(47,180,99,.18); }
.kart .buyuk { margin-top:10px; font-weight:700; font-size:104px; line-height:1.1; letter-spacing:-.02em; }
.kart .s { display:flex; justify-content:space-between; align-items:center; height:70px; border-top:1.5px solid rgba(120,95,50,.16);
  font-size:31px; }
.kart .s .g { font-weight:600; }
.kart .s .z { font-weight:500; color:$ince; }
""", **p)
    satirlar = "".join(f'<div class="s"><span class="g">{g}</span><span class="z">{SAAT}</span></div>'
                       for g in ("Pazartesi – Cuma", "Cumartesi", "Pazar"))
    govde = f"""{defs()}<img class="foto" src="../assets/{TAM[k]}" width="1080" height="1920" alt="">
<div class="ust-g"></div>
<div class="logo-u">{logo(380)}</div>
<div class="gok"><div class="a">Çalışma</div></div>
{yazi_svg(f'<g style="filter:drop-shadow(0 3px 10px rgba(0,0,0,.25))">' + el_yazisi("Saatleri", 570, 660, cfg["font"], cfg["boyut"]) + "</g>")}
<div class="kart">
  <div class="ust"><span class="ne">HAFTANIN HER GÜNÜ</span><span class="acik"><i></i>AÇIK</span></div>
  <div class="buyuk folyo">{SAAT}</div>
  {satirlar}
</div>"""
    return css, govde


V = dict
VARYASYONLAR = [
    ("saten-gumus", saten, V(tema="gumus", foto="yaz", font="MsMadi", boyut=240,
                             baslik=("Çalışma", "Saatleri", "HAFTANIN HER GÜNÜ", "AÇIĞIZ"))),
    ("saten-sampanya", saten, V(tema="sampanya", foto="gb", font="Allison", boyut=220, script_y=414, icerik="seridi",
                                baslik=("Her Gün", "Açığız", "ÇALIŞMA SAATLERİ", "PAZARTESİ – PAZAR"))),
    ("kagit-kemer", pencere, V(tema="inci", foto="yaz", sekil="kemer", script="Her gün açığız", font="MsMadi", boyut=132)),
    ("kagit-kapsul", pencere, V(tema="sampanya", foto="gb", sekil="kapsul", script="Sizi bekliyoruz", font="Allison", boyut=150)),
    ("kagit-dalga-gumus", dalga, V(tema="gumus", foto="yaz", etiket="ÇALIŞMA SAATLERİ", script="Haftanın her günü", font="MsMadi", boyut=124)),
    ("kagit-dalga-kum", dalga, V(tema="kum", foto="gb", etiket="HER GÜN AÇIĞIZ", script="Çalışma Saatleri", font="Allison", boyut=150)),
    ("kart-inci", kart, V(tema="inci", foto="yaz")),
    ("kart-sampanya-hafta-sonu", kart, V(tema="sampanya", foto="gb", metin="hafta-sonu")),
    ("menu-inci", menu, V(tema="inci", foto="yaz")),
    ("menu-sampanya", menu, V(tema="sampanya", foto="gb")),
    ("madalyon-inci", madalyon, V(tema="inci", foto="yaz", script="Her gün açığız", font="MsMadi", boyut=140)),
    ("madalyon-kum", madalyon, V(tema="kum", foto="gb", script="Sizi bekliyoruz", font="Corinthia", boyut=150)),
    ("acik-cam-yaz", cam, V(tema="gumus", foto="yaz", font="MsMadi", boyut=230)),
    ("acik-cam-gunbatimi", cam, V(tema="sampanya", foto="gb", font="Allison", boyut=250)),
]
