import { useRef, type PointerEvent } from "react";
import { prefersReducedMotion } from "../../lib/motion";
import { IMG, STUDIO } from "../../lib/site-data";
import { useScrollFx } from "../../lib/use-fx";
import { Img } from "./img";

const GLYPHS = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ0123456789";

/** Mono readout that decodes its label on hover (Yol tarifi). */
function decode(e: PointerEvent<HTMLAnchorElement>) {
  if (e.pointerType !== "mouse" || prefersReducedMotion()) return;
  const el = e.currentTarget.querySelector<HTMLElement>(".route-link__label");
  if (!el || el.dataset.busy) return;
  const target = el.dataset.text ?? el.textContent ?? "";
  el.dataset.text = target;
  el.dataset.busy = "1";
  let frame = 0;
  const id = window.setInterval(() => {
    frame++;
    el.textContent = target
      .split("")
      .map((ch, k) => (ch === " " || k < frame / 2 ? ch : GLYPHS[Math.floor(Math.random() * GLYPHS.length)]))
      .join("");
    if (frame / 2 >= target.length) {
      window.clearInterval(id);
      el.textContent = target;
      delete el.dataset.busy;
    }
  }, 28);
}

export function Contact({ headingLevel = 2 }: { headingLevel?: 1 | 2 }) {
  const ref = useRef<HTMLElement>(null);
  const H = headingLevel === 1 ? "h1" : "h2";

  useScrollFx(({ gsap, rich }) => {
    const el = ref.current;
    if (!el) return;
    gsap.fromTo(
      el.querySelector(".contact__plate img"),
      { yPercent: -10, scale: 1.15 },
      { yPercent: 10, scale: 1.15, ease: "none", scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: true } },
    );
    if (rich) {
      gsap.fromTo(
        el.querySelector(".contact__title"),
        { "--w": 70 },
        { "--w": 125, ease: "none", scrollTrigger: { trigger: el, start: "top 85%", end: "top 25%", scrub: 0.6 } },
      );
    }
  });

  return (
    <section className="contact" ref={ref} aria-labelledby="contact-title">
      <div className="contact__plate" aria-hidden="true">
        <Img src={IMG.silk} sizes="100vw" alt="" />
      </div>
      <div className="contact__inner">
        <p className="contact__eyebrow">Randevu için</p>
        <H className="contact__title" id="contact-title">
          Yerinizi <em>ayırtın.</em>
        </H>
        <p className="contact__lead">Gelin randevuları için 2 ila 3 ay önceden yazmanızı öneririz.</p>
      </div>
      <a className="wa-band" href={STUDIO.whatsapp} target="_blank" rel="noreferrer" data-cursor="WRITE">
        <span className="wa-band__roll" aria-hidden="true">
          <span>WhatsApp'tan yaz</span>
          <span>WhatsApp'tan yaz</span>
        </span>
        <span className="sr-only">WhatsApp'tan yaz</span>
        <span className="wa-band__num">{STUDIO.phoneDisplay}</span>
        <span className="wa-band__arrow" aria-hidden="true">
          →
        </span>
      </a>
      <dl className="contact__info">
        <div>
          <dt>Adres</dt>
          <dd>
            {STUDIO.addressLines[0]}
            <br />
            {STUDIO.addressLines[1]}
            <a className="route-link" href={STUDIO.maps} target="_blank" rel="noreferrer" onPointerEnter={decode}>
              <span className="route-link__label">Yol tarifi</span>
              <span aria-hidden="true"> ↗</span>
            </a>
          </dd>
        </div>
        <div>
          <dt>Telefon</dt>
          <dd>
            <a className="tel-link" href={STUDIO.phoneHref}>
              {STUDIO.phoneDisplay}
            </a>
          </dd>
        </div>
        <div>
          <dt>Çalışma saatleri</dt>
          <dd>
            {STUDIO.hours[0]}
            <br />
            {STUDIO.hours[1]}
          </dd>
        </div>
      </dl>
    </section>
  );
}
