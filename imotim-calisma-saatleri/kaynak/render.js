// Hikaye sayfalarını 1080x1920 PNG olarak render eder.
// CSS mask (logo) file:// üzerinden yüklenmediği için sayfalar yerel bir
// HTTP sunucusundan açılır.
//
// Kullanım:
//   node render.js [çıktı-klasörü]            -> kaynak/hikaye-*.html
//   node render.js <çıktı-klasörü> <klasör>   -> kaynak/<klasör>/*.html
//
// Her sayfada, yazıların Instagram arayüzünün altında kalabilecek kenarlara
// taşıp taşmadığı kontrol edilir (data-serbest işaretli süs yazıları hariç).

const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const KOK = __dirname;
const CIKTI = path.resolve(process.argv[2] || path.join(KOK, "..", "hikayeler"));
const KLASOR = process.argv[3] || "";
const TURLER = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css",
  ".png": "image/png",
  ".ttf": "font/ttf",
};

function sunucuBaslat() {
  const sunucu = http.createServer((istek, yanit) => {
    const dosya = path.join(KOK, decodeURIComponent(new URL(istek.url, "http://x").pathname));
    if (!dosya.startsWith(KOK) || !fs.existsSync(dosya) || fs.statSync(dosya).isDirectory()) {
      yanit.writeHead(404).end();
      return;
    }
    yanit.writeHead(200, { "Content-Type": TURLER[path.extname(dosya)] || "application/octet-stream" });
    fs.createReadStream(dosya).pipe(yanit);
  });
  return new Promise((coz) => sunucu.listen(0, "127.0.0.1", () => coz(sunucu)));
}

function guvenliAlanKontrolu() {
  const sorunlar = [];
  const gezgin = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (gezgin.nextNode()) {
    const dugum = gezgin.currentNode;
    const yazi = dugum.textContent.trim();
    if (!yazi || dugum.parentElement.closest("[data-serbest], script, style")) continue;
    const aralik = document.createRange();
    aralik.selectNodeContents(dugum);
    for (const k of aralik.getClientRects()) {
      if (k.width === 0) continue;
      if (k.left < 36 || k.right > 1044 || k.top < 150 || k.bottom > 1770) {
        sorunlar.push(`"${yazi.slice(0, 24)}" [${Math.round(k.left)},${Math.round(k.top)} - ${Math.round(k.right)},${Math.round(k.bottom)}]`);
        break;
      }
    }
  }
  for (const f of document.fonts) if (f.status === "error") sorunlar.push(`font yüklenemedi: ${f.family}`);
  return sorunlar;
}

(async () => {
  fs.mkdirSync(CIKTI, { recursive: true });
  const sunucu = await sunucuBaslat();
  const port = sunucu.address().port;
  const tarayici = await chromium.launch();
  const sayfa = await tarayici.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });

  const dizin = path.join(KOK, KLASOR);
  const desen = KLASOR ? /\.html$/ : /^hikaye-.*\.html$/;
  const sayfalar = fs.readdirSync(dizin).filter((f) => desen.test(f)).sort();
  let uyari = 0;
  for (const ad of sayfalar) {
    const url = `http://127.0.0.1:${port}/${KLASOR ? KLASOR + "/" : ""}${ad}`;
    await sayfa.goto(url, { waitUntil: "networkidle" });
    await sayfa.evaluate(() => document.fonts.ready);
    const hedef = path.join(CIKTI, ad.replace(/^hikaye-/, "").replace(/\.html$/, ".png"));
    await sayfa.screenshot({ path: hedef, type: "png" });
    const sorunlar = await sayfa.evaluate(guvenliAlanKontrolu);
    console.log(hedef);
    for (const s of sorunlar) console.log(`  UYARI ${s}`);
    uyari += sorunlar.length;
  }
  if (uyari) console.log(`${uyari} uyarı`);

  await tarayici.close();
  sunucu.close();
})();
