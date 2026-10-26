"""03-haftalik-cam tasarımının geliştirilmiş hali ve aynı dildeki varyasyonları.

Ortak yapı: tam ekran fotoğraf + ton/karartma, ortada logo, serif italik başlık,
buzlu cam kart. Varyasyonlar fotoğraf kadrajı, cam rengi, kart düzeni ve
başlık fontu üzerinden değişir.
"""

from string import Template

from .temel import GUNLER, GUNLER_B, KISA, kirp, logo

# Fotoğraf kaynakları: (kaynak, merkez x, merkez y, ek filtre)
FOTO = {
    "ic-orta": ("ic", 830, 1000, ""),
    "ic-sol": ("ic", 562, 1000, ""),
    "ic-sag": ("ic", 1038, 1000, ""),
    "ic-sb": ("ic", 830, 1000, "grayscale(1) contrast(1.06)"),
    "ic-bulanik": ("ic", 830, 1000, "blur(16px) brightness(.85)"),
    "gb": ("gb", None, None, ""),
    "yaz": ("yaz", None, None, ""),
}

# Fotoğraf üstü ton katmanı: (üst-orta-alt karartma rengi, alfa değerleri)
TON = {
    "notr": ("14,11,9", (.72, .40, .30, .64)),
    "sicak": ("44,22,8", (.74, .42, .32, .66)),
    "soguk": ("8,16,30", (.72, .40, .30, .64)),
    "hafif": ("14,11,9", (.55, .22, .18, .5)),
    "drone": ("8,24,48", (.55, .18, .08, .62)),
}

CAM = {
    "koyu": dict(bg="rgba(24,19,16,.40)", yazi="#ffffff", vurgu="#efe6d6", ince="rgba(255,255,255,.62)", cizgi="rgba(255,255,255,.13)", kenar="rgba(255,255,255,.55)"),
    "amber": dict(bg="rgba(74,42,14,.42)", yazi="#fff8ee", vurgu="#f2cd8d", ince="rgba(255,240,215,.66)", cizgi="rgba(255,230,190,.16)", kenar="rgba(255,220,170,.6)"),
    "bordo": dict(bg="rgba(120,20,36,.50)", yazi="#ffffff", vurgu="#f3e3cc", ince="rgba(255,235,235,.68)", cizgi="rgba(255,220,220,.18)", kenar="rgba(255,210,210,.55)"),
    "lacivert": dict(bg="rgba(10,26,56,.46)", yazi="#ffffff", vurgu="#e2cfa5", ince="rgba(225,235,255,.68)", cizgi="rgba(200,220,255,.16)", kenar="rgba(210,225,255,.55)"),
    "zeytin": dict(bg="rgba(34,46,30,.50)", yazi="#fbf7ec", vurgu="#e6d3a3", ince="rgba(240,240,220,.68)", cizgi="rgba(230,240,210,.16)", kenar="rgba(230,240,210,.5)"),
    "altin": dict(bg="rgba(16,14,12,.52)", yazi="#f6eedd", vurgu="#dcc08a", ince="rgba(220,192,138,.8)", cizgi="rgba(220,192,138,.22)", kenar="rgba(236,206,146,.9)"),
    "beyaz": dict(bg="rgba(252,250,246,.80)", yazi="#171513", vurgu="#8a1b2b", ince="#7a6f64", cizgi="rgba(0,0,0,.08)", kenar="rgba(255,255,255,.95)"),
    "krem": dict(bg="rgba(244,233,214,.84)", yazi="#2a1a12", vurgu="#8a1b2b", ince="#86705e", cizgi="rgba(80,40,20,.10)", kenar="rgba(255,250,240,.95)"),
}

# Başlık fontu: (aile, ağırlık, boyut)
BASLIK = {
    "Cormorant": ("Cormorant", 500, 96),
    "Playfair": ("Playfair", 500, 82),
    "DMSerif": ("DMSerif", 400, 86),
    "Fraunces": ("Fraunces", 400, 88),
    "Instrument": ("Instrument", 400, 100),
    "Bodoni": ("Bodoni", 500, 84),
}

SAAT = '10:00<i class="tr">–</i>19:00'
YESIL = '<span class="nokta"></span>'


def t(css, **kw):
    return Template(css).substitute(**kw)


# --- Kart düzenleri -----------------------------------------------------------

def d_liste(hs=False, sik=False):
    satirlar = ""
    for i, g in enumerate(GUNLER):
        etiket = '<em class="hs">HAFTA SONU</em>' if hs and i >= 5 else ""
        satirlar += f'<div class="satir"><span class="gun">{g}{etiket}</span><span class="saat">{SAAT}</span></div>'
    return f'<div class="kart {"sik" if sik else ""}">{satirlar}</div>'


def d_kisa():
    satirlar = "".join(
        f'<div class="satir"><span class="gun"><b class="daire">{k}</b>{g}</span><span class="saat">{SAAT}</span></div>'
        for k, g in zip(KISA, GUNLER))
    return f'<div class="kart">{satirlar}</div>'


def d_zaman():
    satirlar = "".join(
        f'<div class="z-satir"><span class="gun">{g}</span><span class="cubuk"><i></i></span><span class="saat">{SAAT}</span></div>'
        for g in GUNLER)
    olcek = "".join(f'<span style="left:{p}%">{s}</span>' for p, s in ((0, "00"), (25, "06"), (50, "12"), (75, "18"), (100, "24")))
    return f'<div class="kart">{satirlar}<div class="z-olcek"><span class="bos"></span><span class="cetvel">{olcek}</span><span class="bos2"></span></div></div>'


def d_tablo():
    satirlar = "".join(f'<div class="t-satir"><span class="gun">{g}</span><span>10:00</span><span>19:00</span></div>' for g in GUNLER)
    return f'<div class="kart"><div class="t-bas"><span>GÜN</span><span>AÇILIŞ</span><span>KAPANIŞ</span></div>{satirlar}</div>'


def d_izgara():
    hucreler = "".join(f'<div class="hucre"><span class="ad">{g}</span><span class="saat">{SAAT}</span></div>' for g in GUNLER_B)
    return f'<div class="kart izgara">{hucreler}</div>'


def d_grup():
    def blok(ne, gunler):
        return f'<div class="blok"><div class="ne">{ne}</div><div class="aralik">{gunler}</div><div class="buyuk">{SAAT}</div></div>'
    return f'<div class="kart grup">{blok("HAFTA İÇİ", "Pazartesi – Cuma")}<div class="ayrac"></div>{blok("HAFTA SONU", "Cumartesi – Pazar")}</div>'


def d_kompakt():
    gunler = "".join(f"<span>{k}{YESIL}</span>" for k in KISA)
    return (f'<div class="kart kompakt"><div class="ne2"><span>AÇILIŞ</span><span>KAPANIŞ</span></div>'
            f'<div class="buyuk">{SAAT}</div><div class="cizgi"></div><div class="chips">{gunler}</div></div>')


def d_baslikli(font):
    satirlar = "".join(f'<div class="satir"><span class="gun">{g}</span><span class="saat">{SAAT}</span></div>' for g in GUNLER)
    return (f'<div class="kart baslikli"><div class="k-bas"><div class="baslik">Çalışma Saatleri</div>'
            f'<div class="alt-baslik">HAFTALIK PROGRAM</div></div>{satirlar}</div>')


DUZEN = {
    "liste": lambda c: d_liste(c.get("hs", False)),
    "liste-sik": lambda c: d_liste(False, sik=True),
    "kisa": lambda c: d_kisa(),
    "zaman": lambda c: d_zaman(),
    "tablo": lambda c: d_tablo(),
    "izgara": lambda c: d_izgara(),
    "grup": lambda c: d_grup(),
    "kompakt": lambda c: d_kompakt(),
    "baslikli": lambda c: d_baslikli(c["font"]),
}

CSS = """
/* Fotoğraf ve ton */
.foto-k { position:absolute; inset:0; overflow:hidden; }
.foto-k img { display:block; filter:$filtre; transform:$olcek; }
.ton { background: linear-gradient(180deg, rgba($ton,$a0) 0%, rgba($ton,$a1) 20%, rgba($ton,$a2) 55%, rgba($ton,$a3) 100%); }
.vinyet { background: radial-gradient(120% 80% at 50% 48%, transparent 52%, rgba(0,0,0,.42)); }
/* Başlık alanının arkasında yumuşak koyuluk: tavan çizgileriyle çakışmayı azaltır */
.bas-golge { position:absolute; top:170px; left:40px; right:40px; height:500px;
  background: radial-gradient(50% 50% at 50% 52%, rgba(0,0,0,.52), rgba(0,0,0,.3) 50%, transparent 78%); }

.ust { position:absolute; top:220px; left:0; right:0; display:flex; flex-direction:column; align-items:center; }
.ust .logo { filter: drop-shadow(0 4px 18px rgba(0,0,0,.35)); }
.baslik { font-family:"$bf"; font-style:italic; font-weight:$bw; font-size:${bs}px; line-height:1; color:#fff;
  text-shadow: 0 4px 26px rgba(0,0,0,.45); }
.ust .baslik { margin-top:56px; }
.alt-baslik { display:flex; align-items:center; gap:22px; margin-top:22px; font-family:"Montserrat"; font-weight:600;
  font-size:23px; letter-spacing:.42em; color:$vurgu_bas; text-shadow: 0 2px 10px rgba(0,0,0,.45); }
.alt-baslik::before, .alt-baslik::after { content:""; width:56px; height:1.5px; background:currentColor; opacity:.6; }
.alt-baslik::after { margin-left:-.42em; }

.govde-k { position:absolute; left:0; right:0; display:flex; flex-direction:column; align-items:center; }

/* Cam kart */
.kart { position:relative; width:880px; padding:18px 54px; border-radius:40px; background:$bg; color:$yazi;
  backdrop-filter: blur(28px) saturate(1.25); -webkit-backdrop-filter: blur(28px) saturate(1.25);
  box-shadow: 0 40px 90px rgba(0,0,0,.38), inset 0 1px 0 rgba(255,255,255,.22); font-family:"Montserrat"; }
.kart::before { content:""; position:absolute; inset:0; border-radius:inherit; padding:1.5px; pointer-events:none;
  background: linear-gradient(150deg, $kenar, rgba(255,255,255,.08) 38%, rgba(255,255,255,.04) 62%, $kenar);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor; mask-composite: exclude; }
.kart::after { content:""; position:absolute; inset:0; border-radius:inherit; pointer-events:none;
  background: linear-gradient(180deg, rgba(255,255,255,.10), rgba(255,255,255,0) 28%); }
.tr { font-style:normal; font-weight:300; margin:0 .32em; opacity:.7; }

/* liste */
.satir { display:flex; align-items:center; justify-content:space-between; height:104px; border-bottom:1.5px solid $cizgi; font-size:36px; }
.satir:last-child { border-bottom:0; }
.satir .gun { font-weight:600; display:flex; align-items:center; }
.satir .saat { font-weight:600; color:$vurgu; font-variant-numeric: tabular-nums lining-nums; letter-spacing:.01em; }
.sik .satir { height:66px; font-size:31px; }
.hs { font-style:normal; font-weight:700; font-size:15px; letter-spacing:.2em; padding:7px 12px 6px 14px; margin-left:18px;
  border:1.5px solid $vurgu; color:$vurgu; border-radius:999px; }
.daire { display:inline-flex; align-items:center; justify-content:center; width:58px; height:58px; margin-right:22px; border-radius:50%;
  font-size:19px; font-weight:700; color:$vurgu; border:1.5px solid $cizgi_g; background:rgba(255,255,255,.06); }

/* zaman çizelgesi */
.z-satir { display:flex; align-items:center; gap:24px; height:96px; border-bottom:1.5px solid $cizgi; font-size:30px; }
.z-satir .gun { width:190px; font-weight:600; }
.z-satir .cubuk { flex:1; position:relative; height:12px; border-radius:6px; background:$cizgi_g; }
.z-satir .cubuk i { position:absolute; top:0; bottom:0; left:calc(10/24*100%); width:calc(9/24*100%); border-radius:6px;
  background:$vurgu; box-shadow:0 0 16px $vurgu; }
.z-satir .saat { width:224px; text-align:right; font-weight:600; font-size:28px; color:$vurgu; font-variant-numeric: tabular-nums; }
.z-olcek { display:flex; gap:24px; height:58px; align-items:center; }
.z-olcek .bos { width:190px; } .z-olcek .bos2 { width:224px; }
.z-olcek .cetvel { flex:1; position:relative; height:24px; }
.z-olcek .cetvel span { position:absolute; transform:translateX(-50%); font-size:19px; font-weight:600; color:$ince; }

/* tablo */
.t-bas, .t-satir { display:grid; grid-template-columns: 1fr 190px 190px; align-items:center; }
.t-bas { height:70px; border-bottom:1.5px solid $cizgi_g; font-size:18px; font-weight:700; letter-spacing:.3em; color:$ince; }
.t-bas span:not(:first-child), .t-satir span:not(:first-child) { text-align:right; }
.t-satir { height:94px; border-bottom:1.5px solid $cizgi; font-size:36px; font-weight:600; }
.t-satir:last-child { border-bottom:0; }
.t-satir span:not(:first-child) { color:$vurgu; font-variant-numeric: tabular-nums; }

/* ızgara */
.izgara { width:900px; padding:12px 0; display:grid; grid-template-columns:1fr 1fr; }
.hucre { height:116px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px; border-bottom:1.5px solid $cizgi; }
.hucre:nth-child(odd) { border-right:1.5px solid $cizgi; }
.hucre:last-child { grid-column:1 / -1; border:0; }
.hucre .ad { font-size:19px; font-weight:700; letter-spacing:.3em; padding-left:.3em; color:$ince; }
.hucre .saat { font-size:38px; font-weight:600; color:$vurgu; font-variant-numeric: tabular-nums; }

/* hafta içi / hafta sonu */
.grup { padding:44px 54px; }
.blok { display:flex; flex-direction:column; align-items:center; }
.blok .ne { font-size:20px; font-weight:700; letter-spacing:.42em; padding-left:.42em; color:$ince; }
.blok .aralik { font-family:"$bf"; font-style:italic; font-size:52px; margin-top:12px; }
.blok .buyuk { font-size:92px; font-weight:700; line-height:1; margin-top:14px; color:$vurgu; letter-spacing:-.01em; }
.grup .ayrac { height:1.5px; background:$cizgi_g; margin:38px 0; }

/* kompakt */
.kompakt { padding:46px 54px 50px; }
.ne2 { display:flex; justify-content:space-around; font-size:21px; font-weight:600; letter-spacing:.38em; color:$ince; }
.kompakt .buyuk { text-align:center; font-size:100px; font-weight:600; line-height:1; margin-top:16px; letter-spacing:-.01em; white-space:nowrap; }
.kompakt .cizgi { height:1.5px; background:$cizgi_g; margin:40px 0 34px; }
.chips { display:flex; justify-content:space-between; }
.chips span { width:92px; height:104px; border-radius:24px; border:1.5px solid $cizgi_g; background:rgba(255,255,255,.06);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:14px; font-size:24px; font-weight:600; }
.nokta { width:12px; height:12px; border-radius:50%; background:#5ee08a; box-shadow:0 0 0 5px rgba(94,224,138,.22); }

/* başlıklı kart */
.baslikli { padding-top:46px; }
.k-bas { display:flex; flex-direction:column; align-items:center; padding-bottom:30px; border-bottom:1.5px solid $cizgi_g; margin-bottom:6px; }
.k-bas .baslik { color:$yazi; text-shadow:none; }
.k-bas .alt-baslik { color:$vurgu; text-shadow:none; }
.baslikli .satir { height:92px; }

/* açık göstergesi */
.hap { display:flex; align-items:center; gap:18px; padding:18px 34px 18px 28px; border-radius:999px;
  background:rgba(10,10,10,.34); border:1.5px solid rgba(255,255,255,.2); backdrop-filter: blur(14px);
  font-family:"Montserrat"; font-weight:600; font-size:24px; letter-spacing:.3em; color:#fff; }
.hap .nokta { width:14px; height:14px; box-shadow:0 0 0 6px rgba(94,224,138,.25), 0 0 14px #5ee08a; }
"""


def uret(c):
    k, cx, cy, filtre = FOTO[c["foto"]]
    ton_r, alfa = TON[c["ton"]]
    cam = CAM[c["cam"]]
    bf, bw, bs = BASLIK[c["font"]]
    acik = c["cam"] in ("beyaz", "krem")
    css = t(CSS, filtre=filtre or "none", olcek="scale(1.06)" if "blur" in filtre else "none",
            ton=ton_r, a0=alfa[0], a1=alfa[1], a2=alfa[2], a3=alfa[3],
            bf=bf, bw=bw, bs=bs, vurgu_bas=c.get("vurgu_bas", "#efe6d6"),
            cizgi_g="rgba(0,0,0,.14)" if acik else "rgba(255,255,255,.24)", **cam)
    foto = f'<div class="foto-k"><img src="{kirp(k, 1080, 1920, cx, cy)}" width="1080" height="1920" alt=""></div>'
    hap = f'<div class="hap">{YESIL}HAFTANIN HER GÜNÜ AÇIĞIZ</div>'
    duzen = c["duzen"]
    kart = DUZEN[duzen](c)
    alt_konum = c.get("konum") == "alt"

    if duzen == "baslikli":
        ust = f'<div class="ust">{logo(430)}</div>'
        govde = f'<div class="govde-k" style="top:440px">{kart}<div style="height:44px"></div>{hap}</div>'
    else:
        ust_hap = f'<div style="margin-top:40px">{hap}</div>' if alt_konum else ""
        ust = (f'<div class="ust">{logo(430)}<div class="baslik">Çalışma Saatleri</div>'
               f'<div class="alt-baslik">{c.get("alt", "HAFTALIK PROGRAM")}</div>{ust_hap}</div>')
        if alt_konum:
            govde = f'<div class="govde-k" style="bottom:{c.get("alt_bosluk", 270)}px">{kart}</div>'
        else:
            govde = f'<div class="govde-k" style="top:{c.get("kart_ust", 646)}px">{kart}<div style="height:48px"></div>{hap}</div>'

    html = f"""{foto}
<div class="katman ton"></div><div class="katman vinyet"></div>{"" if c["ton"] == "drone" else '<div class="bas-golge"></div>'}
{ust}
{govde}"""
    return css, html


V = dict  # okunurluk için kısaltma
VARYASYONLAR = [
    ("gelistirilmis", V(foto="ic-orta", ton="notr", cam="koyu", duzen="liste", font="Cormorant", hs=True)),
    ("amber-playfair", V(foto="ic-orta", ton="sicak", cam="amber", duzen="liste", font="Playfair")),
    ("zaman-cizelgesi", V(foto="ic-sol", ton="notr", cam="koyu", duzen="zaman", font="Cormorant", kart_ust=656)),
    ("bordo-hafta-sonu", V(foto="ic-sag", ton="sicak", cam="bordo", duzen="liste", font="DMSerif", hs=True)),
    ("siyah-beyaz-altin", V(foto="ic-sb", ton="notr", cam="altin", duzen="liste", font="Bodoni", vurgu_bas="#dcc08a")),
    ("bulanik-beyaz", V(foto="ic-bulanik", ton="hafif", cam="beyaz", duzen="liste", font="Instrument")),
    ("lacivert-tablo", V(foto="ic-sol", ton="soguk", cam="lacivert", duzen="tablo", font="Fraunces", kart_ust=656)),
    ("zeytin-gun-daireleri", V(foto="ic-sag", ton="notr", cam="zeytin", duzen="kisa", font="Cormorant")),
    ("krem-acik", V(foto="ic-sol", ton="sicak", cam="krem", duzen="liste", font="Playfair", hs=True)),
    ("izgara-koyu", V(foto="ic-orta", ton="notr", cam="koyu", duzen="izgara", font="DMSerif", kart_ust=720)),
    ("hafta-ici-hafta-sonu", V(foto="ic-sag", ton="sicak", cam="amber", duzen="grup", font="Cormorant", kart_ust=720)),
    ("baslikli-altin", V(foto="ic-orta", ton="notr", cam="altin", duzen="baslikli", font="Cormorant")),
    ("kompakt-bordo", V(foto="ic-bulanik", ton="notr", cam="bordo", duzen="kompakt", font="Playfair", kart_ust=760)),
    ("drone-hafta-sonu", V(foto="gb", ton="drone", cam="lacivert", duzen="grup", font="Cormorant", konum="alt", alt="HER GÜN AYNI SAATTE")),
    ("drone-izgara", V(foto="gb", ton="drone", cam="koyu", duzen="izgara", font="Fraunces", konum="alt")),
    ("drone-beyaz-izgara", V(foto="yaz", ton="drone", cam="beyaz", duzen="izgara", font="Instrument", konum="alt")),
    ("drone-kompakt", V(foto="yaz", ton="drone", cam="lacivert", duzen="kompakt", font="DMSerif", konum="alt", alt="PAZARTESİ – PAZAR")),
    ("drone-liste", V(foto="gb", ton="drone", cam="amber", duzen="liste-sik", font="Playfair", konum="alt")),
    ("drone-yaz-liste", V(foto="yaz", ton="drone", cam="koyu", duzen="liste-sik", font="Bodoni", konum="alt")),
    ("bordo-baslikli", V(foto="ic-sol", ton="sicak", cam="bordo", duzen="baslikli", font="DMSerif")),
    ("lacivert-zaman", V(foto="ic-sag", ton="soguk", cam="lacivert", duzen="zaman", font="Instrument", kart_ust=656)),
    ("krem-tablo", V(foto="ic-orta", ton="sicak", cam="krem", duzen="tablo", font="Bodoni", kart_ust=656)),
    ("bulanik-hafta-sonu", V(foto="ic-bulanik", ton="hafif", cam="beyaz", duzen="grup", font="Fraunces", kart_ust=720)),
    ("siyah-beyaz-bordo", V(foto="ic-sb", ton="notr", cam="bordo", duzen="kisa", font="DMSerif")),
]
