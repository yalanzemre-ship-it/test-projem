import { useRouterState } from "@tanstack/react-router";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import { lockScroll, pad2 } from "../../lib/motion";
import { NAV } from "../../lib/nav";
import { STUDIO } from "../../lib/site-data";
import { useScrollFx } from "../../lib/use-fx";
import { Img } from "./img";
import { Monogram } from "./monogram";
import { TLink } from "./transition";

export function Header() {
  const [open, setOpen] = useState(false);
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const menuButton = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const close = () => setOpen(false);
    window.addEventListener("menu:close", close);
    return () => window.removeEventListener("menu:close", close);
  }, []);

  useEffect(() => {
    const html = document.documentElement;
    html.classList.toggle("menu-open", open);
    lockScroll(open);
    for (const id of ["main", "site-footer"]) {
      const el = document.getElementById(id);
      if (el) el.inert = open;
    }
    if (!open) return;
    const first = document.querySelector<HTMLElement>("#site-menu .menu__link");
    const t = window.setTimeout(() => first?.focus({ preventScroll: true }), 350);
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpen(false);
        menuButton.current?.focus();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => {
      window.clearTimeout(t);
      window.removeEventListener("keydown", onKey);
    };
  }, [open]);

  return (
    <>
      <a className="skip" href="#main">
        İçeriğe geç
      </a>
      <header className="hdr">
        <TLink to="/" className="hdr__brand" aria-label="Eda Yalanız Makeup Studio, ana sayfa" data-magnetic="0.25">
          <Monogram className="hdr__mono" />
          <span className="hdr__name">
            Eda Yalanız
            <br />
            Makeup Studio
          </span>
        </TLink>
        <div className="hdr__right">
          <TLink to="/iletisim" className="hdr__book" data-magnetic="0.3">
            <span className="hdr__book-label">Randevu al</span>
            <i className="vf vf--tl" aria-hidden="true" />
            <i className="vf vf--tr" aria-hidden="true" />
            <i className="vf vf--bl" aria-hidden="true" />
            <i className="vf vf--br" aria-hidden="true" />
          </TLink>
          <button
            ref={menuButton}
            type="button"
            className="hdr__menu"
            aria-expanded={open}
            aria-controls="site-menu"
            onClick={() => setOpen((o) => !o)}
            data-magnetic="0.4"
          >
            <span className="hdr__menu-lines" aria-hidden="true">
              <i />
              <i />
            </span>
            <span className="hdr__menu-label">{open ? "Kapat" : "Menü"}</span>
          </button>
        </div>
      </header>
      <Menu open={open} pathname={pathname} />
    </>
  );
}

function Menu({ open, pathname }: { open: boolean; pathname: string }) {
  const [hover, setHover] = useState(0);
  return (
    <div
      id="site-menu"
      className="menu"
      data-open={open}
      role="dialog"
      aria-modal="true"
      aria-label="Site menüsü"
      aria-hidden={!open}
      inert={!open}
    >
      <div className="menu__bg" />
      <div className="menu__grid">
        <nav className="menu__nav" aria-label="Ana menü">
          <ol className="menu__list">
            {NAV.map((item, i) => (
              <li key={item.to} className="menu__item" style={{ "--i": i } as CSSProperties}>
                <TLink
                  to={item.to}
                  className={`menu__link${pathname === item.to ? " is-current" : ""}`}
                  onMouseEnter={() => setHover(i)}
                  onFocus={() => setHover(i)}
                  aria-current={pathname === item.to ? "page" : undefined}
                >
                  <span className="menu__idx">{pad2(i + 1)}</span>
                  <span className="menu__mask">
                    <span className="menu__label">{item.label}</span>
                  </span>
                </TLink>
              </li>
            ))}
          </ol>
        </nav>
        <div className="menu__preview" aria-hidden="true">
          {NAV.map((item, i) => (
            <div key={item.to} className={`menu__shot${hover === i ? " is-on" : ""}`}>
              <Img src={item.img} sizes="34vw" alt="" />
            </div>
          ))}
        </div>
        <div className="menu__foot">
          <a href={STUDIO.phoneHref}>{STUDIO.phoneDisplay}</a>
          <a href={STUDIO.whatsapp} target="_blank" rel="noreferrer">
            WhatsApp
          </a>
          <a href={STUDIO.instagram} target="_blank" rel="noreferrer">
            Instagram
          </a>
          <span>{STUDIO.addressLines.join(", ")}</span>
        </div>
      </div>
    </div>
  );
}

export function Footer() {
  const markRef = useRef<HTMLParagraphElement>(null);

  useScrollFx(({ gsap }) => {
    const mark = markRef.current;
    if (!mark) return;
    gsap.fromTo(
      mark.querySelectorAll(".ftr__ch"),
      { yPercent: 38, "--w": 70 },
      {
        yPercent: 0,
        "--w": 125,
        ease: "none",
        stagger: 0.04,
        scrollTrigger: { trigger: mark, start: "top bottom", end: "bottom bottom", scrub: 0.6 },
      },
    );
  });

  return (
    <footer className="ftr" id="site-footer">
      <div className="ftr__cols">
        <div className="ftr__col">
          <p className="ftr__head">Sayfalar</p>
          <ul>
            {NAV.map((n) => (
              <li key={n.to}>
                <TLink to={n.to} className="ftr__link">
                  {n.label}
                </TLink>
              </li>
            ))}
          </ul>
        </div>
        <div className="ftr__col">
          <p className="ftr__head">Stüdyo</p>
          <p>
            {STUDIO.addressLines[0]}
            <br />
            {STUDIO.addressLines[1]}
          </p>
        </div>
        <div className="ftr__col">
          <p className="ftr__head">İletişim</p>
          <ul>
            <li>
              <a className="ftr__link" href={STUDIO.phoneHref}>
                {STUDIO.phoneDisplay}
              </a>
            </li>
            <li>
              <a className="ftr__link" href={STUDIO.whatsapp} target="_blank" rel="noreferrer">
                WhatsApp
              </a>
            </li>
          </ul>
        </div>
        <div className="ftr__col">
          <p className="ftr__head">Takip</p>
          <ul>
            <li>
              <a className="ftr__link" href={STUDIO.instagram} target="_blank" rel="noreferrer">
                Instagram
              </a>
            </li>
            <li>
              <a className="ftr__link" href={STUDIO.facebook} target="_blank" rel="noreferrer">
                Facebook
              </a>
            </li>
          </ul>
        </div>
      </div>
      <p className="ftr__mark" ref={markRef} aria-hidden="true">
        {"EDA YALANIZ".split("").map((ch, i) => (
          <span key={i} className="ftr__ch">
            {ch === " " ? " " : ch}
          </span>
        ))}
      </p>
      <div className="ftr__base">
        <span>© 2026 Eda Yalanız Makeup Studio</span>
        <span>Nilüfer, Bursa</span>
      </div>
    </footer>
  );
}
