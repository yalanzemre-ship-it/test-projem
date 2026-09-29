import { createFileRoute } from "@tanstack/react-router";
import { About } from "../components/site/about";
import { Manifesto } from "../components/site/manifesto";
import { NextPage, PageHead } from "../components/site/page-bits";
import { Voices } from "../components/site/voices";
import { IMG } from "../lib/site-data";

export const Route = createFileRoute("/hakkimda")({
  head: () => ({
    meta: [
      { title: "Hakkımda · Eda Yalanız Makeup Studio" },
      {
        name: "description",
        content: "Eda Yalanız: 2021'den beri Nilüfer'de gelin ve kalıcı makyaj. PhiBrows, PhiLips, BB Stroke ve PhiLashes sertifikalı.",
      },
    ],
  }),
  component: AboutPage,
});

function AboutPage() {
  return (
    <>
      <PageHead
        path="/hakkimda"
        title="Hakkımda"
        lead="2021'den beri Nilüfer'de, aynı anda tek kişiyle."
        img={IMG.day1}
        alt="Masada yüz oranı çizimleri, pergel ve ruj denemeleri"
      />
      <About />
      <Manifesto />
      <Voices />
      <NextPage from="/hakkimda" />
    </>
  );
}
