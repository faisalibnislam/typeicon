import { existsSync } from "node:fs";
import path from "node:path";
import { request } from "@playwright/test";
import { creds, ROOT } from "./helpers";

/**
 * Sign each local test account in once and save its session. Existing sessions are reused while valid,
 * so repeated runs do not trip the auth sign-in rate limiter.
 */
export default async function globalSetup() {
  const base = process.env.E2E_BASE_URL ?? "http://localhost:3107";
  for (const key of ["admin", "user", "other"] as const) {
    const file = path.join(ROOT, `.data/e2e-state-${key}.json`);
    if (existsSync(file)) {
      const probe = await request.newContext({ baseURL: base, storageState: file });
      const s = await probe.get("/api/auth/get-session");
      const body = s.ok() ? await s.json().catch(() => null) : null;
      await probe.dispose();
      if (body?.user?.email === creds(key).email) continue;
    }
    const ctx = await request.newContext({ baseURL: base, extraHTTPHeaders: { origin: base } });
    const r = await ctx.post("/api/auth/sign-in/email", { data: creds(key) });
    if (!r.ok()) throw new Error(`sign-in failed for ${key}: ${r.status()}`);
    await ctx.storageState({ path: file });
    await ctx.dispose();
  }
}
