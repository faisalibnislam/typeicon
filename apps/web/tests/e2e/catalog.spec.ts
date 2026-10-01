import { expect, test } from "@playwright/test";

test("search, style tabs, filters and pagination live in the URL", async ({ page }) => {
  await page.goto("/icons");
  const search = page.getByRole("searchbox", { name: "Search icons" }).first();
  await search.fill("arrow");
  await expect(page).toHaveURL(/q=arrow/);
  await expect(page.getByRole("heading", { level: 1 })).toContainText("arrow");
  await page.getByRole("navigation", { name: "Style" }).getByRole("link", { name: /^Line/ }).click();
  await expect(page).toHaveURL(/style=line/);
  await page.getByRole("complementary", { name: "Filters" }).getByRole("link", { name: /^Core/ }).click();
  await expect(page).toHaveURL(/area=core/);
  await expect(page.getByRole("list", { name: "Active filters" })).toContainText("Core only");
  await expect(page.getByRole("heading", { level: 1 })).toContainText("arrow");
});

test("pagination and browser history", async ({ page }) => {
  await page.goto("/icons?style=brand");
  await page.getByRole("navigation", { name: "Pagination" }).getByRole("link", { name: "2", exact: true }).click();
  await expect(page).toHaveURL(/page=2/);
  await page.getByRole("navigation", { name: "Pagination" }).getByRole("link", { name: "3", exact: true }).click();
  await expect(page).toHaveURL(/page=3/);
  await page.goBack();
  await expect(page).toHaveURL(/page=2/);
  await expect(page).toHaveURL(/style=brand/);
  await expect(page.getByRole("link", { name: "2", exact: true })).toHaveAttribute("aria-current", "page");
});

test("brand logos have their own tab and never appear as Line/Filled/Rounded", async ({ page }) => {
  await page.goto("/icons?style=brand&q=github");
  await expect(page.getByRole("list", { name: "Icons" }).getByRole("link", { name: /^brand-github$/ })).toBeVisible();
  await page.goto("/icons?style=line&area=brands");
  await expect(page.getByText(/No icons match/)).toBeVisible();
});

test("keyboard: slash focuses search, Enter searches, results are links", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle"); // key handler attaches after hydration
  await page.keyboard.press("/");
  await expect(page.locator("#global-search")).toBeFocused();
  await page.keyboard.type("gear");
  await page.keyboard.press("Enter");
  await expect(page).toHaveURL(/\/icons\?q=gear/);
  await expect(page.getByRole("list", { name: "Icons" }).getByRole("link").first()).toBeVisible();
});

test("views: list and cheatsheet", async ({ page }) => {
  await page.goto("/icons?area=core");
  await page.getByRole("button", { name: "list", exact: true }).click();
  await expect(page).toHaveURL(/view=list/);
  await expect(page.getByRole("table")).toContainText("U+F");
  await page.getByRole("button", { name: "cheatsheet", exact: true }).click();
  await expect(page.getByRole("list", { name: "Icons cheatsheet" })).toBeVisible();
});

test("mobile filter sheet and no horizontal overflow @mobile", async ({ page }) => {
  await page.goto("/icons?q=home");
  await page.getByRole("button", { name: /Filters/ }).click();
  await expect(page.getByRole("dialog", { name: "Filters" })).toBeVisible();
  await page.getByRole("dialog").getByRole("link", { name: /^Brands [0-9,]+$/ }).click();
  await expect(page).toHaveURL(/area=brands/);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  expect(overflow).toBeLessThanOrEqual(1);
});

for (const path of ["/", "/icons/settings?style=filled", "/downloads", "/downloads/subset", "/packs/simple-icons", "/docs/web", "/licenses", "/categories/arrows"]) {
  test(`no horizontal overflow on ${path} @mobile`, async ({ page }) => {
    await page.goto(path);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);
  });
}
