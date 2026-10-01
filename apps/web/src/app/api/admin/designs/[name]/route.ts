import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/db";
import { enqueueOutbox, recomputeStats } from "@/lib/admin";
import { handle, readJson } from "@/lib/api";
import { audit } from "@/lib/audit";
import { apiUser, HttpError } from "@/lib/session";

const kebab = z.string().regex(/^(?=.{2,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$/);
const body = z.object({
  description: z.string().trim().max(300).optional(),
  tags: z.array(z.string().trim().toLowerCase().min(1).max(40)).max(40).optional(),
  categories: z.array(kebab).max(8).optional(),
  aliases: z.array(kebab).max(20).optional(),
  status: z.enum(["published", "pending", "deprecated"]).optional(),
});

/** Edit metadata. Applied live and recorded as an override for the next pipeline build (fonts pick up alias changes on the next release). */
export const PATCH = handle(async (req, ctx: { params: Promise<{ name: string }> }) => {
  const admin = await apiUser({ admin: true });
  const { name } = await ctx.params;
  const input = await readJson(req, body);
  await db.transaction(async (tx) => {
    const d = await tx.execute(sql`SELECT id, namespace, area FROM designs WHERE name = ${name}`);
    const row = d.rows[0] as { id: string; namespace: string; area: string } | undefined;
    if (!row) throw new HttpError(404, "Unknown icon");
    if (input.aliases) {
      const uniq = [...new Set(input.aliases)].filter((a) => a !== name);
      for (const a of uniq) {
        const clash = await tx.execute(sql`SELECT d.name FROM name_registry r JOIN designs d ON d.id = r.design_id
          WHERE r.namespace IN (${row.namespace}, 'global') AND r.name = ${a} AND r.design_id <> ${row.id}`);
        if (clash.rows.length) throw new HttpError(409, `Alias "${a}" collides with ${(clash.rows[0] as { name: string }).name}`);
      }
      await tx.execute(sql`DELETE FROM name_registry WHERE design_id = ${row.id} AND kind = 'alias'`);
      await tx.execute(sql`DELETE FROM aliases WHERE design_id = ${row.id}`);
      for (const a of uniq) {
        await tx.execute(sql`INSERT INTO name_registry (namespace, name, design_id, kind) VALUES (${row.namespace}, ${a}, ${row.id}, 'alias')`);
        await tx.execute(sql`INSERT INTO aliases (design_id, namespace, name) VALUES (${row.id}, ${row.namespace}, ${a})`);
      }
      input.aliases = uniq;
    }
    const arr = (v: string[]) => (v.length ? sql`ARRAY[${sql.join(v.map((x) => sql`${x}`), sql`, `)}]::text[]` : sql`'{}'::text[]`);
    await tx.execute(sql`UPDATE designs SET
      description = ${input.description !== undefined ? input.description || null : sql`description`},
      tags = ${input.tags ? arr(input.tags) : sql`tags`},
      category_slugs = ${input.categories ? arr(input.categories) : sql`category_slugs`},
      alias_names = ${input.aliases ? arr(input.aliases) : sql`alias_names`},
      status = ${input.status ?? sql`status`},
      search_tags = array_to_string(${input.tags ? arr(input.tags) : sql`tags`} || ${input.categories ? arr(input.categories) : sql`category_slugs`}, ' '),
      search_names = concat_ws(' ', name, local_name, replace(name, '-', ' '), array_to_string(${input.aliases ? arr(input.aliases) : sql`alias_names`}, ' ')),
      updated_at = now()
      WHERE id = ${row.id}`);
    if (input.categories) {
      for (const c of input.categories) await tx.execute(sql`INSERT INTO categories (slug, name) VALUES (${c}, ${c.replace(/-/g, " ")}) ON CONFLICT (slug) DO NOTHING`);
      await tx.execute(sql`DELETE FROM design_categories WHERE design_id = ${row.id}`);
      await tx.execute(sql`INSERT INTO design_categories (design_id, category_id) SELECT ${row.id}, id FROM categories WHERE slug = ANY(${arr(input.categories)})`);
    }
    const { status: _s, ...override } = input;
    await tx.execute(sql`INSERT INTO metadata_overrides (design_name, data, updated_by) VALUES (${name}, ${JSON.stringify(override)}::jsonb, ${admin.email})
      ON CONFLICT (design_name) DO UPDATE SET data = metadata_overrides.data || EXCLUDED.data, updated_by = EXCLUDED.updated_by, updated_at = now()`);
  });
  await recomputeStats();
  await enqueueOutbox("catalog.design_updated", { name });
  await audit(admin.id, "design.update", "design", name, input);
  return NextResponse.json({ ok: true });
});
