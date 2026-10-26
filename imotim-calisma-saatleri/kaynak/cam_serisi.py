"""03-haftalik-cam tasarımının geliştirilmiş hali ve benzer varyasyonlarını üretir.

Kullanım:
    python3 cam_serisi.py
    node render.js ../hikayeler/cam-serisi cam
"""

import shutil

from seri_uretec.k_cam import VARYASYONLAR, uret
from seri_uretec.temel import KOK, sayfa


def main():
    hedef = KOK / "cam"
    shutil.rmtree(hedef, ignore_errors=True)
    hedef.mkdir()
    for n, (ad, ayar) in enumerate(VARYASYONLAR, 1):
        css, govde = uret(ayar)
        (hedef / f"{n:02d}-{ad}.html").write_text(sayfa(govde, css))
    print(len(VARYASYONLAR), "sayfa üretildi")


if __name__ == "__main__":
    main()
