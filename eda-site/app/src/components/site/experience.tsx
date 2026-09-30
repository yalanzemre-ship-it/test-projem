import { useEffect, useRef } from "react";
import { loadGsap, richMotion } from "../../lib/motion";

/** Lenis smooth scroll bridged to GSAP's ticker. Desktop pointers only; touch keeps native scroll. */
export function SmoothScroll() {
  useEffect(() => {
    if (!richMotion()) return;
    let alive = true;
    let teardown = () => {};
    Promise.all([import("lenis"), loadGsap()]).then(([{ default: Lenis }, { gsap, ScrollTrigger }]) => {
      if (!alive) return;
      const lenis = new Lenis({ autoRaf: false, lerp: 0.085, wheelMultiplier: 0.95 });
      window.__lenis = lenis;
      lenis.on("scroll", ScrollTrigger.update);
      const tick = (time: number) => lenis.raf(time * 1000);
      gsap.ticker.add(tick);
      gsap.ticker.lagSmoothing(0);
      teardown = () => {
        gsap.ticker.remove(tick);
        lenis.destroy();
        delete window.__lenis;
      };
    });
    return () => {
      alive = false;
      teardown();
    };
  }, []);
  return null;
}

/**
 * Custom cursor: a precise dot plus a trailing ring. Over [data-cursor] targets
 * the ring grows into a labelled disc (VIEW, DISCOVER, NEXT...). Elements with
 * [data-magnetic] lean toward the pointer. Fine pointers only.
 */
export function Cursor() {
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const root = rootRef.current;
    if (!root || !richMotion()) return;
    const ring = root.querySelector<HTMLElement>(".cursor__ring")!;
    const dot = root.querySelector<HTMLElement>(".cursor__dot")!;
    const text = root.querySelector<HTMLElement>(".cursor__text")!;
    const html = document.documentElement;
    let alive = true;
    let teardown = () => {};

    import("gsap").then(({ gsap }) => {
      if (!alive) return;
      html.classList.add("has-cursor");
      gsap.set([ring, dot], { xPercent: -50, yPercent: -50, x: -200, y: -200 });
      const ringX = gsap.quickTo(ring, "x", { duration: 0.55, ease: "power3" });
      const ringY = gsap.quickTo(ring, "y", { duration: 0.55, ease: "power3" });
      const dotX = gsap.quickTo(dot, "x", { duration: 0.1, ease: "power3" });
      const dotY = gsap.quickTo(dot, "y", { duration: 0.1, ease: "power3" });

      let px = -200;
      let py = -200;
      let magnet: HTMLElement | null = null;
      let raf = 0;

      const pullMagnet = () => {
        if (!magnet) return;
        const r = magnet.getBoundingClientRect();
        const strength = Number(magnet.dataset.magnetic) || 0.3;
        gsap.to(magnet, {
          x: (px - (r.left + r.width / 2)) * strength,
          y: (py - (r.top + r.height / 2)) * strength,
          duration: 0.6,
          ease: "power3.out",
        });
      };

      const setTarget = (target: Element | null) => {
        // Cross-origin iframes (the map) draw their own cursor; hide ours over them.
        if (target?.tagName === "IFRAME") {
          root.classList.remove("is-visible");
          return;
        }
        const labelled = target?.closest<HTMLElement>("[data-cursor]") ?? null;
        const interactive = target?.closest("a, button, [role='button'], input, textarea, select, summary") ?? null;
        const nextMagnet = target?.closest<HTMLElement>("[data-magnetic]") ?? null;
        if (nextMagnet !== magnet) {
          if (magnet) gsap.to(magnet, { x: 0, y: 0, duration: 0.9, ease: "elastic.out(1, 0.45)" });
          magnet = nextMagnet;
        }
        const label = labelled?.dataset.cursor ?? "";
        if (text.textContent !== label) text.textContent = label;
        root.classList.toggle("is-label", label !== "");
        root.classList.toggle("is-hover", label === "" && interactive !== null);
      };

      const onMove = (e: PointerEvent) => {
        if (e.pointerType === "touch") return;
        px = e.clientX;
        py = e.clientY;
        root.classList.add("is-visible");
        ringX(px);
        ringY(py);
        dotX(px);
        dotY(py);
        pullMagnet();
      };
      const onOver = (e: PointerEvent) => setTarget(e.target as Element);
      const onScroll = () => {
        if (raf) return;
        raf = requestAnimationFrame(() => {
          raf = 0;
          setTarget(document.elementFromPoint(px, py));
        });
      };
      const onLeave = () => root.classList.remove("is-visible");
      const onDown = () => root.classList.add("is-down");
      const onUp = () => root.classList.remove("is-down");

      window.addEventListener("pointermove", onMove, { passive: true });
      document.addEventListener("pointerover", onOver);
      window.addEventListener("scroll", onScroll, { passive: true });
      html.addEventListener("pointerleave", onLeave);
      window.addEventListener("pointerdown", onDown);
      window.addEventListener("pointerup", onUp);

      teardown = () => {
        window.removeEventListener("pointermove", onMove);
        document.removeEventListener("pointerover", onOver);
        window.removeEventListener("scroll", onScroll);
        html.removeEventListener("pointerleave", onLeave);
        window.removeEventListener("pointerdown", onDown);
        window.removeEventListener("pointerup", onUp);
        cancelAnimationFrame(raf);
      };
    });

    return () => {
      alive = false;
      teardown();
      html.classList.remove("has-cursor");
    };
  }, []);

  return (
    <div ref={rootRef} className="cursor" aria-hidden="true">
      <div className="cursor__ring">
        <span className="cursor__text" />
      </div>
      <div className="cursor__dot" />
    </div>
  );
}

/** Shared SVG filter used by the photo hover distortion (see lib/distort.ts). */
export function DistortDefs() {
  return (
    <svg className="fx-defs" width="0" height="0" aria-hidden="true" focusable="false">
      <defs>
        <filter id="fx-distort" x="-5%" y="-5%" width="110%" height="110%" colorInterpolationFilters="sRGB">
          <feTurbulence type="fractalNoise" baseFrequency="0.006 0.02" numOctaves={2} seed={7} result="noise" />
          <feDisplacementMap
            id="fx-distort-map"
            in="SourceGraphic"
            in2="noise"
            scale={0}
            xChannelSelector="R"
            yChannelSelector="G"
          />
        </filter>
      </defs>
    </svg>
  );
}
