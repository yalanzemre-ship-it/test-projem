"""Fotoğraf ağırlıklı konseptler: polaroid, dergi kapağı, film şeridi, üçlü kemer, daire çerçeve,
müze duvarı, duotone, harita pini, uyarı bantları."""

from string import Template

from .k_tabela import barkod
from .temel import BINA, P, foto, ikon, logo, tam


def t(css, **kw):
    return Template(css).substitute(**kw)


# Tam ekran (1080x1920, %96 ölçek) fotoğraflarda binanın çatı orta noktası
CATI = {"gb": (662, 985), "yaz": (614, 960)}


# --- Polaroid -----------------------------------------------------------------

def polaroid(v):
    k = ["gb", "ic", "yaz"][v]
    zemin = [
        "background-color:#c9a77c; background-image: repeating-linear-gradient(12deg, rgba(90,60,25,.07) 0 2px, transparent 2px 9px), repeating-linear-gradient(-34deg, rgba(255,240,210,.08) 0 1px, transparent 1px 7px);",
        "background-color:#f1efea; background-image: repeating-linear-gradient(0deg, rgba(0,0,0,.035) 0 1px, transparent 1px 4px), repeating-linear-gradient(90deg, rgba(0,0,0,.035) 0 1px, transparent 1px 4px);",
        f"background: radial-gradient(90% 60% at 50% 35%, {P['bordo']['bg']}, {P['bordo']['bg2']});",
    ][v]
    yazi_r = ["#3b2414", "#2a2a2a", "#efe6d6"][v]
    cx, cy = BINA[k]
    css = t("""
.story { $zemin }
.kagit { position:absolute; width:800px; height:960px; background:#fbfbf8; box-shadow:0 20px 40px rgba(0,0,0,.25); }
.p { position:absolute; top:330px; left:140px; width:800px; padding:40px 40px 0; height:960px; background:#fdfdfb;
  box-shadow: 0 30px 50px rgba(0,0,0,.35); }
.p .yazi { font-family:"Caveat"; font-weight:700; font-size:78px; white-space:nowrap; color:#2b2b2b; text-align:center; margin-top:34px; }
.bant { position:absolute; top:296px; left:420px; width:240px; height:74px; background:rgba(236,224,196,.75);
  transform: rotate(-7deg); box-shadow: 0 2px 6px rgba(0,0,0,.12); }
.logo { position:absolute; top:200px; left:50%; transform:translateX(-50%); }
.alt { position:absolute; top:1350px; left:0; right:0; text-align:center; font-family:"Montserrat"; font-weight:600;
  font-size:26px; letter-spacing:.36em; padding-left:.36em; color:$yr; }
""", zemin=zemin, yr=yazi_r)
    govde = f"""
<div class="kagit" style="top:360px;left:150px;transform:rotate(6deg)"></div>
<div class="kagit" style="top:350px;left:130px;transform:rotate(-7deg)"></div>
{logo(380, yazi_r)}
<div class="p">{foto(k, 720, 720, cx, cy)}<div class="yazi">Her gün 10:00 – 19:00 ✓</div></div>
<div class="bant"></div>
<div class="alt">PAZARTESİ – PAZAR</div>"""
    return css, govde


# --- Dergi kapağı -------------------------------------------------------------

def dergi(v):
    k = ["gb", "yaz", "ic"][v]
    vurgu = ["#8a1b2b", "#d8a33a", "#efe6d6"][v]
    vurgu_yazi = ["#ffffff", "#1d1a16", "#5c111c"][v]
    css = t("""
.ust-g { background: linear-gradient(180deg, rgba(0,0,0,.45), rgba(0,0,0,0) 28%); }
.alt-g { background: linear-gradient(0deg, rgba(0,0,0,.78) 0%, rgba(0,0,0,.45) 26%, rgba(0,0,0,0) 48%); }
.kunye { position:absolute; top:170px; left:80px; filter: drop-shadow(0 4px 20px rgba(0,0,0,.3)); }
.sayi { position:absolute; top:520px; right:80px; text-align:right; font-family:"Montserrat"; font-weight:700; font-size:24px;
  letter-spacing:.3em; color:#fff; text-shadow:0 2px 10px rgba(0,0,0,.5); }
.rozet { position:absolute; top:600px; right:90px; width:220px; height:220px; border-radius:50%; background:$vurgu; color:$vy;
  display:flex; flex-direction:column; align-items:center; justify-content:center; transform: rotate(10deg);
  font-family:"Montserrat"; font-weight:800; font-size:30px; line-height:1.15; text-align:center; box-shadow:0 14px 30px rgba(0,0,0,.35); }
.manset { position:absolute; left:80px; bottom:380px; color:#fff; }
.manset .k1 { font-family:"Montserrat"; font-weight:600; font-size:34px; letter-spacing:.4em; }
.manset .k2 { font-family:"Playfair"; font-weight:900; font-size:150px; line-height:.95; margin-top:10px; }
.manset .k3 { font-family:"Playfair"; font-style:italic; font-weight:500; font-size:150px; line-height:.95; }
.manset .kutu { display:inline-block; margin-top:28px; padding:14px 26px; background:$vurgu; color:$vy;
  font-family:"Montserrat"; font-weight:800; font-size:64px; letter-spacing:-.01em; }
.barkod { position:absolute; right:80px; bottom:300px; background:#fff; padding:12px 14px 8px; text-align:center;
  font-family:"SpaceMono"; font-size:14px; color:#111; }
""", vurgu=vurgu, vy=vurgu_yazi)
    govde = f"""{tam(k)}
<div class="katman ust-g"></div><div class="katman alt-g"></div>
<div class="kunye">{logo(920)}</div>
<div class="sayi">SAYI 7/7 · HER GÜN</div>
<div class="rozet">PAZAR<br>DA<br>AÇIK!</div>
<div class="manset">
  <div class="k1">HAFTANIN</div>
  <div class="k2">Her Günü</div>
  <div class="k3">Açığız</div>
  <div class="kutu">10:00 – 19:00</div>
</div>
<div class="barkod">{barkod(150, 70, "#111", 5)}<div>İMOTİM</div></div>"""
    return css, govde


# --- Film şeridi --------------------------------------------------------------

def film(v):
    sira = [["gb", "ic", "yaz"], ["yaz", "gb", "ic"], ["ic", "yaz", "gb"]][v]
    tema = [P["krem"], P["bordo"], P["antrasit"]][v]
    css = t("""
.story { background:$bg; color:$fg; }
.serit { position:absolute; top:-20px; left:70px; width:540px; height:1960px; background:#121212; }
.delikler { position:absolute; top:0; bottom:0; width:30px;
  background-image: linear-gradient(#efe6d6, #efe6d6); background-size: 22px 30px; }
.kare { position:absolute; left:60px; }
.isaret { position:absolute; left:16px; font-family:"SpaceMono"; font-weight:700; font-size:16px; letter-spacing:.2em;
  color:#e0a92e; writing-mode: vertical-rl; }
.sag { position:absolute; top:210px; left:650px; width:370px; }
.sag .ince { font-family:"Montserrat"; font-weight:600; font-size:22px; letter-spacing:.32em; color:$ince; }
.sag .rakam { font-family:"Bebas"; font-size:220px; line-height:.86; }
.sag .ayrac { width:120px; height:6px; background:$vurgu; margin:34px 0; }
.sag .her { font-family:"Fraunces"; font-style:italic; font-size:60px; line-height:1.05; margin-top:30px; }
""", **tema)
    delik = "".join(
        f'<div style="position:absolute;top:{y}px;left:{x}px;width:24px;height:32px;border-radius:5px;background:{tema["bg"]}"></div>'
        for y in range(10, 1960, 64) for x in (12, 504))
    kareler = "".join(
        f'<div class="kare" style="top:{80 + i * 600}px">{foto(k, 420, 560, *BINA[k])}</div>' for i, k in enumerate(sira))
    isaretler = "".join(f'<div class="isaret" data-serbest style="top:{120 + i * 600}px">İMOTİM 7/7 ▸ {i + 1:02d}</div>' for i in range(3))
    govde = f"""
<div class="serit">{delik}{kareler}{isaretler}</div>
<div class="sag">
  {logo(360, tema["fg"])}
  <div class="ince" style="margin-top:80px">ÇALIŞMA SAATLERİ</div>
  <div class="ayrac"></div>
  <div class="ince">AÇILIŞ</div><div class="rakam">10:00</div>
  <div class="ince" style="margin-top:40px">KAPANIŞ</div><div class="rakam">19:00</div>
  <div class="her">Haftanın<br>her günü</div>
</div>"""
    return css, govde


# --- Üçlü kemer ---------------------------------------------------------------

def uc_kemer(v):
    sira = [["gb", "ic", "yaz"], ["ic", "yaz", "gb"], ["yaz", "gb", "ic"]][v]
    tema = [P["krem"], P["bordo"], P["antrasit"]][v]
    css = t("""
.story { background:$bg; color:$fg; }
.logo { position:absolute; top:200px; left:50%; transform:translateX(-50%); }
.baslik { position:absolute; top:430px; left:0; right:0; text-align:center; font-family:"Fraunces"; font-style:italic;
  font-weight:400; font-size:104px; line-height:1; }
.kemer { position:absolute; top:620px; width:300px; height:560px; border-radius:150px 150px 0 0; overflow:hidden; }
.alt { position:absolute; top:1230px; left:0; right:0; display:flex; flex-direction:column; align-items:center; }
.alt .ince { font-family:"Montserrat"; font-weight:600; font-size:24px; letter-spacing:.42em; padding-left:.42em; color:$ince; }
.alt .saat { font-family:"Fraunces"; font-weight:600; font-size:136px; line-height:1; margin-top:20px; letter-spacing:-.02em; }
.alt .noktalar { display:flex; gap:14px; margin-top:30px; }
.alt .noktalar i { width:12px; height:12px; border-radius:50%; background:$vurgu; }
""", **tema)
    kemerler = "".join(
        f'<div class="kemer" style="left:{60 + i * 330}px">{foto(k, 300, 560, *BINA[k])}</div>' for i, k in enumerate(sira))
    govde = f"""{logo(380, tema["fg"])}
<div class="baslik">Çalışma Saatleri</div>
{kemerler}
<div class="alt">
  <div class="ince">HAFTANIN HER GÜNÜ</div>
  <div class="saat">10:00 – 19:00</div>
  <div class="noktalar">{"<i></i>" * 7}</div>
</div>"""
    return css, govde


# --- Daire çerçeve ------------------------------------------------------------

def daire(v):
    k = ["gb", "yaz", "ic"][v]
    tema = [P["lacivert"], P["krem"], P["bordo"]][v]
    css = t("""
.story { background:$bg; color:$fg; }
.logo { position:absolute; top:200px; left:50%; transform:translateX(-50%); }
.halka { position:absolute; top:470px; left:150px; }
.daire { position:absolute; top:545px; left:225px; width:630px; height:630px; border-radius:50%; overflow:hidden;
  box-shadow: 0 30px 60px rgba(0,0,0,.35); }
.alt { position:absolute; top:1300px; left:0; right:0; text-align:center; }
.alt .saat { font-family:"DMSerif"; font-size:140px; line-height:1; }
.alt .gun { font-family:"Montserrat"; font-weight:600; font-size:26px; letter-spacing:.42em; padding-left:.42em; color:$ince; margin-top:22px; }
""", **tema)
    metin = "HAFTANIN HER GÜNÜ AÇIĞIZ • 10:00 – 19:00 • " * 2
    halka = f"""<svg class="halka" width="780" height="780" viewBox="0 0 780 780">
<defs><path id="c" d="M390,390 m-372,0 a372,372 0 1,1 744,0 a372,372 0 1,1 -744,0"/></defs>
<text font-family="Montserrat" font-weight="700" font-size="28" letter-spacing="6" fill="{tema['vurgu']}">
<textPath href="#c" textLength="2320" lengthAdjust="spacing">{metin}</textPath></text></svg>"""
    govde = f"""{logo(380, tema["fg"])}
{halka}
<div class="daire">{foto(k, 630, 630, *BINA[k])}</div>
<div class="alt"><div class="saat">10:00 – 19:00</div><div class="gun">PAZARTESİ – PAZAR</div></div>"""
    return css, govde


# --- Müze duvarı --------------------------------------------------------------

def muze(v):
    k = ["gb", "yaz", "ic"][v]
    duvar, cerceve = [("#8f8579", "#151515"), ("#8d9a87", "linear-gradient(135deg,#b8925a,#ecd9a8 45%,#9c7840)"), ("#5c111c", "linear-gradient(135deg,#b8925a,#ecd9a8 45%,#9c7840)")][v]
    css = t("""
.story { background: radial-gradient(60% 40% at 50% 26%, rgba(255,255,255,.28), transparent 70%), $duvar; }
.logo { position:absolute; top:200px; left:50%; transform:translateX(-50%); }
.cerceve { position:absolute; top:420px; left:182px; width:716px; padding:28px; background:$cerceve;
  box-shadow: 0 40px 50px rgba(0,0,0,.45), inset 0 0 0 2px rgba(0,0,0,.25); }
.paspartu { background:#f7f5f0; padding:50px; box-shadow: inset 0 3px 8px rgba(0,0,0,.18); }
.etiket { position:absolute; top:1350px; left:182px; width:560px; background:#fbfaf7; padding:30px 34px; color:#1c1c1c;
  box-shadow: 0 10px 20px rgba(0,0,0,.25); }
.etiket .a { font-family:"Montserrat"; font-weight:800; font-size:28px; letter-spacing:.08em; }
.etiket .b { font-family:"Instrument"; font-style:italic; font-size:40px; margin-top:6px; }
.etiket .c { font-family:"Montserrat"; font-weight:600; font-size:28px; margin-top:14px; }
.etiket .d { font-family:"Instrument"; font-style:italic; font-size:26px; color:#666; margin-top:10px; }
""", duvar=duvar, cerceve=cerceve)
    govde = f"""{logo(380)}
<div class="cerceve"><div class="paspartu">{foto(k, 560, 700, *BINA[k])}</div></div>
<div class="etiket">
  <div class="a">İMOTİM MOBİLYA AVM</div>
  <div class="b">Çalışma Saatleri</div>
  <div class="c">Haftanın her günü, 10:00 – 19:00</div>
  <div class="d">Karışık teknik: mobilya, ışık ve konfor</div>
</div>"""
    return css, govde


# --- Duotone ------------------------------------------------------------------

def duotone(v):
    k = ["gb", "yaz", "ic"][v]
    koyu, acik = [("#3d0a13", "#f3d9c4"), ("#0a1a33", "#cfe0f2"), ("#121110", "#e6cf9f")][v]
    css = t("""
.duo { position:absolute; inset:0; background:$koyu; }
.duo img { filter: grayscale(1) contrast(1.12); mix-blend-mode: screen; }
.renk { position:absolute; inset:0; background:$acik; mix-blend-mode: multiply; }
.golge { background: linear-gradient(0deg, rgba(0,0,0,.55), rgba(0,0,0,0) 45%); }
.logo { position:absolute; top:200px; left:80px; }
.buyuk { position:absolute; left:74px; top:1000px; font-family:"Unbounded"; font-weight:900; font-size:210px; line-height:.9;
  color:$acik; letter-spacing:-.03em; }
.hap { position:absolute; left:80px; top:1440px; padding:22px 40px; border-radius:999px; background:$acik; color:$koyu;
  font-family:"Unbounded"; font-weight:600; font-size:58px; }
""", koyu=koyu, acik=acik)
    govde = f"""<div class="duo">{tam(k)}<div class="renk"></div></div>
<div class="katman golge"></div>
{logo(400, acik)}
<div class="buyuk">HER<br>GÜN</div>
<div class="hap">10:00 – 19:00</div>"""
    return css, govde


# --- Harita pini --------------------------------------------------------------

def harita(v):
    if v < 2:
        k = ["gb", "yaz"][v]
        x, y = CATI[k]
        zemin = tam(k) + '<div class="katman" style="background:linear-gradient(180deg,rgba(0,0,0,.25),rgba(0,0,0,0) 25%)"></div>'
    else:
        x, y = 560, 900
        zemin = """<div class="katman harita"></div>
<svg class="katman" width="1080" height="1920" style="position:absolute;inset:0">
<path d="M -40 1300 C 200 1180, 420 1260, 620 1120 S 980 900, 1140 980" stroke="#a9cfee" stroke-width="70" fill="none"/>
<rect x="120" y="420" width="300" height="220" rx="30" fill="#cfe8c3"/><rect x="700" y="1320" width="260" height="300" rx="30" fill="#cfe8c3"/>
<g stroke="#ffffff" stroke-width="34" fill="none" stroke-linecap="round">
<path d="M -50 760 L 1130 640"/><path d="M 300 -50 L 420 1970"/><path d="M 820 -50 L 700 1970"/><path d="M -50 1500 L 1130 1650"/></g>
<g stroke="#f6d27a" stroke-width="44" fill="none"><path d="M -50 980 L 1130 860"/></g>
</svg>"""
    css = t("""
.harita { background:#eef0ea; }
.arama { position:absolute; top:200px; left:70px; right:70px; height:110px; border-radius:55px; background:#fff;
  display:flex; align-items:center; gap:24px; padding:0 40px; box-shadow:0 12px 30px rgba(0,0,0,.25);
  font-family:"Manrope"; font-weight:600; font-size:38px; color:#222; }
.dalga { position:absolute; left:${x}px; top:${y}px; transform:translate(-50%,-50%); border-radius:50%; border:3px solid rgba(255,255,255,.85); }
.pin { position:absolute; left:${px}px; top:${py}px; filter: drop-shadow(0 12px 14px rgba(0,0,0,.4)); }
.pin .ikon-y { position:absolute; left:39px; top:38px; }
.kart { position:absolute; top:1290px; left:70px; right:70px; border-radius:36px; background:#fff; padding:36px 40px;
  box-shadow:0 24px 50px rgba(0,0,0,.3); font-family:"Manrope"; color:#1d1d1d; }
.kart .ust { display:flex; align-items:center; gap:26px; }
.kart .avatar { width:110px; height:110px; border-radius:26px; background:#8a1b2b; display:flex; align-items:center; justify-content:center; }
.kart .ad { font-size:44px; font-weight:800; }
.kart .tur { font-size:28px; color:#777; margin-top:4px; }
.kart .cizgi { height:2px; background:#eee; margin:28px 0; }
.kart .saat { display:flex; align-items:center; gap:18px; font-size:40px; font-weight:700; }
.kart .saat .yesil { color:#1a9b4b; }
.kart .gunler { display:flex; gap:10px; margin-top:22px; }
.kart .gunler span { padding:10px 16px; border-radius:14px; background:#f3efe8; font-size:24px; font-weight:700; color:#8a1b2b; }
""", x=x, y=y, px=x - 75, py=y - 196)
    pin = f"""<div class="pin"><svg width="150" height="196" viewBox="0 0 150 196">
<path d="M75 0 C 33 0 0 33 0 75 C 0 128 75 196 75 196 C 75 196 150 128 150 75 C 150 33 117 0 75 0 Z" fill="#8a1b2b"/>
<circle cx="75" cy="75" r="56" fill="#fff"/></svg><div class="ikon-y">{ikon(72, "#8a1b2b")}</div></div>"""
    dalgalar = "".join(f'<div class="dalga" style="width:{d}px;height:{d}px;opacity:{o}"></div>' for d, o in ((90, .9), (170, .55), (250, .3)))
    gunler = "".join(f"<span>{g}</span>" for g in ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"])
    govde = f"""{zemin}
<div class="arama"><svg width="44" height="44" viewBox="0 0 44 44"><circle cx="18" cy="18" r="14" stroke="#555" stroke-width="5" fill="none"/><path d="M29 29 L41 41" stroke="#555" stroke-width="5" stroke-linecap="round"/></svg>İmotim Mobilya AVM</div>
{dalgalar}{pin}
<div class="kart">
  <div class="ust"><div class="avatar">{ikon(72)}</div><div><div class="ad">İmotim Mobilya AVM</div><div class="tur">Mobilya AVM</div></div></div>
  <div class="cizgi"></div>
  <div class="saat"><span class="yesil">●</span> Her gün <span class="yesil">10:00 – 19:00</span></div>
  <div class="gunler">{gunler}</div>
</div>"""
    return css, govde


# --- Uyarı bantları -----------------------------------------------------------

def bantlar(v):
    k = ["gb", "yaz", "ic"][v]
    if v == 1:
        b1 = b2 = dict(bg="repeating-linear-gradient(-45deg,#f5c400 0 40px,#111 40px 80px)", ic="#f5c400", yazi="#111")
        metin = "DİKKAT! HER GÜN AÇIĞIZ • 10:00 – 19:00 • "
    else:
        b1 = dict(bg=["#8a1b2b", "", "#111"][v], ic=["#8a1b2b", "", "#111"][v], yazi=["#efe6d6", "", "#fff"][v])
        b2 = dict(bg=["#efe6d6", "", "#fff"][v], ic=["#efe6d6", "", "#fff"][v], yazi=["#8a1b2b", "", "#111"][v])
        metin = "HER GÜN AÇIĞIZ • 10:00 – 19:00 • "
    css = """
.bant { position:absolute; left:-260px; width:1600px; height:124px; display:flex; align-items:center; padding:10px 0;
  box-shadow: 0 16px 30px rgba(0,0,0,.35); }
.bant .ic { width:100%; height:100%; display:flex; align-items:center; white-space:nowrap; overflow:hidden;
  font-family:"Archivo"; font-stretch:75%; font-weight:900; font-size:62px; letter-spacing:.02em; }
.etiket { position:absolute; top:1040px; left:330px; width:420px; height:420px; border-radius:50%;
  display:flex; flex-direction:column; align-items:center; justify-content:center; transform: rotate(-8deg);
  background:#fff; color:#111; box-shadow:0 24px 50px rgba(0,0,0,.4); font-family:"Archivo"; font-stretch:75%; }
.etiket .a { font-weight:700; font-size:34px; letter-spacing:.2em; }
.etiket .b { font-weight:900; font-size:118px; line-height:.95; }
.logo { position:absolute; top:205px; left:50%; transform:translateX(-50%); }
.golge { background: linear-gradient(180deg, rgba(0,0,0,.4), rgba(0,0,0,0) 26%); }
"""
    def bant(b, ust, aci):
        return (f'<div class="bant" data-serbest style="top:{ust}px;transform:rotate({aci}deg);background:{b["bg"]}">'
                f'<div class="ic" style="background:{b["ic"]};color:{b["yazi"]}">{metin * 4}</div></div>')
    govde = f"""{tam(k)}
<div class="katman golge"></div>
{logo(400)}
{bant(b1, 620, -11)}
{bant(b2, 1600, 8)}
<div class="etiket"><div class="a">HER GÜN</div><div class="b">10:00</div><div class="b">19:00</div></div>"""
    return css, govde


KAVRAMLAR = [
    ("polaroid", polaroid, 3),
    ("dergi-kapagi", dergi, 3),
    ("film-seridi", film, 3),
    ("uc-kemer", uc_kemer, 3),
    ("daire-cerceve", daire, 3),
    ("muze-duvari", muze, 3),
    ("duotone", duotone, 3),
    ("harita-pini", harita, 3),
    ("uyari-bantlari", bantlar, 3),
]
