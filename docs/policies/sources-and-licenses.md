# Sources and licenses policy

## Principles

1. **Pin everything.** Each source is recorded in `assets/sources/manifest.json` with upstream URL, author,
   copyright, version, distribution package + tarball URL + SRI integrity (sha512), retrieval date, SPDX license,
   license file path, notices, attribution text, reserved font names, permissions and modification history.
   Importers refuse a tarball whose integrity does not match.
2. **Keep originals immutable.** Tarballs are cached in `.cache/tarballs/`, extracted read-only into
   `.cache/sources/<slug>/<version>/` with traversal, symlink and size protections. Every variant records the
   upstream file path and its sha256.
3. **Never relicense third-party artwork.** Brand logos keep their own license (collection or per-logo). Release archives, subset
   ZIPs and fonts carry the relevant license texts (`licenses/<source>/…`), `ATTRIBUTION.md` and `NOTICE`, and the
   font `name` table (IDs 0, 13, 14) states the artwork license. Fonts are built per source, so license groups
   never mix inside one font file.
4. **Separate permissions.** `permissions.redistributeSvg`, `permissions.modify`, `permissions.buildFonts` and
   `permissions.repackageUpstreamFonts` are tracked separately. TypeIcon compiles its own fonts from SVG; it
   does not repackage upstream font files.
5. **Quarantine by default.** Unknown or incompatible licenses are not imported. For per-logo licenses this means
   share-alike, non-commercial, GPL/AGPL, MPL and custom-licensed brand logos are quarantined. A source without an approved
   review stays `pending` (not public). Approvals are recorded with who/when/note.
6. **Rights survive monetisation.** Paid service tiers can change capacity (builds, hosting, collaboration),
   never the terms under which downloaded third-party artwork may be used.

## Current sources

| Source | Area | Version | License | Notes |
|---|---|---|---|---|
| TypeIcon Core | core | 0.1.0 | LicenseRef-TypeIcon-Core-Draft | Original artwork; **owner must choose public terms** before public redistribution |
| Brand logos (Simple Icons) | brands | 16.33.0 (npm `simple-icons`) | CC0-1.0 collection; per-logo licenses recorded | Logos are trademarks of their owners; see `assets/sources/licenses/simple-icons/DISCLAIMER.md`. Per-logo licenses and guideline links are recorded; incompatible ones are quarantined |

Tabler Icons, Phosphor Icons and Material Symbols were imported until 2026-09-30 and then removed by owner
decision (`docs/decisions.md`, entry 19).

## Explicitly excluded

- Font Awesome Pro / Pro+ assets (commercial license; not redistributable). Font Awesome Free is not imported
  either; it is used only as a functional reference. No Font Awesome codepoint compatibility is claimed.
- Any collection discovered through Iconify whose individual license has not been verified. Iconify's own
  software license does not cover every icon set it distributes.
- Purchased icon subscriptions: a subscription does not by itself grant the right to build a competing
  downloadable library.

## Adding a source

1. Verify the license and version from the upstream repository (not only the package metadata).
2. Add a manifest entry with integrity, styles mapping and notices; copy the license text into
   `assets/sources/licenses/<slug>/`.
3. Write an adapter in `tools/importers/src/typeicon_import/adapters.py`.
4. `typeicon-import build --source <slug> --dry-run`, review the report, then import and approve in `/admin/packs`.
