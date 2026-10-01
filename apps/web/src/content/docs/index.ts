// Registry of documentation pages. Each page lives in ./<slug>.tsx and exports `meta` + a default component.
import type { DocMeta } from "./types";
import * as installation from "./installation";
import * as subsets from "./subsets";
import * as desktop from "./desktop";
import * as figma from "./figma";
import * as web from "./web";
import * as svg from "./svg";
import * as react from "./react";
import * as vue from "./vue";
import * as accessibility from "./accessibility";
import * as compatibility from "./compatibility";
import * as glyphs from "./glyphs";
import * as troubleshooting from "./troubleshooting";
import * as iconDesign from "./icon-design";

export const docs: { meta: DocMeta; Page: () => React.ReactNode }[] = [
  installation,
  subsets,
  desktop,
  figma,
  web,
  svg,
  react,
  vue,
  accessibility,
  compatibility,
  glyphs,
  troubleshooting,
  iconDesign,
].map((m) => ({ meta: m.meta, Page: m.default }));

export function getDoc(slug: string) {
  return docs.find((d) => d.meta.slug === slug) ?? null;
}
