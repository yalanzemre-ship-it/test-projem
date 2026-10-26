"""Müşterinin önceki paylaşımlarından (bayram ve yılbaşı duyuruları) türetilen iki tasarım ailesi.

ipek: açık/ipeksi kıvrımlı zemin, ince yazı + el yazısı başlık, hap şeklinde gün
      etiketleri, dalga maskeli bina fotoğrafı, altta logo ve web adresi.
kart: koyu girdap desenli zemin, açık renk kart, karttan taşan drone fotoğrafı.
"""

from string import Template

from .temel import BINA, TAM, kirp, logo

SAAT = "10:00 – 19:00"
WEB = "imotim.com.tr"


def t(css, **kw):
    return Template(css).substitute(**kw)


# ============================================================================
# İPEK AİLESİ
# ============================================================================

IPEK_TEMA = {
    "gumus": dict(z1="#f8f8f9", z2="#dfe0e3", k1="#ffffff", k2="#e9eaec", golge=".16", yazi="#1c1c1c", ince="#4d4d4d",
                  a1="#9f7b47", a2="#e6d2a6", a3="#8f6c3c", cip1="#ffffff", cip2="#efefef", cip_y="#2a2a2a", cip_k="rgba(0,0,0,.04)",
                  cizgi="#8f8f8f", logo="#161616", dalga="#f6f6f7"),
    "sampanya": dict(z1="#f8f2e8", z2="#e4d5bd", k1="#fffaf2", k2="#efe2cd", golge=".16", yazi="#2b2118", ince="#5e4c3c",
                     a1="#9c7440", a2="#e9d2a2", a3="#86612f", cip1="#fffdf8", cip2="#f2e8d8", cip_y="#3a2c1f", cip_k="rgba(80,50,20,.06)",
                     cizgi="#a08a72", logo="#2b2118", dalga="#f6efe3"),
    "bordo": dict(z1="#7d1828", z2="#430a14", k1="#9e2539", k2="#5e0f1c", golge=".35", yazi="#ffffff", ince="rgba(255,255,255,.78)",
                  a1="#c9a76a", a2="#fff1d6", a3="#b8925a", cip1="rgba(255,255,255,.16)", cip2="rgba(255,255,255,.06)", cip_y="#ffffff",
                  cip_k="rgba(255,255,255,.35)", cizgi="rgba(255,255,255,.5)", logo="#ffffff", dalga="#4f0d18"),
    "gece": dict(z1="#18305a", z2="#09152a", k1="#244677", k2="#0f2140", golge=".35", yazi="#ffffff", ince="rgba(255,255,255,.78)",
                 a1="#c9a76a", a2="#fff1d6", a3="#b8925a", cip1="rgba(255,255,255,.14)", cip2="rgba(255,255,255,.05)", cip_y="#ffffff",
                 cip_k="rgba(255,255,255,.3)", cizgi="rgba(255,255,255,.5)", logo="#ffffff", dalga="#0b1a33"),
}

BASLIKLAR = {
    "calisma": ("Çalışma", "Saatleri", "HAFTANIN HER GÜNÜ", "AÇIĞIZ"),
    "her-gun": ("Her Gün", "Açığız", "ÇALIŞMA SAATLERİ", "PAZARTESİ – PAZAR"),
    "hafta-sonu": ("Hafta Sonu", "da açığız", "CUMARTESİ & PAZAR", "ÇALIŞMA SAATLERİ"),
    "bekliyoruz": ("Sizi", "Bekliyoruz", "ÇALIŞMA SAATLERİ", "HAFTANIN HER GÜNÜ"),
}

SATIRLAR = {
    "standart": ([("PZT – CUMA", SAAT), ("CUMARTESİ", SAAT), ("PAZAR", SAAT)],
                 "<b>Pazar dahil</b> her gün kapılarımızı siz değerli<br>müşterilerimize açıyoruz."),
    "acilis": ([("AÇILIŞ", "10:00"), ("KAPANIŞ", "19:00")],
               "<b>Pazartesi'den Pazar'a</b> haftanın her günü<br>sizleri bekliyoruz."),
    "hafta-sonu": ([("CUMARTESİ", SAAT), ("PAZAR", SAAT)],
                   "<b>Hafta içi de</b> aynı saatlerde<br>kapılarımız açık."),
}

# Tam ekran fotoğrafın dalga bölgesine göre dikey kaydırması (ölçekleme yok)
KAYDIR_ALT = {"gb": 250, "yaz": 250, "ic": 420}

IPEK_CSS = """
.story { color:$yazi; font-family:"Montserrat"; }
.zemin { position:absolute; inset:0; }
.ince { position:absolute; top:${ince_ust}px; left:0; right:0; text-align:center; font-weight:200; font-size:${ince_boyut}px;
  line-height:1; letter-spacing:-.005em; color:$yazi; }
.script { position:absolute; top:${script_ust}px; left:0; }
.ayrac { position:absolute; top:${ayrac_ust}px; left:0; right:0; display:flex; align-items:center; justify-content:center; gap:30px; }
.ayrac i { width:130px; height:1.5px; background:$yazi; opacity:.75; }
.blok { position:absolute; top:${blok_ust}px; height:${blok_yuk}px; left:0; right:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center; }
.h1 { font-weight:500; font-size:46px; letter-spacing:.07em; }
.h2 { font-weight:300; font-size:36px; letter-spacing:.42em; padding-left:.42em; margin-top:12px; color:$ince; }
.satirlar { margin-top:42px; display:flex; flex-direction:column; gap:18px; }
.satir { display:flex; align-items:center; }
.cip { width:300px; height:78px; border-radius:999px; display:flex; align-items:center; justify-content:center;
  background: linear-gradient(180deg, $cip1, $cip2); border:1.5px solid $cip_k; color:$cip_y;
  box-shadow: 0 10px 22px rgba(0,0,0,.10), inset 0 1px 0 rgba(255,255,255,.7);
  font-weight:500; font-size:29px; letter-spacing:.08em; }
.dik { width:1.5px; height:58px; background:$cizgi; margin:0 36px; }
.sag { width:330px; font-weight:600; font-size:33px; letter-spacing:.05em; }
.not { margin-top:34px; text-align:center; font-style:italic; font-weight:400; font-size:28px; line-height:1.45; color:$ince; }
.not b { font-weight:700; color:$yazi; }
.foto-golge { position:absolute; inset:0; filter: drop-shadow(0 18px 30px rgba(0,0,0,.28)); }
.foto-dalga { position:absolute; inset:0; overflow:hidden; clip-path: path("$foto_yol"); }
.foto-dalga img { position:absolute; left:0; top:${kaydir}px; }
.alt { position:absolute; top:${alt_ust}px; left:0; right:0; display:flex; flex-direction:column; align-items:center; }
.alt .web { margin-top:14px; font-weight:500; font-size:24px; letter-spacing:.12em; color:$ince; }
.ust-logo { position:absolute; top:200px; left:50%; transform:translateX(-50%); filter: drop-shadow(0 4px 16px rgba(0,0,0,.3)); }
.ust-golge { position:absolute; left:0; right:0; top:0; height:520px; background: linear-gradient(180deg, rgba(0,0,0,.35), transparent); }
"""


def ipek_zemin(c):
    return f"""<svg class="zemin" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs>
<linearGradient id="z" x1="0" y1="0" x2=".55" y2="1"><stop offset="0" stop-color="{c['z1']}"/><stop offset="1" stop-color="{c['z2']}"/></linearGradient>
<linearGradient id="k1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['k1']}"/><stop offset="1" stop-color="{c['k2']}"/></linearGradient>
<linearGradient id="k2" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['k1']}"/><stop offset=".7" stop-color="{c['k2']}"/></linearGradient>
<linearGradient id="k3" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{c['k2']}"/><stop offset="1" stop-color="{c['k1']}"/></linearGradient>
<filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#000" flood-opacity="{c['golge']}"/></filter>
</defs>
<rect width="1080" height="1920" fill="url(#z)"/>
<path d="M0 640 C 260 520, 600 600, 1080 380 V 1920 H 0 Z" fill="url(#k3)" opacity=".55" filter="url(#g)"/>
<path d="M0 0 H 780 C 640 230, 400 450, 0 560 Z" fill="url(#k1)" filter="url(#g)"/>
<path d="M1080 0 V 1240 C 930 1010, 850 690, 900 430 C 930 240, 1010 100, 1080 0 Z" fill="url(#k2)" filter="url(#g)"/>
</svg>"""


def ipek_script(metin, ust, font, boyut, c, x=560, aci=-5):
    return f"""<svg class="script" width="1080" height="330" viewBox="0 0 1080 330" style="top:{ust}px;overflow:visible">
<defs><linearGradient id="altin" x1="0" y1="0" x2="1" y2=".4"><stop offset="0" stop-color="{c['a1']}"/>
<stop offset=".5" stop-color="{c['a2']}"/><stop offset="1" stop-color="{c['a3']}"/></linearGradient></defs>
<text x="{x}" y="215" text-anchor="middle" font-family="{font}" font-size="{boyut}" fill="url(#altin)"
 transform="rotate({aci} {x} 170)">{metin}</text></svg>"""


def ipek(cfg):
    c = IPEK_TEMA[cfg["tema"]]
    ince, script, h1, h2 = BASLIKLAR[cfg["baslik"]]
    satirlar, notu = SATIRLAR[cfg["satirlar"]]
    k = cfg["foto"]
    ust_foto = cfg.get("duzen") == "ust-foto"
    font, boyut = cfg["script"]

    if ust_foto:
        g = dict(ince_ust=716, ince_boyut=128, script_ust=748, ayrac_ust=0, blok_ust=1040, blok_yuk=470, alt_ust=1546,
                 foto_yol="M0 0 H1080 V 600 C 760 700, 330 590, 0 690 Z", kaydir=-480)
    else:
        g = dict(ince_ust=170, ince_boyut=150, script_ust=212, ayrac_ust=494, blok_ust=578, blok_yuk=524, alt_ust=1548,
                 foto_yol="M0 1150 C 280 1080, 720 1160, 1080 1060 L1080 1500 C 760 1560, 330 1470, 0 1540 Z",
                 kaydir=KAYDIR_ALT[k])
    css = t(IPEK_CSS, **g, **c)
    cipler = "".join(f'<div class="satir"><span class="cip">{a}</span><span class="dik"></span><span class="sag">{b}</span></div>'
                     for a, b in satirlar)
    blok = (f'<div class="blok"><div class="h1">{h1}</div><div class="h2">{h2}</div>'
            f'<div class="satirlar">{cipler}</div><div class="not">{notu}</div></div>')
    foto = (f'<div class="foto-golge"><div class="foto-dalga"><img src="../assets/{TAM[k]}" width="1080" height="1920" alt=""></div></div>')
    if ust_foto:
        foto += '<div class="ust-golge" style="clip-path:path(\'M0 0 H1080 V 600 C 760 700, 330 590, 0 690 Z\')"></div>'
        foto += f'<div class="ust-logo">{logo(400)}</div>'
        alt_dalga = ""
        ayrac = ""
    else:
        alt_dalga = f"""<svg class="zemin" width="1080" height="1920" viewBox="0 0 1080 1920" style="filter:drop-shadow(0 -10px 22px rgba(0,0,0,.18))">
<path d="M0 1520 C 330 1460, 760 1580, 1080 1470 V 1920 H 0 Z" fill="{c['dalga']}"/></svg>"""
        ayrac = f'<div class="ayrac"><i></i><div class="logo-ikon" style="width:74px;background:{c["yazi"]}"></div><i></i></div>'
    alt = f'<div class="alt">{logo(360, c["logo"])}<div class="web">{WEB}</div></div>'
    govde = f"""{ipek_zemin(c)}
{foto}
{alt_dalga}
<div class="ince">{ince}</div>
{ipek_script(script, g["script_ust"], font, boyut, c)}
{ayrac}
{blok}
{alt}"""
    return css, govde


# ============================================================================
# KART AİLESİ
# ============================================================================

KART_TEMA = {
    "siyah": dict(zemin="#0a0a0a", b1="#232323", b2="#111111", b3="#2e2e2e", b4="#181818", kart1="#f7f7f7", kart2="#e6e6e7",
                  yazi="#1b1b1b", vurgu="#1b1b1b", ince="#3a3a3a", logo="#ffffff", parilti="rgba(255,255,255,.06)"),
    "bordo": dict(zemin="#2c060c", b1="#5c111c", b2="#3c0910", b3="#741a29", b4="#4a0d17", kart1="#f8f1e6", kart2="#eadfcb",
                  yazi="#2a1418", vurgu="#8a1b2b", ince="#4a3a32", logo="#f3e3cc", parilti="rgba(255,220,220,.07)"),
    "lacivert": dict(zemin="#060e1a", b1="#12284a", b2="#0a1730", b3="#1a3560", b4="#0d1d3a", kart1="#f7f8fa", kart2="#e4e8ee",
                     yazi="#0f2340", vurgu="#0f2340", ince="#36465e", logo="#ffffff", parilti="rgba(200,220,255,.07)"),
    "acik": dict(zemin="#e7e8ea", b1="#f6f6f7", b2="#dcdde0", b3="#ffffff", b4="#d3d4d7", kart1="#1f1d1b", kart2="#121110",
                 yazi="#f6f0e4", vurgu="#d9c39b", ince="rgba(246,240,228,.78)", logo="#1b1b1b", parilti="rgba(0,0,0,.05)"),
}

METINLER = {
    "her-gun": ("AVM'miz her gün", SAAT, "arası açıktır.",
                "Pazartesi'den Pazar'a, haftanın her günü sizleri ağırlamaktan mutluluk duyarız."),
    "yedi-gun": ("Haftanın 7 günü", SAAT, "sizlerleyiz.",
                 "Mobilya alışverişinizi hafta içi ya da hafta sonu, size en uygun gün planlayabilirsiniz."),
    "hafta-sonu": ("Hafta sonu da", "açığız!", "",
                   "Cumartesi ve Pazar dahil her gün 10:00 – 19:00 arası kapılarımız açık."),
}

KART_CSS = """
.story { background:$zemin; font-family:"Montserrat"; }
.zemin { position:absolute; inset:0; }
.kart { position:absolute; top:300px; left:96px; width:888px; height:1060px; border-radius:48px;
  background: linear-gradient(180deg, $kart1, $kart2); box-shadow: 0 40px 90px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.6); }
.metin { position:absolute; top:${metin_ust}px; left:136px; right:136px; text-align:center; color:$yazi; }
.metin .s1 { font-weight:700; font-size:74px; line-height:1.08; letter-spacing:-.01em; }
.metin .s2 { font-weight:800; font-size:${s2}px; line-height:1.05; letter-spacing:-.02em; color:$vurgu; margin-top:4px; }
.metin .s3 { font-weight:700; font-size:74px; line-height:1.08; letter-spacing:-.01em; color:$ince; }
.metin .p { font-weight:500; font-size:36px; line-height:1.4; color:$ince; margin-top:34px; }
.metin .cizgi { width:90px; height:4px; border-radius:2px; background:$vurgu; margin:30px auto 0; opacity:.85; }
.foto-k { position:absolute; top:${foto_ust}px; left:96px; width:984px; height:700px;
  -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000 30%), radial-gradient(ellipse 128% 152% at 100% 0%, #000 69.6%, transparent 70%);
  -webkit-mask-composite: source-in; mask-composite: intersect; }
.logo-a { position:absolute; top:1578px; left:50%; transform:translateX(-50%); }
.cipler { display:flex; flex-direction:column; gap:18px; margin-top:40px; align-items:center; }
.cipler .satir { display:flex; align-items:center; gap:28px; }
.cipler .cip { width:290px; height:72px; border-radius:999px; display:flex; align-items:center; justify-content:center;
  background:$yazi; color:$kart1; font-weight:600; font-size:27px; letter-spacing:.08em; }
.cipler .sag { width:300px; text-align:left; font-weight:700; font-size:34px; color:$yazi; }
"""


def kart_zemin(c):
    """Kamera diyaframı/girdap benzeri iç içe kıvrımlar."""
    return f"""<svg class="zemin" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs>
<linearGradient id="b1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['b3']}"/><stop offset="1" stop-color="{c['b2']}"/></linearGradient>
<linearGradient id="b2" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['b1']}"/><stop offset="1" stop-color="{c['b4']}"/></linearGradient>
<filter id="g" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="0" stdDeviation="26" flood-color="#000" flood-opacity=".45"/></filter>
</defs>
<rect width="1080" height="1920" fill="{c['zemin']}"/>
<ellipse cx="760" cy="760" rx="1180" ry="1380" fill="url(#b1)" filter="url(#g)"/>
<ellipse cx="820" cy="840" rx="1000" ry="1180" fill="url(#b2)" filter="url(#g)"/>
<ellipse cx="880" cy="920" rx="820" ry="980" fill="url(#b1)" filter="url(#g)"/>
<ellipse cx="930" cy="1000" rx="650" ry="780" fill="{c['b4']}" filter="url(#g)"/>
<ellipse cx="300" cy="1900" rx="760" ry="560" fill="{c['zemin']}" filter="url(#g)"/>
<path d="M-40 260 C 300 40, 820 30, 1120 300" stroke="{c['parilti']}" stroke-width="3" fill="none"/>
<path d="M-40 1500 C 260 1720, 760 1780, 1120 1600" stroke="{c['parilti']}" stroke-width="3" fill="none"/>
</svg>"""


def kart(cfg):
    c = KART_TEMA[cfg["tema"]]
    k = cfg["foto"]
    liste = cfg.get("metin") == "liste"
    cx, cy = BINA[k]
    if k == "ic":
        cy = 900
    foto_src = kirp(k, 984, 700, cx, cy)
    if liste:
        metin = ('<div class="s1" style="font-size:66px">Çalışma Saatlerimiz</div>'
                 '<div class="p" style="margin-top:16px">Haftanın her günü sizleri bekliyoruz.</div>'
                 '<div class="cipler">'
                 + "".join(f'<div class="satir"><span class="cip">{a}</span><span class="sag">{SAAT}</span></div>'
                           for a in ("PZT – CUMA", "CUMARTESİ", "PAZAR")) + "</div>")
        g = dict(metin_ust=390, foto_ust=900, s2=0)
    else:
        s1, s2, s3, p = METINLER[cfg["metin"]]
        s3_html = f'<div class="s3">{s3}</div>' if s3 else ""
        metin = f'<div class="s1">{s1}</div><div class="s2">{s2}</div>{s3_html}<div class="cizgi"></div><div class="p">{p}</div>'
        g = dict(metin_ust=400, foto_ust=840, s2=104 if s2 == SAAT else 150)
    css = t(KART_CSS, **g, **c)
    govde = f"""{kart_zemin(c)}
<div class="kart"></div>
<div class="metin">{metin}</div>
<div class="foto-k"><img src="{foto_src}" width="984" height="700" style="display:block" alt=""></div>
<div class="logo-a">{logo(360, c["logo"])}</div>"""
    return css, govde


V = dict
VARYASYONLAR = [
    ("ipek-gumus", ipek, V(tema="gumus", foto="gb", baslik="calisma", satirlar="standart", script=("MsMadi", 230))),
    ("ipek-sampanya", ipek, V(tema="sampanya", foto="yaz", baslik="calisma", satirlar="standart", script=("Allison", 250))),
    ("ipek-ic-mekan", ipek, V(tema="gumus", foto="ic", baslik="her-gun", satirlar="acilis", script=("Corinthia", 250))),
    ("ipek-bordo", ipek, V(tema="bordo", foto="gb", baslik="calisma", satirlar="standart", script=("MsMadi", 230))),
    ("ipek-hafta-sonu", ipek, V(tema="gumus", foto="yaz", baslik="hafta-sonu", satirlar="hafta-sonu", script=("Parisienne", 170))),
    ("ipek-ust-fotograf", ipek, V(tema="sampanya", foto="yaz", baslik="calisma", satirlar="acilis", script=("MsMadi", 210), duzen="ust-foto")),
    ("ipek-gece", ipek, V(tema="gece", foto="ic", baslik="bekliyoruz", satirlar="standart", script=("Allison", 240))),
    ("kart-siyah", kart, V(tema="siyah", foto="gb", metin="her-gun")),
    ("kart-siyah-yaz", kart, V(tema="siyah", foto="yaz", metin="yedi-gun")),
    ("kart-bordo-hafta-sonu", kart, V(tema="bordo", foto="gb", metin="hafta-sonu")),
    ("kart-lacivert", kart, V(tema="lacivert", foto="yaz", metin="her-gun")),
    ("kart-acik", kart, V(tema="acik", foto="gb", metin="yedi-gun")),
    ("kart-liste", kart, V(tema="siyah", foto="ic", metin="liste")),
    ("kart-bordo-ic-mekan", kart, V(tema="bordo", foto="ic", metin="her-gun")),
]
