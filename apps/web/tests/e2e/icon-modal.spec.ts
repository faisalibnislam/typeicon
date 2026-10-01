import { expect, test } from "@playwright/test";

test("clicking an icon in the grid opens it in a modal with a shareable URL", async ({ page, context }) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"]);
  await page.goto("/icons?q=arrow&area=core");
  await page.waitForLoadState("networkidle");
  const grid = page.getByRole("list", { name: "Icons" });
  const order = await grid.locator("a[href^='/icons/']").evaluateAll((as) => as.map((a) => new URL((a as HTMLAnchorElement).href).pathname.split("/").pop()!));
  const next = order[order.indexOf("arrow-down") + 1];
  await grid.getByRole("link", { name: /^arrow-down$/ }).click();

  const dialog = page.getByRole("dialog");
  await expect(dialog).toBeVisible();
  await expect(page).toHaveURL(/\/icons\/arrow-down\?style=line$/);
  // Results stay underneath (hidden from assistive tech while the dialog is open).
  await expect(page.getByRole("list", { name: "Icons", includeHidden: true })).toBeAttached();
  await expect(dialog.getByText("TypeIcon Line", { exact: true })).toBeVisible();

  // Clicking the name copies it.
  await dialog.getByRole("button", { name: "arrow-down", exact: true }).click();
  await expect(dialog.getByRole("status").filter({ hasText: "Copied" })).toBeVisible();
  expect(await page.evaluate(() => navigator.clipboard.readText())).toBe("arrow-down");

  // Arrow keys step through the visible results; Escape returns to the search.
  await page.keyboard.press("ArrowRight");
  await expect(page).toHaveURL(new RegExp(`/icons/${next}\\?`));
  await expect(dialog.getByRole("button", { name: next, exact: true })).toBeVisible();
  await page.keyboard.press("ArrowLeft");
  await expect(page).toHaveURL(/\/icons\/arrow-down/);
  await page.keyboard.press("Escape");
  await expect(dialog).toBeHidden();
  await expect(page).toHaveURL(/\/icons\?q=arrow&area=core$/);
});

test("modal closes with the close button and browser Back; style switching stays in the modal", async ({ page }) => {
  await page.goto("/icons?q=home&area=core");
  await page.waitForLoadState("networkidle");
  await page.getByRole("list", { name: "Icons" }).getByRole("link", { name: /^home$/ }).click();
  const dialog = page.getByRole("dialog");
  await expect(dialog).toBeVisible();
  await dialog.getByRole("radio", { name: "Filled" }).click();
  await expect(page).toHaveURL(/\/icons\/home\?style=filled/);
  await expect(dialog).toBeVisible();
  await dialog.getByRole("button", { name: "Close" }).click();
  await expect(dialog).toBeHidden();
  await expect(page).toHaveURL(/\/icons\?q=home&area=core$/);
  await page.goForward();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.goBack();
  await expect(page.getByRole("dialog")).toBeHidden();
});

test("direct visits and refresh render the full icon page, where the name also copies", async ({ page, context }) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"]);
  await page.goto("/icons/settings?style=line");
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(page.getByRole("heading", { level: 1 })).toContainText("settings");
  await page.getByRole("button", { name: "settings", exact: true }).click();
  expect(await page.evaluate(() => navigator.clipboard.readText())).toBe("settings");

  await page.goto("/icons?q=settings&area=core");
  await page.waitForLoadState("networkidle");
  await page.getByRole("list", { name: "Icons" }).getByRole("link", { name: /^settings$/ }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.reload();
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(page.getByRole("heading", { level: 1 })).toContainText("settings");
});
