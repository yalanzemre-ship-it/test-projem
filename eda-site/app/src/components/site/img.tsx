import type { ImgHTMLAttributes } from "react";
import type { ImgSrc } from "../../lib/site-data";

type Props = Omit<ImgHTMLAttributes<HTMLImageElement>, "src" | "srcSet" | "width" | "height"> & {
  src: ImgSrc;
  /** Vertical crop served to phones (max-width: 760px). */
  mobile?: ImgSrc;
  alt: string;
  sizes: string;
  priority?: boolean;
};

const srcSetOf = (s: ImgSrc) => s.widths.map((w) => `${s.base}-${w}.webp ${w}w`).join(", ");

/** Responsive webp from the generated asset kit (files named <base>-<width>.webp). */
export function Img({ src, mobile, alt, sizes, priority = false, ...rest }: Props) {
  const img = (
    <img
      src={`${src.base}-${src.widths[Math.min(1, src.widths.length - 1)]}.webp`}
      srcSet={srcSetOf(src)}
      sizes={sizes}
      width={src.w}
      height={src.h}
      alt={alt}
      loading={priority ? "eager" : "lazy"}
      decoding="async"
      fetchPriority={priority ? "high" : "auto"}
      draggable={false}
      {...rest}
    />
  );
  if (!mobile) return img;
  return (
    <picture className="pic">
      <source media="(max-width: 760px)" srcSet={srcSetOf(mobile)} sizes="100vw" width={mobile.w} height={mobile.h} />
      {img}
    </picture>
  );
}
