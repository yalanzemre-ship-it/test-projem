"""Arayüz temalı konseptler: telefon kilit ekranı, sohbet, bento ızgara."""

from string import Template

from .temel import BINA, P, foto, ikon, logo, tam


def t(css, **kw):
    return Template(css).substitute(**kw)


# --- Kilit ekranı -------------------------------------------------------------

def kilit(v):
    k = ["gb", "yaz", "ic"][v]
    css = """
.ust-g { background: linear-gradient(180deg, rgba(0,0,0,.42), rgba(0,0,0,0) 34%); }
.alt-g { background: linear-gradient(0deg, rgba(0,0,0,.35), rgba(0,0,0,0) 40%); }
.ust { position:absolute; top:215px; left:0; right:0; text-align:center; color:#fff; font-family:"DMSans";
  text-shadow: 0 2px 20px rgba(0,0,0,.25); }
.ust .tarih { font-weight:600; font-size:40px; letter-spacing:.01em; }
.ust .saat { font-weight:700; font-size:250px; line-height:1; letter-spacing:-.03em; margin-top:6px; }
.ust .alt { font-weight:500; font-size:38px; margin-top:6px; opacity:.92; }
.bildirim { position:absolute; left:60px; right:60px; border-radius:44px; padding:30px 34px;
  background:rgba(250,250,250,.72); backdrop-filter: blur(24px) saturate(1.4); color:#111; font-family:"DMSans";
  box-shadow: 0 10px 30px rgba(0,0,0,.18); }
.bildirim .bas { display:flex; align-items:center; gap:20px; }
.bildirim .uygulama { width:76px; height:76px; border-radius:18px; background:#8a1b2b; display:flex; align-items:center; justify-content:center; flex:none; }
.bildirim .kim { font-weight:700; font-size:28px; letter-spacing:.04em; color:#444; }
.bildirim .zaman { margin-left:auto; font-size:28px; color:#666; }
.bildirim .baslik { font-weight:800; font-size:40px; margin-top:18px; }
.bildirim .govde { font-weight:500; font-size:36px; line-height:1.3; margin-top:6px; color:#222; }
"""
    govde = f"""{tam(k)}
<div class="katman ust-g"></div><div class="katman alt-g"></div>
<div class="ust"><div class="tarih">Pazartesi – Pazar</div><div class="saat">10:00</div><div class="alt">19:00'a kadar açığız</div></div>
<div class="bildirim" style="top:1150px">
  <div class="bas"><div class="uygulama">{ikon(52)}</div><div class="kim">İMOTİM MOBİLYA AVM</div><div class="zaman">şimdi</div></div>
  <div class="baslik">Bugün de açığız! 🛋️</div>
  <div class="govde">Haftanın her günü 10:00 – 19:00 arası sizi bekliyoruz.</div>
</div>
<div class="bildirim" style="top:1430px;padding:24px 34px">
  <div class="bas"><div class="uygulama" style="width:60px;height:60px;border-radius:15px">{ikon(40)}</div><div class="kim">HATIRLATMA</div><div class="zaman">1 dk</div></div>
  <div class="govde" style="margin-top:12px">Pazar günü de 10:00 – 19:00 açığız.</div>
</div>"""
    return css, govde


# --- Sohbet -------------------------------------------------------------------

MESAJLAR = [
    ("sag", "Merhaba! Kaçta açıksınız? 🙂", "09:41"),
    ("sol", "Merhaba 👋 Haftanın her günü 10:00 – 19:00 arası açığız.", "09:41"),
    ("sag", "Pazar günü de mi?", "09:42"),
    ("sol", "Evet, Pazar dahil her gün! 😊", "09:42"),
    ("sag", "Harika, yarın geliyorum 🛋️", "09:43"),
    ("sol", "Sizi bekliyoruz! ❤️", "09:43"),
]


def sohbet(v):
    tema = [
        dict(zemin="background-color:#efe6d6; background-image: radial-gradient(rgba(138,27,43,.07) 2px, transparent 2.5px); background-size: 34px 34px;",
             bas="#ffffff", bas_y="#1b1b1b", sag="#8a1b2b", sag_y="#ffffff", sol="#ffffff", sol_y="#1b1b1b", ince="#8c8279", giris="#ffffff"),
        dict(zemin="background:#0e0e10;", bas="#1a1a1d", bas_y="#ffffff", sag="#c9a86a", sag_y="#1a1408", sol="#232327", sol_y="#f2f2f2",
             ince="#8d8d93", giris="#1f1f23"),
        dict(zemin="background:#000;", bas="rgba(255,255,255,.18)", bas_y="#ffffff", sag="rgba(138,27,43,.88)", sag_y="#ffffff",
             sol="rgba(255,255,255,.82)", sol_y="#1b1b1b", ince="rgba(255,255,255,.7)", giris="rgba(255,255,255,.2)"),
    ][v]
    zemin_foto = tam("yaz", stil="filter:blur(30px) brightness(.75);transform:scale(1.1)") if v == 2 else ""
    css = t("""
.story { $zemin font-family:"Manrope"; }
.bas { position:absolute; top:170px; left:0; right:0; height:150px; background:$bas; color:$bas_y; backdrop-filter: blur(20px);
  display:flex; align-items:center; gap:24px; padding:20px 50px 0; box-shadow:0 2px 0 rgba(0,0,0,.06); }
.bas .geri { font-size:56px; font-weight:300; }
.bas .avatar { width:92px; height:92px; border-radius:50%; background:#8a1b2b; display:flex; align-items:center; justify-content:center; }
.bas .ad { font-weight:800; font-size:38px; }
.bas .durum { font-weight:600; font-size:26px; color:#2fb463; margin-top:2px; }
.akis { position:absolute; top:380px; left:50px; right:50px; display:flex; flex-direction:column; gap:32px; }
.balon { max-width:780px; padding:26px 32px 18px; font-size:46px; font-weight:600; line-height:1.3; box-shadow:0 2px 6px rgba(0,0,0,.08); }
.balon .zaman { display:block; text-align:right; font-size:22px; font-weight:600; margin-top:6px; opacity:.6; }
.sag { align-self:flex-end; background:$sag; color:$sag_y; border-radius:36px 36px 10px 36px; }
.sol { align-self:flex-start; background:$sol; color:$sol_y; border-radius:36px 36px 36px 10px; }
.giris { position:absolute; top:1610px; left:50px; right:50px; height:100px; border-radius:50px; background:$giris;
  display:flex; align-items:center; padding:0 40px; font-size:34px; font-weight:600; color:$ince; }
""", **tema)
    balonlar = "".join(f'<div class="balon {y}">{m}<span class="zaman">{z}</span></div>' for y, m, z in MESAJLAR)
    govde = f"""{zemin_foto}
<div class="bas"><span class="geri">‹</span><div class="avatar">{ikon(58)}</div><div><div class="ad">İmotim Mobilya AVM</div><div class="durum">● çevrimiçi</div></div></div>
<div class="akis">{balonlar}</div>
<div class="giris">Mesaj yazın…</div>"""
    return css, govde


# --- Bento ızgara -------------------------------------------------------------

def bento(v):
    k = ["gb", "yaz", "ic"][v]
    tema = [
        dict(bg="#f4efe6", kutu="#ffffff", yazi="#1b1b1b", vurgu="#8a1b2b", vurgu_y="#ffffff", ince="#8c8279", koyu="#1b1b1b", koyu_y="#efe6d6"),
        dict(bg="#0d0c0b", kutu="#1c1a18", yazi="#f3ead9", vurgu="#d9c39b", vurgu_y="#1a1408", ince="#8d867c", koyu="#2a2622", koyu_y="#d9c39b"),
        dict(bg="#8a1b2b", kutu="#efe6d6", yazi="#2a1418", vurgu="#ffffff", vurgu_y="#8a1b2b", ince="#8c7268", koyu="#2a0a10", koyu_y="#efe6d6"),
    ][v]
    css = t("""
.story { background:$bg; color:$yazi; font-family:"Manrope"; }
.izgara { position:absolute; top:190px; left:60px; width:960px; display:grid; grid-template-columns:470px 470px; gap:20px; }
.k { border-radius:38px; background:$kutu; padding:34px 38px; overflow:hidden; position:relative; }
.logo-k { grid-column:1 / -1; height:210px; display:flex; align-items:center; justify-content:space-between; }
.logo-k .not { font-weight:700; font-size:24px; letter-spacing:.3em; color:$ince; text-align:right; line-height:1.5; }
.foto-k { grid-row: span 2; padding:0; height:620px; }
.ne { font-weight:700; font-size:24px; letter-spacing:.3em; color:$ince; }
.rakam { font-family:"SpaceGrotesk"; font-weight:700; font-size:150px; line-height:1; letter-spacing:-.04em; margin-top:40px; }
.vurgu { background:$vurgu; color:$vurgu_y; }
.vurgu .ne { color:$vurgu_y; opacity:.75; }
.koyu { background:$koyu; color:$koyu_y; }
.koyu .ne { color:$koyu_y; opacity:.7; }
.yedi { font-family:"SpaceGrotesk"; font-weight:700; font-size:170px; line-height:1; letter-spacing:-.05em; margin-top:10px; }
.yedi-alt { font-weight:800; font-size:40px; margin-top:4px; }
.noktalar { display:grid; grid-template-columns:repeat(4, 1fr); gap:16px 10px; margin-top:34px; }
.noktalar span { font-weight:800; font-size:30px; display:flex; align-items:center; gap:10px; }
.noktalar span::before { content:""; width:14px; height:14px; border-radius:50%; background:#3fbf6f; }
.genis { grid-column:1 / -1; height:190px; display:flex; align-items:center; justify-content:space-between; }
.genis .italik { font-family:"Instrument"; font-style:italic; font-size:74px; }
.genis .ok { width:110px; height:110px; border-radius:50%; background:$vurgu; color:$vurgu_y; display:flex; align-items:center;
  justify-content:center; font-size:60px; }
""", **tema)
    gunler = "".join(f"<span>{g}</span>" for g in ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"])
    govde = f"""<div class="izgara">
  <div class="k logo-k">{logo(400, tema["yazi"])}<div class="not">ÇALIŞMA<br>SAATLERİ</div></div>
  <div class="k foto-k">{foto(k, 470, 620, *BINA[k])}</div>
  <div class="k vurgu" style="height:300px"><div class="ne">AÇILIŞ</div><div class="rakam">10:00</div></div>
  <div class="k koyu" style="height:300px"><div class="ne">KAPANIŞ</div><div class="rakam">19:00</div></div>
  <div class="k koyu" style="height:300px"><div class="yedi">7/7</div><div class="yedi-alt">gün açığız</div></div>
  <div class="k" style="height:300px"><div class="ne">GÜNLER</div><div class="noktalar">{gunler}</div></div>
  <div class="k genis"><span class="italik">Sizi bekliyoruz</span><span class="ok">→</span></div>
</div>"""
    return css, govde


KAVRAMLAR = [
    ("kilit-ekrani", kilit, 3),
    ("sohbet", sohbet, 3),
    ("bento", bento, 3),
]
