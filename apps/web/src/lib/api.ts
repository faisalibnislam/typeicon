import "server-only";
import { NextResponse } from "next/server";
import { z } from "zod";
import { HttpError } from "./session";

/** Wrap a route handler: typed errors -> JSON, zod errors -> 400, unknown -> 500 (no internals leaked). */
export function handle<A extends unknown[]>(fn: (req: Request, ...args: A) => Promise<Response>) {
  return async (req: Request, ...args: A): Promise<Response> => {
    try {
      if (!["GET", "HEAD", "OPTIONS"].includes(req.method)) assertSameOrigin(req);
      return await fn(req, ...args);
    } catch (e) {
      if (e instanceof HttpError) return NextResponse.json({ error: e.message }, { status: e.status });
      if (e instanceof z.ZodError) return NextResponse.json({ error: "Invalid request", issues: e.issues.map((i) => ({ path: i.path.join("."), message: i.message })) }, { status: 400 });
      console.error("[api]", req.method, new URL(req.url).pathname, e);
      return NextResponse.json({ error: "Internal error" }, { status: 500 });
    }
  };
}

/** CSRF defence for cookie-authenticated mutations: require a same-origin Origin header. */
export function assertSameOrigin(req: Request) {
  const origin = req.headers.get("origin");
  const host = req.headers.get("x-forwarded-host") ?? req.headers.get("host");
  if (!origin || !host) throw new HttpError(403, "Missing origin");
  let o: URL;
  try {
    o = new URL(origin);
  } catch {
    throw new HttpError(403, "Bad origin");
  }
  if (o.host !== host) throw new HttpError(403, "Cross-origin request refused");
}

export async function readJson<T>(req: Request, schema: z.ZodType<T>, maxBytes = 64 * 1024): Promise<T> {
  const len = Number(req.headers.get("content-length") ?? 0);
  if (len > maxBytes) throw new HttpError(413, "Request body too large");
  const text = await req.text();
  if (text.length > maxBytes) throw new HttpError(413, "Request body too large");
  let data: unknown;
  try {
    data = JSON.parse(text || "{}");
  } catch {
    throw new HttpError(400, "Body must be JSON");
  }
  return schema.parse(data);
}

export const uuid = z.string().uuid();
export const styleSlug = z.enum(["filled", "line", "rounded", "thin", "brand"]);
