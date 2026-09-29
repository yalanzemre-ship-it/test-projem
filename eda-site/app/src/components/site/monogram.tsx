// "EY" monogram, outlined from Archivo (width 125, weight 700): the studio's
// existing type, so the mark renders identically everywhere without a font load.
const D =
  "M0 687V0H704V136H173V271H642V405H173V550H712V687ZM1128 687V411L791 0H997L1214 275H1224L1443 0H1639L1301 411V687Z";

export function Monogram({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 1639 687" role="img" aria-label="EY">
      <path d={D} fill="currentColor" />
    </svg>
  );
}
