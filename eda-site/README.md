# Eda Yalanız Makeup Studio: web sitesi kaynağı

Higgsfield website builder (React 19 + TanStack Start, Cloudflare Worker) üzerinde çalışan sitenin
bu repoda tutulan kaynak kopyası. Canlı proje Higgsfield'da `eda-yalaniz-studio` adıyla durur;
buradaki dosyalar o projenin `app/` klasörüne birebir kopyalanır.

- `app/src/routes/`: sayfalar (`/`, `/hizmetler`, `/galeri`, `/hakkimda`, `/iletisim`)
- `app/src/components/site/`: bölümler, cursor, smooth scroll, sayfa geçişi, menü
- `app/src/lib/site-data.ts`: tüm metinler ve iletişim bilgileri
- `app/src/lib/gallery-data.ts`: gerçek çalışma fotoğrafları listesi
- `app/src/site.css`: tasarım sistemi
- `app/design-brief.md`: tasarım kararları

Görseller (webp) ve favicon seti Higgsfield projesinin `app/public/` klasöründe.
