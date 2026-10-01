import { readFileSync } from "node:fs";
import { expect, test } from "@playwright/test";

test("detail page: style in URL, real SVG and PNG downloads, glyph facts", async ({ page, context }) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"]);
  await page.goto("/icons/home?style=line");
  await expect(page.getByRole("heading", { level: 1, name: "home" })).toBeVisible();
  await expect(page.getByText("TypeIcon Line", { exact: true })).toBeVisible();
  await expect(page.getByText(/U\+F0023/)).toBeVisible();
  await page.getByRole("radio", { name: "Rounded" }).first().click();
  await expect(page).toHaveURL(/style=rounded/);
  await expect(page.getByText("TypeIcon Rounded", { exact: true })).toBeVisible();

  const [svgDl] = await Promise.all([page.waitForEvent("download"), page.getByRole("button", { name: "Download SVG" }).click()]);
  expect(svgDl.suggestedFilename()).toBe("home-rounded.svg");
  const svg = readFileSync(await svgDl.path(), "utf8");
  expect(svg).toMatch(/^<svg /);
  expect(svg).toContain('xmlns="http://www.w3.org/2000/svg"');
  expect(svg).toContain('width="24" height="24"');
  expect(svg).toContain('stroke-linecap="round"');
  expect(svg).not.toMatch(/script|onload|href/i);

  await page.getByLabel("PNG size").selectOption("128");
  const [pngDl] = await Promise.all([page.waitForEvent("download"), page.getByRole("button", { name: "PNG" }).click()]);
  expect(pngDl.suggestedFilename()).toBe("home-rounded-128.png");
  const png = readFileSync(await pngDl.path());
  expect(png.subarray(1, 4).toString()).toBe("PNG");
  expect(png.readUInt32BE(16)).toBe(128); // IHDR width
  expect(png.readUInt32BE(20)).toBe(128);
  expect(png[25]).toBe(6); // colour type RGBA: transparent background

  await page.getByRole("button", { name: "Copy glyph", exact: true }).click();
  const glyph = await page.evaluate(() => navigator.clipboard.readText());
  expect(glyph.codePointAt(0)).toBe(0xf0023);
  expect(glyph.length).toBe(2); // one supplementary character = surrogate pair in UTF-16, not truncated
  await expect(page.getByRole("status").filter({ hasText: "Copied" })).toBeVisible();
});

test("brand logos have one style, their own font and a trademark notice", async ({ page }) => {
  await page.goto("/icons/brand-github?style=line");
  await expect(page.getByRole("radio", { name: "Line" })).toHaveCount(0);
  await expect(page.getByRole("radio", { name: "Brand" })).toBeChecked();
  await expect(page.getByText("TypeIcon Brands", { exact: true })).toBeVisible();
  await expect(page.getByText(/trademark of its owner/).first()).toBeVisible();
});

test("variants link to their base design", async ({ page }) => {
  await page.goto("/icons/bell-plus?style=line");
  await expect(page.getByText(/Variant of/)).toContainText("bell");
  await expect(page.getByText("TypeIcon Line", { exact: true })).toBeVisible();
});

test("canonical SVG endpoint is sanitized and sandboxed", async ({ request }) => {
  const r = await request.get("/api/icons/settings/svg?style=filled");
  expect(r.status()).toBe(200);
  expect(r.headers()["content-type"]).toContain("image/svg+xml");
  expect(r.headers()["content-security-policy"]).toContain("sandbox");
  expect(await request.get("/api/icons/does-not-exist/svg").then((x) => x.status())).toBe(404);
});
