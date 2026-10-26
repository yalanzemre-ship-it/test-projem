"""Seri şablonlarının ortak yardımcıları: fotoğraf kırpma, logo, palet, sayfa iskeleti."""

from pathlib import Path

from PIL import Image

KOK = Path(__file__).resolve().parent.parent  # kaynak/

ORIJINAL = {
    "gb": "orijinal/dis-gunbatimi.webp",  # 1125x2000, gün batımı drone
    "yaz": "orijinal/dis-yaz.webp",  # 1125x2000, yaz günü drone
    "ic": "orijinal/ic-koridor.webp",  # 1600x2000, iç mekan koridoru
}
TAM = {"gb": "foto-1-tam.png", "yaz": "foto-2-tam.png", "ic": "foto-3-tam.png"}

# Orijinal piksel koordinatlarında ana konuların merkezi
BINA = {"gb": (690, 1070), "yaz": (640, 1050), "ic": (830, 820)}

GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
GUNLER_B = ["PAZARTESİ", "SALI", "ÇARŞAMBA", "PERŞEMBE", "CUMA", "CUMARTESİ", "PAZAR"]
KISA = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]

# bg: zemin, bg2: ikincil zemin, fg: yazı, vurgu: aksan, ince: ikincil yazı
P = {
    "bordo": dict(bg="#8a1b2b", bg2="#5c111c", fg="#ffffff", vurgu="#efe6d6", ince="rgba(255,255,255,.72)"),
    "krem": dict(bg="#efe6d6", bg2="#e2d5bd", fg="#171513", vurgu="#8a1b2b", ince="#6b5f53"),
    "antrasit": dict(bg="#171513", bg2="#26221f", fg="#f3ead9", vurgu="#d9c39b", ince="rgba(243,234,217,.62)"),
    "lacivert": dict(bg="#0f2340", bg2="#0a172b", fg="#ffffff", vurgu="#d9c39b", ince="rgba(255,255,255,.7)"),
    "beyaz": dict(bg="#ffffff", bg2="#f1efeb", fg="#121212", vurgu="#8a1b2b", ince="#6d6d6d"),
    "zeytin": dict(bg="#39442f", bg2="#262e1f", fg="#f4efe2", vurgu="#d8b15a", ince="rgba(244,239,226,.7)"),
    "hardal": dict(bg="#d8a33a", bg2="#b9831f", fg="#1d1a16", vurgu="#5c111c", ince="rgba(29,26,22,.7)"),
    "pudra": dict(bg="#ead2c9", bg2="#dcb9ad", fg="#3a1d1f", vurgu="#8a1b2b", ince="#7a5a55"),
}

_acik = {}


def _resim(k):
    if k not in _acik:
        _acik[k] = Image.open(KOK / ORIJINAL[k]).convert("RGB")
    return _acik[k]


def kirp(k, w, h, cx=None, cy=None, s=None):
    """Kaynak k'dan (cx, cy) merkezli w x h piksellik kare üretir, sayfaya göre yolunu döner.

    s = çıktı pikseli / kaynak pikseli. Verilmezse kareye sığan en geniş görüş
    alanı seçilir. s > 1 (büyütme) reddedilir; kalite korunur.
    """
    im = _resim(k)
    W, H = im.size
    s_min = max(w / W, h / H)
    s = s_min if s is None else s
    if s > 1 + 1e-9:
        raise ValueError(f"{k} {w}x{h}: büyütme gerekir (s={s:.3f})")
    if s < s_min - 1e-9:
        raise ValueError(f"{k} {w}x{h}: kutu kaynağa sığmıyor (s={s:.3f} < {s_min:.3f})")
    bw, bh = w / s, h / s
    cx = W / 2 if cx is None else cx
    cy = H / 2 if cy is None else cy
    x0 = round(min(max(cx - bw / 2, 0), W - bw))
    y0 = round(min(max(cy - bh / 2, 0), H - bh))
    bw, bh = min(bw, W - x0), min(bh, H - y0)
    ad = f"{k}-{w}x{h}-{x0}-{y0}-{round(s * 1000)}.png"
    hedef = KOK / "assets" / "kirp" / ad
    if not hedef.exists():
        hedef.parent.mkdir(parents=True, exist_ok=True)
        im.resize((w, h), Image.LANCZOS, box=(x0, y0, x0 + bw, y0 + bh)).save(hedef)
    return f"../assets/kirp/{ad}"


def img(src, w, h, stil="", cls=""):
    return f'<img class="{cls}" src="{src}" width="{w}" height="{h}" style="display:block;{stil}" alt="">'


def foto(k, w, h, cx=None, cy=None, s=None, stil="", cls=""):
    return img(kirp(k, w, h, cx, cy, s), w, h, stil, cls)


def tam(k, stil="", cls="foto"):
    """1080x1920 hazır tam ekran fotoğraf (assets/foto-*-tam.png)."""
    return f'<img class="{cls}" src="../assets/{TAM[k]}" width="1080" height="1920" style="{stil}" alt="">'


def logo(w, renk="#fff", stil=""):
    return f'<div class="logo" style="width:{w}px;background:{renk};{stil}"></div>'


def ikon(w, renk="#fff", stil=""):
    return f'<div class="logo-ikon" style="width:{w}px;background:{renk};{stil}"></div>'


def saat(a="10", b="19", ayrac=" – "):
    return f"{a}:00{ayrac}{b}:00"


def sayfa(govde, css="", cam=False):
    linkler = ["../ortak.css", "../fontlar.css"] + (["../cam.css"] if cam else [])
    bas = "".join(f'<link rel="stylesheet" href="{l}">' for l in linkler)
    return (
        '<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
        f"{bas}\n<style>\n{css}\n</style>\n</head>\n<body>\n"
        f'<div class="story">\n{govde}\n</div>\n</body>\n</html>\n'
    )
