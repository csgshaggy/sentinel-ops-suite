import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Sentinel Ops UI",
  description: "Component library & design system for the Sentinel Ops Suite",

  themeConfig: {
    nav: [
      { text: "Overview", link: "/" },
      { text: "Components", link: "/components" },
      { text: "Theme", link: "/theme" },
      { text: "Design Tokens", link: "/design-tokens" }
    ],
    sidebar: {
      "/": [
        { text: "Overview", link: "/" },
        { text: "Components", link: "/components" },
        { text: "Theme Tokens", link: "/theme" },
        { text: "Design Tokens", link: "/design-tokens" }
      ]
    }
  }
});
