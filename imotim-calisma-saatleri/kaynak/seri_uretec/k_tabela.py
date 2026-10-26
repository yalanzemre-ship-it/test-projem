"""Tabela/işaret temalı konseptler: otoyol tabelası, neon, uçuş panosu, LED saat, kapı tabelası, fiyat etiketi."""

from string import Template

from .temel import GUNLER_B, P, ikon, logo, tam


def t(css, **kw):
    return Template(css).substitute(**kw)


# --- Otoyol tabelası -----------------------------------------------------------

def otoyol(v):
    renk, foto = [("#0d6b3b", "yaz"), ("#0b4ea2", "gb"), ("#6b3e26", None)][v]
    if foto:
        zemin = tam(foto) + '<div class="katman" style="background:linear-gradient(180deg,rgba(0,0,0,.25),rgba(0,0,0,0) 30%)"></div>'
    else:
        # Asfalt yol, kuşbakışı: orta şerit çizgisi ve kenar çizgileri
        zemin = """<div class="katman asfalt"></div>
<div class="serit-cizgi" style="left:536px"></div>
<div class="kenar" style="left:120px"></div><div class="kenar" style="left:952px"></div>"""
    css = t("""
.asfalt { background: radial-gradient(120% 80% at 50% 30%, #4a4a4a, #2b2b2b 70%), #2b2b2b; }
.asfalt::after { content:""; position:absolute; inset:0; opacity:.35;
  background-image: radial-gradient(rgba(255,255,255,.18) 1px, transparent 1.5px); background-size: 7px 7px; }
.serit-cizgi { position:absolute; top:0; bottom:0; width:8px;
  background: repeating-linear-gradient(180deg, #f2f2f2 0 90px, transparent 90px 170px); }
.kenar { position:absolute; top:0; bottom:0; width:8px; background:#e9c43b; }
.direk { position:absolute; top:880px; bottom:0; width:30px;
  background: linear-gradient(90deg, #6d7276, #c9ced2 40%, #7c8185); box-shadow: 0 0 20px rgba(0,0,0,.35); }
.tabela { position:absolute; top:240px; left:80px; width:920px; padding:16px; border-radius:26px;
  background:$renk; box-shadow: 0 30px 60px rgba(0,0,0,.4); }
.ic { border:6px solid #fff; border-radius:16px; padding:34px 46px 30px; color:#fff;
  font-family:"Archivo"; font-stretch:72%; }
.ic .logo { margin: 0 auto; }
.cizgi { height:5px; background:#fff; margin:28px -46px; }
.sira { display:flex; align-items:center; gap:36px; }
.sira svg { flex:none; }
.sira .yazi .ust { font-size:54px; font-weight:800; letter-spacing:.04em; line-height:1; }
.sira .yazi .saat { font-size:112px; font-weight:800; line-height:1; margin-top:8px; }
.alt { display:flex; justify-content:space-between; font-size:52px; font-weight:800; letter-spacing:.04em; }
""", renk=renk)
    ok = '<svg width="150" height="190" viewBox="0 0 150 190"><polygon points="75,0 150,80 100,80 100,190 50,190 50,80 0,80" fill="#fff"/></svg>'
    govde = f"""{zemin}
<div class="direk" style="left:290px"></div><div class="direk" style="left:760px"></div>
<div class="tabela"><div class="ic">
  {logo(470)}
  <div class="cizgi"></div>
  <div class="sira">{ok}<div class="yazi"><div class="ust">AÇIK</div><div class="saat">10:00 – 19:00</div></div></div>
  <div class="cizgi"></div>
  <div class="alt"><span>HER GÜN</span><span>PZT – PAZ</span></div>
</div></div>"""
    return css, govde


# --- Neon ---------------------------------------------------------------------

def tugla(zemin, harc):
    return f"""<svg class="katman" width="1080" height="1920" style="position:absolute;inset:0">
<defs><pattern id="tugla" width="132" height="66" patternUnits="userSpaceOnUse">
<rect width="132" height="66" fill="{harc}"/>
<rect x="3" y="3" width="126" height="27" rx="3" fill="{zemin}"/>
<rect x="-63" y="36" width="126" height="27" rx="3" fill="{zemin}"/>
<rect x="69" y="36" width="126" height="27" rx="3" fill="{zemin}"/>
</pattern></defs><rect width="1080" height="1920" fill="url(#tugla)"/></svg>"""


def neon(v):
    renk, cekirdek = [("#ff3d6e", "#ffe6ee"), ("#ffb347", "#fff3df"), ("#38c8ff", "#e6f8ff")][v]
    if v == 1:
        zemin = tam("ic", stil="filter:brightness(.32) saturate(.9)")
    else:
        zemin = tugla(["#2a1a1d", "", "#14223a"][v], ["#140c0e", "", "#0a1222"][v])
    css = t("""
.vinyet { background: radial-gradient(70% 55% at 50% 45%, transparent 30%, rgba(0,0,0,.65)); }
.isik { color:$cek; text-shadow: 0 0 4px #fff, 0 0 12px $r, 0 0 28px $r, 0 0 60px $r, 0 0 110px $r; }
.cerceve { position:absolute; top:330px; left:110px; width:860px; height:1200px; border-radius:60px;
  border:5px solid $cek; box-shadow: 0 0 10px #fff, 0 0 24px $r, 0 0 60px $r, inset 0 0 24px $r, inset 0 0 60px $r; }
.logo-n { position:absolute; top:205px; left:50%; transform:translateX(-50%);
  filter: drop-shadow(0 0 6px $r) drop-shadow(0 0 22px $r); }
.yazi { position:absolute; left:0; right:0; text-align:center; }
.acik { top:420px; font-family:"Sacramento"; font-size:300px; line-height:1; }
.saat { font-family:"Monoton"; font-size:150px; line-height:1; letter-spacing:.02em; }
.her { top:1400px; font-family:"Montserrat"; font-weight:300; font-size:44px; letter-spacing:.5em; padding-left:.5em; }
""", r=renk, cek=cekirdek)
    govde = f"""{zemin}
<div class="katman vinyet"></div>
<div class="logo-n">{logo(400, cekirdek)}</div>
<div class="cerceve"></div>
<div class="yazi isik acik">Açığız</div>
<div class="yazi isik saat" style="top:850px">10:00</div>
<div class="yazi isik saat" style="top:1080px">19:00</div>
<div class="yazi isik her">HER GÜN</div>"""
    return css, govde


# --- Uçuş panosu (split-flap) --------------------------------------------------

def karolar(metin, cls="k"):
    return "".join(f'<i class="{cls}">{c if c != " " else "&nbsp;"}</i>' for c in metin)


def ucus_panosu(v):
    tema = [
        dict(zemin="#0b0b0b", yazi="#f6c431", ince="#8a8a8a", pano="#141414", karo="#1e1e1e"),
        dict(zemin="", yazi="#ffffff", ince="#bcbcbc", pano="rgba(12,12,12,.88)", karo="#202020"),
        dict(zemin=P["bordo"]["bg"], yazi="#efe6d6", ince="rgba(239,230,214,.6)", pano="#2a0a10", karo="#3a1219"),
    ][v]
    foto = tam("yaz") if v == 1 else ""
    pano_ust = 1100 if v == 1 else 700
    css = t("""
.story { background:$zemin; }
.k, .bk { display:inline-flex; align-items:center; justify-content:center; position:relative;
  font-family:"SpaceMono"; font-weight:700; font-style:normal; color:$yazi;
  background: linear-gradient(180deg, $karo 0 49%, #000 49% 51%, $karo 51%); border-radius:5px; }
.k { width:30px; height:46px; font-size:30px; margin-right:3px; }
.bk { width:82px; height:124px; font-size:86px; margin-right:6px; border-radius:9px; }
.logo { position:absolute; top:205px; left:50%; transform:translateX(-50%); }
.hero { position:absolute; top:${hu}px; left:0; right:0; display:flex; justify-content:center; gap:44px; }
.hero .grup .ad { font-family:"Montserrat"; font-size:22px; font-weight:600; letter-spacing:.4em; color:$ince; margin-bottom:12px; }
.pano { position:absolute; top:${pu}px; left:50%; transform:translateX(-50%); width:900px;
  background:$pano; border-radius:18px; padding:26px 30px 30px; box-shadow:0 30px 70px rgba(0,0,0,.45); }
.pano .baslik { font-family:"Montserrat"; font-weight:700; font-size:26px; letter-spacing:.35em; color:$yazi; margin-bottom:18px; }
.basliklar, .satir { display:flex; align-items:center; }
.basliklar span { font-family:"Montserrat"; font-size:16px; font-weight:600; letter-spacing:.25em; color:$ince; }
.satir { margin-top:10px; }
.satir .bosluk { width:16px; }
.durum .k { color:#5ee08a; }
.alt { position:absolute; top:1330px; left:0; right:0; text-align:center; font-family:"Montserrat";
  font-size:26px; font-weight:600; letter-spacing:.38em; padding-left:.38em; color:$yazi; }
""", pu=pano_ust, hu=420 if v == 1 else 470, **tema)
    satirlar = ""
    for g in GUNLER_B:
        satirlar += (f'<div class="satir">{karolar(g.ljust(9))}<span class="bosluk"></span>{karolar("10:00")}'
                     f'<span class="bosluk"></span>{karolar("19:00")}<span class="bosluk"></span>'
                     f'<span class="durum">{karolar("AÇIK")}</span></div>')
    basliklar = ('<div class="basliklar"><span style="width:315px">GÜN</span><span style="width:181px">AÇILIŞ</span>'
                 '<span style="width:181px">KAPANIŞ</span><span>DURUM</span></div>')
    alt = "" if v == 1 else '<div class="alt">HAFTANIN HER GÜNÜ AÇIĞIZ</div>'
    govde = f"""{foto}
{logo(400, "#fff" if v != 2 else "#efe6d6")}
<div class="hero">
  <div class="grup"><div class="ad">AÇILIŞ</div>{karolar("10:00", "bk")}</div>
  <div class="grup"><div class="ad">KAPANIŞ</div>{karolar("19:00", "bk")}</div>
</div>
<div class="pano"><div class="baslik">ÇALIŞMA SAATLERİ</div>{basliklar}{satirlar}</div>
{alt}"""
    return css, govde


# --- LED (7 segment) saat ------------------------------------------------------

SEG = {"0": "abcdef", "1": "bc", "9": "abcdfg"}


def led(metin, h, renk, sonuk):
    """7 segmentli LED göstergesi (SVG)."""
    w, t_, bos = h * 0.52, h * 0.1, h * 0.13
    parcalar, x = [], 0.0
    for c in metin:
        if c == ":":
            for cy in (h * 0.32, h * 0.7):
                parcalar.append(f'<rect x="{x + t_ * .2:.1f}" y="{cy - t_ / 2:.1f}" width="{t_:.1f}" height="{t_:.1f}" rx="2" fill="{renk}"/>')
            x += t_ * 1.4 + bos
            continue
        acik = SEG[c]
        yarim = t_ / 2
        # Yatay ve dikey segment çokgenleri
        def yatay(y):
            return f"{x + yarim:.1f},{y:.1f} {x + t_:.1f},{y - yarim:.1f} {x + w - t_:.1f},{y - yarim:.1f} {x + w - yarim:.1f},{y:.1f} {x + w - t_:.1f},{y + yarim:.1f} {x + t_:.1f},{y + yarim:.1f}"

        def dikey(xx, y0, y1):
            return f"{xx:.1f},{y0 + yarim:.1f} {xx + yarim:.1f},{y0 + t_:.1f} {xx + yarim:.1f},{y1 - t_:.1f} {xx:.1f},{y1 - yarim:.1f} {xx - yarim:.1f},{y1 - t_:.1f} {xx - yarim:.1f},{y0 + t_:.1f}"

        seg = {
            "a": yatay(yarim), "g": yatay(h / 2), "d": yatay(h - yarim),
            "f": dikey(x + yarim, yarim, h / 2), "e": dikey(x + yarim, h / 2, h - yarim),
            "b": dikey(x + w - yarim, yarim, h / 2), "c": dikey(x + w - yarim, h / 2, h - yarim),
        }
        for ad, nokta in seg.items():
            parcalar.append(f'<polygon points="{nokta}" fill="{renk if ad in acik else sonuk}"/>')
        x += w + bos
    gen = x - bos
    return (f'<svg width="{gen:.0f}" height="{h:.0f}" viewBox="0 0 {gen:.1f} {h:.1f}" '
            f'style="overflow:visible;transform:skewX(-6deg);filter:drop-shadow(0 0 10px {renk}) drop-shadow(0 0 26px {renk}88)">'
            + "".join(parcalar) + "</svg>")


def led_saat(v):
    renk = ["#ff3030", "#3dff7c", "#ffb000"][v]
    sonuk = "rgba(255,255,255,.05)"
    zemin = tam("gb", stil="filter:brightness(.3)") if v == 2 else ""
    css = t("""
.story { background: radial-gradient(100% 70% at 50% 40%, #1b1b1b, #050505); }
.logo { position:absolute; top:205px; left:50%; transform:translateX(-50%); }
.cihaz { position:absolute; top:470px; left:90px; width:900px; padding:50px 0 54px; border-radius:34px;
  background: linear-gradient(180deg, #161616, #0b0b0b); border:2px solid #2c2c2c;
  box-shadow: inset 0 2px 0 rgba(255,255,255,.06), 0 30px 80px rgba(0,0,0,.6);
  display:flex; flex-direction:column; align-items:center; }
.etiket { font-family:"VT323"; font-size:46px; letter-spacing:.2em; color:$r; opacity:.85; margin-bottom:22px;
  text-shadow: 0 0 10px $r; }
.ayrac { width:760px; height:2px; background:#262626; margin:46px 0 40px; }
.alt { position:absolute; top:1300px; left:0; right:0; text-align:center; font-family:"VT323";
  font-size:64px; letter-spacing:.18em; color:$r; text-shadow: 0 0 12px $r; }
""", r=renk)
    govde = f"""{zemin}
{logo(400)}
<div class="cihaz">
  <div class="etiket">AÇILIŞ</div>{led("10:00", 210, renk, sonuk)}
  <div class="ayrac"></div>
  <div class="etiket">KAPANIŞ</div>{led("19:00", 210, renk, sonuk)}
</div>
<div class="alt">HER GÜN · PZT-PAZ</div>"""
    return css, govde


# --- Kapı tabelası (AÇIĞIZ) ---------------------------------------------------

def kapi_tabelasi(v):
    css = """
.karartma { background: linear-gradient(180deg, rgba(10,8,6,.55), rgba(10,8,6,.2) 40%, rgba(10,8,6,.5)); }
.ip { position:absolute; top:150px; left:540px; width:3px; background:#d9c39b; transform-origin:top center; }
.kanca { position:absolute; top:136px; left:526px; width:30px; height:30px; border-radius:50%; border:6px solid #d9c39b; }
.tabela { position:absolute; top:560px; left:150px; width:780px; padding:24px; border-radius:28px;
  background: linear-gradient(160deg, #9b2234, #6e1422); transform: rotate(-2.5deg);
  box-shadow: 0 40px 70px rgba(0,0,0,.5); }
.tabela .ic { border:3px solid rgba(239,230,214,.7); border-radius:18px; padding:46px 40px 50px;
  display:flex; flex-direction:column; align-items:center; color:#efe6d6; }
.tabela .ust { font-family:"Montserrat"; font-weight:600; font-size:24px; letter-spacing:.45em; padding-left:.45em; }
.tabela .buyuk { font-family:"DMSerif"; font-size:200px; line-height:1; margin:14px 0 6px; }
.tabela .saat { font-family:"Montserrat"; font-weight:700; font-size:72px; letter-spacing:-.01em; }
.tabela .her { margin-top:22px; font-family:"DMSerif"; font-style:italic; font-size:48px; }
.delik { position:absolute; top:22px; width:22px; height:22px; border-radius:50%; background:#2a0a10; box-shadow: inset 0 2px 4px rgba(0,0,0,.6); }
.logo { position:absolute; top:1420px; left:50%; transform:translateX(-50%); }
"""
    govde = f"""{tam("ic")}
<div class="katman karartma"></div>
<div class="kanca"></div>
<div class="ip" style="height:470px;transform:rotate(36deg)"></div>
<div class="ip" style="height:470px;transform:rotate(-36deg)"></div>
<div class="tabela">
  <div class="delik" style="left:250px"></div><div class="delik" style="right:250px"></div>
  <div class="ic">
    <div class="ust">HOŞ GELDİNİZ</div>
    <div class="buyuk">Açığız</div>
    <div class="saat">10:00 – 19:00</div>
    <div class="her">Haftanın her günü</div>
  </div>
</div>
{logo(420)}"""
    return css, govde


# --- Fiyat etiketi (askılı etiket) --------------------------------------------

def barkod(gen, yuk, renk, tohum=7):
    x, cubuk, r = 0, [], tohum
    while x < gen:
        r = (r * 1103515245 + 12345) & 0x7FFFFFFF
        w = 2 + r % 5
        if (r >> 8) % 3:
            cubuk.append(f'<rect x="{x}" y="0" width="{w}" height="{yuk}" fill="{renk}"/>')
        x += w + 2
    return f'<svg width="{gen}" height="{yuk}" viewBox="0 0 {gen} {yuk}">{"".join(cubuk)}</svg>'


def fiyat_etiketi(v):
    tema = [
        dict(kagit="linear-gradient(170deg,#d2b083,#b98f5f)", yazi="#2a1a10", vurgu="#5c111c", zemin=tam("ic", stil="filter:brightness(.45)")),
        dict(kagit="linear-gradient(170deg,#9b2234,#6e1422)", yazi="#efe6d6", vurgu="#ffffff", zemin=""),
        dict(kagit="linear-gradient(170deg,#1f1c19,#0e0d0c)", yazi="#e6d2a6", vurgu="#ffffff", zemin=tam("gb", stil="filter:brightness(.55)")),
    ][v]
    css = t("""
.story { background: radial-gradient(90% 60% at 50% 40%, #f6efe2, #e3d5bc); }
.ip { position:absolute; top:0; left:0; }
.etiket { position:absolute; top:330px; left:250px; width:580px; height:1170px; transform: rotate(-5deg);
  background:$kagit; color:$yazi; filter: drop-shadow(0 34px 40px rgba(0,0,0,.45));
  clip-path: polygon(22% 0, 78% 0, 100% 11%, 100% 100%, 0 100%, 0 11%);
  display:flex; flex-direction:column; align-items:center; padding-top:170px; }
.etiket .delik { position:absolute; top:58px; left:50%; width:44px; height:44px; margin-left:-22px; border-radius:50%;
  background:#000; opacity:.55; }
.etiket .ust { font-family:"Montserrat"; font-weight:700; font-size:24px; letter-spacing:.4em; padding-left:.4em; }
.etiket .cizgi { width:380px; height:2px; background:currentColor; opacity:.4; margin:30px 0; }
.etiket .rakam { font-family:"Bodoni"; font-weight:700; font-size:190px; line-height:.95; letter-spacing:-.02em; }
.etiket .tire { width:70px; height:5px; background:$vurgu; margin:18px 0 22px; }
.etiket .her { font-family:"Bodoni"; font-style:italic; font-size:54px; margin-top:16px; }
.etiket .barkod { margin-top:44px; opacity:.85; }
.etiket .kod { font-family:"SpaceMono"; font-size:20px; letter-spacing:.3em; margin-top:10px; }
""", **tema)
    ip = ('<svg class="ip" width="1080" height="1920"><path d="M 560 0 C 540 160, 600 260, 552 392" '
          'fill="none" stroke="#e8e0d0" stroke-width="5"/></svg>')
    govde = f"""{tema["zemin"]}
{ip}
<div class="etiket">
  <div class="delik"></div>
  {ikon(110, tema["yazi"])}
  <div class="ust" style="margin-top:34px">ÇALIŞMA SAATLERİ</div>
  <div class="cizgi"></div>
  <div class="rakam">10:00</div>
  <div class="tire"></div>
  <div class="rakam">19:00</div>
  <div class="her">her gün</div>
  <div class="barkod">{barkod(360, 90, tema["yazi"])}</div>
  <div class="kod">İMOTİM · 7/7</div>
</div>"""
    return css, govde


KAVRAMLAR = [
    ("otoyol-tabelasi", otoyol, 3),
    ("neon", neon, 3),
    ("ucus-panosu", ucus_panosu, 3),
    ("led-saat", led_saat, 3),
    ("kapi-tabelasi", kapi_tabelasi, 1),
    ("fiyat-etiketi", fiyat_etiketi, 3),
]
