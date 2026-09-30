// Content for the whole site, taken from the studio's existing website.
// Visible strings must never contain em or en dashes (design rule).

export type PagePath = "/" | "/hizmetler" | "/galeri" | "/hakkimda" | "/iletisim";

export type ImgSrc = { base: string; widths: number[]; w: number; h: number };

const wide = (name: string, widths = [1000, 2000]): ImgSrc => ({
  base: `/assets/img/${name}`,
  widths,
  w: 2752,
  h: 1536,
});
const phone = (name: string): ImgSrc => ({
  base: `/assets/img/${name}`,
  widths: [600, 1100],
  w: 1536,
  h: 2752,
});
const tall = (name: string, widths = [500, 800]): ImgSrc => ({
  base: `/assets/img/${name}`,
  widths,
  w: 1856,
  h: 2304,
});

export const IMG = {
  heroA: wide("hero-a", [900, 1400, 2400]),
  heroAm: phone("hero-a-m"),
  heroB: wide("hero-b"),
  heroBm: phone("hero-b-m"),
  day1m: phone("day-1-m"),
  day2m: phone("day-2-m"),
  day3m: phone("day-3-m"),
  day4m: phone("day-4-m"),
  day1: wide("day-1"),
  day2: wide("day-2"),
  day3: wide("day-3"),
  day4: wide("day-4"),
  silk: wide("silk"),
  studio: tall("studio", [800, 1400]),
  svcGelin: tall("svc-gelin"),
  svcOzel: tall("svc-ozel"),
  svcKalici: tall("svc-kalici"),
  svcKas: tall("svc-kas"),
  svcKirpik: tall("svc-kirpik"),
  svcSac: tall("svc-sac"),
} satisfies Record<string, ImgSrc>;

export const STUDIO = {
  name: "Eda Yalanız Makeup Studio",
  phoneDisplay: "0541 557 22 90",
  phoneHref: "tel:+905415572290",
  whatsapp: "https://wa.me/905415572290",
  instagram: "https://www.instagram.com/edayalanizmakeupp",
  facebook: "https://www.facebook.com/profile.php?id=61592817747456",
  addressLines: ["Odunluk Mah. İbrahim İşseverler Cad. No: 18", "Nilüfer / Bursa"],
  // Google Maps listing: "Eda Yalanız Makeup Studio", Nilüfer / Bursa
  maps: "https://www.google.com/maps/dir/?api=1&destination=Eda+Yalan%C4%B1z+Makeup+Studio+Nil%C3%BCfer+Bursa",
  mapEmbed:
    "https://www.google.com/maps?q=Eda%20Yalan%C4%B1z%20Makeup%20Studio%2C%20Odunluk%2C%20Nil%C3%BCfer%2C%20Bursa&hl=tr&z=16&output=embed",
  hours: ["Pazartesi ile Cumartesi, 10.00 ile 19.00 arası", "Pazar günleri yalnızca gelin randevuları"],
};

export type Service = {
  slug: string;
  name: string;
  meta: string;
  text: string;
  img: ImgSrc;
  alt: string;
};

export const SERVICES: Service[] = [
  {
    slug: "gelin",
    name: "Gelin makyajı",
    meta: "Prova dahil",
    text: "Prova, gün planı ve uygulamayı kapsayan tam gün eşlik. Fotoğrafta ve gerçekte aynı duran bir sonuç.",
    img: IMG.svcGelin,
    alt: "Dantel duvağın kenarında inci gelin tarağı",
  },
  {
    slug: "ozel-gun",
    name: "Günlük ve özel gün",
    meta: "45 ile 70 dk",
    text: "Nişan, kına, davet veya çekim için ölçülü, cildin dokusunu bozmayan uygulama.",
    img: IMG.svcOzel,
    alt: "Mermer üzerinde ruj tonları ve açık pudralık",
  },
  {
    slug: "kalici",
    name: "Kalıcı makyaj",
    meta: "2 seans",
    text: "Microblading, pudra kaş ve dudak renklendirme. Doğal pigment, kontrollü ton, iki seanslı takip.",
    img: IMG.svcKalici,
    alt: "Kaş tonlarında pigment kapları ve microblading kalemi",
  },
  {
    slug: "kas",
    name: "Kaş tasarımı",
    meta: "30 dk",
    text: "Yüz oranına göre ölçülen form, alma ve renklendirme. Kalıcı makyaj öncesi zorunlu adım.",
    img: IMG.svcKas,
    alt: "Kaş ölçüm ipi, pergel ve kaş kalemi",
  },
  {
    slug: "kirpik",
    name: "Kirpik lifting",
    meta: "6 ile 8 hafta",
    text: "Kendi kirpiğinizle çalışan kaldırma ve besleme uygulaması. Ekleme yok, ağırlık yok.",
    img: IMG.svcKirpik,
    alt: "Kirpik lifting pedleri, tarak ve cımbız",
  },
  {
    slug: "sac",
    name: "Saç tasarımı",
    meta: "Makyajla birlikte",
    text: "Makyajla birlikte planlanan topuz, dalga ve gelin saçı. Aynı odada, aynı elden.",
    img: IMG.svcSac,
    alt: "İnci tokalar, kuyruklu tarak ve saten kurdele",
  },
];

export type Chapter = { label: string; title: string; text: string; img: ImgSrc; mobile: ImgSrc; alt: string };

export const BRIDAL_DAY: Chapter[] = [
  {
    label: "Ön görüşme",
    title: "Önce konuşuruz.",
    text: "Cilt yapısı, saç rengi, gelinlik ve günün saati konuşulur. Plan buradan çıkar.",
    img: IMG.day1,
    mobile: IMG.day1m,
    alt: "Eda Yalanız ön görüşmede defterine kaş oranlarını çiziyor",
  },
  {
    label: "Prova",
    title: "Sonra deneriz.",
    text: "Görünüm düğünden önce denenir, gün ışığında ve fotoğrafta kontrol edilir.",
    img: IMG.day2,
    mobile: IMG.day2m,
    alt: "Eda Yalanız prova sırasında geline makyaj uyguluyor",
  },
  {
    label: "Sabah",
    title: "Gün acele etmez.",
    text: "Düğün sabahı her adım planlandığı sırayla, telaş olmadan uygulanır.",
    img: IMG.day3,
    mobile: IMG.day3m,
    alt: "Eda Yalanız düğün sabahı gelinin duvağını takıyor",
  },
  {
    label: "Akşam",
    title: "İlk andaki gibi.",
    text: "Amaç basit: akşam fotoğraflarında da ilk andaki gibi durması.",
    img: IMG.day4,
    mobile: IMG.day4m,
    alt: "Akşam ışıklarında sandalyede gelin buketi ve duvak",
  },
];

export type Review = { quote: string; name: string; role: string };

export const REVIEWS: Review[] = [
  {
    quote:
      "Düğün sabahı hiç telaş yaşamadım. Akşam fotoğraflarında makyajım ilk andaki gibiydi, abartısız ve tam bana göre.",
    name: "Merve K.",
    role: "Gelin, 2025",
  },
  {
    quote:
      "Kaşlarımı yıllardır kimseye teslim edemiyordum. Eda önce ölçtü, çizdi, konuştuk; sonra uyguladı. Fark bu.",
    name: "Zeynep A.",
    role: "Kalıcı makyaj",
  },
  {
    quote: "Stüdyoda tek kişi olmak çok değerli. Acele yok, sohbet var, sonuç sakin ve zarif.",
    name: "Ayşe D.",
    role: "Özel gün makyajı",
  },
  {
    quote: "Kına ve düğün için iki farklı görünüm çalıştık; ikisi de gün boyu hiç bozulmadı.",
    name: "Elif T.",
    role: "Gelin, 2024",
  },
  {
    quote: "Kirpik lifting sonrası sabahları hiç maskara sürmüyorum. Doğal ve hafif.",
    name: "Selin B.",
    role: "Kirpik lifting",
  },
];

export const CERTS = ["PhiBrows", "PhiLips", "BB Stroke", "PhiLashes"];

export type NavItem = { to: PagePath; label: string; img: ImgSrc };
