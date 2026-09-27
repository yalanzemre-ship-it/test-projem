# Eda Yalanız — Makeup Artist

Statik, build step gerektirmeyen, sinematik bir portfolyo sitesi. Klasörü herhangi bir hosting'e (Netlify, Vercel, cPanel, GitHub Pages) olduğu gibi yükleyin.

## Sayfalar

| Dosya | İçerik |
| --- | --- |
| `index.html` | Loader, sinematik hero, manifesto, scroll tipografisi, "Bir gelinin sabahı" scrub sahnesi, hizmet listesi, yatay galeri, hakkında, CTA |
| `hizmetler.html` | Açılan hizmet panelleri (hover / dokunma), genişleyen görsel, üst üste binen süreç kartları |
| `portfolyo.html` | Tam sayfa yatay galeri + tam ekran fotoğraf görüntüleyici |
| `iletisim.html` | İletişim linkleri + WhatsApp / e-posta mesajı hazırlayan randevu formu |

## Özellikler

- **Smooth scroll:** Lenis (yalnızca masaüstünde; mobilde native scroll kalır)
- **Custom cursor:** Bağlama göre `VIEW`, `DISCOVER`, `NEXT`, `PREV`, `BOOK`, `CLOSE`, `OPEN` etiketlerine dönüşür (`data-cursor="..."`)
- **Magnetic hover:** `data-magnetic="0.3"` taşıyan her öğe, imleç yaklaşınca ona doğru çekilir
- **Scroll animasyonları:** GSAP ScrollTrigger + SplitText ile satır/harf reveal, kelime kelime aydınlanan manifesto, hıza göre eğilen dev tipografi
- **Cinematic scrub:** Pinlenen sahne; kareler clip-path ile açılır, saat sayacı döner, bölümler değişir
- **Fotoğraf efektleri:** Parallax, clip-path reveal, hover'da SVG displacement distortion + imleçten açılan renk maskesi
- **Yatay galeri:** Masaüstünde dikey scroll ile yatay kayar; mobilde doğal swipe + snap
- **Lightbox:** Küçük görselden tam ekrana FLIP geçişi, clip-path wipe ile ileri/geri, klavye (← → Esc) ve swipe desteği
- **Sayfa geçişi:** Sütun perdesi + hedef sayfa adı; bfcache (geri tuşu) uyumlu
- **Menü:** Tam ekran editoryal menü, harf harf giriş, hover'da görsel önizleme
- **Mobil:** Cursor, magnetic, distortion ve Lenis kapalı; scrub sahnesi daha kısa ve hafif; galeri native swipe
- **`prefers-reduced-motion`:** Tüm animasyonlar kapanır; scrub sahnesi ve galeri statik, okunabilir düzene geçer; menü ve lightbox anında açılır
- **JS olmadan / hata durumunda:** İçerik görünür kalır (failsafe), form ve menü çalışır

## Yapman gerekenler (placeholder içerik)

Mevcut siteye (edayalanizmakeup.com) geliştirme ortamından erişilemediği için **içerikler placeholder**. Yayına almadan önce şunları değiştir:

1. **Fotoğraflar** — `assets/img/` içindeki görseller kod ile üretilmiş soyut placeholder'lar. Aynı isim ve oranla gerçek fotoğrafları koy:
   - `hero.jpg` (2400×1400) + `hero-m.jpg` (1080×1920, mobil dikey)
   - `scene-1…4.jpg` (2000×1250) — "Bir gelinin sabahı" sahneleri
   - `service-1…4.jpg` (1200×1500) — hizmet görselleri
   - `work-01…10.jpg` (dikey 1200×1560 veya yatay 1800×1200) — portfolyo
   - `about.jpg` (1200×1560) — portre
   - Her görselin yarı genişlikte bir `-sm.jpg` kopyası da olmalı (mobil için).
2. **İletişim bilgileri** — tüm HTML dosyalarında bul-değiştir:
   - `+90 5XX XXX XX XX` → telefon
   - `905000000000` → WhatsApp numarası (başında `+` olmadan)
   - `+905000000000` → `tel:` linki
   - `merhaba@edayalanizmakeup.com` → e-posta
   - `edayalanizmakeup` → Instagram kullanıcı adı
   - `Türkiye · Randevu ile` → konum
3. **Metinler** — hizmet açıklamaları, "Neler dahil" listeleri, süreç adımları ve hakkında metni örnek metindir; gerçek bilgilerle güncelle. Galeri açıklamaları (`data-caption`) ve `alt` metinleri de fotoğraflara göre düzenlenmeli.
4. **İsim** — marka adı her yerde `Eda Yalanız` olarak yazıldı; yazımını kontrol et.

Header, menü ve footer 4 sayfada tekrar ediyor (build step yok); bu bölümlerde yaptığın değişikliği her dosyada tekrarla.

## Teknik

- `assets/css/main.css` — tüm stiller (renkler ve tipografi `:root` token'larında)
- `assets/js/main.js` — tüm etkileşimler
- `assets/vendor/` — GSAP 3.15 (ScrollTrigger, SplitText) ve Lenis 1.3, yerel kopya (CDN bağımlılığı yok)
- `assets/fonts/` — Instrument Serif + Manrope, Türkçe karakterli `latin-ext` alt kümeleri dahil

Yerelde denemek için:

```bash
python3 -m http.server 8000
# http://localhost:8000
```
