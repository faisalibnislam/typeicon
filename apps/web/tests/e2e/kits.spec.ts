import { expect, test } from "@playwright/test";
import { drainWorker, stateFile } from "./helpers";

const ORIGIN = { origin: "http://localhost:3107" };
const EVIL =
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" onload="alert(1)"><script>alert(2)</script>' +
  '<a href="https://evil.example"><path d="M1 1h2v2z"/></a><foreignObject><div>x</div></foreignObject>' +
  '<path d="M4 4h16v16H4z" fill="currentColor"/></svg>';
const GOOD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="8"/><path d="M8 12h8"/></svg>';

test("kits: sanitized private uploads, ownership isolation, private builds and cache scope", async ({ browser, request }) => {
  const owner = await browser.newPage({ storageState: stateFile("user") });
  const other = await browser.newPage({ storageState: stateFile("other") });
  const stamp = Date.now().toString(36);

  const kit = await (await owner.request.post("/api/kits", { data: { name: `E2E kit ${stamp}` }, headers: ORIGIN })).json();
  expect(kit.id).toBeTruthy();

  // Name collisions with Core names are refused; non-SVG uploads are refused before storage.
  expect((await owner.request.post(`/api/kits/${kit.id}/icons`, { data: { name: "home", style: "line", svg: GOOD }, headers: ORIGIN })).status()).toBe(409);
  expect((await owner.request.post(`/api/kits/${kit.id}/icons`, { data: { name: "e2e-bad", style: "line", svg: "<html><body>definitely not an svg document</body></html>" }, headers: ORIGIN })).status()).toBe(422);

  const evil = await owner.request.post(`/api/kits/${kit.id}/icons`, { data: { name: `e2e-evil-${stamp}`, style: "filled", svg: EVIL }, headers: ORIGIN });
  const good = await owner.request.post(`/api/kits/${kit.id}/icons`, { data: { name: `e2e-mark-${stamp}`, style: "line", svg: GOOD }, headers: ORIGIN });
  expect(evil.status()).toBe(202);
  expect(good.status()).toBe(202);

  // Other users can neither read nor write this kit; anonymous requests need a session; cross-origin writes are refused.
  expect((await other.request.get(`/api/kits/${kit.id}`)).status()).toBe(404);
  expect((await other.request.post(`/api/kits/${kit.id}/icons`, { data: { name: "e2e-x", style: "line", svg: GOOD }, headers: ORIGIN })).status()).toBe(404);
  expect((await request.get(`/api/kits/${kit.id}`)).status()).toBe(401);
  expect((await owner.request.post("/api/kits", { data: { name: "x" }, headers: { origin: "https://evil.example" } })).status()).toBe(403);

  drainWorker();
  const detail = await (await owner.request.get(`/api/kits/${kit.id}`)).json();
  const evilIcon = detail.customIcons.find((c: { name: string }) => c.name.startsWith("e2e-evil"));
  const goodIcon = detail.customIcons.find((c: { name: string }) => c.name.startsWith("e2e-mark"));
  expect(evilIcon.status).toBe("ready");
  expect(evilIcon.svg).not.toMatch(/script|onload|href|foreignObject|evil\.example/i);
  expect(evilIcon.reasons.join(" ")).toMatch(/removed: .*<script>/);
  expect(goodIcon.route).toBe("font");

  const ver = await owner.request.post(`/api/kits/${kit.id}/versions`, {
    data: { items: [], customIconIds: [goodIcon.id], formats: ["otf", "woff2", "css", "svg"] },
    headers: ORIGIN,
  });
  expect(ver.status()).toBe(202);
  drainWorker();
  const built = await (await owner.request.get(`/api/kits/${kit.id}`)).json();
  const job = built.versions[0].job;
  expect(job.status).toBe("succeeded");
  expect(job.storageKey).toMatch(/^builds\/private\//);
  // Private artifacts: owner only.
  expect((await owner.request.get(`/api/files/${job.storageKey}`)).status()).toBe(200);
  expect((await other.request.get(`/api/files/${job.storageKey}`)).status()).toBe(404);
  expect((await request.get(`/api/files/${job.storageKey}`)).status()).toBe(404);
  // Another user's version of a kit can never use this user's custom icons.
  const otherKit = await (await other.request.post("/api/kits", { data: { name: `Other ${stamp}` }, headers: ORIGIN })).json();
  if (otherKit.id) {
    const steal = await other.request.post(`/api/kits/${otherKit.id}/versions`, { data: { items: [], customIconIds: [goodIcon.id], formats: ["otf"] }, headers: ORIGIN });
    expect([409, 422]).toContain(steal.status());
    await other.request.delete(`/api/kits/${otherKit.id}`, { headers: ORIGIN });
  }
  await owner.request.delete(`/api/kits/${kit.id}`, { headers: ORIGIN });
});
