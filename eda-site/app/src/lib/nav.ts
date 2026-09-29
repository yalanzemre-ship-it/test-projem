import { GALLERY } from "./gallery-data";
import { IMG, type NavItem, type PagePath } from "./site-data";

export const HAS_GALLERY = GALLERY.length > 0;

export const NAV: NavItem[] = [
  { to: "/", label: "Ana sayfa", img: IMG.heroA },
  { to: "/hizmetler", label: "Hizmetler", img: IMG.heroB },
  ...(HAS_GALLERY ? [{ to: "/galeri" as const, label: "Galeri", img: IMG.day3 }] : []),
  { to: "/hakkimda", label: "Hakkımda", img: IMG.studio },
  { to: "/iletisim", label: "İletişim", img: IMG.silk },
];

/** The page that follows `path` in the reading order (home is skipped). */
export function nextPage(path: PagePath): NavItem {
  const pages = NAV.filter((n) => n.to !== "/");
  const i = pages.findIndex((n) => n.to === path);
  return pages[(i + 1) % pages.length];
}

export function pageIndex(path: PagePath): { index: number; total: number } {
  return { index: NAV.findIndex((n) => n.to === path) + 1, total: NAV.length };
}
