import { createFileRoute } from "@tanstack/react-router";
import { About } from "../components/site/about";
import { BridalDay } from "../components/site/bridal-day";
import { Contact } from "../components/site/contact";
import { GalleryRail } from "../components/site/gallery";
import { Hero } from "../components/site/hero";
import { Manifesto } from "../components/site/manifesto";
import { Services } from "../components/site/services";
import { Voices } from "../components/site/voices";

export const Route = createFileRoute("/")({
  // The home page inherits title/description from the root route.
  component: Home,
});

function Home() {
  return (
    <>
      <Hero />
      <Manifesto />
      <Services />
      <BridalDay />
      <GalleryRail />
      <About />
      <Voices />
      <Contact />
    </>
  );
}
