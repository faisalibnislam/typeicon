import { NextResponse } from "next/server";
import { getDesign } from "@/lib/catalog";
import { isSafeSvg } from "@/lib/svg";

/** Canonical sanitized SVG for one published variant (unmodified). */
export async function GET(req: Request, ctx: { params: Promise<{ slug: string }> }) {
  const { slug } = await ctx.params;
  const style = new URL(req.url).searchParams.get("style") ?? "line";
  const d = await getDesign(slug);
  const v = d?.variants.find((x) => x.style === style);
  if (!d || !v || !isSafeSvg(v.svg)) return NextResponse.json({ error: "Not found" }, { status: 404 });
  const body = v.svg.includes("xmlns=") ? v.svg : v.svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ');
  return new Response(body + "\n", {
    headers: {
      "content-type": "image/svg+xml; charset=utf-8",
      "content-disposition": `inline; filename="${d.name}-${style}.svg"`,
      "content-security-policy": "default-src 'none'; style-src 'unsafe-inline'; sandbox",
      "cache-control": "public, max-age=3600",
      etag: `"${v.svgSha256}"`,
    },
  });
}
