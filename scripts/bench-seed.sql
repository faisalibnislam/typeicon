-- Synthetic load-test catalog for the SEPARATE typeicon_bench database only.
-- Never run against the public database: these rows are fake and must never reach counts or pages.
DO $$ BEGIN
  IF current_database() NOT LIKE '%bench%' THEN RAISE EXCEPTION 'bench-seed.sql refuses to run outside a *_bench database'; END IF;
END $$;

INSERT INTO source_packs (slug, area, display_name, namespace, name_prefix, version, license_id, review_status)
VALUES ('synthetic', 'community', 'Synthetic load test', 'pack:synthetic', 'synth', '0.0.0', 'MIT', 'approved')
ON CONFLICT (slug) DO NOTHING;

WITH words AS (
  SELECT array_agg(w) AS w FROM (SELECT DISTINCT unnest(tags) AS w FROM designs WHERE status = 'published' LIMIT 3000) t
), gen AS (
  SELECT g, w[1 + (g::bigint * 7919) % array_length(w, 1)] AS a, w[1 + (g::bigint * 104729) % array_length(w, 1)] AS b,
         w[1 + (g::bigint * 1299709) % array_length(w, 1)] AS c
  FROM generate_series(1, 140000) g, words
)
INSERT INTO concepts (id, slug, name)
SELECT md5('synth-concept-' || g)::uuid, 'synth-' || regexp_replace(lower(a || '-' || b), '[^a-z0-9-]', '', 'g') || '-' || g, a || ' ' || b FROM gen
ON CONFLICT DO NOTHING;

WITH words AS (
  SELECT array_agg(w) AS w FROM (SELECT DISTINCT unnest(tags) AS w FROM designs WHERE status = 'published' LIMIT 3000) t
), cats AS (SELECT array_agg(slug) AS c FROM categories), gen AS (
  SELECT g, w[1 + (g::bigint * 7919) % array_length(w, 1)] AS a, w[1 + (g::bigint * 104729) % array_length(w, 1)] AS b,
         w[1 + (g::bigint * 1299709) % array_length(w, 1)] AS c, cats.c[1 + g % array_length(cats.c, 1)] AS cat
  FROM generate_series(1, 140000) g, words, cats
)
INSERT INTO designs (id, concept_id, source_pack_id, name, local_name, native_name, namespace, area, tags, category_slugs,
                     alias_names, published_styles, status, license_id, search_names, search_tags, codepoint)
SELECT md5('synth-design-' || g)::uuid, md5('synth-concept-' || g)::uuid, (SELECT id FROM source_packs WHERE slug = 'synthetic'),
       'synth-' || regexp_replace(lower(a || '-' || b), '[^a-z0-9-]', '', 'g') || '-' || g,
       regexp_replace(lower(a || '-' || b), '[^a-z0-9-]', '', 'g') || '-' || g, 'n' || g, 'pack:synthetic', 'community',
       ARRAY[lower(a), lower(b), lower(c)], ARRAY[cat], '{}',
       CASE g % 3 WHEN 0 THEN ARRAY['filled','line','rounded'] WHEN 1 THEN ARRAY['line','rounded'] ELSE ARRAY['filled'] END,
       'published', 'MIT',
       'synth ' || lower(a) || ' ' || lower(b) || ' ' || g, lower(a || ' ' || b || ' ' || c || ' ' || cat), 1048576 + g
FROM gen ON CONFLICT DO NOTHING;

INSERT INTO variants (id, design_id, style, native_style, native_label, status, route, svg, svg_sha256, source_path, source_sha256, font_supported)
SELECT md5('synth-variant-' || d.id || s)::uuid, d.id, s, s, s, 'published', 'font',
       '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M4 4h16v16H4z"/></svg>',
       md5(d.id::text || s), 'synthetic', md5(d.id::text), true
FROM designs d, unnest(d.published_styles) s WHERE d.namespace = 'pack:synthetic'
ON CONFLICT DO NOTHING;

ANALYZE;
SELECT count(*) AS designs, (SELECT count(*) FROM variants) AS variants FROM designs;
