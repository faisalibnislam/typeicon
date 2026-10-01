import { sql } from "drizzle-orm";
import { db } from "@/db";
import { getSessionUser } from "@/lib/session";
import { checkKey, contentTypeFor, storage } from "@/lib/storage";

/**
 * Serve objects from storage with access control:
 *  - releases/...                public, immutable (versioned paths)
 *  - builds/public/...           public subset builds (contain only public catalog assets)
 *  - builds/private/<userId>/... only the owning user (server-side check, never inferred from the URL)
 */
export async function GET(req: Request, ctx: { params: Promise<{ key: string[] }> }) {
  const { key: parts } = await ctx.params;
  let key: string;
  try {
    key = checkKey(parts.join("/"));
  } catch {
    return new Response("Not found", { status: 404 });
  }
  let cache = "public, max-age=31536000, immutable";
  if (key.startsWith("builds/private/")) {
    const user = await getSessionUser();
    const owner = key.split("/")[2];
    if (!user || user.id !== owner) return new Response("Not found", { status: 404 });
    cache = "private, no-store";
  } else if (key.startsWith("builds/public/")) {
    cache = "public, max-age=86400";
  } else if (!key.startsWith("releases/")) {
    return new Response("Not found", { status: 404 });
  }
  const s = storage();
  const direct = s.publicUrl(key);
  if (direct) return Response.redirect(direct, 302);
  const obj = await s.get(key);
  if (!obj) return new Response("Not found", { status: 404 });
  const name = parts[parts.length - 1];
  const headers: Record<string, string> = {
    "content-type": contentTypeFor(name),
    "content-length": String(obj.size),
    "cache-control": cache,
    "x-content-type-options": "nosniff",
  };
  if (name.endsWith(".zip") || name.endsWith(".otf") || name.endsWith(".ttf")) headers["content-disposition"] = `attachment; filename="${name}"`;
  if (name.endsWith(".woff2") || name.endsWith(".woff")) headers["access-control-allow-origin"] = "*";
  if (key.startsWith("releases/") && name.endsWith(".zip")) {
    void db.execute(sql`INSERT INTO audit_events (actor_id, action, subject_type, subject_id) VALUES (NULL, 'download', 'release_archive', ${key})`).catch(() => undefined);
  }
  return new Response(req.method === "HEAD" ? null : obj.body, { headers });
}

export const HEAD = GET;
