import { useRef } from "react";
import { pad2 } from "../../lib/motion";
import { BRIDAL_DAY } from "../../lib/site-data";
import { useScrollFx } from "../../lib/use-fx";
import { Img } from "./img";

/**
 * Cinematic scrub: a sticky stage where scrolling advances the bridal day
 * through four scenes. Each new scene wipes up over the last while the ruler
 * marker travels. Reduced motion renders the four chapters as a static list.
 */
export function BridalDay() {
  const ref = useRef<HTMLElement>(null);

  useScrollFx(({ gsap, rich }) => {
    const el = ref.current;
    if (!el) return;
    const frames = gsap.utils.toArray<HTMLElement>(".day__frame", el);
    const caps = gsap.utils.toArray<HTMLElement>(".day__cap", el);
    const ticks = gsap.utils.toArray<HTMLElement>(".day__tick", el);
    const marker = el.querySelector(".day__marker");
    const n = frames.length;

    const tl = gsap.timeline({
      defaults: { ease: "none" },
      scrollTrigger: { trigger: el, start: "top top", end: "bottom bottom", scrub: rich ? 0.8 : 0.4 },
    });
    tl.fromTo(frames[0].querySelector("img"), { scale: 1.08 }, { scale: 1.0, duration: 1 }, 0);
    for (let i = 1; i < n; i++) {
      const at = i - 0.5;
      tl.fromTo(frames[i], { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.7 }, at)
        .fromTo(frames[i].querySelector("img"), { scale: 1.25, yPercent: 6 }, { scale: 1, yPercent: 0, duration: 1.2 }, at)
        .to(frames[i - 1].querySelector("img"), { scale: 1.06, yPercent: -5, duration: 0.7 }, at)
        .fromTo(caps[i - 1], { yPercent: 0 }, { yPercent: -120, duration: 0.35 }, at)
        .fromTo(caps[i], { yPercent: 120 }, { yPercent: 0, duration: 0.4 }, at + 0.3);
    }
    tl.fromTo(marker, { "--t": 0 }, { "--t": 1, duration: n - 0.5 }, 0);
    let last = 0;
    tl.eventCallback("onUpdate", () => {
      const t = tl.time();
      let step = 0;
      for (let i = 1; i < n; i++) if (t >= i - 0.2) step = i;
      if (step === last) return;
      last = step;
      ticks.forEach((tick, k) => tick.classList.toggle("is-on", k <= step));
    });
  });

  return (
    <section className="day" ref={ref} aria-labelledby="day-title">
      <div className="day__sticky">
        <div className="day__frames">
          {BRIDAL_DAY.map((c, i) => (
            <figure className="day__frame" key={c.label} style={{ zIndex: i + 1 }}>
              <Img src={c.img} sizes="100vw" alt={c.alt} />
            </figure>
          ))}
        </div>
        <div className="day__shade" aria-hidden="true" />
        <h2 className="day__title" id="day-title">
          Gelin günü, <em>dört ölçüde.</em>
        </h2>
        <div className="day__rail">
          <span className="day__marker" aria-hidden="true" />
          <ol aria-label="Gelin günü aşamaları">
            {BRIDAL_DAY.map((c, i) => (
              <li key={c.label} className={`day__tick${i === 0 ? " is-on" : ""}`}>
                {c.label}
              </li>
            ))}
          </ol>
        </div>
        <div className="day__caps">
          {BRIDAL_DAY.map((c, i) => (
            <div className="day__cap" key={c.label}>
              <span className="day__num" aria-hidden="true">
                {pad2(i + 1)}
              </span>
              <div className="day__copy">
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
