// Hover distortion for photos: a brief displacement pulse through the shared
// SVG filter (#fx-distort, rendered once in the root). Desktop only; callers
// check richMotion() first.

let active: HTMLElement | null = null;
let tween: { kill: () => void } | null = null;

export async function distortPulse(el: HTMLElement, strength = 42) {
  const map = document.getElementById("fx-distort-map");
  if (!map) return;
  const { gsap } = await import("gsap");
  tween?.kill();
  if (active && active !== el) active.style.filter = "";
  active = el;
  el.style.filter = "url(#fx-distort)";
  tween = gsap.fromTo(
    map,
    { attr: { scale: 0 } },
    {
      attr: { scale: strength },
      duration: 0.32,
      ease: "sine.out",
      yoyo: true,
      repeat: 1,
      onComplete: () => {
        el.style.filter = "";
        if (active === el) active = null;
      },
    },
  );
}
