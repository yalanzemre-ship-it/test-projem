"""Açık tema, yalnızca drone: referans paylaşımların işlenmiş halleri.

Kullanım:
    python3 premium_serisi.py
    node render.js ../hikayeler/premium-serisi premium
"""

import shutil

from seri_uretec.k_premium import VARYASYONLAR
from seri_uretec.temel import KOK, sayfa


def main():
    hedef = KOK / "premium"
    shutil.rmtree(hedef, ignore_errors=True)
    hedef.mkdir()
    for n, (ad, fn, ayar) in enumerate(VARYASYONLAR, 1):
        css, govde = fn(ayar)
        (hedef / f"{n:02d}-{ad}.html").write_text(sayfa(govde, css))
    print(len(VARYASYONLAR), "sayfa üretildi")


if __name__ == "__main__":
    main()
