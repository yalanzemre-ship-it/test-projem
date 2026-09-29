// Real work photos from the studio. Files live in /public/assets/gallery.
// The gallery sections and the /galeri link only render when this list has items.

export type Photo = {
  /** ~800px wide, used in rails and grids */
  src: string;
  /** ~1800px wide, used in the fullscreen viewer */
  large: string;
  w: number;
  h: number;
  alt: string;
};

export const GALLERY: Photo[] = [];
