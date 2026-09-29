import { createFileRoute } from "@tanstack/react-router";
import { Contact } from "../components/site/contact";
import { NextPage, PageHead } from "../components/site/page-bits";
import { IMG } from "../lib/site-data";

export const Route = createFileRoute("/iletisim")({
  head: () => ({
    meta: [
      { title: "İletişim · Eda Yalanız Makeup Studio" },
      {
        name: "description",
        content: "Randevu için WhatsApp veya telefon: 0541 557 22 90. Odunluk Mah. İbrahim İşseverler Cad. No: 18, Nilüfer / Bursa.",
      },
    ],
  }),
  component: ContactPage,
});

function ContactPage() {
  return (
    <>
      <PageHead
        path="/iletisim"
        title="İletişim"
        lead="Randevu tek mesaj uzağınızda."
        img={IMG.day4}
        alt="Akşam ışıklarında sandalyede gelin buketi ve duvak"
      />
      <Contact />
      <NextPage from="/iletisim" />
    </>
  );
}
