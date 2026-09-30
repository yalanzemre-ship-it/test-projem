import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Outlet, createRootRouteWithContext, useRouter, HeadContent, Scripts } from "@tanstack/react-router";
import { useEffect, type ReactNode } from "react";

import appCss from "../styles.css?url";
import { reportHiggsfieldError } from "../lib/higgsfield-error-reporting";
// Page metadata (browser <title> + social title/description) committed into the
// repo and read at BUILD time. The feed-card cover in app-meta.json is for the
// marketplace listing; the site's own share image is the brand OG below.
import appMetaJson from "../app-meta.json";
import { STUDIO } from "../lib/site-data";
import { Header, Footer } from "../components/site/chrome";
import { Cursor, DistortDefs, SmoothScroll } from "../components/site/experience";
import { TransitionProvider } from "../components/site/transition";

declare const __HF_DESIGN_INSPECTOR__: boolean;

type AppMeta = { og_title?: string | null; og_description?: string | null };
const appMeta = appMetaJson as AppMeta;

const SITE_URL ="https://eda-yalaniz-studio.higgsfield.app";
const TITLE = appMeta.og_title ?? "Eda Yalanız Makeup Studio";
const DESCRIPTION =
  appMeta.og_description ??
  "Nilüfer, Bursa'da gelin makyajı, kalıcı makyaj, kaş tasarımı ve kirpik lifting. Randevu ile, tek kişilik seanslar.";
const OG_IMAGE = `${SITE_URL}/assets/brand/og.jpg`;

const FONTS =
  "https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=IBM+Plex+Mono:wght@400;500&display=swap";

const JSON_LD = {
  "@context": "https://schema.org",
  "@type": "BeautySalon",
  name: STUDIO.name,
  url: SITE_URL,
  image: OG_IMAGE,
  telephone: "+905415572290",
  address: {
    "@type": "PostalAddress",
    streetAddress: "Odunluk Mah. İbrahim İşseverler Cad. No: 18",
    addressLocality: "Nilüfer",
    addressRegion: "Bursa",
    addressCountry: "TR",
  },
  openingHoursSpecification: [
    {
      "@type": "OpeningHoursSpecification",
      dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
      opens: "10:00",
      closes: "19:00",
    },
  ],
  sameAs: [STUDIO.instagram, STUDIO.facebook],
};

function NotFoundComponent() {
  return (
    <section className="nf">
      <p className="nf__code">404</p>
      <h1 className="nf__title">Bu sayfa ölçüye uymadı.</h1>
      <a className="nf__link" href="/">
        Ana sayfaya dön
      </a>
    </section>
  );
}

function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  console.error(error);
  const router = useRouter();
  useEffect(() => {
    reportHiggsfieldError(error, { boundary: "tanstack_root_error_component" });
  }, [error]);

  return (
    <section className="nf">
      <p className="nf__code">Hata</p>
      <h1 className="nf__title">Sayfa yüklenemedi.</h1>
      <button
        type="button"
        className="nf__link"
        onClick={() => {
          router.invalidate();
          reset();
        }}
      >
        Tekrar dene
      </button>
    </section>
  );
}

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1, viewport-fit=cover" },
      { title: TITLE },
      { name: "description", content: DESCRIPTION },
      { name: "theme-color", content: "#F7F1EF" },
      { property: "og:site_name", content: STUDIO.name },
      { property: "og:title", content: TITLE },
      { property: "og:description", content: DESCRIPTION },
      { property: "og:type", content: "website" },
      { property: "og:url", content: SITE_URL },
      { property: "og:locale", content: "tr_TR" },
      { property: "og:image", content: OG_IMAGE },
      { property: "og:image:width", content: "1200" },
      { property: "og:image:height", content: "630" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "twitter:title", content: TITLE },
      { name: "twitter:description", content: DESCRIPTION },
      { name: "twitter:image", content: OG_IMAGE },
    ],
    links: [
      { rel: "preconnect", href: "https://fonts.googleapis.com" },
      { rel: "preconnect", href: "https://fonts.gstatic.com", crossOrigin: "anonymous" },
      { rel: "stylesheet", href: FONTS },
      { rel: "stylesheet", href: appCss },
      { rel: "icon", href: "/favicon.ico", sizes: "48x48" },
      { rel: "icon", href: "/favicon.svg", type: "image/svg+xml" },
      { rel: "icon", href: "/favicon-32.png", type: "image/png", sizes: "32x32" },
      { rel: "icon", href: "/favicon-16.png", type: "image/png", sizes: "16x16" },
      { rel: "apple-touch-icon", href: "/apple-touch-icon.png" },
      { rel: "manifest", href: "/site.webmanifest" },
    ],
  }),
  shellComponent: RootShell,
  component: RootComponent,
  notFoundComponent: NotFoundComponent,
  errorComponent: ErrorComponent,
});

function RootShell({ children }: { children: ReactNode }) {
  return (
    <html lang="tr" style={{ colorScheme: "dark" }}>
      <head>
        <HeadContent />
        <script dangerouslySetInnerHTML={{ __html: "document.documentElement.classList.add('js')" }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(JSON_LD) }} />
      </head>
      <body>
        {children}
        <Scripts />
      </body>
    </html>
  );
}

function RootComponent() {
  const { queryClient } = Route.useRouteContext();

  useEffect(() => {
    if (!__HF_DESIGN_INSPECTOR__) {
      return;
    }

    void import("../module/design-inspector/runtime")
      .then(({ installHiggsfieldDesignInspector }) => {
        installHiggsfieldDesignInspector();
      })
      .catch((error) => {
        reportHiggsfieldError(error instanceof Error ? error : new Error("Failed to load design inspector"), {
          boundary: "higgsfield_design_inspector_import",
        });
      });
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <TransitionProvider>
        <Header />
        <main id="main" tabIndex={-1}>
          {/* Required: nested routes render here. */}
          <Outlet />
        </main>
        <Footer />
        <Cursor />
        <SmoothScroll />
        <DistortDefs />
      </TransitionProvider>
    </QueryClientProvider>
  );
}
