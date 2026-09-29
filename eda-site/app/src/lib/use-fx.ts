import { useEffect } from "react";
import { hasFinePointer, loadGsap, prefersReducedMotion } from "./motion";

export type Fx = {
  gsap: typeof import("gsap").gsap;
  ScrollTrigger: typeof import("gsap/ScrollTrigger").ScrollTrigger;
  /** true on mouse/trackpad devices; false on touch (lighter effects) */
  rich: boolean;
};

/**
 * Runs scroll-linked GSAP setup after mount, inside a gsap.context that is
 * reverted on unmount. Skipped entirely under prefers-reduced-motion, so every
 * caller's static markup is the reduced-motion fallback.
 */
export function useScrollFx(setup: (fx: Fx) => void | (() => void), deps: unknown[] = []) {
  useEffect(() => {
    if (prefersReducedMotion()) return;
    let dead = false;
    let ctx: { revert: () => void } | undefined;
    let extra: void | (() => void);
    loadGsap().then(({ gsap, ScrollTrigger }) => {
      if (dead) return;
      ctx = gsap.context(() => {
        extra = setup({ gsap, ScrollTrigger, rich: hasFinePointer() });
      });
      ScrollTrigger.refresh();
    });
    return () => {
      dead = true;
      if (typeof extra === "function") extra();
      ctx?.revert();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
}
