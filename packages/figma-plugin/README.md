# TypeIcon for Figma (`@typeicon/figma-plugin`)

> **Status: unverified, unpublished.**
> This plugin has **not** been published to the Figma Community and has **not**
> been run inside Figma by its author (Figma could not be run in the
> environment where it was written). Build, typecheck and Node tests pass, and the UI
> was smoke-tested in a regular browser against the local catalog API, but
> everything that touches the `figma` API (SVG import, sizing, placement,
> plugin data, client storage, manifest acceptance) still needs a manual
> pass in Figma desktop using the checklist below.

The plugin searches the same catalog as the TypeIcon website
(`GET /api/icons`) and inserts icons as **editable SVG vectors** via
`figma.createNodeFromSvg`. No fonts need to be installed.

## Layout

| File | Purpose |
| --- | --- |
| `manifest.json` | Figma plugin manifest (`main: dist/code.js`, `ui: dist/ui.html`). |
| `src/code.ts` | Main thread: validates insert messages, creates the vector, sizes/places/selects it, writes plugin data, stores settings in `figma.clientStorage`. |
| `src/ui.html`, `src/ui.ts` | Plugin UI (iframe): search, filters, results grid, settings. |
| `src/shared.ts` | Pure helpers shared by both sides and the tests (validation, URL building, response parsing, scaling). |
| `src/messages.ts` | Types for UI ↔ main-thread messages. |
| `build.mjs` | esbuild build: `dist/code.js` + `dist/ui.html` (UI JS inlined). |
| `test/` | Node tests (`node:test`) for validation and for the built artifacts. |

## Build

From the repo root:

```sh
pnpm install
pnpm --filter @typeicon/figma-plugin build       # production: default API https://typeicon.net
pnpm --filter @typeicon/figma-plugin build:dev   # dev: default API http://localhost:3107
pnpm --filter @typeicon/figma-plugin typecheck   # tsc --noEmit (main thread + UI configs)
pnpm --filter @typeicon/figma-plugin test        # run after a build
```

`dist/` is git-ignored (`packages/*/dist/`), so build before loading the plugin.

## Load it in Figma desktop

1. Build it (`build:dev` if you want to use a local catalog).
2. In the Figma **desktop app**, open a design file.
3. Go to **Plugins → Development → Import plugin from manifest…** and pick
   `packages/figma-plugin/manifest.json`.
4. Run it from **Plugins → Development → TypeIcon**.

The manifest `id` (`typeicon-local-dev`) is a placeholder for local development.
Figma assigns a real id when a plugin is created or published under an
account. Replace it then. Publishing is out of scope for now.

## Pointing it at a local dev server

1. Start the web app so the API is on `http://localhost:3107`
   (`pnpm dev` from the repo root; check with
   `curl -s 'http://localhost:3107/api/icons?q=home&style=line'`).
2. Build with `build:dev` so the default API base is `http://localhost:3107`.
   With a production build you can also open **⚙ Settings**, enter
   `http://localhost:3107`, and click **Save**. The value is stored per user in
   `figma.clientStorage`.
3. Only origins listed in the manifest can be used:
   `https://typeicon.net` (`allowedDomains`) and `http://localhost:3107`
   (`devAllowedDomains`, which applies during development only). The settings
   field rejects anything else. Figma would block it with a CSP error anyway. To
   use another port, update `manifest.json`, `ALLOWED_API_ORIGINS` in
   `src/shared.ts` and the CSP `connect-src` in `src/ui.html` together. A test
   checks that these three agree.

The production origin `https://typeicon.net` is **not live yet**. Until it
is, a production build shows a "could not reach" error unless you switch to the
local server.

## Using it

- Type to search (debounced). **Enter** in the search box runs the search now,
  or inserts the selected icon if the query is unchanged.
- **Style**: All / Filled / Line / Rounded / Thin. **Source**: All sources / Core / Brands
  (sends `area=all|core|brands`). Brand logos have one style and only appear under All.
- Grid: click to select, double-click to insert. Arrow keys, Home and End move
  the selection. **Enter** or **Space** inserts it. **↑** from the first row returns to search.
  The footer shows the name, style, source and license.
- Icons whose SVG is `null` for the chosen style are shown as **"unavailable in
  this style"** and can't be inserted. The plugin never substitutes another style.
- **Load more** fetches the next page (48 per page).
- **Custom color**: when checked, `currentColor` is replaced with the chosen
  hex color. Otherwise it is replaced with black (`#000000`) so the vector is visible.

### What an insert does

1. The main thread validates `{ svg, name, style, source, license, id, color }`.
   The SVG must be a single `<svg>…</svg>` document of at most 100,000 characters
   with no `<script>`, `<foreignObject>`, `<image>`, `<use>`, event handlers,
   `javascript:`, DOCTYPE/entities, non-fragment `href`s or external `url()`s.
   Metadata strings are length- and charset-checked.
2. `currentColor` is replaced with the chosen color or black, then
   `figma.createNodeFromSvg(svg)` runs.
3. The frame is named `typeicon/<style>/<name>` and rescaled uniformly so its
   longest side is 24px (aspect ratio is kept and strokes scale). Then the aspect ratio is locked.
4. It is placed 16px to the right of the current selection, or centered in
   the viewport when nothing is selected. It is then selected.
5. Plugin data is written with `setPluginData`: key `typeicon` holds JSON
   `{ name, style, source, license, iconId, variantId: "<id>:<style>", color }`.
   The individual keys are `name`, `style`, `source`, `license` and `variantId`.
6. `figma.notify` confirms the insert, or reports the error.

## Security notes

- **Network**: requests go only from the UI iframe to the configured API base.
  The manifest allow-lists the domains. The UI also sets its own CSP
  (`default-src 'none'; connect-src https://typeicon.net http://localhost:3107; …`).
  Fetches use `credentials: 'omit'`. The only data sent is the search query and
  filters. No analytics, no other endpoints.
- **Untrusted markup**: API SVGs are never assigned to `innerHTML`. Previews are
  parsed with `DOMParser` and rebuilt with `createElementNS`, keeping only
  allow-listed SVG elements and attributes (`url()` only as `url(#id)`).
- **Main thread**: re-validates every message (it doesn't trust the UI), with a
  bounded size. No `eval` or `new Function` in either bundle (a test checks this).
- Network failures, timeouts (15s), non-2xx responses and malformed JSON are
  shown as an error state in the UI.

## Manual test checklist (to run in Figma desktop)

- [ ] `Import plugin from manifest…` accepts `manifest.json` without warnings
      (`api`, `editorType`, `documentAccess: "dynamic-page"`, `networkAccess`).
- [ ] With `build:dev` and the local server running, the grid loads on open.
      The UI follows Figma light/dark theme (`themeColors: true`).
- [ ] Search "home" and check the results update after typing stops. Test the
      Filled/Line/Rounded/Thin and source filters.
- [ ] Load more appends the next page. A nonsense query shows the empty state.
- [ ] Stop the local server and check that an error state appears and the plugin doesn't crash.
- [ ] Settings: `https://evil.example` is rejected. `http://localhost:3107` saves and persists
      after closing and reopening the plugin. Reset restores the default.
- [ ] Insert a Core line icon (24×24 viewBox) with nothing selected. The node appears
      at the viewport center, 24×24, named `typeicon/line/home`, selected,
      with black strokes, editable vector paths and a notification.
- [ ] Insert a brand logo (e.g. `brand-github`, filled artwork). The longest side is 24px and
      the icon isn't clipped or offset.
- [ ] Insert with an object selected. The icon is placed 16px to the right of it.
- [ ] Custom color: the inserted fills/strokes use the chosen hex.
- [ ] Keyboard only: search, ↓ into the grid, arrows, Enter inserts.
- [ ] Plugin data: in another dev plugin or the console, `node.getPluginData('typeicon')`
      returns the JSON above. (Plugin data is private to this plugin id.)
- [ ] Works on a non-first page of a multi-page file (`dynamic-page` access).

## Future work: private collections / account linking (not implemented)

Private collections and account linking are out of scope. If they are added,
use a device-authorization style flow (like OAuth 2.0 Device Authorization Grant,
RFC 8628) so the plugin never handles the user's password:

1. The plugin calls `POST /api/figma/device-code` and gets back a short
   `user_code`, an opaque `device_code`, `verification_uri`, `expires_in`
   (~10 min) and `interval`.
2. The UI shows the `user_code` and opens `verification_uri` with
   `figma.openExternal`. The user signs in on typeicon.net in their
   normal browser and approves "Figma plugin" access, with a narrow read-only scope for collections.
3. The plugin polls `POST /api/figma/token` with the `device_code` at the given
   interval until it gets a short-lived access token (for example 1 hour) and a
   rotating refresh token. It stops on `expired_token` or `access_denied`.
4. Tokens are stored in `figma.clientStorage` (per user and plugin, but not
   encrypted), are sent only to the configured API base in an `Authorization` header,
   and are never put in URLs or plugin data. The server binds tokens to the scope,
   rotates refresh tokens on use, rate-limits polling, and lets the user
   revoke the "Figma plugin" session from account settings. Sign-out deletes the
   stored tokens and calls a revoke endpoint.
5. Private-collection responses would need `Cache-Control: no-store`, and
   `Access-Control-Allow-Origin: *` without cookies. Auth would be header-only,
   because the plugin iframe has a `null` origin.
