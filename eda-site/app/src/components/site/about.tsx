import { useRef } from "react";
import { CERTS, IMG } from "../../lib/site-data";
import { useScrollFx } from "../../lib/use-fx";
import { Img } from "./img";

export function About({ headingLevel = 2 }: { headingLevel?: 1 | 2 }) {
  const ref = useRef<HTMLElement>(null);
  const H = headingLevel === 1 ? "h1" : "h2";

  useScrollFx(({ gsap }) => {
    const el = ref.current;
    if (!el) return;
    const frame = el.querySelector(".about__frame");
    gsap.fromTo(
      frame,
      { clipPath: "inset(14% 12% 14% 12%)" },
      {
        clipPath: "inset(0% 0% 0% 0%)",
        ease: "none",
        scrollTrigger: { trigger: frame, start: "top 90%", end: "center 55%", scrub: 0.6 },
      },
    );
    gsap.fromTo(
      el.querySelector(".about__frame img"),
      { scale: 1.3, yPercent: -6 },
      {
        scale: 1.05,
        yPercent: 6,
        ease: "none",
        scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: true },
      },
    );
  });

  return (
    <section className="about" ref={ref} aria-labelledby="about-title">
      <div className="about__media">
        <div className="about__frame">
          <Img src={IMG.studio} sizes="(max-width: 760px) 100vw, 42vw" alt="Eda Yalanız stüdyosunda, aynanın yanında otururken" />
        </div>
      </div>
      <div className="about__body">
        <H className="about__title" id="about-title">
          Stüdyoda aynı anda <em>tek kişiyle</em> çalışırım.
        </H>
        <p className="about__text">
          İstanbul Sağlık ve Sosyal Bilimler, Saç Bakımı ve Güzellik Hizmetleri mezunuyum. Beş yıldır Bursa'da çalışıyorum. Gelin
          provaları, kalıcı makyaj ve kaş tasarımı: hepsi randevu ile, acele edilmeden.
        </p>
        <blockquote className="about__quote">
          <p>“İyi makyaj fotoğrafta değil, günün sonunda aynaya bakıldığında anlaşılır.”</p>
        </blockquote>
        <ul className="certs" aria-label="Sertifikalar">
          {CERTS.map((c) => (
            <li key={c} className="certs__row">
              <span className="certs__name">{c}</span>
              <span className="certs__tag">Sertifikalı</span>
            </li>
          ))}
        </ul>
        <p className="about__sign">
          Eda Yalanız
          <span>Kurucu ve makyaj sanatçısı</span>
        </p>
      </div>
    </section>
  );
}
