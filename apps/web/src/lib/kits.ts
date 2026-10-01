import "server-only";
import { randomBytes } from "node:crypto";
import { sql } from "drizzle-orm";
import { db } from "@/db";

export const KIT_CODEPOINT_BASE = 0x10f000;
export const KIT_CODEPOINT_LIMIT = 4094;

export function newEmbedId(): string {
  return randomBytes(9).toString("base64url"); // public identifier, not a secret
}

export interface KitDetail {
  id: string;
  name: string;
  slug: string;
  embedId: string;
  allowedDomains: string[];
  currentVersion: number;
  pinnedRelease: string | null;
  versions: { version: number; createdAt: string; contentHash: string; formats: string[]; items: number; customIcons: number; job: { id: string; status: string; error: string | null; storageKey: string | null; fileName: string | null; bytes: number | null } | null }[];
  customIcons: { id: string; name: string; style: string; status: string; route: string | null; reasons: string[]; svg: string | null; codepoint: number }[];
}

export async function getKit(id: string): Promise<KitDetail | null> {
  const k = await db.execute(sql`SELECT k.*, r.version AS release_version FROM kits k LEFT JOIN releases r ON r.id = k.pinned_release_id WHERE k.id = ${id}`);
  const kit = k.rows[0] as Record<string, unknown> | undefined;
  if (!kit) return null;
  const [vers, icons] = await Promise.all([
    db.execute(sql`
      SELECT kv.version, kv.created_at, kv.content_hash, kv.formats, kv.selection,
             j.id AS job_id, j.status, j.error, j.result->>'storageKey' AS storage_key, j.result->>'fileName' AS file_name, (j.result->>'bytes')::int AS bytes
      FROM kit_versions kv
      LEFT JOIN LATERAL (SELECT * FROM jobs WHERE kind = 'kit_build' AND payload->>'kitVersionId' = kv.id::text ORDER BY created_at DESC LIMIT 1) j ON true
      WHERE kv.kit_id = ${id} ORDER BY kv.version DESC`),
    db.execute(sql`SELECT id, name, style, status, route, reasons, svg, codepoint FROM custom_icons WHERE kit_id = ${id} AND archived_at IS NULL ORDER BY created_at`),
  ]);
  return {
    id: kit.id as string,
    name: kit.name as string,
    slug: kit.slug as string,
    embedId: kit.embed_id as string,
    allowedDomains: (kit.allowed_domains as string[]) ?? [],
    currentVersion: Number(kit.current_version),
    pinnedRelease: (kit.release_version as string) ?? null,
    versions: (vers.rows as Record<string, unknown>[]).map((v) => {
      const sel = v.selection as { items: unknown[]; customIconIds: unknown[] };
      return {
        version: Number(v.version),
        createdAt: String(v.created_at),
        contentHash: v.content_hash as string,
        formats: v.formats as string[],
        items: sel.items.length,
        customIcons: sel.customIconIds.length,
        job: v.job_id
          ? { id: v.job_id as string, status: v.status as string, error: (v.error as string) ?? null, storageKey: (v.storage_key as string) ?? null, fileName: (v.file_name as string) ?? null, bytes: (v.bytes as number) ?? null }
          : null,
      };
    }),
    customIcons: (icons.rows as Record<string, unknown>[]).map((i) => ({
      id: i.id as string,
      name: i.name as string,
      style: i.style as string,
      status: i.status as string,
      route: (i.route as string) ?? null,
      reasons: (i.reasons as string[]) ?? [],
      svg: (i.svg as string) ?? null,
      codepoint: Number(i.codepoint),
    })),
  };
}
