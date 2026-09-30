import { createFileRoute } from "@tanstack/react-router";
import { BridalDay } from "../components/site/bridal-day";
import { NextPage, PageHead } from "../components/site/page-bits";
import { Services } from "../components/site/services";
import { IMG } from "../lib/site-data";

export const Route = createFileRoute("/hizmetler")({
  head: () => ({
    meta: [
      { title: "Hizmetler · Eda Yalanız Makeup Studio" },
      {
        name: "description",
        content: "Gelin makyajı, özel gün makyajı, kalıcı makyaj, kaş tasarımı, kirpik lifting ve saç tasarımı. Nilüfer, Bursa.",
      },
    ],
  }),
  component: ServicesPage,
});

function ServicesPage() {
  return (
    <>
      <PageHead
        path="/hizmetler"
        title="Hizmetler"
        lead="Gelin makyajından kaş tasarımına altı uzmanlık. Hepsi randevu ile, tek kişilik seanslarda."
        img={IMG.heroB}
        alt="Eda Yalanız makyaj masasında fırçalarını düzenliyor"
      />
      <Services />
      <BridalDay />
      <NextPage from="/hizmetler" />
    </>
  );
}
