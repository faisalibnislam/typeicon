import { afterAll, describe, expect, it } from "vitest";
import { pool } from "@/db";
import { parseSearchParams, searchIcons } from "@/lib/search";

afterAll(async () => pool.end());
const run = (raw: Record<string, string>) => searchIcons(parseSearchParams(raw));

describe("search ranking (test database)", () => {
  it("ranks the exact Core name first; brand logos are found by brand name", async () => {
    expect((await run({ q: "home" })).items[0].name).toBe("home");
    expect((await run({ q: "github" })).items[0].name).toBe("brand-github");
  });
  it("resolves aliases and synonyms", async () => {
    expect((await run({ q: "gear" })).items.slice(0, 3).map((i) => i.name)).toContain("settings");
    expect((await run({ q: "magnify" })).items[0].name).toBe("search");
    expect((await run({ q: "house" })).items.slice(0, 4).map((i) => i.name)).toContain("home");
  });
  it("finds icons by what they are used for, not only by name (keywords and context)", async () => {
    const names = async (q: string, n = 8) => (await run({ q, area: "core" })).items.slice(0, n).map((i) => i.name);
    expect(await names("rubbish")).toContain("trash");
    expect(await names("shopping cart")).toContain("cart");
    expect(await names("log out")).toEqual(expect.arrayContaining([expect.stringMatching(/logout|log-out|sign-out/)]));
    expect(await names("summation")).toContain("sigma");
  });
  it("drops filler words and matches singular forms", async () => {
    expect((await run({ q: "icon for trash" })).items[0].name).toBe("trash");
    expect((await run({ q: "users" })).items.slice(0, 5).map((i) => i.name)).toContain("user");
  });
  it("lists a drawn icon before its badge variants", async () => {
    const items = (await run({ q: "file", area: "core", per: "96" })).items.map((i) => i.name);
    expect(items[0]).toBe("file");
    // file-pdf is drawn on its own; file-plus is the file icon with a badge
    expect(items.indexOf("file-pdf")).toBeGreaterThan(-1);
    expect(items.indexOf("file-pdf")).toBeLessThan(items.indexOf("file-plus"));
  });
  it("finds variants by the action people type", async () => {
    expect((await run({ q: "add user" })).items.slice(0, 5).map((i) => i.name)).toContain("user-plus");
  });
  it("tolerates a typo", async () => {
    expect((await run({ q: "setings" })).items[0].name).toBe("settings");
  });
  it("handles multi-word queries and hyphenated names", async () => {
    expect((await run({ q: "arrow right" })).items[0].name).toBe("arrow-right");
  });
  it("returns an empty, well-formed result for nonsense and hostile input", async () => {
    const r = await run({ q: "zzqqxxjj" });
    expect(r.total).toBe(0);
    const inj = await run({ q: "'); DELETE FROM designs; --" });
    expect(inj.total).toBeGreaterThanOrEqual(0);
    expect((await run({})).total).toBeGreaterThan(4000);
  });
});

describe("filters and counts use the same published dataset", () => {
  it("style facet counts match filtered totals", async () => {
    const all = await run({ q: "arrow" });
    for (const f of all.facets.styles) {
      const r = await run({ q: "arrow", style: f.value });
      expect(r.total).toBe(f.count);
      expect(r.items.every((i) => i.displayStyle === f.value)).toBe(true);
    }
  });
  it("area facet counts match filtered totals", async () => {
    const all = await run({});
    for (const f of all.facets.areas) expect((await run({ area: f.value })).total).toBe(f.count);
  });
  it("never substitutes a style: brand logos only appear in the Brand style", async () => {
    expect((await run({ area: "brands", style: "line" })).total).toBe(0);
    const brands = await run({ style: "brand", per: "48" });
    expect(brands.total).toBeGreaterThan(3000);
    expect(brands.items.every((i) => i.displayStyle === "brand" && i.area === "brands")).toBe(true);
    const core = await run({ area: "core", style: "rounded", per: "48" });
    expect(core.items.every((i) => i.displayStyle === "rounded")).toBe(true);
    expect(core.missingInStyle).toBe(0); // every Core icon has all three styles
  });
  it("bounds page size", async () => {
    const r = await run({ per: "192" });
    expect(r.items.length).toBe(192);
    expect((await run({ per: "100000" })).items.length).toBe(96);
  });
  it("core area and brand filters", async () => {
    const core = await run({ area: "core" });
    expect(core.items.every((i) => i.area === "core")).toBe(true);
    const brands = await run({ brands: "only", per: "48" });
    expect(brands.items.every((i) => i.isBrand)).toBe(true);
  });
});
