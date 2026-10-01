import "server-only";
import { sql } from "drizzle-orm";
import { db } from "@/db";

/** Recompute catalog_stats from published rows (same definition as the Python loader). */
export async function recomputeStats() {
  await db.execute(sql`
    WITH d AS (SELECT * FROM designs),
    core AS (SELECT count(*) FILTER (WHERE status='published' AND area='core') AS designs,
                    count(*) FILTER (WHERE status='published' AND area='core' AND published_styles @> ARRAY['filled','line','rounded']) AS complete,
                    count(*) FILTER (WHERE status='published' AND area='core' AND published_styles @> ARRAY['filled','line','rounded'] AND derived_from IS NULL) AS counted,
                    count(*) FILTER (WHERE status='published' AND area='core' AND published_styles @> ARRAY['filled','line','rounded'] AND derived_from IS NULL
                                     AND NOT (attributes ? 'variantOf')) AS base
             FROM d)
    UPDATE catalog_stats SET computed_at = now(), data = jsonb_set(jsonb_set(jsonb_set(data,
      '{designs,total}', to_jsonb((SELECT count(*) FROM d WHERE status='published'))),
      '{core}', jsonb_build_object('designs', (SELECT designs FROM core), 'completeThreeStyle', (SELECT complete FROM core),
                                   'countedTowardTarget', (SELECT counted FROM core), 'transformDerived', (SELECT complete - counted FROM core))),
      '{target}', jsonb_build_object('uniqueCoreConcepts', 20000, 'current', (SELECT base FROM core), 'gap', GREATEST(0, 20000 - (SELECT base FROM core))))
    WHERE id = 'current'`);
}

export async function enqueueOutbox(topic: string, payload: Record<string, unknown>) {
  await db.execute(sql`INSERT INTO outbox (topic, payload) VALUES (${topic}, ${JSON.stringify(payload)}::jsonb)`);
}
