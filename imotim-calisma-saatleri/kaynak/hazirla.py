"""Hikaye görsellerinde kullanılan logo ve fotoğrafları hazırlar.

Fotoğraflar tarayıcıda tekrar ölçeklenmesin diye her biri, sayfada
gösterileceği piksel boyutuna Lanczos ile bir kez küçültülür ve kayıpsız
PNG olarak kaydedilir. Sayfalar deviceScaleFactor 1 ile render edildiği
için bu görseller ekrana 1:1 piksel olarak basılır.

Kullanım:
    python3 hazirla.py <logo.pdf> <foto-1> <foto-2> <foto-3>
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ASSETS = Path(__file__).resolve().parent / "assets"
W, H = 1080, 1920


def logo_cikar(pdf: Path) -> None:
    # PDF içindeki logo, JPEG renk katmanı + ayrı alfa maskesinden oluşuyor.
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdfimages", "-all", str(pdf), f"{tmp}/img"], check=True)
        renk = Image.open(f"{tmp}/img-000.jpg").convert("RGB")
        alfa = Image.open(f"{tmp}/img-001.png").convert("L")
    renk.putalpha(alfa)
    renk.save(ASSETS / "logo.png", optimize=True)
    # Sembol (T monogramı) ile yazı arasında 998-1078 px boş sütun var.
    renk.crop((0, 0, 998, renk.height)).save(ASSETS / "logo-ikon.png", optimize=True)


def kirp_olcekle(src: Image.Image, kutu, boyut, ad: str) -> None:
    src.crop(kutu).resize(boyut, Image.LANCZOS).save(ASSETS / ad, optimize=True)


def main() -> None:
    pdf, f1, f2, f3 = (Path(a) for a in sys.argv[1:5])
    ASSETS.mkdir(exist_ok=True)
    logo_cikar(pdf)

    dis_gunbatimi = Image.open(f1).convert("RGB")  # 1125x2000
    dis_yaz = Image.open(f2).convert("RGB")  # 1125x2000
    ic_koridor = Image.open(f3).convert("RGB")  # 1600x2000

    # Tam ekran (9:16 kaynaklar birebir oranda)
    kirp_olcekle(dis_gunbatimi, (0, 0, 1125, 2000), (W, H), "foto-1-tam.png")
    kirp_olcekle(dis_yaz, (0, 0, 1125, 2000), (W, H), "foto-2-tam.png")

    # 4:5 iç mekan -> 9:16; koridorun kaçış noktası (~x=830) ortada kalacak şekilde
    olcek = H / ic_koridor.height
    gen = round(1080 / olcek)
    sol = 830 - gen // 2
    kirp_olcekle(ic_koridor, (sol, 0, sol + gen, 2000), (W, H), "foto-3-tam.png")
    # Sol panelli tasarım için: koridor ve sağdaki mağazalar panelin dışında kalsın
    kirp_olcekle(ic_koridor, (0, 0, gen, 2000), (W, H), "foto-3-sol.png")

    # Kemer çerçeve (800x880): gökyüzü, dağlar, bina ve otopark
    kirp_olcekle(dis_gunbatimi, (0, 410, 1125, 410 + 1238), (800, 880), "foto-1-kemer.png")

    # Üst panel (1080x1350): iç mekanın tamamı
    kirp_olcekle(ic_koridor, (0, 0, 1600, 2000), (1080, 1350), "foto-3-ust.png")


if __name__ == "__main__":
    main()
