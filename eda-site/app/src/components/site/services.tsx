import { useEffect, useRef, useState } from "react";
import { distortPulse } from "../../lib/distort";
import { pad2, richMotion } from "../../lib/motion";
import { SERVICES } from "../../lib/site-data";
import { Img } from "./img";

/**
 * Interactive services index. Desktop: hovering a row opens it and a masked
 * photo follows the cursor. Touch and keyboard: rows are disclosure buttons
 * that open inline with the photo inside the panel.
 */
export function Services({ headingLevel = 2 }: { headingLevel?: 1 | 2 }) {
  const [open, setOpen] = useState<number | null>(null);
  const [floatOn, setFloatOn] = useState(false);
  const listRef = useRef<HTMLUListElement>(null);
  const floatRef = useRef<HTMLDivElement>(null);
  const rich = useRef(false);
  const H = headingLevel === 1 ? "h1" : "h2";

  useEffect(() => {
    rich.current = richMotion();
    const list = listRef.current;
    const float = floatRef.current;
    if (!rich.current || !list || !float) return;
    let alive = true;
    let teardown = () => {};
    import("gsap").then(({ gsap }) => {
      if (!alive) return;
      gsap.set(float, { xPercent: -50, yPercent: -50 });
      const x = gsap.quickTo(float, "x", { duration: 0.7, ease: "power3" });
      const y = gsap.quickTo(float, "y", { duration: 0.7, ease: "power3" });
      const r = gsap.quickTo(float, "rotation", { duration: 0.9, ease: "power3" });
      let lastX = 0;
      const onMove = (e: PointerEvent) => {
        x(e.clientX);
        y(e.clientY);
        r(Math.max(-8, Math.min(8, (e.clientX - lastX) * 0.4)));
        lastX = e.clientX;
      };
      list.addEventListener("pointermove", onMove);
      teardown = () => list.removeEventListener("pointermove", onMove);
    });
    return () => {
      alive = false;
      teardown();
    };
  }, []);

  const hoverRow = (i: number) => {
    if (!rich.current) return;
    setOpen(i);
    setFloatOn(true);
    const shot = floatRef.current?.querySelectorAll<HTMLElement>(".svc-float__shot")[i];
    if (shot) void distortPulse(shot, 30);
  };

  return (
    <section className="services" aria-labelledby="services-title">
      <div className="services__head">
        <H className="services__title" id="services-title">
          Az sayıda iş, <em>tam odak.</em>
        </H>
        <p className="services__lead">
          Her hizmet ön görüşmeyle başlar. Cilt yapısı, saç rengi ve günün ışığı konuşulmadan hiçbir uygulamaya geçilmez.
        </p>
      </div>
      <ul
        className="svc-list"
        ref={listRef}
        onPointerLeave={() => {
          if (!rich.current) return;
          setFloatOn(false);
          setOpen(null);
        }}
      >
        {SERVICES.map((s, i) => {
          const isOpen = open === i;
          return (
            <li key={s.slug} className={`svc${isOpen ? " is-open" : ""}`}>
              <button
                type="button"
                className="svc__row"
                aria-expanded={isOpen}
                aria-controls={`svc-panel-${s.slug}`}
                onPointerEnter={() => hoverRow(i)}
                onClick={() => setOpen(isOpen ? null : i)}
                data-cursor="DISCOVER"
              >
                <span className="svc__idx">{pad2(i + 1)}</span>
                <span className="svc__name">{s.name}</span>
                <span className="svc__meta">{s.meta}</span>
                <span className="svc__plus" aria-hidden="true" />
              </button>
              <div className="svc__panel" id={`svc-panel-${s.slug}`} role="region" aria-label={s.name}>
                <div className="svc__panel-inner">
                  <p className="svc__text">{s.text}</p>
                  <div className="svc__thumb">
                    <Img src={s.img} sizes="40vw" alt={s.alt} />
                  </div>
                </div>
              </div>
            </li>
          );
        })}
      </ul>
      <p className="services__note">Tüm uygulamalar randevu iledir.</p>
      <div className={`svc-float${floatOn ? " is-on" : ""}`} ref={floatRef} aria-hidden="true">
        {SERVICES.map((s, i) => (
          <div key={s.slug} className={`svc-float__shot${open === i ? " is-on" : ""}`}>
            <Img src={s.img} sizes="340px" alt="" />
          </div>
        ))}
      </div>
    </section>
  );
}
