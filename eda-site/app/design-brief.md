# Design brief: Eda Yalanız Makeup Studio

**Design read:** Brides-to-be and permanent-makeup clients in Bursa choosing a single-chair studio; the register is calm, exact and quietly luxurious, never glossy or loud.

**Concept spine:** *The measure* (tool / precision instrument). The studio's own line is "Her yüz kendi ölçüsünde" and "Makyaj bir maske değil, bir ölçü işidir"; brow work is literally measured (PhiBrows, golden-ratio calipers). So the site is a measuring instrument: hairline rulers and tick scales, mono readouts, a fixed scroll ruler on the right edge, a cursor that reads its target, type that stretches and compresses on Archivo's width axis.

**Delivery tier:** spectacle (the user asked for custom cursor, magnetic hover, smooth scroll, scroll-linked type, photo distortion, cinematic scrub, page transitions, editorial menu).

Animation mode: non-animated — user picked Non-animated at intake

**Tier-1 technique:** D2 sticky-stack chapters with clip-path scrub ("Gelin günü, dört ölçüde"): a sticky stage where scroll advances four generated scenes of the bridal day (ön görüşme, prova, sabah, akşam), each wiping up over the last while a ruler marker travels. It enacts the spine: the day is measured out in four marks. **Second beat:** D1 horizontal cinema rail for the real work gallery with a fullscreen clip-wipe viewer. Custom cursor (VIEW / DISCOVER / NEXT / PREV / CLOSE / WRITE) per the spectacle contract.

**Anti-convergence ledger:** first build in this chat, so all six axes are derived from the studio's material world (veil, pigment, brow string, calipers, mirror bulbs): palette warm ink + rose-brick; type Archivo width-axis + IBM Plex Mono; hero image-as-canvas with bottom-left type; Tier-1 D2 scrub; garments listed below (none of the rationed trio except one flood-free band shift); corners sharp, circles only for pointing/moving things (cursor, gallery badge).

## Locked palette

| Token | Hex | Use |
|---|---|---|
| ink | `#15100F` | ground, every section (one dark theme) |
| ink-2 | `#1D1715` | menu surface, giant quote mark |
| ink-3 | `#4B3D39` | un-inked manifesto words |
| mute | `#9A8C87` | secondary text, mono labels |
| bone | `#F2E9E6` | primary type |
| accent | `#C0736B` | the one accent |
| accent-deep | `#9C544E` | fills of the same accent (cursor disc, curtain, band hover) |

Defense: `#9C544E` is the studio's existing brand color (from edayalanizmakeup.com); it is lifted to `#C0736B` for AA text contrast on the dark ground. Not a banned family: no orange/amber, no neon, no beige+brass, no violet.

## Locked type

- Display: **Archivo** variable (wdth 62 to 125, wght 100 to 900), the studio's existing brand face. The width axis is the kinetic material (`--w`).
- Readouts: **IBM Plex Mono** 400/500, for ruler labels, indices and metadata.
- No serif. Emphasis is Archivo italic in the accent color.

## Section plan (home)

1. Hero: image-as-canvas, bottom-left type, 2-line headline. Eyebrow 1.
2. Manifesto: full-width kinetic statement + measuring tape stats strip.
3. Services: interactive index rows with cursor-following masked photo (hover-accordion).
4. Gelin günü: sticky cinematic scrub (Tier-1).
5. Galeri: pinned horizontal rail + fullscreen viewer (renders only when real photos exist).
6. About: off-grid split with masked tall photo + ruled certificate list.
7. Voices: one large quote at a time over an oversized quotation mark (second-read moment). Mono section label = eyebrow 2.
8. Contact: giant headline over silk plate + full-width band CTA + info columns. Eyebrow 3.

Eyebrow budget ceil(8/3) = 3, used exactly. Sub-pages: /hizmetler, /galeri, /hakkimda, /iletisim, each opened by a letter-rise page head and closed by an oversized next-page link.

## Asset plan

Generated on Higgsfield, no people (portfolio honesty: the gallery uses only the studio's real photos):
hero-a (studio vanity at dusk), hero-b (vanity from above), day-1..4 (the four bridal-day scenes), svc-* (six service still lifes), studio (single chair + bulb mirror), silk (contact plate). Brand: EY monogram outlined from Archivo, favicon set, 1200x630 OG card. Reference boards in `/refs`.

## CTA inventory (one garment each)

- Nav "Randevu al": viewfinder corner brackets that close around the label.
- Hero "Randevu al": label compresses on the width axis while a ruler underline slides its ticks; magnetic.
- Hero "Hizmetler": arrow that travels along a drawn hairline path.
- Service rows: whole row shifts and the name stretches to full width in accent.
- Gallery "Tüm galeri": circular text badge that rotates with scroll.
- Contact "WhatsApp'tan yaz": full-width band that shears and shifts grade, label rolls.
- "Yol tarifi": mono readout that decodes its label on hover.
- Next page: oversized title as the hit area, image reveals from center, cursor NEXT.
- Menu: toggle whose two hairlines cross into an X.

## Motion and fallbacks

Lenis smooth scroll bridged to GSAP ticker (desktop fine pointers only; touch keeps native scroll). Intros are CSS keyframes on mount; scroll effects animate transform, clip-path and color only. Mobile: no Lenis, no cursor, no magnetic, no distortion, gallery becomes a native swipe rail, service photos show inline. `prefers-reduced-motion`: every animation and transition collapsed, the bridal day renders as a static 2x2 story, no scroll hijack, instant page changes.
