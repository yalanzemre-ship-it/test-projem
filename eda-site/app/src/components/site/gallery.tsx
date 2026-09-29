import { useCallback, useEffect, useRef, useState, type CSSProperties, type PointerEvent } from "react";
import { distortPulse } from "../../lib/distort";
import { GALLERY, type Photo } from "../../lib/gallery-data";
import { loadGsap, lockScroll, pad2, prefersReducedMotion, richMotion } from "../../lib/motion";
import { useScrollFx } from "../../lib/use-fx";
import { TLink } from "./transition";

function useLightbox() {
  const [index, setIndex] = useState<number | null>(null);
  const openerRef = useRef<HTMLElement | null>(null);
  const open = useCallback((i: number, opener: HTMLElement) => {
    openerRef.current = opener;
    setIndex(i);
  }, []);
  const close = useCallback(() => {
    setIndex(null);
    openerRef.current?.focus({ preventScroll: true });
  }, []);
  return { index, setIndex, open, close };
}

function PhotoImg({ p, sizes, eager = false }: { p: Photo; sizes: string; eager?: boolean }) {
  return (
    <img
      src={p.src}
      srcSet={`${p.src} 800w, ${p.large} 1800w`}
      sizes={sizes}
      width={p.w}
      height={p.h}
      alt={p.alt}
      loading={eager ? "eager" : "lazy"}
      decoding="async"
      draggable={false}
    />
  );
}

const pulse = (e: PointerEvent<HTMLElement>) => {
  if (e.pointerType !== "mouse" || !richMotion()) return;
  const img = e.currentTarget.querySelector("img");
  if (img) void distortPulse(img);
};

/** Home: pinned horizontal rail of real work photos. Touch and reduced motion get a native swipe rail. */
export function GalleryRail({ limit = 10 }: { limit?: number }) {
  const photos = GALLERY.slice(0, limit);
  const ref = useRef<HTMLElement>(null);
  const trackRef = useRef<HTMLDivElement>(null);
  const lb = useLightbox();

  useScrollFx(({ gsap, rich }) => {
    const el = ref.current;
    const track = trackRef.current;
    if (!el || !track || !rich) return;
    el.classList.add("is-pinned");
    const distance = () => Math.max(0, track.scrollWidth - window.innerWidth);
    const setHeight = () => {
      el.style.height = `${distance() + window.innerHeight}px`;
    };
    setHeight();
    const tl = gsap.timeline({
      defaults: { ease: "none" },
      scrollTrigger: {
        trigger: el,
        start: "top top",
        end: "bottom bottom",
        scrub: 0.7,
        invalidateOnRefresh: true,
        onRefreshInit: setHeight,
      },
    });
    tl.to(track, { x: () => -distance(), duration: 1 }, 0)
      .fromTo(el.querySelectorAll(".rail__frame img"), { xPercent: -7 }, { xPercent: 7, duration: 1 }, 0)
      .fromTo(el.querySelector(".rail__bar i"), { scaleX: 0 }, { scaleX: 1, duration: 1 }, 0)
      .fromTo(el.querySelector(".rail__badge-ring"), { rotation: 0 }, { rotation: 300, duration: 1 }, 0);
    return () => {
      el.classList.remove("is-pinned");
      el.style.height = "";
    };
  });

  if (photos.length === 0) return null;

  return (
    <section className="rail" ref={ref} aria-labelledby="rail-title">
      <div className="rail__sticky">
        <div className="rail__head">
          <h2 className="rail__title" id="rail-title">
            Galeri
          </h2>
          <p className="rail__count">{pad2(GALLERY.length)} kare, stüdyodan</p>
        </div>
        <div className="rail__track" ref={trackRef}>
          {photos.map((p, i) => (
            <button
              key={p.src}
              type="button"
              className="rail__item"
              style={{ "--r": p.w / p.h, "--k": i % 4 } as CSSProperties}
              onClick={(e) => lb.open(i, e.currentTarget)}
              onPointerEnter={pulse}
              data-cursor="VIEW"
              aria-label={`Fotoğrafı büyüt: ${p.alt}`}
            >
              <span className="rail__frame">
                <PhotoImg p={p} sizes="(max-width: 760px) 70vw, 30vw" />
              </span>
              <span className="rail__cap">{pad2(i + 1)}</span>
            </button>
          ))}
          <TLink to="/galeri" className="rail__badge" data-cursor="DISCOVER">
            <svg className="rail__badge-ring" viewBox="0 0 200 200" aria-hidden="true">
              <defs>
                <path id="rail-circle" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0" />
              </defs>
              <text>
                <textPath href="#rail-circle">TÜM GALERİ · TÜM GALERİ · TÜM GALERİ ·</textPath>
              </text>
            </svg>
            <span className="rail__badge-core">Tüm galeri</span>
          </TLink>
        </div>
        <div className="rail__bar" aria-hidden="true">
          <i />
        </div>
      </div>
      <Lightbox photos={photos} index={lb.index} onIndex={lb.setIndex} onClose={lb.close} />
    </section>
  );
}

/** /galeri: staggered masonry of every photo with scroll mask reveals. */
export function GalleryGrid() {
  const ref = useRef<HTMLDivElement>(null);
  const lb = useLightbox();

  useScrollFx(({ gsap }) => {
    const el = ref.current;
    if (!el) return;
    gsap.utils.toArray<HTMLElement>(".grid__frame", el).forEach((frame) => {
      gsap.fromTo(
        frame,
        { clipPath: "inset(10% 6% 10% 6%)" },
        {
          clipPath: "inset(0% 0% 0% 0%)",
          ease: "none",
          scrollTrigger: { trigger: frame, start: "top bottom", end: "top 55%", scrub: 0.5 },
        },
      );
      gsap.fromTo(
        frame.querySelector("img"),
        { yPercent: -6, scale: 1.12 },
        {
          yPercent: 6,
          scale: 1.12,
          ease: "none",
          scrollTrigger: { trigger: frame, start: "top bottom", end: "bottom top", scrub: true },
        },
      );
    });
  });

  // Three staggered columns on desktop (the middle one drops lower); on phones
  // the columns dissolve (display: contents) into a two-column grid.
  const cols: { p: Photo; i: number }[][] = [[], [], []];
  GALLERY.forEach((p, i) => cols[i % 3].push({ p, i }));

  return (
    <div className="grid" ref={ref}>
      {cols.map((col, c) => (
        <div className={`grid__col grid__col--${c}`} key={c}>
          {col.map(({ p, i }) => (
            <button
              key={p.src}
              type="button"
              className="grid__item"
              style={{ "--r": p.w / p.h } as CSSProperties}
              onClick={(e) => lb.open(i, e.currentTarget)}
              onPointerEnter={pulse}
              data-cursor="VIEW"
              aria-label={`Fotoğrafı büyüt: ${p.alt}`}
            >
              <span className="grid__frame">
                <PhotoImg p={p} sizes="(max-width: 760px) 50vw, 33vw" eager={i < 3} />
              </span>
              <span className="grid__cap">{pad2(i + 1)}</span>
            </button>
          ))}
        </div>
      ))}
      <Lightbox photos={GALLERY} index={lb.index} onIndex={lb.setIndex} onClose={lb.close} />
    </div>
  );
}

/** Fullscreen viewer: clip-path wipes between photos, cursor reads PREV / NEXT per half. */
function Lightbox({
  photos,
  index,
  onIndex,
  onClose,
}: {
  photos: Photo[];
  index: number | null;
  onIndex: (i: number) => void;
  onClose: () => void;
}) {
  const rootRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  const prevIndex = useRef<number | null>(null);
  const touchX = useRef<number | null>(null);
  const isOpen = index !== null;
  const total = photos.length;

  const step = useCallback(
    (dir: 1 | -1) => {
      if (index === null) return;
      onIndex((index + dir + total) % total);
    },
    [index, onIndex, total],
  );

  useEffect(() => {
    if (!isOpen) return;
    lockScroll(true);
    closeRef.current?.focus({ preventScroll: true });
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
      if (e.key === "ArrowRight") step(1);
      if (e.key === "ArrowLeft") step(-1);
    };
    window.addEventListener("keydown", onKey);
    return () => {
      window.removeEventListener("keydown", onKey);
      lockScroll(false);
    };
  }, [isOpen, onClose, step]);

  // Open reveal and photo-to-photo wipes.
  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    const from = prevIndex.current;
    prevIndex.current = index;
    if (index === null || prefersReducedMotion()) return;
    const current = root.querySelector<HTMLElement>(`[data-slide="${index}"]`);
    if (!current) return;
    loadGsap().then(({ gsap }) => {
      if (from === null) {
        gsap.fromTo(root, { clipPath: "inset(50% 0% 50% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.75, ease: "power4.inOut" });
        gsap.fromTo(current.querySelector("img"), { scale: 1.18 }, { scale: 1, duration: 1.1, ease: "power3.out" });
        return;
      }
      const forward = (index > from && !(from === 0 && index === total - 1)) || (from === total - 1 && index === 0);
      gsap.fromTo(
        current,
        { clipPath: forward ? "inset(0% 0% 0% 100%)" : "inset(0% 100% 0% 0%)" },
        { clipPath: "inset(0% 0% 0% 0%)", duration: 0.8, ease: "power4.inOut" },
      );
      gsap.fromTo(current.querySelector("img"), { scale: 1.12, xPercent: forward ? 6 : -6 }, { scale: 1, xPercent: 0, duration: 1, ease: "power3.out" });
    });
  }, [index, total]);

  const show = (i: number) => index === i || prevIndex.current === i;

  return (
    <div
      ref={rootRef}
      className={`lb${isOpen ? " is-open" : ""}`}
      role="dialog"
      aria-modal="true"
      aria-label="Fotoğraf görüntüleyici"
      aria-hidden={!isOpen}
      inert={!isOpen}
      onTouchStart={(e) => {
        touchX.current = e.touches[0].clientX;
      }}
      onTouchEnd={(e) => {
        if (touchX.current === null) return;
        const dx = e.changedTouches[0].clientX - touchX.current;
        touchX.current = null;
        if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
      }}
    >
      <div className="lb__stage">
        {photos.map((p, i) =>
          show(i) ? (
            <figure key={p.src} className={`lb__slide${index === i ? " is-current" : ""}`} data-slide={i}>
              <img src={p.large} width={p.w} height={p.h} alt={p.alt} decoding="async" draggable={false} />
            </figure>
          ) : null,
        )}
      </div>
      <button type="button" className="lb__half lb__half--prev" onClick={() => step(-1)} data-cursor="PREV" aria-label="Önceki fotoğraf" />
      <button type="button" className="lb__half lb__half--next" onClick={() => step(1)} data-cursor="NEXT" aria-label="Sonraki fotoğraf" />
      <div className="lb__bar">
        <span className="lb__count">
          {index !== null ? pad2(index + 1) : "00"} / {pad2(total)}
        </span>
        <button type="button" ref={closeRef} className="lb__close" onClick={onClose} data-cursor="CLOSE">
          Kapat
        </button>
      </div>
    </div>
  );
}
