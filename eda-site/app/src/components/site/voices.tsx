import { useState, type CSSProperties } from "react";
import { pad2 } from "../../lib/motion";
import { REVIEWS } from "../../lib/site-data";

/** One review at a time. Clicking the stage advances (cursor reads NEXT); buttons cover keyboard use. */
export function Voices() {
  const [i, setI] = useState(0);
  const n = REVIEWS.length;
  const r = REVIEWS[i];
  const go = (d: number) => setI((v) => (v + d + n) % n);

  return (
    <section className="voices" aria-labelledby="voices-title">
      <span className="voices__mark" aria-hidden="true">
        “
      </span>
      <h2 className="voices__title" id="voices-title">
        Söyleyeni müşterilerim olsun.
      </h2>
      <div className="voices__stage" onClick={() => go(1)} data-cursor="NEXT" aria-live="polite">
        <p className="voices__stars" aria-label="5 üzerinden 5 puan">
          ★★★★★
        </p>
        <blockquote className="voices__quote" key={i}>
          <p>
            {r.quote.split(" ").map((w, k) => (
              <span key={k} className="vw" style={{ "--k": k } as CSSProperties}>
                <span>{w}</span>{" "}
              </span>
            ))}
          </p>
          <footer className="voices__who">
            {r.name} · {r.role}
          </footer>
        </blockquote>
      </div>
      <div className="voices__nav">
        <button type="button" className="voices__arrow" onClick={() => go(-1)} aria-label="Önceki yorum" data-magnetic="0.4">
          ←
        </button>
        <ol className="voices__dots">
          {REVIEWS.map((rv, k) => (
            <li key={rv.name}>
              <button
                type="button"
                className={`voices__dot${k === i ? " is-on" : ""}`}
                onClick={() => setI(k)}
                aria-label={`Yorum ${k + 1}: ${rv.name}`}
                aria-current={k === i ? "true" : undefined}
              />
            </li>
          ))}
        </ol>
        <span className="voices__count">
          {pad2(i + 1)} / {pad2(n)}
        </span>
        <button type="button" className="voices__arrow" onClick={() => go(1)} aria-label="Sonraki yorum" data-magnetic="0.4">
          →
        </button>
      </div>
    </section>
  );
}
