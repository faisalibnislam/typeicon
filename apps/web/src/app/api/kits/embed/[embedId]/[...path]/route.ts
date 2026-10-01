import { sql } from "drizzle-orm";
import { db } from "@/db";
import { contentTypeFor, storage } from "@/lib/storage";

/**
 * Hosted kit assets: /api/kits/embed/<embedId>/latest/kit.css (+ fonts referenced by it).
 * The embed id is a public identifier, not a credential. Allowed domains are a usage control:
 * requests with a non-matching Origin/Referer are refused, but anyone who has the font URLs can
 * still fetch publicly delivered font files directly.
 */
export async function GET(req: Request, ctx: { params: Promise<{ embedId: string; path: string[] }> }) {
  const { embedId, path } = await ctx.params;
  if (!/^[A-Za-z0-9_-]{8,32}$/.test(embedId) || path.length !== 2) return new Response("Not found", { status: 404 });
  const [ver, file] = path;
  if (!/^(latest|v\d{1,6})$/.test(ver) || !/^[A-Za-z0-9._-]+\.(css|woff2|woff)$/.test(file)) return new Response("Not found", { status: 404 });
  const k = await db.execute(sql`SELECT id, allowed_domains FROM kits WHERE embed_id = ${embedId}`);
  const kit = k.rows[0] as { id: string; allowed_domains: string[] } | undefined;
  if (!kit) return new Response("Not found", { status: 404 });
  if (kit.allowed_domains.length) {
    const src = req.headers.get("origin") ?? req.headers.get("referer");
    let host = "";
    try {
      host = src ? new URL(src).host : "";
    } catch {}
    const ok = kit.allowed_domains.some((d) => (d.startsWith("*.") ? host.endsWith(d.slice(1)) : host === d));
    if (!ok) return new Response("Domain not allowed for this kit", { status: 403 });
  }
  const v = await db.execute(sql`
    SELECT kv.version FROM kit_versions kv
    JOIN jobs j ON j.kind = 'kit_build' AND j.payload->>'kitVersionId' = kv.id::text AND j.status = 'succeeded' AND (j.result->>'hosted')::boolean
    WHERE kv.kit_id = ${kit.id} ${ver === "latest" ? sql`` : sql`AND kv.version = ${Number(ver.slice(1))}`}
    ORDER BY kv.version DESC LIMIT 1`);
  const row = v.rows[0] as { version: number } | undefined;
  if (!row) return new Response("No hosted build", { status: 404 });
  const obj = await storage().get(`kits/${embedId}/v${row.version}/${file}`);
  if (!obj) return new Response("Not found", { status: 404 });
  return new Response(obj.body, {
    headers: {
      "content-type": contentTypeFor(file),
      "cache-control": ver === "latest" ? "public, max-age=300" : "public, max-age=31536000, immutable",
      "access-control-allow-origin": "*",
      "x-content-type-options": "nosniff",
    },
  });
}
