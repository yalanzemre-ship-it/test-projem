"""Müşterinin önceki bayram/yılbaşı paylaşımlarının diliyle çalışma saatleri hikayeleri üretir.

Kullanım:
    python3 referans_serisi.py
    node render.js ../hikayeler/referans-serisi referans
"""

import shutil

from seri_uretec.k_referans import VARYASYONLAR
from seri_uretec.temel import KOK, sayfa


def main():
    hedef = KOK / "referans"
    shutil.rmtree(hedef, ignore_errors=True)
    hedef.mkdir()
    for n, (ad, fn, ayar) in enumerate(VARYASYONLAR, 1):
        css, govde = fn(ayar)
        (hedef / f"{n:02d}-{ad}.html").write_text(sayfa(govde, css))
    print(len(VARYASYONLAR), "sayfa üretildi")


if __name__ == "__main__":
    main()
