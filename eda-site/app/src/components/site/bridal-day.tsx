import { useRef } from "react";
import { pad2 } from "../../lib/motion";
import { BRIDAL_DAY } from "../../lib/site-data";
import { useScrollFx } from "../../lib/use-fx";
import { Img } from "./img";

/**
 * Cinematic scrub: a sticky stage where scrolling advances the bridal day
 * through four scenes. Each new scene wipes up over the last and its caption
 * replaces the previous one. Reduced motion renders the chapters as a static list.
 *
 * Every animated element gets its start state once via gsap.set, and the
 * timeline only uses .to() tweens. Stacking several fromTo() tweens on the same
 * caption made later tweens apply their "from" values at creation time, which
 * pulled all four captions into view at once and made them overlap.
 */
export function BridalDay() {
  const ref = useRef<HTMLElement>(null);

  useScrollFx(({ gsap, rich }) => {
    const el = ref.current;
    if (!el) return;
    const frames = gsap.utils.toArray<HTMLElement>(".day__frame", el);
    const imgs = frames.map((f) => f.querySelector("img"));
    const caps = gsap.utils.toArray<HTMLElement>(".day__cap", el);
    const step = el.querySelector<HTMLElement>(".day__step");
    const n = frames.length;

    gsap.set(frames.slice(1), { clipPath: "inset(100% 0% 0% 0%)" });
    gsap.set(imgs[0], { scale: 1.08 });
    gsap.set(imgs.slice(1), { scale: 1.2, yPercent: 5 });
    // y: 0 clears any pixel offset so yPercent is the only vertical move
    gsap.set(caps, { y: 0, yPercent: 110, autoAlpha: 0 });
    gsap.set(caps[0], { yPercent: 0, autoAlpha: 1 });

    const tl = gsap.timeline({
      defaults: { ease: "none" },
      scrollTrigger: { trigger: el, start: "top top", end: "bottom bottom", scrub: rich ? 0.8 : 0.4 },
    });
    tl.to(imgs[0], { scale: 1, duration: 1 }, 0);
    for (let i = 1; i < n; i++) {
      const at = i - 0.5;
      tl.to(frames[i], { clipPath: "inset(0% 0% 0% 0%)", duration: 0.7 }, at)
        .to(imgs[i], { scale: 1, yPercent: 0, duration: 1.1 }, at)
        .to(imgs[i - 1], { scale: 1.06, yPercent: -4, duration: 0.7 }, at)
        // the outgoing caption leaves completely before the next one arrives
        .to(caps[i - 1], { yPercent: -110, autoAlpha: 0, duration: 0.25 }, at)
        .to(caps[i], { yPercent: 0, autoAlpha: 1, duration: 0.3 }, at + 0.3);
    }
    tl.to({}, { duration: 0.4 });

    let last = -1;
    tl.eventCallback("onUpdate", () => {
      const t = tl.time();
      let s = 0;
      for (let i = 1; i < n; i++) if (t >= i - 0.2) s = i;
      if (s === last || !step) return;
      last = s;
      step.textContent = `${pad2(s + 1)} / ${pad2(n)}`;
    });
  });

  return (
    <section className="day" ref={ref} aria-labelledby="day-title">
      <div className="day__sticky">
        <div className="day__frames">
          {BRIDAL_DAY.map((c, i) => (
            <figure className="day__frame" key={c.label} style={{ zIndex: i + 1 }}>
              <Img src={c.img} mobile={c.mobile} sizes="100vw" alt={c.alt} />
            </figure>
          ))}
        </div>
        <div className="day__shade" aria-hidden="true" />
        <div className="day__head">
          <h2 className="day__title" id="day-title">
            Gelin günü, <em>dört ölçüde.</em>
          </h2>
          <p className="day__step" aria-hidden="true">
            01 / {pad2(BRIDAL_DAY.length)}
          </p>
        </div>
        <div className="day__caps">
          {BRIDAL_DAY.map((c, i) => (
            <div className="day__cap" key={c.label}>
              <span className="day__num" aria-hidden="true">
                {pad2(i + 1)}
              </span>
              <div className="day__copy">
                <p className="day__label">{c.label}</p>
                <h3>{c.title}</h3>
                <p>{c.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
