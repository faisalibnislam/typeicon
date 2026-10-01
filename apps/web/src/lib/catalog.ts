import "server-only";
import { cache } from "react";
import { sql } from "drizzle-orm";
import { db } from "@/db";
import type { StyleSlug } from "./search-params";

type Row = Record<string, unknown>;

export interface CatalogStats {
  designs: { total: number; core: number; community: number; brands: number };
  concepts: number;
  variants: { total: number; byStyle: Record<string, { variants: number; fontSupported: number; svgOnly: number }>; fontSupported: number; svgOnly: number };
  aliases: number;
  core: { designs: number; completeThreeStyle: number; countedTowardTarget: number; transformDerived: number; variants?: number; base?: number };
  target: { uniqueCoreConcepts: number; current: number; gap: number };
  sources: { slug: string; displayName: string; area: string; designs: number; variants: number }[];
  computedAt: string;
}

export const getStats = cache(async (): Promise<CatalogStats | null> => {
  const r = await db.execute(sql`SELECT data, computed_at FROM catalog_stats WHERE id = 'current'`);
  const row = r.rows[0] as Row | undefined;
  if (!row) return null;
  return { ...(row.data as Omit<CatalogStats, "computedAt">), computedAt: String(row.computed_at) };
});

export interface VariantDetail {
  id: string;
  style: StyleSlug;
  nativeStyle: string;
  nativeLabel: string;
  status: string;
  route: string;
  reasons: string[];
  svg: string | null;
  svgSha256: string | null;
  viewBox: number[] | null;
  sourcePath: string;
  sourceSha256: string;
  fontSupported: boolean;
  fontFamily: string | null;
  fontSlug: string | null;
  keywords: string[];
  cssClass: string | null;
}

export interface DesignDetail {
  id: string;
  name: string;
  localName: string;
  nativeName: string;
  area: "core" | "brands";
  namespace: string;
  description: string | null;
  context: string | null;
  keywords: string[];
  tags: string[];
  categories: string[];
  aliases: string[];
  isBrand: boolean;
  derivedFrom: { name: string; transform: string } | null;
  attributes: { title?: string; hex?: string; sourceUrl?: string | null; guidelines?: string | null; licenseUrl?: string | null; variantOf?: { name: string; modifier: string }; designReview?: { status: "pending" | "approved"; note?: string | null } };
  codepoint: number | null;
  bmpCodepoint: number | null;
  concept: { id: string; slug: string };
  license: { id: string; name: string; url: string | null };
  source: {
    slug: string;
    displayName: string;
    version: string;
    upstreamUrl: string | null;
    author: string | null;
    copyright: string | null;
    attributionRequired: boolean;
    attributionText: string | null;
    styleMappingNote: string | null;
    trademarkNote: string | null;
    retrievedAt: string | null;
    reviewStatus: string;
  };
  release: { version: string; releaseDate: string } | null;
  variants: VariantDetail[];
}

export const getDesign = cache(async (name: string): Promise<DesignDetail | null> => {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name) || name.length > 80) return null;
  const r = await db.execute(sql`
    SELECT d.*, c.slug AS concept_slug, l.name AS license_name, l.url AS license_url,
           sp.slug AS source_slug, sp.display_name, sp.version AS source_version, sp.upstream_url, sp.author, sp.copyright,
           sp.attribution_required, sp.attribution_text, sp.style_mapping_note, sp.trademark_note, sp.retrieved_at,
           sp.review_status, rel.version AS release_version, rel.release_date
    FROM designs d
    JOIN concepts c ON c.id = d.concept_id
    JOIN licenses l ON l.id = d.license_id
    JOIN source_packs sp ON sp.id = d.source_pack_id
    LEFT JOIN releases rel ON rel.id = d.first_release_id
    WHERE d.name = ${name} AND d.status = 'published'`);
  const d = r.rows[0] as Row | undefined;
  if (!d) return null;
  const v = await db.execute(sql`
    SELECT v.id, v.style, v.native_style, v.native_label, v.status, v.route, v.reasons, v.svg, v.svg_sha256, v.view_box,
           v.source_path, v.source_sha256, v.font_supported, fb.family, fb.slug AS font_slug, fb.css_class, ga.keywords
    FROM variants v
    LEFT JOIN glyph_assignments ga ON ga.variant_id = v.id
    LEFT JOIN font_bundles fb ON fb.id = ga.font_bundle_id
      AND fb.release_id = (SELECT id FROM releases WHERE status = 'published' ORDER BY release_date DESC, created_at DESC LIMIT 1)
    WHERE v.design_id = ${d.id as string} AND v.status = 'published'
    ORDER BY array_position(ARRAY['filled','line','rounded']::text[], v.style)`);
  return {
    id: d.id as string,
    name: d.name as string,
    localName: d.local_name as string,
    nativeName: d.native_name as string,
    area: d.area as DesignDetail["area"],
    namespace: d.namespace as string,
    description: (d.description as string) ?? null,
    context: (d.context as string) ?? null,
    keywords: (d.keywords as string[]) ?? [],
    tags: (d.tags as string[]) ?? [],
    categories: (d.category_slugs as string[]) ?? [],
    aliases: (d.alias_names as string[]) ?? [],
    isBrand: Boolean(d.is_brand),
    derivedFrom: (d.derived_from as DesignDetail["derivedFrom"]) ?? null,
    attributes: (d.attributes as DesignDetail["attributes"]) ?? {},
    codepoint: (d.codepoint as number) ?? null,
    bmpCodepoint: (d.bmp_codepoint as number) ?? null,
    concept: { id: d.concept_id as string, slug: d.concept_slug as string },
    license: { id: d.license_id as string, name: d.license_name as string, url: (d.license_url as string) ?? null },
    source: {
      slug: d.source_slug as string,
      displayName: d.display_name as string,
      version: d.source_version as string,
      upstreamUrl: (d.upstream_url as string) ?? null,
      author: (d.author as string) ?? null,
      copyright: (d.copyright as string) ?? null,
      attributionRequired: Boolean(d.attribution_required),
      attributionText: (d.attribution_text as string) ?? null,
      styleMappingNote: (d.style_mapping_note as string) ?? null,
      trademarkNote: (d.trademark_note as string) ?? null,
      retrievedAt: d.retrieved_at ? String(d.retrieved_at) : null,
      reviewStatus: d.review_status as string,
    },
    release: d.release_version ? { version: d.release_version as string, releaseDate: String(d.release_date) } : null,
    variants: (v.rows as Row[]).map((x) => ({
      id: x.id as string,
      style: x.style as StyleSlug,
      nativeStyle: x.native_style as string,
      nativeLabel: x.native_label as string,
      status: x.status as string,
      route: x.route as string,
      reasons: (x.reasons as string[]) ?? [],
      svg: (x.svg as string) ?? null,
      svgSha256: (x.svg_sha256 as string) ?? null,
      viewBox: (x.view_box as number[]) ?? null,
      sourcePath: x.source_path as string,
      sourceSha256: x.source_sha256 as string,
      fontSupported: Boolean(x.font_supported),
      fontFamily: (x.family as string) ?? null,
      fontSlug: (x.font_slug as string) ?? null,
      keywords: (x.keywords as string[]) ?? [],
      cssClass: (x.css_class as string) ?? null,
    })),
  };
});

export interface RelatedIcon {
  name: string;
  area: string;
  sourceName: string;
  style: StyleSlug;
  svg: string;
  relation: "same-concept" | "same-category";
}

export async function getRelated(design: DesignDetail, limit = 18): Promise<RelatedIcon[]> {
  const r = await db.execute(sql`
    WITH candidates AS (
      SELECT d.id, d.name, d.area, sp.display_name, d.published_styles, 0 AS pri, 'same-concept' AS relation
      FROM designs d JOIN source_packs sp ON sp.id = d.source_pack_id
      WHERE d.concept_id = ${design.concept.id} AND d.id <> ${design.id} AND d.status = 'published'
      UNION ALL
      SELECT d.id, d.name, d.area, sp.display_name, d.published_styles, 1, 'same-category'
      FROM designs d JOIN source_packs sp ON sp.id = d.source_pack_id
      WHERE d.category_slugs && ${design.categories.length ? sql`ARRAY[${sql.join(design.categories.map((c) => sql`${c}`), sql`, `)}]::text[]` : sql`ARRAY[]::text[]`}
        AND d.source_pack_id = (SELECT source_pack_id FROM designs WHERE id = ${design.id})
        AND d.id <> ${design.id} AND d.status = 'published'
    ), picked AS (
      SELECT DISTINCT ON (id) * FROM candidates ORDER BY id, pri
    )
    SELECT p.name, p.area, p.display_name, p.relation, v.style, v.svg
    FROM picked p
    JOIN LATERAL (
      SELECT style, svg FROM variants WHERE design_id = p.id AND status = 'published'
      ORDER BY array_position(ARRAY['line','rounded','filled']::text[], style) LIMIT 1
    ) v ON true
    ORDER BY p.pri, (p.area <> 'core'), p.name
    LIMIT ${limit}`);
  return (r.rows as Row[]).map((x) => ({
    name: x.name as string,
    area: x.area as string,
    sourceName: x.display_name as string,
    style: x.style as StyleSlug,
    svg: x.svg as string,
    relation: x.relation as RelatedIcon["relation"],
  }));
}

export async function listCategories(): Promise<{ slug: string; name: string; count: number; coreCount: number }[]> {
  const r = await db.execute(sql`
    SELECT c.slug, c.name, count(d.id)::int AS n, count(d.id) FILTER (WHERE d.area = 'core')::int AS core
    FROM categories c JOIN design_categories dc ON dc.category_id = c.id
    JOIN designs d ON d.id = dc.design_id AND d.status = 'published'
    GROUP BY c.slug, c.name ORDER BY core DESC, n DESC, c.slug`);
  return (r.rows as Row[]).map((x) => ({ slug: x.slug as string, name: x.name as string, count: Number(x.n), coreCount: Number(x.core) }));
}

export async function getCategory(slug: string) {
  const r = await db.execute(sql`SELECT slug, name, description FROM categories WHERE slug = ${slug}`);
  return (r.rows[0] as { slug: string; name: string; description: string | null } | undefined) ?? null;
}

export interface PackSummary {
  slug: string;
  area: string;
  displayName: string;
  version: string;
  upstreamUrl: string | null;
  author: string | null;
  copyright: string | null;
  licenseId: string;
  licenseName: string;
  attributionText: string | null;
  attributionRequired: boolean;
  styleMapping: Record<string, { style: string; nativeLabel?: string }>;
  styleMappingNote: string | null;
  trademarkNote: string | null;
  notices: string[];
  modificationHistory: string[];
  distribution: Record<string, string>;
  retrievedAt: string | null;
  reviewStatus: string;
  reviewNote: string | null;
  designs: number;
  variants: number;
  byStyle: Record<string, number>;
}

export const listPacks = cache(async (): Promise<PackSummary[]> => {
  const r = await db.execute(sql`
    SELECT sp.*, l.name AS license_name,
      (SELECT count(*)::int FROM designs d WHERE d.source_pack_id = sp.id AND d.status = 'published') AS designs,
      (SELECT json_object_agg(style, n) FROM (SELECT v.style, count(*)::int AS n FROM variants v JOIN designs d ON d.id = v.design_id
         WHERE d.source_pack_id = sp.id AND v.status = 'published' GROUP BY v.style) s) AS by_style
    FROM source_packs sp JOIN licenses l ON l.id = sp.license_id
    ORDER BY (sp.area <> 'core'), sp.display_name`);
  return (r.rows as Row[]).map((x) => {
    const byStyle = (x.by_style as Record<string, number>) ?? {};
    return {
      slug: x.slug as string,
      area: x.area as string,
      displayName: x.display_name as string,
      version: x.version as string,
      upstreamUrl: (x.upstream_url as string) ?? null,
      author: (x.author as string) ?? null,
      copyright: (x.copyright as string) ?? null,
      licenseId: x.license_id as string,
      licenseName: x.license_name as string,
      attributionText: (x.attribution_text as string) ?? null,
      attributionRequired: Boolean(x.attribution_required),
      styleMapping: (x.style_mapping as PackSummary["styleMapping"]) ?? {},
      styleMappingNote: (x.style_mapping_note as string) ?? null,
      trademarkNote: (x.trademark_note as string) ?? null,
      notices: (x.notices as string[]) ?? [],
      modificationHistory: (x.modification_history as string[]) ?? [],
      distribution: (x.distribution as Record<string, string>) ?? {},
      retrievedAt: x.retrieved_at ? String(x.retrieved_at) : null,
      reviewStatus: x.review_status as string,
      reviewNote: (x.review_note as string) ?? null,
      designs: Number(x.designs),
      variants: Object.values(byStyle).reduce((a, b) => a + b, 0),
      byStyle,
    };
  });
});

export interface ReleaseInfo {
  id: string;
  version: string;
  releaseDate: string;
  counts: Record<string, number>;
  archives: { kind: string; label: string; file: string; bytes: number; sha256: string; meta: Record<string, unknown> }[];
  families: {
    slug: string;
    family: string;
    postscriptName: string;
    source: string;
    style: string;
    cssClass: string;
    glyphCount: number;
    keywordCount: number;
    files: Record<string, { name: string; bytes: number; sha256: string; storageKey?: string }>;
    validation: Record<string, { ok: boolean; stats: Record<string, unknown> }>;
    raster: { minIoU: number; meanIoU: number; checked: number } | null;
  }[];
}

export const getLatestRelease = cache(async (): Promise<ReleaseInfo | null> => {
  const r = await db.execute(sql`SELECT id, version, release_date, counts FROM releases WHERE status = 'published'
                                 ORDER BY release_date DESC, created_at DESC LIMIT 1`);
  const rel = r.rows[0] as Row | undefined;
  if (!rel) return null;
  const [a, f] = await Promise.all([
    db.execute(sql`SELECT kind, label, file, bytes, sha256, meta FROM release_archives WHERE release_id = ${rel.id as string} ORDER BY bytes DESC`),
    db.execute(sql`SELECT fb.slug, fb.family, fb.postscript_name, sp.slug AS source, fb.style, fb.css_class, fb.glyph_count,
                          fb.keyword_count, fb.files, fb.validation, fb.raster
                   FROM font_bundles fb JOIN source_packs sp ON sp.id = fb.source_pack_id
                   WHERE fb.release_id = ${rel.id as string}
                   ORDER BY (sp.area <> 'core'), sp.slug, array_position(ARRAY['filled','line','rounded']::text[], fb.style)`),
  ]);
  return {
    id: rel.id as string,
    version: rel.version as string,
    releaseDate: String(rel.release_date),
    counts: rel.counts as Record<string, number>,
    archives: (a.rows as Row[]).map((x) => ({
      kind: x.kind as string,
      label: x.label as string,
      file: x.file as string,
      bytes: Number(x.bytes),
      sha256: x.sha256 as string,
      meta: x.meta as Record<string, unknown>,
    })),
    families: (f.rows as Row[]).map((x) => ({
      slug: x.slug as string,
      family: x.family as string,
      postscriptName: x.postscript_name as string,
      source: x.source as string,
      style: x.style as string,
      cssClass: x.css_class as string,
      glyphCount: Number(x.glyph_count),
      keywordCount: Number(x.keyword_count),
      files: x.files as ReleaseInfo["families"][number]["files"],
      validation: x.validation as ReleaseInfo["families"][number]["validation"],
      raster: (x.raster as ReleaseInfo["families"][number]["raster"]) ?? null,
    })),
  };
});

/** Small sample of Core icons for the home page previews. */
export async function getCoreSamples(names: string[]) {
  const r = await db.execute(sql`
    SELECT d.name, v.style, v.svg FROM designs d JOIN variants v ON v.design_id = d.id AND v.status = 'published'
    WHERE d.area = 'core' AND d.status = 'published' AND d.name IN (${sql.join(names.map((n) => sql`${n}`), sql`, `)})`);
  const out: Record<string, Partial<Record<StyleSlug, string>>> = {};
  for (const x of r.rows as Row[]) (out[x.name as string] ??= {})[x.style as StyleSlug] = x.svg as string;
  return out;
}
