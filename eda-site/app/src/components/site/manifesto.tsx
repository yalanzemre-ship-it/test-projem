import { useRef } from "react";
import { useScrollFx } from "../../lib/use-fx";

const WORDS = ["Makyaj", "bir", "maske", "değil,", "bir", "ölçü", "işidir."];
const ACCENT = new Set([5, 6]);

const STATS = [
  { value: "5", label: "Yıl deneyim" },
  { value: "6", label: "Uzmanlık alanı" },
  { value: "1:1", label: "Özel seans" },
  { value: "4", label: "Sertifika" },
];

/** Kinetic statement: words gain ink as you scroll, while a measuring tape slides beneath. */
export function Manifesto() {
  const ref = useRef<HTMLElement>(null);

  useScrollFx(({ gsap, rich }) => {
    const el = ref.current;
    if (!el) return;
    const words = el.querySelectorAll<HTMLElement>(".mw");
    const tl = gsap.timeline({
      scrollTrigger: { trigger: el.querySelector(".manifesto__text"), start: "top 85%", end: "bottom 45%", scrub: 0.6 },
    });
    words.forEach((w, i) => {
      tl.fromTo(
        w,
        { color: "#4b3d39", yPercent: rich ? 18 : 0 },
        { color: ACCENT.has(i) ? "#c0736b" : "#f2e9e6", yPercent: 0, ease: "none", duration: 1 },
        i * 0.55,
      );
    });
    gsap.fromTo(
      el.querySelector(".tape__scale"),
      { xPercent: 0 },
      {
        xPercent: -25,
        ease: "none",
        scrollTrigger: { trigger: el.querySelector(".tape"), start: "top bottom", end: "bottom top", scrub: 0.4 },
      },
    );
  });

  return (
    <section className="manifesto" ref={ref} aria-label="Yaklaşım">
      <p className="manifesto__text">
        {WORDS.map((w, i) => (
          <span key={i} className={`mw${ACCENT.has(i) ? " mw--accent" : ""}`}>
            {w}
          </span>
        ))}
      </p>
      <div className="tape">
        <div className="tape__window" aria-hidden="true">
          <div className="tape__scale" />
        </div>
        <dl className="tape__stats">
          {STATS.map((s) => (
            <div className="tape__stat" key={s.label}>
              <dt>{s.label}</dt>
              <dd>{s.value}</dd>
            </div>
          ))}
        </dl>
      </div>
    </section>
  );
}
