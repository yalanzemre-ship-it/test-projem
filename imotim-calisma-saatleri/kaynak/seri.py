"""Çok sayıda farklı konseptten oluşan hikaye serisini üretir.

Her konsept (seri_uretec/k_*.py içindeki KAVRAMLAR listesi) birkaç varyasyon
verir; her varyasyon seri/ altına ayrı bir HTML sayfası olarak yazılır.
Gereken fotoğraf kırpımları assets/kirp/ altına bir kez üretilir.

Kullanım:
    python3 seri.py
    node render.js ../hikayeler/seri seri
"""

import importlib
import shutil
import sys

from seri_uretec.temel import KOK, sayfa

MODULLER = ["k_tabela", "k_kagit", "k_foto", "k_tipo", "k_arayuz", "k_grafik"]


def main():
    hedef = KOK / "seri"
    shutil.rmtree(hedef, ignore_errors=True)
    hedef.mkdir()
    n = 0
    # Deneme için yalnızca bazı modüller verilebilir: python3 seri.py k_tabela
    for m in sys.argv[1:] or MODULLER:
        mod = importlib.import_module(f"seri_uretec.{m}")
        for ad, fn, adet in mod.KAVRAMLAR:
            for v in range(adet):
                css, govde = fn(v)
                n += 1
                (hedef / f"{n:03d}-{ad}-{v + 1}.html").write_text(sayfa(govde, css))
    print(n, "sayfa üretildi")


if __name__ == "__main__":
    main()
