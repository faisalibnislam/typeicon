import "server-only";
import { type SQL, sql } from "drizzle-orm";
import { db } from "@/db";
import { synonymGroups } from "@/generated/synonyms";
import { type Facet, type IconCard, type SearchInput, STYLE_SLUGS, type StyleSlug, normalizeQuery } from "./search-params";

export * from "./search-params";

export function synonymsFor(term: string): string[] {
  const out = new Set<string>();
  for (const g of synonymGroups) if (g.includes(term)) g.forEach((t) => t !== term && out.add(t));
  return [...out];
}

/** Words people add to queries that no icon is described by ("an icon for delete", "arrow symbol"). */
const FILLER_WORDS = new Set(["a", "an", "the", "for", "of", "to", "with", "and", "or", "in", "on", "icon", "icons", "symbol", "glyph", "logo"]);

/** The query word plus its singular, so "users" finds "user" and "boxes" finds "box" (prefix matching covers plurals). */
export function wordForms(term: string): string[] {
  const out = new Set([term]);
  if (term.length > 3) {
    if (term.endsWith("ies")) out.add(term.slice(0, -3) + "y");
    else if (/(ches|shes|sses|xes|zes)$/.test(term)) out.add(term.slice(0, -2));
    else if (term.endsWith("s") && !term.endsWith("ss")) out.add(term.slice(0, -1));
  }
  return [...out];
}

export interface SearchResult {
  input: SearchInput;
  normalizedQuery: string;
  items: IconCard[];
  total: number;
  pages: number;
  missingInStyle: number;
  facets: { styles: Facet[]; packs: Facet[]; licenses: Facet[]; categories: Facet[]; areas: Facet[] };
  tookMs: number;
}

const textArray = (values: string[]) => sql`ARRAY[${sql.join(values.map((v) => sql`${v}`), sql`, `)}]::text[]`;

type Dim = "q" | "style" | "pack" | "license" | "category" | "area" | "brands";

function buildConditions(input: SearchInput) {
  const conds: Partial<Record<Dim, SQL>> = {};
  const raw = normalizeQuery(input.q);
  let rank: SQL | null = null;
  let tier: SQL | null = null;
  let variantFirstTiers = 0;
  if (raw) {
    const words = raw.split("-").filter(Boolean);
    const meaningful = words.filter((t) => !FILLER_WORDS.has(t));
    const terms = meaningful.length ? meaningful : words; // "icon for delete" searches "delete"
    const qn = terms.join("-");
    const clean = (x: string) => x.replace(/[^a-z0-9]/g, "");
    // The typed word (and its singular) is prefix-matched; synonyms must match as whole words, otherwise
    // "bin" (a synonym of trash) would pull in binary and binoculars.
    const tsq = terms
      .map((t) => {
        const typed = wordForms(t).map(clean).filter(Boolean).map((x) => `${x}:*`);
        const syns = synonymsFor(t).map(clean).filter((x) => x.length > 1);
        return `(${[...new Set([...typed, ...syns])].join(" | ")})`;
      })
      .join(" & ");
    const exact = terms.length === 1 ? wordForms(terms[0]) : [qn]; // "users" is an exact match for user
    const syn = synonymsFor(qn);
    const prefix = qn.replace(/[\\%_]/g, "\\$&") + "%";
    const phrase = terms.length > 1 ? `% ${terms.join(" ")} %` : null; // "add user" among the keywords
    const tsquery = sql`to_tsquery('simple', ${tsq})`;
    const synCond = syn.length ? sql`d.local_name = ANY(${textArray(syn)})` : sql`false`;
    const phraseCond = phrase ? sql`(' ' || d.search_tags || ' ') LIKE ${phrase}` : sql`false`;
    conds.q = sql`(d.name = ANY(${textArray(exact)}) OR d.local_name = ANY(${textArray(exact)}) OR d.alias_names @> ${textArray([qn])} OR ${synCond}
      OR d.local_name LIKE ${prefix} OR d.name LIKE ${prefix} OR d.search @@ ${tsquery}
      OR (char_length(${qn}) >= 4 AND d.local_name % ${qn}))`;
    tier = sql`CASE WHEN d.local_name = ANY(${textArray(exact)}) OR d.name = ANY(${textArray(exact)}) THEN 0
      WHEN d.alias_names @> ${textArray([qn])} THEN 1
      WHEN ${synCond} THEN 2
      WHEN d.local_name LIKE ${prefix} OR d.name LIKE ${prefix} THEN 3
      WHEN ${phraseCond} THEN 4
      WHEN d.search @@ ${tsquery} THEN 5 ELSE 6 END`;
    variantFirstTiers = 3; // name matches: file before file-plus; text matches rank by relevance
    rank = sql`ts_rank_cd(d.search, ${tsquery}) DESC, similarity(d.local_name, ${qn}) DESC`;
  }
  if (input.style !== "all" && !input.missing) conds.style = sql`d.published_styles @> ${textArray([input.style])}`;
  if (input.pack.length) conds.pack = sql`sp.slug IN (${sql.join(input.pack.map((p) => sql`${p}`), sql`, `)})`;
  if (input.license.length) conds.license = sql`d.license_id IN (${sql.join(input.license.map((p) => sql`${p}`), sql`, `)})`;
  if (input.category.length) conds.category = sql`d.category_slugs && ${textArray(input.category)}`;
  if (input.area !== "all") conds.area = sql`d.area = ${input.area}`;
  if (input.brands === "exclude") conds.brands = sql`NOT d.is_brand`;
  if (input.brands === "only") conds.brands = sql`d.is_brand`;
  const where = (except?: Dim) =>
    sql.join(
      [sql`d.status = 'published'`, ...Object.entries(conds).filter(([k]) => k !== except).map(([, v]) => v as SQL)],
      sql` AND `,
    );
  return { qn: raw, where, tier, rank, variantFirstTiers };
}

const displayStyleExpr = (input: SearchInput) =>
  input.style !== "all"
    ? sql`${input.style}::text`
    : sql`CASE WHEN 'line' = ANY(d.published_styles) THEN 'line'
               WHEN 'rounded' = ANY(d.published_styles) THEN 'rounded'
               WHEN 'filled' = ANY(d.published_styles) THEN 'filled'
               WHEN 'thin' = ANY(d.published_styles) THEN 'thin'
               ELSE 'brand' END`;

type Row = Record<string, unknown>;

export async function searchIcons(input: SearchInput): Promise<SearchResult> {
  const t0 = performance.now();
  const { qn, where, tier, rank, variantFirstTiers } = buildConditions(input);
  const offset = (input.page - 1) * input.per;
  const order: SQL[] = [];
  // Within a tier, drawn base icons come before their badge variants (file before file-plus, file-lock, ...).
  // Within name tiers, drawn icons come before their badge variants (file before file-plus); for text matches
  // relevance decides, so "add user" finds user-plus first.
  if (tier && input.sort === "relevance")
    order.push(sql`${tier}`, sql`(d.area <> 'core')`, sql`(${tier} <= ${variantFirstTiers} AND d.attributes ? 'variantOf')`, rank!, sql`(d.attributes ? 'variantOf')`);
  if (input.sort === "pack") order.push(sql`(d.area <> 'core')`, sql`sp.slug`);
  if (!tier || input.sort !== "relevance") order.push(sql`(d.area <> 'core')`);
  order.push(sql`d.local_name`, sql`d.name`);
  const from = sql`FROM designs d JOIN source_packs sp ON sp.id = d.source_pack_id`;

  const pageQuery = db.execute(sql`
    SELECT d.id, d.name, d.local_name, d.area, d.is_brand, sp.slug AS source, sp.display_name AS source_name,
           d.license_id, d.codepoint, d.published_styles, ds.style AS display_style, v.svg
    ${from}
    CROSS JOIN LATERAL (SELECT ${displayStyleExpr(input)} AS style) ds
    LEFT JOIN variants v ON v.design_id = d.id AND v.style = ds.style AND v.status = 'published'
    WHERE ${where()}
    ORDER BY ${sql.join(order, sql`, `)}
    LIMIT ${input.per} OFFSET ${offset}`);
  const countQuery = db.execute(sql`SELECT count(*)::int AS n ${from} WHERE ${where()}`);
  const facet = (dim: Dim, select: SQL, group: SQL, extraFrom = sql``, limit = 200) =>
    db.execute(sql`SELECT ${select} AS value, count(*)::int AS n ${from} ${extraFrom} WHERE ${where(dim)}
                   GROUP BY ${group} ORDER BY n DESC, value LIMIT ${limit}`);
  const [pageRes, countRes, styleF, packF, licF, catF, areaF] = await Promise.all([
    pageQuery,
    countQuery,
    facet("style", sql`s.style`, sql`s.style`, sql`CROSS JOIN LATERAL unnest(d.published_styles) AS s(style)`),
    db.execute(sql`SELECT sp.slug AS value, sp.display_name AS label, count(*)::int AS n ${from} WHERE ${where("pack")}
                   GROUP BY sp.slug, sp.display_name ORDER BY (min(d.area) <> 'core'), n DESC`),
    facet("license", sql`d.license_id`, sql`d.license_id`),
    facet("category", sql`c.slug`, sql`c.slug`, sql`CROSS JOIN LATERAL unnest(d.category_slugs) AS c(slug)`, 60),
    facet("area", sql`d.area`, sql`d.area`),
  ]);
  const total = Number((countRes.rows[0] as Row).n);
  const styleCounts = Object.fromEntries((styleF.rows as Row[]).map((r) => [r.value as string, Number(r.n)]));
  let missingInStyle = 0;
  if (input.style !== "all") {
    // Only designs that could have this style count as "missing" (brand logos never have Core styles, and vice versa).
    const eligible = input.style === "brand" ? sql`d.area = 'brands'` : sql`d.area = 'core'`;
    const all = await db.execute(sql`SELECT count(*)::int AS n ${from} WHERE ${where("style")} AND ${eligible}`);
    missingInStyle = Number((all.rows[0] as Row).n) - (styleCounts[input.style] ?? 0);
  }
  const items: IconCard[] = (pageRes.rows as Row[]).map((r) => {
    const styles = (r.published_styles as StyleSlug[]) ?? [];
    const display = r.display_style as StyleSlug;
    const available = styles.includes(display);
    return {
      id: r.id as string,
      name: r.name as string,
      localName: r.local_name as string,
      area: r.area as IconCard["area"],
      isBrand: Boolean(r.is_brand),
      source: r.source as string,
      sourceName: r.source_name as string,
      license: r.license_id as string,
      codepoint: (r.codepoint as number) ?? null,
      styles,
      displayStyle: available ? display : null,
      svg: available ? (r.svg as string) : null,
    };
  });
  const tookMs = performance.now() - t0;
  void db
    .execute(sql`INSERT INTO search_metrics (query_length, result_count, duration_ms) VALUES (${qn.length}, ${total}, ${tookMs})`)
    .catch(() => undefined);
  const label = (s: string) => s.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  return {
    input,
    normalizedQuery: qn,
    items,
    total,
    pages: Math.max(1, Math.ceil(total / input.per)),
    missingInStyle,
    tookMs,
    facets: {
      styles: STYLE_SLUGS.map((s) => ({ value: s, label: label(s), count: styleCounts[s] ?? 0 })),
      packs: (packF.rows as Row[]).map((r) => ({ value: r.value as string, label: r.label as string, count: Number(r.n) })),
      licenses: (licF.rows as Row[]).map((r) => ({ value: r.value as string, label: r.value as string, count: Number(r.n) })),
      categories: (catF.rows as Row[]).map((r) => ({ value: r.value as string, label: label(r.value as string), count: Number(r.n) })),
      areas: (areaF.rows as Row[]).map((r) => ({ value: r.value as string, label: r.value === "core" ? "TypeIcon Core" : "Brand logos", count: Number(r.n) })),
    },
  };
}

