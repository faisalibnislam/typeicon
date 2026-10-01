/**
 * Search latency benchmark at target scale. Runs the production searchIcons() (page query +
 * count + 5 facet queries) against a SEPARATE benchmark database (typeicon_bench) that holds the
 * real catalog plus synthetic rows. Synthetic rows never exist in the public database.
 *   DATABASE_URL=postgres://…/typeicon_bench pnpm tsx --conditions=react-server scripts/bench-search.ts
 */
import { writeFileSync, mkdirSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { sql } from "drizzle-orm";
import { db, pool } from "@/db";
import { repoRoot } from "@/lib/paths";
import { parseSearchParams, searchIcons } from "@/lib/search";

const N = Number(process.env.BENCH_QUERIES ?? 600);
const CONCURRENCY = Number(process.env.BENCH_CONCURRENCY ?? 8);

function pct(xs: number[], p: number) {
  const s = [...xs].sort((a, b) => a - b);
  return s[Math.min(s.length - 1, Math.floor((p / 100) * s.length))];
}

async function main() {
  if (!/bench/.test(process.env.DATABASE_URL ?? "")) throw new Error("Run against the *_bench database only");
  const names = (await db.execute(sql`SELECT local_name FROM designs ORDER BY random() LIMIT 400`)).rows.map((r) => (r as { local_name: string }).local_name);
  const tags = (await db.execute(sql`SELECT DISTINCT unnest(tags) AS t FROM designs LIMIT 400`)).rows.map((r) => (r as { t: string }).t).filter((t) => /^[a-z]{3,}$/.test(t));
  const cats = (await db.execute(sql`SELECT slug FROM categories LIMIT 40`)).rows.map((r) => (r as { slug: string }).slug);
  const pick = <T,>(a: T[], i: number) => a[(i * 2654435761) % a.length];
  const workload: { kind: string; raw: Record<string, string> }[] = [];
  for (let i = 0; i < N; i++) {
    const r = i % 20;
    if (r < 6) workload.push({ kind: "exact-name", raw: { q: pick(names, i) } });
    else if (r < 10) workload.push({ kind: "single-word", raw: { q: pick(tags, i) } });
    else if (r < 13) workload.push({ kind: "prefix", raw: { q: pick(tags, i).slice(0, 3) } });
    else if (r < 15) workload.push({ kind: "multi-word", raw: { q: `${pick(tags, i)} ${pick(tags, i + 7)}` } });
    else if (r < 17) {
      const t = pick(tags, i);
      workload.push({ kind: "typo", raw: { q: t.slice(0, 1) + t.slice(2) } });
    } else if (r < 19) workload.push({ kind: "browse-filtered", raw: { style: ["filled", "line", "rounded"][i % 3], category: pick(cats, i) } });
    else workload.push({ kind: "deep-page", raw: { page: String(20 + (i % 30)), style: "line" } });
  }
  // warm-up
  for (const w of workload.slice(0, 20)) await searchIcons(parseSearchParams(w.raw));
  const times: Record<string, number[]> = {};
  const all: number[] = [];
  let next = 0;
  const t0 = performance.now();
  await Promise.all(
    Array.from({ length: CONCURRENCY }, async () => {
      while (next < workload.length) {
        const w = workload[next++];
        const r = await searchIcons(parseSearchParams(w.raw));
        (times[w.kind] ??= []).push(r.tookMs);
        all.push(r.tookMs);
      }
    }),
  );
  const wall = (performance.now() - t0) / 1000;
  const counts = (await db.execute(sql`SELECT (SELECT count(*) FROM designs)::int AS designs, (SELECT count(*) FROM variants)::int AS variants`)).rows[0];
  const summary = {
    environment: { host: `${os.type()} ${os.release()} ${os.arch()}`, cpus: os.cpus().length, cpuModel: os.cpus()[0]?.model, node: process.version, postgres: "17 (Homebrew, local, default config)", poolMax: Number(process.env.DATABASE_POOL_MAX ?? 10) },
    dataset: counts,
    workload: { queries: all.length, concurrency: CONCURRENCY, throughputQps: +(all.length / wall).toFixed(1) },
    overall: { p50: +pct(all, 50).toFixed(1), p95: +pct(all, 95).toFixed(1), p99: +pct(all, 99).toFixed(1), max: +Math.max(...all).toFixed(1) },
    byKind: Object.fromEntries(Object.entries(times).map(([k, v]) => [k, { n: v.length, p50: +pct(v, 50).toFixed(1), p95: +pct(v, 95).toFixed(1), max: +Math.max(...v).toFixed(1) }])),
  };
  console.log(JSON.stringify(summary, null, 1));
  const out = path.join(repoRoot(), "build/bench");
  mkdirSync(out, { recursive: true });
  writeFileSync(path.join(out, "search-latency.json"), JSON.stringify(summary, null, 1));
  await pool.end();
}
main().catch((e) => {
  console.error(e);
  process.exit(1);
});
