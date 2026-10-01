import { NextResponse } from "next/server";
import { z } from "zod";
import { handle, readJson, styleSlug, uuid } from "@/lib/api";
import { resolveItems } from "@/lib/builds";
import { capabilitiesFor } from "@/lib/entitlements";
import { getSessionUser } from "@/lib/session";

const PACK: Record<string, string> = { "typeicon-core": "", "simple-icons": "" };
const STYLE: Record<string, string> = { filled: "Filled", line: "Line", rounded: "Rounded", thin: "Thin", brand: "Brands" };

/** Dry-run review for the subset builder: compatibility, families to be produced, licenses. */
export const POST = handle(async (req) => {
  const user = await getSessionUser();
  const caps = await capabilitiesFor(user?.id ?? null);
  const body = await readJson(req, z.object({ items: z.array(z.object({ designId: uuid, style: styleSlug })).max(2000) }));
  const items = await resolveItems(body.items);
  const found = new Set(items.map((i) => `${i.designId}:${i.style}`));
  const missing = body.items.filter((i) => !found.has(`${i.designId}:${i.style}`));
  const groups = new Map<string, { family: string; source: string; style: string; count: number }>();
  for (const i of items.filter((x) => x.fontSupported)) {
    const k = `${i.source}:${i.style}`;
    const g = groups.get(k) ?? { family: `TypeIcon Kit <name> <hash> ${PACK[i.source] ?? ""}${STYLE[i.style]}`.replace(/\s+/g, " "), source: i.source, style: i.style, count: 0 };
    g.count++;
    groups.set(k, g);
  }
  const licenses = new Map<string, { license: string; sources: Set<string> }>();
  for (const i of items) {
    const l = licenses.get(i.license) ?? { license: i.license, sources: new Set() };
    l.sources.add(i.sourceName);
    licenses.set(i.license, l);
  }
  return NextResponse.json({
    items: items.map((i) => ({ designId: i.designId, name: i.name, style: i.style, source: i.source, sourceName: i.sourceName, license: i.license, fontSupported: i.fontSupported })),
    missing,
    families: [...groups.values()],
    svgOnly: items.filter((i) => !i.fontSupported).map((i) => ({ name: i.name, style: i.style })),
    licenses: [...licenses.values()].map((l) => ({ license: l.license, sources: [...l.sources] })),
    limits: { maxIcons: caps.maxSubsetIcons, buildsPerHour: caps.subsetBuildsPerHour, plan: caps.plan },
  });
});
