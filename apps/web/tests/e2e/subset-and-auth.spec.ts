import { expect, test } from "@playwright/test";
import { drainWorker, signInViaForm, stateFile, unzipList } from "./helpers";

test("select icons across pages, build a subset with the real worker, download the ZIP", async ({ page }) => {
  await page.goto("/icons?area=core&q=home");
  await page.evaluate(() => localStorage.removeItem("typeicon:selection:v1"));
  await page.reload();
  const card = page.getByRole("list", { name: "Icons" }).getByRole("listitem").first();
  await card.hover();
  await card.getByRole("button", { name: /Add home/ }).click();
  await page.goto("/icons?area=core&q=bell");
  const card2 = page.getByRole("list", { name: "Icons" }).getByRole("listitem").first();
  await card2.hover();
  await card2.getByRole("button", { name: /Add bell/ }).click();
  await expect(page.getByRole("region", { name: "Selected icons" })).toContainText("2");
  await page.getByRole("link", { name: "Build subset" }).click();
  await expect(page.getByText("TypeIcon Kit Line")).toBeVisible();
  await page.getByLabel("Project name").fill(`E2E ${Date.now()}`);
  await page.getByRole("button", { name: "Build subset" }).click();
  await expect(page.getByText(/queued|running|succeeded/).first()).toBeVisible();
  drainWorker();
  const link = page.getByRole("link", { name: /Download typeicon-kit-e2e/ });
  await expect(link).toBeVisible({ timeout: 20_000 });
  const [dl] = await Promise.all([page.waitForEvent("download"), link.click()]);
  const files = unzipList(await dl.path());
  expect(files.some((f) => f.endsWith(".otf"))).toBe(true);
  expect(files.some((f) => f.endsWith("css/kit.css"))).toBe(true);
  expect(files.some((f) => f.endsWith("licenses/ATTRIBUTION.md"))).toBe(true);
  expect(files.some((f) => f.endsWith("checksums.sha256"))).toBe(true);
});

test("sign-in form works", async ({ page }) => {
  await signInViaForm(page, "other");
  await expect(page.getByRole("heading", { name: "Account" })).toBeVisible();
});

test("admin area: anonymous redirected, non-admin gets 404, admin allowed", async ({ request, browser }) => {
  const anon = await request.get("/admin", { maxRedirects: 0 });
  expect(anon.status()).toBe(307);
  expect((await request.post("/api/admin/imports", { data: {}, headers: { origin: "http://localhost:3107" } })).status()).toBe(401);
  const user = await browser.newPage({ storageState: stateFile("user") });
  expect((await user.goto("/admin"))?.status()).toBe(404);
  expect((await user.request.post("/api/admin/imports", { data: { sources: [], dryRun: true }, headers: { origin: "http://localhost:3107" } })).status()).toBe(403);
  const admin = await browser.newPage({ storageState: stateFile("admin") });
  await admin.goto("/admin");
  await expect(admin.getByRole("heading", { name: "Overview" })).toBeVisible();
});

test("collections are private to their owner", async ({ browser }) => {
  const page = await browser.newPage({ storageState: stateFile("user") });
  const res = await page.request.post("/api/collections", { data: { name: `Private ${Date.now()}` }, headers: { origin: "http://localhost:3107" } });
  expect(res.status()).toBe(201);
  const { id } = await res.json();
  const other = await browser.newPage({ storageState: stateFile("other") });
  expect((await other.goto(`/collections/${id}`))?.status()).toBe(404);
  expect((await other.request.delete(`/api/collections/${id}`, { headers: { origin: "http://localhost:3107" } })).status()).toBe(404);
  await other.close();
});
