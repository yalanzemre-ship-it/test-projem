"""Tipografi ağırlıklı konseptler: İsviçre posteri, tekrar eden yazı, fotoğraflı rakamlar,
editoryal alıntı, retro gün batımı, modern gradyan."""

from string import Template

from .temel import BINA, P, TAM, foto, logo


def t(css, **kw):
    return Template(css).substitute(**kw)


# --- İsviçre posteri ----------------------------------------------------------

def isvicre(v):
    tema = [
        dict(bg="#8a1b2b", fg="#ffffff", vurgu="#efe6d6", ince="rgba(255,255,255,.7)"),
        dict(bg="#efe6d6", fg="#141414", vurgu="#8a1b2b", ince="#6b5f53"),
        dict(bg="#141312", fg="#efe6d6", vurgu="#d9c39b", ince="rgba(239,230,214,.6)"),
    ][v]
    k = ["gb", "yaz", "ic"][v]
    css = t("""
.story { background:$bg; color:$fg; font-family:"Archivo"; }
.cizgi { position:absolute; left:60px; right:60px; height:3px; background:$fg; }
.logo { position:absolute; top:205px; left:60px; }
.ust-yazi { position:absolute; top:212px; right:60px; text-align:right; font-weight:600; font-size:22px; line-height:1.45; letter-spacing:.06em; color:$ince; }
.rakam { position:absolute; font-weight:900; font-size:520px; line-height:.78; letter-spacing:-.06em; }
.etiket { position:absolute; font-weight:800; font-size:30px; letter-spacing:.12em; color:$vurgu; }
.dikey { position:absolute; top:1310px; left:76px; transform-origin:left top; transform: rotate(-90deg) translateX(-100%);
  font-weight:800; font-size:26px; letter-spacing:.4em; white-space:nowrap; }
.kutu { position:absolute; top:1300px; left:140px; }
.blok { position:absolute; top:1300px; left:480px; right:60px; font-weight:500; font-size:34px; line-height:1.3; }
.blok b { display:block; font-weight:900; font-size:64px; line-height:1; margin-bottom:16px; color:$vurgu; }
""", **tema)
    govde = f"""{logo(300, tema["fg"])}
<div class="ust-yazi">ÇALIŞMA<br>SAATLERİ</div>
<div class="cizgi" style="top:395px"></div>
<div class="rakam" style="top:430px;left:40px">10</div>
<div class="etiket" style="top:470px;right:60px">AÇILIŞ</div>
<div class="rakam" style="top:860px;right:40px">19</div>
<div class="etiket" style="top:1200px;left:60px">KAPANIŞ</div>
<div class="cizgi" style="top:1270px"></div>
<div class="dikey">HER GÜN</div>
<div class="kutu">{foto(k, 300, 330, *BINA[k])}</div>
<div class="blok"><b>10:00 – 19:00</b>Pazartesi'den Pazar'a, haftanın her günü açığız.</div>"""
    return css, govde


# --- Tekrar eden yazı ---------------------------------------------------------

def tekrar(v):
    tema = [
        dict(bg="#8a1b2b", kontur="rgba(239,230,214,.55)", dolu="#ffffff", vurgu="#efe6d6", logo_r="#ffffff"),
        dict(bg="#0f0e0d", kontur="rgba(255,255,255,.28)", dolu="#d9c39b", vurgu="#ffffff", logo_r="#d9c39b"),
        dict(bg="#efe6d6", kontur="rgba(138,27,43,.45)", dolu="#141414", vurgu="#8a1b2b", logo_r="#141414"),
    ][v]
    css = t("""
.story { background:$bg; }
.satir { position:absolute; left:50%; transform:translateX(-50%); white-space:nowrap; font-family:"Anton";
  font-size:150px; line-height:1; letter-spacing:.01em; }
.kontur { color:transparent; -webkit-text-stroke: 2.5px $kontur; }
.dolu { color:$dolu; }
.vurgu { color:$vurgu; }
.logo-kutu { position:absolute; top:190px; left:50%; transform:translateX(-50%); background:$bg; padding:20px 34px; }
""", **tema)
    satirlar = []
    for i in range(14):
        ust = 330 + i * 140 - 280
        if i == 6:
            satirlar.append(f'<div class="satir dolu" style="top:{ust}px">HER GÜN AÇIĞIZ</div>')
        elif i == 7:
            satirlar.append(f'<div class="satir vurgu" style="top:{ust}px">10:00 – 19:00</div>')
        elif ust >= 0:
            satirlar.append(f'<div class="satir kontur" data-serbest style="top:{ust}px">AÇIK AÇIK AÇIK AÇIK AÇIK</div>')
    govde = "\n".join(satirlar) + f'\n<div class="logo-kutu">{logo(360, tema["logo_r"])}</div>'
    return css, govde


# --- Fotoğraflı rakamlar ------------------------------------------------------

def rakam_maske(v):
    k = ["gb", "yaz", "ic"][v]
    tema = [
        dict(bg="#efe6d6", fg="#141414", vurgu="#8a1b2b"),
        dict(bg="#0d0d0d", fg="#ffffff", vurgu="#d9c39b"),
        dict(bg="#8a1b2b", fg="#ffffff", vurgu="#efe6d6"),
    ][v]
    css = t("""
.story { background:$bg; color:$fg; }
.rakam { position:absolute; left:0; width:1080px; padding:120px 0; text-align:center; font-family:"Anton"; font-size:700px; line-height:.84;
  color:transparent; background-image:url("../assets/$foto"); background-size:1080px 1920px; background-repeat:no-repeat;
  -webkit-background-clip:text; background-clip:text; }
.ne { position:absolute; font-family:"Montserrat"; font-weight:700; font-size:26px; letter-spacing:.4em; color:$vurgu;
  writing-mode: vertical-rl; transform: rotate(180deg); }
.logo { position:absolute; top:1490px; left:50%; transform:translateX(-50%); }
.alt { position:absolute; top:1666px; left:0; right:0; text-align:center; font-family:"Montserrat"; font-weight:700;
  font-size:26px; letter-spacing:.38em; padding-left:.38em; }
""", foto=TAM[k], **tema)
    govde = f"""<div class="rakam" data-serbest style="top:110px;background-position:0 -110px">10</div>
<div class="rakam" data-serbest style="top:750px;background-position:0 -750px">19</div>
<div class="ne" style="top:370px;left:110px">AÇILIŞ</div>
<div class="ne" style="top:1010px;left:110px">KAPANIŞ</div>
{logo(400, tema["fg"])}
<div class="alt">HER GÜN · PZT – PAZ</div>"""
    return css, govde


# --- Editoryal alıntı ---------------------------------------------------------

def alinti(v):
    tema = [
        dict(bg="#efe6d6", fg="#2a1418", vurgu="#8a1b2b", font="Instrument"),
        dict(bg="#8a1b2b", fg="#fbf3e6", vurgu="#efe6d6", font="Fraunces"),
        dict(bg="#141312", fg="#f3ead9", vurgu="#d9c39b", font="DMSerif"),
    ][v]
    css = t("""
.story { background:$bg; color:$fg; }
.isaret { position:absolute; top:190px; left:70px; font-family:"Fraunces"; font-weight:700; font-size:420px; line-height:1;
  color:$vurgu; opacity:.9; }
.metin { position:absolute; top:500px; left:90px; right:90px; font-family:"$font"; font-style:italic; font-weight:400;
  font-size:104px; line-height:1.1; letter-spacing:-.005em; }
.metin em { font-style:normal; color:$vurgu; }
.cizgi { position:absolute; top:1420px; left:90px; width:160px; height:4px; background:$vurgu; }
.imza { position:absolute; top:1468px; left:90px; }
.imza .alt { font-family:"Montserrat"; font-weight:600; font-size:26px; letter-spacing:.3em; margin-top:26px; opacity:.8; }
""", **tema)
    govde = f"""<div class="isaret" data-serbest>“</div>
<div class="metin">Haftanın her günü, sabah <em>10:00</em>'da kapılarımızı açıyor; akşam <em>19:00</em>'a kadar sizi bekliyoruz.</div>
<div class="cizgi"></div>
<div class="imza">{logo(380, tema["fg"])}<div class="alt">PAZARTESİ – PAZAR</div></div>"""
    return css, govde


# --- Retro gün batımı ---------------------------------------------------------

def retro(v):
    tema = [
        dict(bg="#f3e6cc", gunes="linear-gradient(180deg,#ffd166,#f78c3b 50%,#b02a37)", yazi="#8a1b2b", g1="#f78c3b", g2="#ffd166", saat_bg="#8a1b2b", saat_y="#f3e6cc"),
        dict(bg="#13213d", gunes="linear-gradient(180deg,#ffc6a8,#ff7f7f 50%,#c2457a)", yazi="#fbe9d6", g1="#ff7f7f", g2="#c2457a", saat_bg="#fbe9d6", saat_y="#13213d"),
        dict(bg="#3a4530", gunes="linear-gradient(180deg,#f4d06f,#e39b3a 55%,#b4532a)", yazi="#f6edd8", g1="#e39b3a", g2="#b4532a", saat_bg="#f4d06f", saat_y="#3a4530"),
    ][v]
    css = t("""
.story { background:$bg; }
.logo { position:absolute; top:200px; left:50%; transform:translateX(-50%); }
.gunes { position:absolute; top:420px; left:170px; width:740px; height:740px; border-radius:50%; background:$gunes;
  -webkit-mask: linear-gradient(180deg, #000 0 52%, transparent 52% 55%, #000 55% 63%, transparent 63% 67%,
     #000 67% 74%, transparent 74% 79%, #000 79% 85%, transparent 85% 91%, #000 91%); }
.yazi { position:absolute; left:0; right:0; text-align:center; font-family:"Shrikhand"; color:$yazi; line-height:1;
  text-shadow: 7px 7px 0 $g1, 14px 14px 0 $g2; }
.saat { position:absolute; top:1500px; left:50%; transform:translateX(-50%); padding:18px 44px; border-radius:999px;
  background:$saat_bg; color:$saat_y; font-family:"Righteous"; font-size:76px; white-space:nowrap; }
""", **tema)
    govde = f"""{logo(380, tema["yazi"])}
<div class="gunes"></div>
<div class="yazi" style="top:1060px;font-size:200px">Her gün</div>
<div class="yazi" style="top:1270px;font-size:150px">açığız!</div>
<div class="saat">10:00 – 19:00</div>"""
    return css, govde


# --- Modern gradyan -----------------------------------------------------------

def gradyan(v):
    tema = [
        dict(zemin="radial-gradient(60% 45% at 15% 15%, #ff7a45 0%, transparent 70%), radial-gradient(55% 40% at 90% 40%, #ff4f8b 0%, transparent 70%), radial-gradient(70% 50% at 30% 90%, #8a1b2b 0%, transparent 75%), #5c111c",
             fg="#ffffff", hap="rgba(255,255,255,.16)", cizgi="rgba(255,255,255,.45)"),
        dict(zemin="radial-gradient(60% 45% at 85% 12%, #1fb5a8 0%, transparent 70%), radial-gradient(55% 40% at 10% 45%, #6b5bff 0%, transparent 70%), radial-gradient(70% 50% at 70% 95%, #0f2340 0%, transparent 75%), #0a172b",
             fg="#ffffff", hap="rgba(255,255,255,.14)", cizgi="rgba(255,255,255,.4)"),
        dict(zemin="radial-gradient(60% 45% at 20% 10%, #fff6e5 0%, transparent 70%), radial-gradient(55% 40% at 90% 50%, #e6c98f 0%, transparent 70%), radial-gradient(70% 50% at 20% 95%, #d8b892 0%, transparent 75%), #efe6d6",
             fg="#1f1a14", hap="rgba(255,255,255,.45)", cizgi="rgba(31,26,20,.35)"),
    ][v]
    k = ["gb", "yaz", "ic"][v]
    css = t("""
.story { background:$zemin; color:$fg; }
.logo { position:absolute; top:200px; left:80px; }
.buyuk { position:absolute; top:430px; left:76px; font-family:"Syne"; font-weight:800; font-size:156px; line-height:.98; letter-spacing:-.04em; white-space:nowrap; }
.foto-hap { position:absolute; top:880px; left:80px; width:920px; height:300px; border-radius:150px; overflow:hidden; }
.saatler { position:absolute; top:1250px; left:80px; right:80px; display:flex; align-items:center; gap:22px; }
.saatler .hap { padding:24px 40px; border-radius:999px; background:$hap; border:2px solid $cizgi; backdrop-filter: blur(10px);
  font-family:"Syne"; font-weight:700; font-size:88px; line-height:1; }
.saatler .ok { font-family:"Syne"; font-size:80px; }
.alt { position:absolute; top:1460px; left:80px; font-family:"Syne"; font-weight:600; font-size:36px; letter-spacing:.02em; }
""", **tema)
    govde = f"""{logo(360, tema["fg"])}
<div class="buyuk">her gün<br>açığız</div>
<div class="foto-hap">{foto(k, 920, 300, *BINA[k])}</div>
<div class="saatler"><span class="hap">10:00</span><span class="ok">→</span><span class="hap">19:00</span></div>
<div class="alt">pazartesi'den pazar'a · haftanın 7 günü</div>"""
    return css, govde


KAVRAMLAR = [
    ("isvicre-posteri", isvicre, 3),
    ("tekrar-tipografi", tekrar, 3),
    ("fotografli-rakamlar", rakam_maske, 3),
    ("editoryal-alinti", alinti, 3),
    ("retro-gunbatimi", retro, 3),
    ("modern-gradyan", gradyan, 3),
]
