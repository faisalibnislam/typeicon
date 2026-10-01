import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

for (const path of ["/", "/icons?q=home", "/icons/home?style=line", "/downloads", "/downloads/subset", "/docs/accessibility", "/packs/simple-icons", "/licenses"]) {
  test(`no serious accessibility violations on ${path}`, async ({ page }) => {
    await page.goto(path);
    const r = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa"]).analyze();
    const serious = r.violations.filter((v) => v.impact === "serious" || v.impact === "critical");
    expect(serious.map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`)).toEqual([]);
  });
}

test("dark theme toggle persists", async ({ page }) => {
  await page.goto("/");
  const btn = page.getByRole("button", { name: /theme/ });
  await btn.click(); // system -> light
  await btn.click(); // light -> dark
  await expect(page.locator("html")).toHaveClass(/dark/);
  await page.reload();
  await expect(page.locator("html")).toHaveClass(/dark/);
  await page.evaluate(() => localStorage.setItem("theme", "system"));
});

test("no serious accessibility violations with the icon modal open", async ({ page }) => {
  await page.goto("/icons?q=home&area=core");
  await page.waitForLoadState("networkidle");
  await page.getByRole("list", { name: "Icons" }).getByRole("link", { name: /^home$/ }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  const r = await new AxeBuilder({ page }).include("[role=dialog]").withTags(["wcag2a", "wcag2aa", "wcag21aa"]).analyze();
  const serious = r.violations.filter((v) => v.impact === "serious" || v.impact === "critical");
  expect(serious.map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`)).toEqual([]);
});
