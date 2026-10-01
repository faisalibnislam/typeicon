# Naming, alias and codepoint policy

## Names

- Canonical names are lowercase ASCII kebab-case: `^[a-z0-9]+(-[a-z0-9]+)*$`, 2–64 characters.
- **Core** names are bare: `home`, `arrow-right`.
- Core **variants** (base + badge) are named `<base>-<badge>`: `file-plus`, `user-off`, `bell-lock`.
- **Brand** names are prefixed `brand-`: `brand-github`. The prefix keeps logos out of the Core name space.
- Names used by the removed Tabler, Phosphor and Material Symbols packs (`tabler-…`, `phosphor-…`,
  `material-…`) are retired and not reused.
- **Custom** (kit upload) names are namespaced per kit in the database (`kit:<kitId>/<name>`), and are
  only compiled into that kit's fonts.
- Names are permanent once published. A rename is performed by deprecating the old name and adding it as
  an alias of the new canonical name. Deprecated names keep working in fonts.

## Aliases

- Aliases follow the same syntax and live in the same **global name registry** (`name_registry` table,
  unique on `(namespace, name)`), so an alias can never collide with a canonical name or another alias in
  the same namespace.
- Explicit aliases are compiled as ligatures that point at the **same output glyph** as the canonical
  name (no duplicated glyphs).
- Website search tags and synonyms are broader than aliases and are *not* compiled into fonts.

## Keywords inside the Brands font

Each font family is its own ligature namespace. In `TypeIcon Line` you type `home`. In `TypeIcon Brands`
you may type either the full name (`brand-github`) or the short name (`github`); both are explicit rules
pointing at one glyph.

## Codepoints

Codepoints are stored as integers (`int4`), never as 4-character hex strings, and allocated by the
`codepoint_assignments` table with unique constraints on `(namespace, codepoint)` and
`(namespace, subject_id)`. A codepoint is **never** reassigned to a different concept within a namespace,
even after deprecation.

| Namespace | Primary range | Notes |
|---|---|---|
| `core` | U+F0000 + n (Plane 15 Supplementary PUA-A), n < 65,534 | Shared by the Filled, Line, Rounded and Thin fonts for the same concept |
| `core` (BMP mirror) | U+E000 + n for n < 6,400 | Permanent second mapping for the first 6,400 Core concepts, for software that cannot type supplementary characters |
| `pack:brands` | U+100000 + n (Plane 16 Supplementary PUA-B), n < 61,440 | Brand logos, `TypeIcon Brands` family only |
| retired `pack:tabler`, `pack:phosphor`, `pack:material` | (were U+100000 + n) | Kept in the `retired` section of `codepoints.json`; never edited or reused |
| `kit:<id>` custom uploads | U+10F000 + n, n < 4,094 | Only inside that kit's families |

`n` is the allocation index, assigned in import order and recorded permanently. Allocation is append-only.

Consequences we document for users:

- A copied PUA character is only meaningful together with its font family. U+100000 is a brand logo in
  `TypeIcon Brands` and nothing in the Core families. (The removed packs also used U+100000 upward in their
  own families; those assignments are retired.)
- Supplementary characters are 4 bytes in UTF-8 and a surrogate pair in UTF-16. All UI copy actions use
  `String.fromCodePoint`, never `String.fromCharCode`.
- TypeIcon does **not** claim Font Awesome codepoint compatibility.

## Glyph names

Glyph names inside fonts are `u` + uppercase hex (`uF0000`, `u100000`), or `uniE000` style for BMP
mirrors when needed. Glyph order and glyph IDs change between builds and are never exposed as identifiers.

## Font family names

| Scope | Family | PostScript name |
|---|---|---|
| Core | `TypeIcon Filled`, `TypeIcon Line`, `TypeIcon Rounded`, `TypeIcon Thin` | `TypeIconFilled-Regular` … `TypeIconThin-Regular` |
| Brands | `TypeIcon Brands` (CSS family class `typeicon-brands`) | `TypeIconBrands-Regular` |
| Split packs (if needed) | `TypeIcon Line Part 2` | explicit contents listed in the manifest |
| Kits / subsets | `TypeIcon Kit <kit-slug> <hash6> Line` | `TypeIconKit<hash6>Line-Regular` |

Kit family names embed a content hash so two different subsets never share a family name (avoids OS and
browser font-cache collisions).
