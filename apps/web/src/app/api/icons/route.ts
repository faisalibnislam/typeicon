import { NextResponse } from "next/server";
import { parseSearchParams, searchIcons } from "@/lib/search";

/**
 * Public catalog search API (used by the Figma plugin and scripts).
 * GET /api/icons?q=home&style=line&area=core&page=1&per=48
 * Returns bounded pages of published icons with sanitized SVG for the requested style.
 */
export async function GET(req: Request) {
  const url = new URL(req.url);
  const raw = Object.fromEntries(url.searchParams.entries());
  const input = parseSearchParams({ ...raw, per: raw.per && ["48", "96"].includes(raw.per) ? raw.per : "48" });
  const r = await searchIcons(input);
  return NextResponse.json(
    {
      query: r.normalizedQuery,
      style: input.style,
      page: input.page,
      pages: r.pages,
      total: r.total,
      items: r.items.map((i) => ({
        id: i.id,
        name: i.name,
        area: i.area,
        source: i.source,
        sourceName: i.sourceName,
        license: i.license,
        styles: i.styles,
        style: i.displayStyle,
        codepoint: i.codepoint,
        svg: i.svg,
      })),
    },
    { headers: { "cache-control": "public, max-age=60", "access-control-allow-origin": "*" } },
  );
}
