"""Müşterinin önceki paylaşımlarından (bayram ve yılbaşı duyuruları) türetilen iki tasarım ailesi.

Yalnızca açık tema ve yalnızca drone fotoğrafları kullanılır.

ipek: ipeksi kıvrımlı açık zemin, ince yazı + el yazısı başlık, hap şeklinde gün
      etiketleri, dalga maskeli ya da çerçeveli drone fotoğrafı, altta logo ve web adresi.
kart: açık girdap desenli zemin, beyaz kart, karttan taşan drone fotoğrafı.
"""

from string import Template

from .temel import BINA, KISA, TAM, kirp, logo

SAAT = "10:00 – 19:00"
WEB = "imotim.com.tr"


def t(css, **kw):
    return Template(css).substitute(**kw)


# ============================================================================
# İPEK AİLESİ
# ============================================================================

_CIP = dict(cip1="#ffffff", cip2="#eeeeee", cip_y="#2a2a2a", cip_k="rgba(0,0,0,.04)")
_ALTIN = dict(a1="#9f7b47", a2="#e6d2a6", a3="#8f6c3c")

IPEK_TEMA = {
    "gumus": dict(z1="#f8f8f9", z2="#dfe0e3", k1="#ffffff", k2="#e9eaec", golge=".16", yazi="#1c1c1c", ince="#4d4d4d",
                  cizgi="#8f8f8f", logo="#161616", dalga="#f6f6f7", **_ALTIN, **_CIP),
    "inci": dict(z1="#ffffff", z2="#e8e6e2", k1="#ffffff", k2="#f1efeb", golge=".12", yazi="#1a1a1a", ince="#555555",
                 cizgi="#9a9a9a", logo="#161616", dalga="#fbfaf8", a1="#a8865a", a2="#ecdcb8", a3="#8d6c40", **_CIP),
    "sampanya": dict(z1="#f8f2e8", z2="#e4d5bd", k1="#fffaf2", k2="#efe2cd", golge=".16", yazi="#2b2118", ince="#5e4c3c",
                     a1="#9c7440", a2="#e9d2a2", a3="#86612f", cip1="#fffdf8", cip2="#f2e8d8", cip_y="#3a2c1f",
                     cip_k="rgba(80,50,20,.06)", cizgi="#a08a72", logo="#2b2118", dalga="#f6efe3"),
    "kum": dict(z1="#f3ede4", z2="#d9cdbb", k1="#faf6ef", k2="#e6dccd", golge=".15", yazi="#2c241c", ince="#62574a",
                a1="#94703f", a2="#e3c998", a3="#7e5d30", cip1="#fdfaf5", cip2="#efe7da", cip_y="#2c241c",
                cip_k="rgba(80,50,20,.07)", cizgi="#a39380", logo="#2c241c", dalga="#f1ebe1"),
    # Gümüş zemin, altın yerine grafit el yazısı
    "grafit": dict(z1="#f8f8f9", z2="#dfe0e3", k1="#ffffff", k2="#e9eaec", golge=".16", yazi="#1c1c1c", ince="#4d4d4d",
                   cizgi="#8f8f8f", logo="#161616", dalga="#f6f6f7", a1="#1f1f1f", a2="#6b6b6b", a3="#141414", **_CIP),
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
    # Büyük saat + 7 günlük hap şeridi (satır listesi yerine)
    "seridi": (None, "<b>Pazartesi'den Pazar'a</b> haftanın her günü<br>sizleri bekliyoruz."),
}

# Dalga maskesinde binanın görüneceği dikey kaydırma (tam ekran fotoğraf, ölçekleme yok)
KAYDIR_ALT = {"gb": 250, "yaz": 250}
KAYDIR_UST = {"gb": -470, "yaz": -480}

DALGA_ALT = "M0 1150 C 280 1080, 720 1160, 1080 1060 L1080 1500 C 760 1560, 330 1470, 0 1540 Z"
DALGA_UST = "M0 0 H1080 V 600 C 760 700, 330 590, 0 690 Z"

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
.buyuk-saat { margin-top:34px; font-weight:300; font-size:104px; line-height:1; letter-spacing:-.01em; }
.seridi { display:flex; gap:12px; margin-top:34px; }
.seridi span { width:104px; height:66px; border-radius:999px; display:flex; align-items:center; justify-content:center;
  background: linear-gradient(180deg, $cip1, $cip2); border:1.5px solid $cip_k; color:$cip_y;
  box-shadow: 0 8px 18px rgba(0,0,0,.09), inset 0 1px 0 rgba(255,255,255,.7); font-weight:600; font-size:24px; }
.not { margin-top:34px; text-align:center; font-style:italic; font-weight:400; font-size:28px; line-height:1.45; color:$ince; }
.not b { font-weight:700; color:$yazi; }
.foto-golge { position:absolute; inset:0; filter: drop-shadow(0 18px 30px rgba(0,0,0,.28)); }
.foto-dalga { position:absolute; inset:0; overflow:hidden; clip-path: path("$foto_yol"); }
.foto-dalga img { position:absolute; left:0; top:${kaydir}px; }
.cerceve { position:absolute; top:560px; left:90px; width:900px; height:440px; border-radius:44px; overflow:hidden;
  box-shadow: 0 30px 60px rgba(0,0,0,.22); outline:10px solid rgba(255,255,255,.7); }
.alt { position:absolute; top:${alt_ust}px; left:0; right:0; display:flex; flex-direction:column; align-items:center; }
.alt .web { margin-top:14px; font-weight:500; font-size:24px; letter-spacing:.12em; color:$ince; }
.ust-logo { position:absolute; top:200px; left:50%; transform:translateX(-50%); filter: drop-shadow(0 4px 16px rgba(0,0,0,.3)); }
.ust-golge { position:absolute; left:0; right:0; top:0; height:520px; background: linear-gradient(180deg, rgba(0,0,0,.35), transparent); }
"""

DUZEN = {
    "alt": dict(ince_ust=170, ince_boyut=150, script_ust=212, ayrac_ust=494, blok_ust=578, blok_yuk=524, alt_ust=1548),
    "ust": dict(ince_ust=716, ince_boyut=128, script_ust=748, ayrac_ust=0, blok_ust=1040, blok_yuk=470, alt_ust=1546),
    "cerceve": dict(ince_ust=170, ince_boyut=136, script_ust=198, ayrac_ust=0, blok_ust=1040, blok_yuk=470, alt_ust=1548),
}


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
    duzen = cfg.get("duzen", "alt")
    font, boyut = cfg["script"]
    g = dict(DUZEN[duzen])
    g["foto_yol"] = DALGA_UST if duzen == "ust" else DALGA_ALT
    g["kaydir"] = KAYDIR_UST[k] if duzen == "ust" else KAYDIR_ALT[k]
    css = t(IPEK_CSS, **g, **c)

    if satirlar is None:
        icerik = (f'<div class="buyuk-saat">{SAAT}</div>'
                  f'<div class="seridi">{"".join(f"<span>{g_}</span>" for g_ in KISA)}</div>')
    else:
        icerik = '<div class="satirlar">' + "".join(
            f'<div class="satir"><span class="cip">{a}</span><span class="dik"></span><span class="sag">{b}</span></div>'
            for a, b in satirlar) + "</div>"
    # Çerçeveli düzende başlık zaten üstte; blokta yalnızca alt başlık kalır
    basliklar = f'<div class="h2" style="margin-top:0">{h1}</div>' if duzen == "cerceve" else f'<div class="h1">{h1}</div><div class="h2">{h2}</div>'
    blok = f'<div class="blok">{basliklar}{icerik}<div class="not">{notu}</div></div>'

    foto = ayrac = alt_dalga = ""
    if duzen == "ust":
        foto = (f'<div class="foto-golge"><div class="foto-dalga"><img src="../assets/{TAM[k]}" width="1080" height="1920" alt=""></div></div>'
                f'<div class="ust-golge" style="clip-path:path(\'{DALGA_UST}\')"></div><div class="ust-logo">{logo(400)}</div>')
    elif duzen == "cerceve":
        foto = f'<div class="cerceve"><img src="{kirp(k, 900, 440, *BINA[k])}" width="900" height="440" style="display:block" alt=""></div>'
    else:
        foto = f'<div class="foto-golge"><div class="foto-dalga"><img src="../assets/{TAM[k]}" width="1080" height="1920" alt=""></div></div>'
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
    "gumus": dict(zemin="#e6e7e9", b1="#f6f6f7", b2="#dadbde", b3="#ffffff", b4="#d2d3d6", golge=".16",
                  kart1="#ffffff", kart2="#f3f3f4", kart_golge="rgba(0,0,0,.16)", yazi="#1b1b1b", vurgu="#1b1b1b",
                  ince="#4a4a4a", cip_y="#ffffff", logo="#1b1b1b", parilti="rgba(0,0,0,.05)"),
    "sampanya": dict(zemin="#e9e0d0", b1="#f8f2e8", b2="#ddd0b9", b3="#fffaf2", b4="#d5c6ac", golge=".14",
                     kart1="#fffdf9", kart2="#f7f0e4", kart_golge="rgba(70,45,15,.16)", yazi="#2b2118", vurgu="#9c7440",
                     ince="#5e4c3c", cip_y="#fffaf2", logo="#2b2118", parilti="rgba(80,50,20,.06)"),
    "inci": dict(zemin="#f1f0ed", b1="#fbfbfa", b2="#e5e3df", b3="#ffffff", b4="#dedcd7", golge=".12",
                 kart1="#ffffff", kart2="#faf9f7", kart_golge="rgba(0,0,0,.13)", yazi="#1a1a1a", vurgu="#9f7b47",
                 ince="#555555", cip_y="#ffffff", logo="#1a1a1a", parilti="rgba(0,0,0,.05)"),
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
  background: linear-gradient(180deg, $kart1, $kart2); box-shadow: 0 40px 90px $kart_golge, inset 0 1px 0 rgba(255,255,255,.9); }
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
  background:$yazi; color:$cip_y; font-weight:600; font-size:27px; letter-spacing:.08em; }
.cipler .sag { width:300px; text-align:left; font-weight:700; font-size:34px; color:$yazi; }
"""


def kart_zemin(c):
    """Kamera diyaframı/girdap benzeri iç içe kıvrımlar."""
    return f"""<svg class="zemin" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs>
<linearGradient id="b1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['b3']}"/><stop offset="1" stop-color="{c['b2']}"/></linearGradient>
<linearGradient id="b2" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['b1']}"/><stop offset="1" stop-color="{c['b4']}"/></linearGradient>
<filter id="g" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="0" stdDeviation="26" flood-color="#000" flood-opacity="{c['golge']}"/></filter>
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
    foto_src = kirp(k, 984, 700, *BINA[k])
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
    # İpek: fotoğraf altta dalga içinde
    ("ipek-gumus", ipek, V(tema="gumus", foto="gb", baslik="calisma", satirlar="standart", script=("MsMadi", 230))),
    ("ipek-sampanya", ipek, V(tema="sampanya", foto="yaz", baslik="calisma", satirlar="standart", script=("Allison", 250))),
    ("ipek-inci-her-gun", ipek, V(tema="inci", foto="yaz", baslik="her-gun", satirlar="acilis", script=("Corinthia", 250))),
    ("ipek-kum-hafta-sonu", ipek, V(tema="kum", foto="gb", baslik="hafta-sonu", satirlar="hafta-sonu", script=("Parisienne", 170))),
    ("ipek-grafit", ipek, V(tema="grafit", foto="yaz", baslik="calisma", satirlar="seridi", script=("MsMadi", 230))),
    # İpek: fotoğraf üstte
    ("ipek-ust-sampanya", ipek, V(tema="sampanya", foto="yaz", baslik="calisma", satirlar="acilis", script=("MsMadi", 210), duzen="ust")),
    ("ipek-ust-gumus", ipek, V(tema="gumus", foto="gb", baslik="bekliyoruz", satirlar="seridi", script=("Allison", 220), duzen="ust")),
    # İpek: çerçeveli fotoğraf
    ("ipek-cerceve-inci", ipek, V(tema="inci", foto="gb", baslik="calisma", satirlar="standart", script=("MsMadi", 220), duzen="cerceve")),
    ("ipek-cerceve-kum", ipek, V(tema="kum", foto="yaz", baslik="her-gun", satirlar="seridi", script=("Allison", 240), duzen="cerceve")),
    # Kart
    ("kart-gumus", kart, V(tema="gumus", foto="gb", metin="her-gun")),
    ("kart-gumus-yaz", kart, V(tema="gumus", foto="yaz", metin="yedi-gun")),
    ("kart-sampanya", kart, V(tema="sampanya", foto="yaz", metin="her-gun")),
    ("kart-sampanya-hafta-sonu", kart, V(tema="sampanya", foto="gb", metin="hafta-sonu")),
    ("kart-inci-liste", kart, V(tema="inci", foto="yaz", metin="liste")),
    ("kart-inci", kart, V(tema="inci", foto="gb", metin="yedi-gun")),
]
