import { execFileSync, spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import type { Page } from "@playwright/test";

export const ROOT = path.resolve(__dirname, "../../../..");

/** Local test accounts created by scripts/seed-dev-users.ts (credentials live in the git-ignored .data folder). */
export function creds(key: "admin" | "user" | "other"): { email: string; password: string } {
  return JSON.parse(readFileSync(path.join(ROOT, ".data/dev-credentials.json"), "utf8"))[key];
}

export const stateFile = (key: "admin" | "user" | "other") => path.join(ROOT, `.data/e2e-state-${key}.json`);

/** Sign-in through the real form (used once to prove the UI flow works). */
export async function signInViaForm(page: Page, key: "admin" | "user" | "other") {
  const c = creds(key);
  await page.goto("/sign-in");
  await page.getByLabel("Email").fill(c.email);
  await page.getByLabel("Password").fill(c.password);
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL("**/account");
}

/** Run the real Python worker until the queue is empty (no mocks). */
export function drainWorker() {
  const env = { ...process.env, DATABASE_URL: process.env.DATABASE_URL ?? "postgres://typeicon@localhost:54329/typeicon" };
  const r = spawnSync(path.join(ROOT, ".venv/bin/typeicon-worker"), ["--drain"], { env, encoding: "utf8", timeout: 120_000 });
  if (r.status !== 0) throw new Error(r.stderr);
  return r.stdout;
}

export function unzipList(file: string): string[] {
  return execFileSync("unzip", ["-Z1", file], { encoding: "utf8" }).trim().split("\n");
}
