# TypeIcon developer packages

> **Local workspace packages only.** The `@typeicon/*` names below are pnpm
> workspace package names. No npm scope has been registered and nothing is
> published; every package is `"private": true`. Consume them inside this
> monorepo with `"<name>": "workspace:*"`.

All generated content comes from a validated release (by default the newest
`dist/releases/<version>/typeicon-release/`, currently 0.2.0) and lands in git-ignored
`generated/` or `dist/` directories. Only the hand-written sources
(`package.json`, `src/`, catalog `index.js`/`index.d.ts`, this README) are committed.

| Package | Directory | Contents |
| --- | --- | --- |
| `@typeicon/catalog` | `packages/catalog` | `icons.json`, `families.json`, `manifest.json`, `names.json`, one JSON per icon, TypeScript types and lookup helpers |
| `@typeicon/icons-svg` | `packages/icons-svg` | Sanitized SVG files and per-source, per-style sprites |
| `@typeicon/icons-webfont` | `packages/icons-webfont` | woff2/woff webfonts and CSS (class + ligature usage) |
| `@typeicon/react` | `packages/icons-react` | One typed React component per icon style |
| `@typeicon/vue` | `packages/icons-vue` | One typed Vue 3 component per icon style |
| `@typeicon/scripts` | `packages/scripts` | `generate.mjs` and `verify.mjs` (private tooling) |

Each package also ships the release licences (`licenses/ATTRIBUTION.md`, `NOTICE`
and the per-source licence texts). TypeIcon Core is
`LicenseRef-TypeIcon-Core-Draft` until the owner chooses terms. Brand logos
come from Simple Icons (collection CC0-1.0); some logos carry their own licence,
listed in `licenses/simple-icons/PER-ICON-LICENSES.md`. Brand logos are
trademarks of their owners. The SPDX id of each icon is in `icons.json` and in
the doc comment of every generated module.

## Import patterns

Core icons have bare names; brand logos are prefixed with `brand-`.

```ts
// React, Core: @typeicon/react/<style>/<name>
import Home from '@typeicon/react/line/home';
import Search from '@typeicon/react/rounded/search';
import FilePlus from '@typeicon/react/filled/file-plus';  // a variant (base + badge)
// React, brand logos: @typeicon/react/brands/<name>
import BrandGithub from '@typeicon/react/brands/brand-github';

// Vue: identical subpaths
import VueHome from '@typeicon/vue/line/home';

// Build your own icon from a compact node array
import { createIcon } from '@typeicon/react'; // root export: createIcon + types only

// SVG files and sprites (paths mirror icons.json `styles.<style>.svg`)
import homeUrl from '@typeicon/icons-svg/svg/typeicon-core/line/home.svg';
// shorthand: '@typeicon/icons-svg/typeicon-core/line/home.svg'
// brands:    '@typeicon/icons-svg/svg/simple-icons/brand/brand-github.svg'
// sprites:   '@typeicon/icons-svg/sprites/typeicon-core-line.svg', '.../sprites/simple-icons-brand.svg'

// Webfonts + CSS (url()s are relative: ../webfonts/*)
import '@typeicon/icons-webfont/typeicon.css';                // Core families + .typeicon base classes
import '@typeicon/icons-webfont/css/typeicon-simple-icons.css'; // TypeIcon Brands (needs the base CSS)

// Metadata
import { getIcon, iconImportPath } from '@typeicon/catalog';
const icon = await getIcon('brand-github');       // loads dist/icon/brand-github.json only
iconImportPath(icon, 'brand', 'vue');              // '@typeicon/vue/brands/brand-github'
// Full data, when you really need it:
// import icons from '@typeicon/catalog/icons.json' with { type: 'json' };
```

Core styles are `filled`, `line`, `rounded` and `thin`. Every published Core icon has
Filled, Line and Rounded; `thin` exists only for icons whose Thin differs from Line
(for example `@typeicon/react/thin/search`). Brand logos have the single style `brand` (see `names.json` or
`icons.json`). There is intentionally **no barrel**: the root
`@typeicon/react` / `@typeicon/vue` export exposes only `createIcon` and
types, and both packages are `"sideEffects": false`, so a bundle contains only
the icons you import. A JSON list of all subpaths is at
`@typeicon/react/subpaths.json` (for tooling, not for bundling).

`getIcon(name)` uses a dynamic `import()` of one JSON file. That is ideal in
Node; in a bundler, prefer a static import of
`@typeicon/catalog/icon/<name>.json` so the bundler does not enumerate
every icon file.

## Component props

| Prop | Default | Notes |
| --- | --- | --- |
| `size` | `24` | Number (px) or CSS length. Sets `height`; `width` follows the viewBox aspect ratio (all current viewBoxes are square). The viewBox itself is never changed. |
| `color` | none | Sets the SVG `color`; artwork paints with `currentColor`, so it also inherits text colour. |
| `strokeWidth` | none | Overrides the root `stroke-width` on stroke-based icons only (Core line/rounded/thin). In React, fill-based icons are typed without this prop; in Vue it is accepted but ignored. |
| `title` | none | Accessible name (see below). |
| `className` / `class`, `style`, any SVG attribute | none | Passed through to the `<svg>`. |
| `ref` | none | React: forwarded to the `<svg>` (`forwardRef`, works in React 18 and 19). Vue: use a template ref and `$el`. |

Artwork is rendered from a compact node array (`[["path", {d: "…"}], …]`) with
`React.createElement` / Vue `h()`, never `dangerouslySetInnerHTML` / `innerHTML`.

## Accessibility

- **Decorative (default)**: no `title`, `aria-label` or `aria-labelledby`:
  renders `aria-hidden="true"` and `focusable="false"`.
- **`title="…"`**: renders `role="img"`, a `<title>` child with a stable
  unique id (React `useId`, Vue `useId`; SSR-safe) and `aria-labelledby`
  pointing at it.
- **`aria-label` / `aria-labelledby`**: renders `role="img"` without a `<title>`.
- Explicit props win: e.g. `aria-hidden={false}` overrides the default.

## Generate and verify

```sh
pnpm install                              # from the repo root
node packages/scripts/generate.mjs        # ≈10–15 s; --release <dir>, --skip-tsc, --quiet
node packages/scripts/verify.mjs          # exits non-zero on any failure
```

`generate.mjs` uses only Node built-ins (plus one `tsc` spawn per framework
package to compile `src/` → `dist/`). It verifies each SVG against the
release `checksums.sha256`, parses it strictly (allow-listed elements and
attributes only), wipes and rewrites every generated tree, and produces
byte-identical output on every run.

`verify.mjs` checks the generated structure and exports maps, catalog helpers,
`tsc --noEmit` on `examples/react-sample` and `examples/vue-sample` (including
`@ts-expect-error` negatives), production esbuild bundles of both samples with
tree-shaking assertions (imported icon path data present; 20 seeded-random
non-imported icons absent; icon payload < 15 KB with the framework external),
and SSR output via `react-dom/server` and `@vue/server-renderer`.

The samples can also be built by hand: `pnpm --filter @typeicon/example-react-sample build`
(or `build:icons-only`), and likewise for `@typeicon/example-vue-sample`.
