import type { CSSProperties, ReactNode } from "react";
import { pad2 } from "../../lib/motion";
import { nextPage, pageIndex } from "../../lib/nav";
import type { ImgSrc, PagePath } from "../../lib/site-data";
import { Img } from "./img";
import { TLink } from "./transition";

/** Sub-page opener: oversized title rising letter by letter, index readout, masked image strip. */
export function PageHead({
  path,
  title,
  lead,
  img,
  alt,
}: {
  path: PagePath;
  title: string;
  lead: ReactNode;
  img: ImgSrc;
  alt: string;
}) {
  const { index, total } = pageIndex(path);
  return (
    <header className="phead">
      <p className="phead__idx" aria-hidden="true">
        {pad2(index)} / {pad2(total)}
      </p>
      <h1 className="phead__title" aria-label={title}>
        {title.split("").map((ch, i) => (
          <span key={i} className="phead__ch" style={{ "--i": i } as CSSProperties} aria-hidden="true">
            {ch === " " ? " " : ch}
          </span>
        ))}
      </h1>
      <p className="phead__lead">{lead}</p>
      <div className="phead__media">
        <Img src={img} sizes="100vw" priority alt={alt} />
      </div>
    </header>
  );
}

/** Oversized next-page link: the title itself is the hit area, the cursor reads NEXT. */
export function NextPage({ from }: { from: PagePath }) {
  const next = nextPage(from);
  return (
    <section className="next" aria-label="Sonraki sayfa">
      <TLink to={next.to} className="next__link" data-cursor="NEXT">
        <span className="next__label">Sonraki sayfa</span>
        <span className="next__title">{next.label}</span>
        <span className="next__media" aria-hidden="true">
          <Img src={next.img} sizes="40vw" alt="" />
        </span>
      </TLink>
    </section>
  );
}
