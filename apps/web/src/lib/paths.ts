import "server-only";
import { existsSync } from "node:fs";
import path from "node:path";

let cached: string | undefined;

/** Repository root (directory containing pnpm-workspace.yaml), or TYPEICON_ROOT. */
export function repoRoot(): string {
  if (cached) return cached;
  if (process.env.TYPEICON_ROOT) return (cached = path.resolve(process.env.TYPEICON_ROOT));
  let dir = process.cwd();
  for (let i = 0; i < 6; i++) {
    if (existsSync(path.join(dir, "pnpm-workspace.yaml"))) return (cached = dir);
    dir = path.dirname(dir);
  }
  return (cached = process.cwd());
}
