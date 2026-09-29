import { useRef } from "react";
import { IMG } from "../../lib/site-data";
import { useScrollFx } from "../../lib/use-fx";
import { Img } from "./img";
import { TLink } from "./transition";

export function Hero() {
  const ref = useRef<HTMLElement>(null);

  useScrollFx(({ gsap, rich }) => {
    const el = ref.current;
    if (!el) return;
    const st = { trigger: el, start: "top top", end: "bottom top", scrub: 0.5 };
    gsap.to(el.querySelector(".hero__media img"), { yPercent: 16, scale: 1.12, ease: "none", scrollTrigger: st });
    gsap.to(el.querySelector(".hero__shade"), { "--shade": 0.85, ease: "none", scrollTrigger: st });
    const title = el.querySelector(".hero__title");
    // Scroll-linked type: the headline compresses its width axis as it leaves (desktop only; it reflows text).
    if (rich) gsap.to(title, { yPercent: -35, "--w": 72, ease: "none", scrollTrigger: st });
    else gsap.to(title, { yPercent: -20, ease: "none", scrollTrigger: st });
  });

  return (
    <section className="hero" ref={ref} aria-labelledby="hero-title">
      <div className="hero__media">
        <Img
          src={IMG.heroA}
          sizes="100vw"
          priority
          alt="Loş ışıkta makyaj stüdyosu: ışıklı ayna, sandalyeye bırakılmış gelin duvağı, mermer üzerinde fırçalar ve paletler"
        />
        <div className="hero__shade" />
      </div>
      <div className="hero__content">
        <p className="hero__eyebrow">Nilüfer, Bursa · 2021'den beri</p>
        <h1 className="hero__title" id="hero-title">
          <span className="line">
            <span>Her yüz</span>
          </span>
          <span className="line">
            <span>
              kendi <em>ölçüsünde.</em>
            </span>
          </span>
        </h1>
        <p className="hero__sub">Gelin makyajından kalıcı makyaja, abartısız ve size ait kalan bir estetik.</p>
        <div className="hero__ctas">
          <TLink to="/iletisim" className="hero-book" data-magnetic="0.35">
            <span className="hero-book__label">Randevu al</span>
            <span className="hero-book__rule" aria-hidden="true" />
          </TLink>
          <TLink to="/hizmetler" className="hero-route">
            <span>Hizmetler</span>
            <span className="hero-route__path" aria-hidden="true">
              <i />
            </span>
          </TLink>
        </div>
      </div>
    </section>
  );
}
