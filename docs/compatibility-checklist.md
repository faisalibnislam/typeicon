# Manual compatibility checklist

Automated checks prove the fonts are valid and shape correctly in HarfBuzz and in a Chromium-based browser.
They do **not** prove every desktop application behaves the same. Record results here. Never mark an entry
"Pass" without running it.

Test file: install `desktop/TypeIconLine-Regular.otf`, `TypeIconFilled-Regular.otf`,
`TypeIconRounded-Regular.otf` (and `TypeIconThin-Regular.otf` if you want to test Thin) from `dist/releases/<version>/typeicon-release/` (or the downloaded archive).

## Standard test script

1. Remove any older TypeIcon fonts, install the OTF files, restart the application.
2. Create a text layer and set the family to **TypeIcon Line** (exact name).
3. Make sure ligatures are enabled (Figma: Type details → Details → Letterforms → Ligatures).
4. Type `home search settings user arrow-right`. Expected: five icons separated by spaces.
5. Type `hom`. Expected: the letters `hom` in the fallback letterforms (not an icon, not blank).
6. Type `arrow`, then `arrow-right`, then `arrow-right-circle`. Expected: three different icons.
7. Type `house` and `gear`. Expected: the home and settings icons (aliases).
8. Switch the family to **TypeIcon Filled**, then **TypeIcon Rounded**, then **TypeIcon Thin**. Expected: same keywords, new style (Thin shows plain text for icons that have no distinct Thin).
9. Paste a copied glyph (U+F0023 from the website "Copy glyph" button) into a TypeIcon Line layer. Expected: home icon.
10. (Figma) Flatten / outline the text. Expected: vector shapes that no longer need the font.

## Matrix

| Application | Version | OS | Result | Date | Tester | Notes |
|---|---|---|---|---|---|---|
| HarfBuzz (uharfbuzz 0.56.2) | n/a | macOS 27 | Pass (automated) | 2026-09-30 | CI | Every keyword and alias in every family |
| Chromium (Claude desktop browser pane) | n/a | macOS 27 | Pass (manual demo + Playwright) | 2026-09-30 | automated | WOFF2 + `liga` |
| Figma desktop | | macOS | **Untested** | | | |
| Figma desktop | | Windows | **Untested** | | | |
| Figma in browser (with font installer) | | macOS | **Untested** | | | |
| Sketch | | macOS | **Untested** | | | |
| Adobe Illustrator | | macOS / Windows | **Untested** | | | OpenType panel ligatures |
| Affinity Designer | | macOS | **Untested** | | | |
| Apple Keynote / Pages | | macOS | **Untested** | | | |
| Microsoft Word / PowerPoint | | macOS / Windows | **Untested** | | | Word needs ligatures enabled in Font → Advanced |
| Safari | | macOS | **Untested** | | | |
| Firefox | | macOS | **Untested** | | | |
| macOS Font Book installation | | macOS | **Untested** | | | |
| Windows font installation | | Windows 11 | **Untested** | | | |
| TypeIcon Figma plugin | | Figma desktop | **Untested** | | | Source in `packages/figma-plugin` |
