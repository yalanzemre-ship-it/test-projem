import type { ImgHTMLAttributes } from "react";
import type { ImgSrc } from "../../lib/site-data";

type Props = Omit<ImgHTMLAttributes<HTMLImageElement>, "src" | "srcSet" | "width" | "height"> & {
  src: ImgSrc;
  alt: string;
  sizes: string;
  priority?: boolean;
};

/** Responsive webp from the generated asset kit (files named <base>-<width>.webp). */
export function Img({ src, alt, sizes, priority = false, ...rest }: Props) {
  const srcSet = src.widths.map((w) => `${src.base}-${w}.webp ${w}w`).join(", ");
  const fallback = `${src.base}-${src.widths[Math.min(1, src.widths.length - 1)]}.webp`;
  return (
    <img
      src={fallback}
      srcSet={srcSet}
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
}
