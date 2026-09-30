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

/** Kinetic statement: words gain ink as you scroll. */
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
        { color: "#d8cbc7", yPercent: rich ? 18 : 0 },
        { color: ACCENT.has(i) ? "#9c544e" : "#1c1614", yPercent: 0, ease: "none", duration: 1 },
        i * 0.55,
      );
    });
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
