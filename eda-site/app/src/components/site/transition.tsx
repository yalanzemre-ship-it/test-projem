import { Link, useRouter, useRouterState } from "@tanstack/react-router";
import {
  createContext,
  useCallback,
  useContext,
  useRef,
  type AnchorHTMLAttributes,
  type MouseEvent,
  type ReactNode,
} from "react";
import { getLenis, loadGsap, prefersReducedMotion, scrollToTop } from "../../lib/motion";
import type { PagePath } from "../../lib/site-data";

const LABEL: Record<PagePath, string> = {
  "/": "Ana sayfa",
  "/hizmetler": "Hizmetler",
  "/galeri": "Galeri",
  "/hakkimda": "Hakkımda",
  "/iletisim": "İletişim",
};

type PageNav = { go: (to: PagePath) => Promise<void> };
const NavContext = createContext<PageNav>({ go: async () => {} });
export const usePageNav = () => useContext(NavContext);

const closeMenu = () => window.dispatchEvent(new CustomEvent("menu:close"));

/**
 * Premium page transition: two panels wipe up over the page carrying the
 * destination name, the route changes underneath, then the panels lift away.
 * Reduced motion navigates instantly.
 */
export function TransitionProvider({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const curtainRef = useRef<HTMLDivElement>(null);
  const wordRef = useRef<HTMLSpanElement>(null);
  const busy = useRef(false);
  const current = useRef(pathname);
  current.current = pathname;

  const go = useCallback(
    async (to: PagePath) => {
      if (busy.current) return;
      if (to === current.current) {
        closeMenu();
        const lenis = getLenis();
        if (lenis) lenis.scrollTo(0);
        else window.scrollTo({ top: 0, behavior: prefersReducedMotion() ? "auto" : "smooth" });
        return;
      }
      const curtain = curtainRef.current;
      if (!curtain || prefersReducedMotion()) {
        closeMenu();
        await router.navigate({ to });
        scrollToTop();
        return;
      }

      busy.current = true;
      const root = document.documentElement;
      try {
        const { gsap, ScrollTrigger } = await loadGsap();
        const panels = Array.from(curtain.querySelectorAll<HTMLElement>(".curtain__panel"));
        const word = wordRef.current;
        if (word) word.textContent = LABEL[to];
        gsap.set(curtain, { visibility: "visible" });
        await gsap
          .timeline()
          .fromTo(panels, { yPercent: 100 }, { yPercent: 0, duration: 0.8, ease: "power4.inOut", stagger: 0.09 })
          .fromTo(word, { yPercent: 115 }, { yPercent: 0, duration: 0.6, ease: "power3.out" }, "-=0.4");
        root.dataset.transition = "out";
        closeMenu();
        await router.navigate({ to });
        scrollToTop();
        ScrollTrigger.refresh();
        await gsap
          .timeline()
          .to(word, { yPercent: -115, duration: 0.45, ease: "power3.in", delay: 0.1 })
          .to(panels.slice().reverse(), { yPercent: -100, duration: 0.85, ease: "power4.inOut", stagger: 0.08 }, "-=0.2");
        gsap.set(curtain, { visibility: "hidden" });
      } finally {
        delete root.dataset.transition;
        busy.current = false;
      }
    },
    [router],
  );

  return (
    <NavContext.Provider value={{ go }}>
      {children}
      <div className="curtain" ref={curtainRef} aria-hidden="true">
        <div className="curtain__panel curtain__panel--accent" />
        <div className="curtain__panel curtain__panel--ink" />
        <div className="curtain__stage">
          <span className="curtain__mask">
            <span className="curtain__word" ref={wordRef} />
          </span>
        </div>
      </div>
    </NavContext.Provider>
  );
}

type TLinkProps = Omit<AnchorHTMLAttributes<HTMLAnchorElement>, "href"> & {
  to: PagePath;
  children: ReactNode;
};

/** Internal link that plays the page transition. Modified clicks behave natively. */
export function TLink({ to, onClick, children, ...rest }: TLinkProps) {
  const { go } = usePageNav();
  return (
    <Link
      to={to}
      {...rest}
      onClick={(e: MouseEvent<HTMLAnchorElement>) => {
        onClick?.(e);
        if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        e.preventDefault();
        void go(to);
      }}
    >
      {children}
    </Link>
  );
}
