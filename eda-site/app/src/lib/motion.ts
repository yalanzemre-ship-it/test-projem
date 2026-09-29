// Client-only environment checks. Call these inside effects or handlers, never
// during render or at module top level (the page is server-rendered).

import type Lenis from "lenis";

export function prefersReducedMotion(): boolean {
  return typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/** Desktop-class pointer: mouse or trackpad with hover. */
export function hasFinePointer(): boolean {
  return typeof window !== "undefined" && window.matchMedia("(hover: hover) and (pointer: fine)").matches;
}

/** Heavy effects (smooth scroll, cursor, distortion) run only here. */
export function richMotion(): boolean {
  return hasFinePointer() && !prefersReducedMotion();
}

declare global {
  interface Window {
    __lenis?: Lenis;
  }
}

export function getLenis(): Lenis | undefined {
  return typeof window === "undefined" ? undefined : window.__lenis;
}

export function scrollToTop(): void {
  const lenis = getLenis();
  if (lenis) lenis.scrollTo(0, { immediate: true, force: true });
  window.scrollTo(0, 0);
}

export function lockScroll(locked: boolean): void {
  const lenis = getLenis();
  if (lenis) {
    if (locked) lenis.stop();
    else lenis.start();
  }
  document.documentElement.classList.toggle("is-locked", locked);
}

/** Lazy GSAP + ScrollTrigger, registered once. */
export async function loadGsap() {
  const [{ gsap }, { ScrollTrigger }] = await Promise.all([import("gsap"), import("gsap/ScrollTrigger")]);
  gsap.registerPlugin(ScrollTrigger);
  return { gsap, ScrollTrigger };
}

export const pad2 = (n: number) => String(n).padStart(2, "0");
