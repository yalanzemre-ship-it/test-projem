import { createFileRoute, redirect } from "@tanstack/react-router";
import { GalleryGrid } from "../components/site/gallery";
import { NextPage, PageHead } from "../components/site/page-bits";
import { HAS_GALLERY } from "../lib/nav";
import { IMG } from "../lib/site-data";

export const Route = createFileRoute("/galeri")({
  beforeLoad: () => {
    if (!HAS_GALLERY) throw redirect({ to: "/" });
  },
  head: () => ({
    meta: [
      { title: "Galeri · Eda Yalanız Makeup Studio" },
      { name: "description", content: "Eda Yalanız Makeup Studio'dan gelin, özel gün ve kalıcı makyaj çalışmaları." },
    ],
  }),
  component: GalleryPage,
});

function GalleryPage() {
  return (
    <>
      <PageHead
        path="/galeri"
        title="Galeri"
        lead="Stüdyoda yapılan çalışmalardan bir seçki."
        img={IMG.day3}
        alt="Sabah ışığında askıda gelinlik ve katlanmış duvak"
      />
      <GalleryGrid />
      <NextPage from="/galeri" />
    </>
  );
}
