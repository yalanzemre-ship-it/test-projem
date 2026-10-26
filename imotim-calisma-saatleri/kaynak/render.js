// hikaye-*.html sayfalarını 1080x1920 PNG olarak render eder.
// CSS mask (logo) file:// üzerinden yüklenmediği için sayfalar yerel bir
// HTTP sunucusundan açılır.
//
// Kullanım: node render.js [çıktı-klasörü]

const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const KOK = __dirname;
const CIKTI = path.resolve(process.argv[2] || path.join(KOK, "..", "hikayeler"));
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

(async () => {
  fs.mkdirSync(CIKTI, { recursive: true });
  const sunucu = await sunucuBaslat();
  const port = sunucu.address().port;
  const tarayici = await chromium.launch();
  const sayfa = await tarayici.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });

  const sayfalar = fs.readdirSync(KOK).filter((f) => /^hikaye-.*\.html$/.test(f)).sort();
  for (const ad of sayfalar) {
    await sayfa.goto(`http://127.0.0.1:${port}/${ad}`, { waitUntil: "networkidle" });
    await sayfa.evaluate(() => document.fonts.ready);
    const hedef = path.join(CIKTI, ad.replace(/^hikaye-/, "").replace(/\.html$/, ".png"));
    await sayfa.screenshot({ path: hedef, type: "png" });
    console.log(hedef);
  }

  await tarayici.close();
  sunucu.close();
})();
