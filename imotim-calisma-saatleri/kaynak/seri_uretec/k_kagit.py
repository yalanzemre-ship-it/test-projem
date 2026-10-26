"""Kağıt/basılı malzeme temalı konseptler: fiş, bilet, takvim yaprağı, post-it, davetiye, posta pulu, gazete."""

from string import Template

from .k_tabela import barkod
from .temel import BINA, GUNLER_B, P, foto, ikon, logo, tam


def t(css, **kw):
    return Template(css).substitute(**kw)


def bulanik(k, parlaklik=.6):
    return tam(k, stil=f"filter:blur(36px) brightness({parlaklik}) saturate(1.1);transform:scale(1.12)")


def zikzak(gen, yuk, dis=22, derin=11):
    """Üstü ve altı tırtıklı kağıt için clip-path çokgeni."""
    n = int(gen // dis)
    ust = [f"{i * gen / n:.1f}px {0 if i % 2 == 0 else derin}px" for i in range(n + 1)]
    alt = [f"{(n - i) * gen / n:.1f}px {yuk - (0 if i % 2 == 0 else derin)}px" for i in range(n + 1)]
    return "polygon(" + ", ".join(ust + alt) + ")"


# --- Fiş ----------------------------------------------------------------------

def fis(v):
    zemin = ["", bulanik("ic", .55), ""][v]
    bg = [P["bordo"]["bg"], "#000", P["krem"]["bg2"]][v]
    aci = [0, -2, 2][v]
    css = t("""
.story { background:$bg; }
.desen { background-image: radial-gradient(rgba(255,255,255,.07) 2px, transparent 2.5px); background-size: 26px 26px; }
.fis { position:absolute; top:260px; left:180px; width:720px; height:1200px; background:#fbfaf6;
  clip-path:$zz; transform: rotate(${aci}deg); padding:64px 56px; color:#1f1f1f;
  font-family:"SpaceMono"; font-size:27px; line-height:1.5; }
.golge { position:absolute; top:280px; left:190px; width:720px; height:1200px; background:rgba(0,0,0,.35);
  filter: blur(22px); transform: rotate(${aci}deg); }
.fis .logo { margin: 0 auto 24px; }
.orta { text-align:center; }
.kesik { border-top: 3px dashed #444; margin: 18px 0; }
.cift { border-top: 3px double #222; border-bottom: 3px double #222; height:9px; margin: 18px 0; }
.satir { display:flex; justify-content:space-between; }
.kalin { font-weight:700; }
.barkod { display:flex; justify-content:center; margin-top:16px; }
""", bg=bg, zz=zikzak(720, 1200), aci=aci)
    satirlar = "".join(f'<div class="satir"><span>{g}</span><span>10:00-19:00</span></div>' for g in GUNLER_B)
    desen = '<div class="katman desen"></div>' if v == 0 else ""
    govde = f"""{zemin}{desen}
<div class="golge"></div>
<div class="fis">
  {logo(360, "#1f1f1f")}
  <div class="orta kalin">ÇALIŞMA SAATLERİ</div>
  <div class="orta">HAFTALIK PROGRAM</div>
  <div class="kesik"></div>
  <div class="satir kalin"><span>GÜN</span><span>SAAT</span></div>
  {satirlar}
  <div class="kesik"></div>
  <div class="satir kalin"><span>TOPLAM</span><span>7 GÜN AÇIK</span></div>
  <div class="cift"></div>
  <div class="orta">* PAZAR DAHİL HER GÜN *</div>
  <div class="barkod">{barkod(420, 80, "#1f1f1f", 11)}</div>
  <div class="orta" style="margin-top:14px">SİZLERİ BEKLİYORUZ</div>
</div>"""
    return css, govde


# --- Bilet --------------------------------------------------------------------

def bilet(v):
    k, sayfa_bg = [("gb", P["lacivert"]["bg"]), ("yaz", P["bordo"]["bg"]), ("ic", P["zeytin"]["bg"])][v]
    cx, cy = BINA[k]
    css = t("""
.story { background: radial-gradient(90% 60% at 50% 30%, ${bg}, #000 160%); }
.bilet { position:absolute; top:300px; left:110px; width:860px; border-radius:34px; overflow:hidden;
  background:#f6f0e4; color:#1b1b1b; box-shadow: 0 40px 80px rgba(0,0,0,.45); }
.govde { padding:36px 56px 30px; }
.ust { display:flex; justify-content:space-between; align-items:center; }
.ust .tur { font-family:"Montserrat"; font-weight:700; font-size:22px; letter-spacing:.35em; color:#8a1b2b; }
.alanlar { display:grid; grid-template-columns:1fr 1fr; gap:26px 30px; margin-top:34px; }
.alan .ad { font-family:"Montserrat"; font-size:18px; font-weight:600; letter-spacing:.3em; color:#8a7c6c; }
.alan .deger { font-family:"Montserrat"; font-size:40px; font-weight:700; margin-top:6px; }
.alan .deger.buyuk { font-size:84px; font-weight:800; letter-spacing:-.02em; line-height:1; }
.delikli { position:relative; height:0; border-top:4px dashed #cbbfa9; margin:6px 40px 0; }
.delikli::before, .delikli::after { content:""; position:absolute; top:-30px; width:56px; height:56px; border-radius:50%; background:${bg}; }
.delikli::before { left:-70px; } .delikli::after { right:-70px; }
.kocan { display:flex; align-items:center; justify-content:space-between; padding:30px 56px 36px; }
.kocan .yazi { font-family:"SpaceMono"; font-size:22px; letter-spacing:.12em; line-height:1.5; }
""", bg=sayfa_bg)
    govde = f"""
<div class="bilet">
  {foto(k, 860, 420, cx, cy)}
  <div class="govde">
    <div class="ust">{logo(330, "#1b1b1b")}<span class="tur">GİRİŞ KARTI</span></div>
    <div class="alanlar">
      <div class="alan"><div class="ad">NEREDEN</div><div class="deger">Evinizden</div></div>
      <div class="alan"><div class="ad">NEREYE</div><div class="deger">İmotim AVM</div></div>
      <div class="alan"><div class="ad">AÇILIŞ</div><div class="deger buyuk">10:00</div></div>
      <div class="alan"><div class="ad">KAPANIŞ</div><div class="deger buyuk">19:00</div></div>
      <div class="alan"><div class="ad">GEÇERLİLİK</div><div class="deger">Her gün</div></div>
      <div class="alan"><div class="ad">GÜNLER</div><div class="deger">Pzt – Paz</div></div>
    </div>
  </div>
  <div class="delikli"></div>
  <div class="kocan">{barkod(400, 86, "#1b1b1b", 3)}<div class="yazi">İMOTİM<br>10:00-19:00<br>7/7</div></div>
</div>"""
    return css, govde


# --- Takvim yaprağı -------------------------------------------------------------

def takvim(v):
    tema = [
        dict(zemin="", bg=P["krem"]["bg2"], bas="#8a1b2b", sayfa="#fffdf8", yazi="#1b1717", rakam="#8a1b2b", logo_r="#1b1717"),
        dict(zemin=bulanik("yaz", .7), bg="#000", bas="#0f2340", sayfa="#ffffff", yazi="#0f2340", rakam="#0f2340", logo_r="#ffffff"),
        dict(zemin="", bg=P["antrasit"]["bg"], bas="#b8925a", sayfa="#f3ead9", yazi="#171513", rakam="#171513", logo_r="#d9c39b"),
    ][v]
    css = t("""
.story { background:$bg; }
.yaprak { position:absolute; left:130px; width:820px; height:1130px; border-radius:22px; background:$sayfa;
  box-shadow: 0 30px 60px rgba(0,0,0,.25); }
.arka1 { top:428px; transform: rotate(2.4deg); opacity:.9; }
.arka2 { top:420px; transform: rotate(-1.6deg); opacity:.95; }
.on { top:410px; overflow:hidden; display:flex; flex-direction:column; align-items:center; }
.bas { width:100%; height:150px; background:$bas; display:flex; align-items:flex-end; justify-content:center; padding-bottom:30px;
  font-family:"Montserrat"; font-weight:800; font-size:46px; letter-spacing:.42em; padding-left:.42em; color:#fff; }
.halka { position:absolute; top:-26px; width:34px; height:72px; border-radius:17px; background: linear-gradient(90deg,#8d8d8d,#e8e8e8,#8d8d8d); }
.rakam { font-family:"Abril"; font-size:520px; line-height:1; color:$rakam; margin-top:6px; }
.alt1 { font-family:"Montserrat"; font-weight:800; font-size:60px; letter-spacing:.12em; color:$yazi; margin-top:-36px; }
.cizgi { width:560px; height:3px; background:$yazi; opacity:.15; margin:38px 0 30px; }
.saat { font-family:"Montserrat"; font-weight:700; font-size:92px; color:$yazi; letter-spacing:-.01em; }
.gunler { font-family:"Montserrat"; font-weight:600; font-size:24px; letter-spacing:.4em; color:$yazi; opacity:.65; margin-top:16px; }
.logo { position:absolute; top:205px; left:50%; transform:translateX(-50%); }
""", **tema)
    halkalar = "".join(f'<div class="halka" style="left:{x}px"></div>' for x in (170, 300, 486, 616))
    govde = f"""{tema["zemin"]}
{logo(380, tema["logo_r"])}
<div class="yaprak arka1"></div><div class="yaprak arka2"></div>
<div class="yaprak on">
  <div class="bas">HAFTANIN</div>
  <div class="rakam">7</div>
  <div class="alt1">GÜNÜ AÇIĞIZ</div>
  <div class="cizgi"></div>
  <div class="saat">10:00 – 19:00</div>
  <div class="gunler">PAZARTESİ – PAZAR</div>
</div>
<div style="position:absolute;top:410px;left:130px;width:820px">{halkalar}</div>"""
    return css, govde


# --- Post-it ------------------------------------------------------------------

def postit(v):
    if v == 0:
        zemin = '<div class="katman mantar"></div>'
        logo_r = "#3b2414"
    elif v == 1:
        zemin = tam("ic", stil="filter:brightness(.62)")
        logo_r = "#ffffff"
    else:
        zemin = '<div class="katman defter"></div>'
        logo_r = "#22303f"
    css = """
.mantar { background-color:#b88a5a;
  background-image: radial-gradient(rgba(70,40,15,.35) 1.5px, transparent 2px), radial-gradient(rgba(255,230,190,.25) 1px, transparent 1.6px);
  background-size: 11px 13px, 17px 15px; background-position: 0 0, 5px 7px; }
.defter { background-color:#f7f4ec;
  background-image: linear-gradient(90deg, transparent 118px, rgba(200,60,60,.45) 118px 121px, transparent 121px),
    linear-gradient(rgba(70,110,170,.22) 2px, transparent 2px); background-size: 100% 100%, 100% 54px; }
.not { position:absolute; padding:70px 50px 40px; font-family:"Caveat"; color:#2b2420;
  box-shadow: 0 22px 34px rgba(0,0,0,.28), inset 0 -30px 40px rgba(0,0,0,.04); }
.not::after { content:""; position:absolute; top:-14px; left:50%; width:44px; height:44px; margin-left:-22px; border-radius:50%;
  background: radial-gradient(circle at 35% 30%, #ff8a8a, #c41d2e 55%, #7a0f19); box-shadow: 0 6px 8px rgba(0,0,0,.35); }
.sari { left:120px; top:410px; width:680px; height:680px; background:#ffe46b; transform: rotate(-3deg); }
.pembe { left:560px; top:1090px; width:420px; height:420px; background:#ffb4c8; transform: rotate(5deg); }
.mavi { left:110px; top:1170px; width:400px; height:400px; background:#b5e0ff; transform: rotate(-6deg); }
.sari .k1 { font-size:64px; font-weight:600; }
.sari .k2 { font-size:150px; font-weight:700; line-height:1; margin-top:20px; }
.sari .k3 { font-size:72px; font-weight:600; margin-top:24px; }
.pembe, .mavi { font-size:70px; font-weight:700; line-height:1.05; }
.logo { position:absolute; top:205px; left:50%; transform:translateX(-50%); }
"""
    govde = f"""{zemin}
{logo(400, logo_r)}
<div class="not sari"><div class="k1">Unutma! 📌</div><div class="k2">10:00 – 19:00</div><div class="k3">İmotim her gün açık ✓</div></div>
<div class="not mavi">Sizi<br>bekliyoruz ♥</div>
<div class="not pembe">Pazar<br>da açık! 😊</div>"""
    return css, govde


# --- Davetiye -----------------------------------------------------------------

def davetiye(v):
    tema = [
        dict(zemin="", bg=P["bordo"]["bg"], kart="#f6efe1", yazi="#3a1d1f", altin="#b8925a", logo_r="#3a1d1f"),
        dict(zemin="", bg="#0c0b0a", kart="#151311", yazi="#efe2c6", altin="#c9a86a", logo_r="#d9c39b"),
        dict(zemin=bulanik("ic", .55), bg="#000", kart="#ffffff", yazi="#5c111c", altin="#8a1b2b", logo_r="#5c111c"),
    ][v]
    css = t("""
.story { background:$bg; }
.kart { position:absolute; top:300px; left:110px; width:860px; height:1180px; background:$kart; color:$yazi;
  box-shadow: 0 40px 90px rgba(0,0,0,.45); border:2px solid $altin; }
.kart::before { content:""; position:absolute; inset:18px; border:1px solid $altin; }
.kose { position:absolute; width:70px; height:70px; border:3px solid $altin; }
.icerik { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; padding-top:110px; }
.script { font-family:"GreatVibes"; font-size:132px; line-height:1; color:$altin; margin-top:60px; }
.ince { font-family:"Montserrat"; font-weight:600; font-size:24px; letter-spacing:.45em; padding-left:.45em; margin-top:46px; }
.saat { font-family:"Bodoni"; font-weight:500; font-size:116px; line-height:1; margin-top:22px; letter-spacing:-.01em; }
.sus { display:flex; align-items:center; gap:22px; color:$altin; margin:48px 0 38px; font-size:28px; }
.sus::before, .sus::after { content:""; width:150px; height:1.5px; background:$altin; }
.italik { font-family:"Bodoni"; font-style:italic; font-size:50px; }
""", **tema)
    koseler = "".join(
        f'<div class="kose" style="{y}:40px;{x}:40px;border-{"bottom" if y == "top" else "top"}:0;border-{"right" if x == "left" else "left"}:0"></div>'
        for y in ("top", "bottom") for x in ("left", "right"))
    govde = f"""{tema["zemin"]}
<div class="kart">{koseler}
  <div class="icerik">
    {logo(400, tema["logo_r"])}
    <div class="script">Sizi davet ediyoruz</div>
    <div class="ince">HAFTANIN HER GÜNÜ</div>
    <div class="saat">10:00 – 19:00</div>
    <div class="sus">✦</div>
    <div class="italik">Kapımız her gün açık.</div>
  </div>
</div>"""
    return css, govde


# --- Posta pulu ---------------------------------------------------------------

def posta_pulu(v):
    k = ["gb", "yaz", "ic"][v]
    zarf = ["#f1e8d6", "#ecd6cd", "#dde7ee"][v]
    cx, cy = BINA[k]
    css = t("""
.story { background:$zarf; }
.kenar { position:absolute; inset:0; border:34px solid transparent;
  border-image: repeating-linear-gradient(45deg, #b3202f 0 34px, $zarf 34px 52px, #1d3c78 52px 86px, $zarf 86px 104px) 34; }
.pul { position:absolute; top:360px; left:250px; width:580px; padding:14px; background:#fffdf7;
  -webkit-mask: radial-gradient(circle at center, transparent 9px, #000 9.5px) -14px -14px / 28px 28px,
                linear-gradient(#000 0 0) content-box;
  filter: drop-shadow(0 14px 16px rgba(0,0,0,.2)); }
.pul .ic { padding:14px 14px 8px; }
.pul .yazi { display:flex; justify-content:space-between; align-items:baseline; margin-top:14px; color:#5c111c; }
.pul .yazi .a { font-family:"DMSerif"; font-size:44px; }
.pul .yazi .b { font-family:"DMSerif"; font-size:60px; }
.damga { position:absolute; top:760px; left:600px; transform: rotate(-14deg); opacity:.82; }
.adres { position:absolute; top:1330px; left:150px; font-family:"Caveat"; font-size:68px; line-height:1.25; color:#24324a; }
.adres u { text-decoration-thickness:2px; text-underline-offset:10px; }
.logo { position:absolute; top:205px; left:120px; }
""", zarf=zarf)
    damga = """<svg width="330" height="330" viewBox="0 0 330 330">
<defs><path id="ust-yay" d="M 45 165 A 120 120 0 0 1 285 165"/></defs>
<circle cx="165" cy="165" r="150" fill="none" stroke="#1f2a44" stroke-width="5"/>
<circle cx="165" cy="165" r="104" fill="none" stroke="#1f2a44" stroke-width="3"/>
<text font-family="Montserrat" font-weight="700" font-size="24" letter-spacing="4" fill="#1f2a44">
<textPath href="#ust-yay" startOffset="50%" text-anchor="middle">İMOTİM MOBİLYA AVM</textPath></text>
<text x="165" y="158" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="46" fill="#1f2a44">10:00</text>
<text x="165" y="206" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="46" fill="#1f2a44">19:00</text>
<text x="165" y="292" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="22" letter-spacing="5" fill="#1f2a44">HER GÜN</text>
</svg>"""
    govde = f"""<div class="kenar"></div>
{logo(380, "#24324a")}
<div class="pul"><div class="ic">{foto(k, 524, 640, cx, cy)}
  <div class="yazi"><span class="a">İMOTİM</span><span class="b">7/7</span></div></div></div>
<div class="damga">{damga}</div>
<div class="adres">Kime: <u>Tüm misafirlerimize</u><br>Ne zaman: <u>Her gün 10:00 – 19:00</u></div>"""
    return css, govde


# --- Gazete -------------------------------------------------------------------

def gazete(v):
    k = ["gb", "yaz", "ic"][v]
    kagit = ["#f1ece1", "#efefea", "#e9dfc9"][v]
    vurgu = ["#171513", "#8a1b2b", "#3b2a1a"][v]
    filtre = "grayscale(1) contrast(1.05)" if v == 1 else "none"
    cx, cy = BINA[k]
    css = t("""
.story { background:$kagit; color:#1a1712; }
.story::after { content:""; position:absolute; inset:0; pointer-events:none; opacity:.5;
  background-image: radial-gradient(rgba(0,0,0,.05) 1px, transparent 1.4px); background-size: 5px 5px; }
.sayfa { position:absolute; top:200px; left:70px; right:70px; }
.kunye { display:flex; align-items:center; justify-content:center; gap:22px; }
.kunye .ad { font-family:"Playfair"; font-weight:900; font-size:104px; line-height:1; letter-spacing:-.01em; color:$vurgu; }
.cizgiler { border-top:4px solid #1a1712; border-bottom:1.5px solid #1a1712; height:9px; margin-top:16px; }
.tarih { display:flex; justify-content:space-between; font-family:"Montserrat"; font-weight:600; font-size:18px; letter-spacing:.22em;
  padding:12px 0; border-bottom:1.5px solid #1a1712; }
.manset { font-family:"Playfair"; font-weight:900; font-size:96px; line-height:1.02; margin-top:30px; letter-spacing:-.01em; }
.foto-k { margin-top:28px; filter:$filtre; }
.altyazi { font-family:"Fraunces"; font-style:italic; font-size:22px; margin-top:10px; color:#4a443a; }
.sutunlar { display:grid; grid-template-columns:1fr 1fr; gap:36px; margin-top:24px; font-family:"Fraunces"; font-size:30px; line-height:1.4; }
.sutunlar p::first-letter { font-family:"Playfair"; font-weight:900; font-size:76px; float:left; line-height:.8; margin:6px 8px 0 0; color:$vurgu; }
.kutu { margin-top:34px; background:$vurgu; color:$kagit; text-align:center; padding:20px; font-family:"Montserrat"; font-weight:800;
  font-size:34px; letter-spacing:.06em; }
""", kagit=kagit, vurgu=vurgu, filtre=filtre)
    govde = f"""<div class="sayfa">
  <div class="kunye">{ikon(92, vurgu)}<span class="ad">İMOTİM HABER</span></div>
  <div class="cizgiler"></div>
  <div class="tarih"><span>HER GÜN YAYINDA</span><span>SAYI: 7/7</span><span>10:00 – 19:00</span></div>
  <div class="manset">Haftanın 7 günü kapılarımız açık!</div>
  <div class="foto-k">{foto(k, 940, 560, cx, cy)}</div>
  <div class="altyazi">İmotim Mobilya AVM, her gün 10:00'dan 19:00'a kadar ziyaretçilerini bekliyor.</div>
  <div class="sutunlar">
    <p>İmotim Mobilya AVM pazartesiden pazara her gün saat 10:00'da kapılarını açıyor.</p>
    <p>Hafta içi ya da hafta sonu, mobilya alışverişinizi 19:00'a kadar dilediğiniz gün planlayabilirsiniz.</p>
  </div>
  <div class="kutu">HER GÜN 10:00 – 19:00</div>
</div>"""
    return css, govde


KAVRAMLAR = [
    ("fis", fis, 3),
    ("bilet", bilet, 3),
    ("takvim-yapragi", takvim, 3),
    ("post-it", postit, 3),
    ("davetiye", davetiye, 3),
    ("posta-pulu", posta_pulu, 3),
    ("gazete", gazete, 3),
]
