import { describe, expect, it } from "vitest";
import { normalizeQuery, parseSearchParams, toQueryString } from "@/lib/search-params";

describe("normalizeQuery", () => {
  it("lowercases, hyphenates and strips unsafe characters", () => {
    expect(normalizeQuery("  Arrow Right ")).toBe("arrow-right");
    expect(normalizeQuery("arrow_forward")).toBe("arrow-forward");
    expect(normalizeQuery("'; DROP TABLE designs;--")).toBe("drop-table-designs");
    expect(normalizeQuery("Café")).toBe("cafe");
    expect(normalizeQuery("x".repeat(500))).toHaveLength(64);
  });
});

describe("parseSearchParams", () => {
  it("applies safe defaults and bounds", () => {
    const p = parseSearchParams({});
    expect(p).toMatchObject({ q: "", style: "all", page: 1, per: 96, sort: "relevance", area: "all", brands: "include", missing: false });
    expect(parseSearchParams({ page: "99999" }).page).toBe(1);
    expect(parseSearchParams({ per: "5000" }).per).toBe(96);
    expect(parseSearchParams({ style: "bold" }).style).toBe("all");
    expect(parseSearchParams({ q: "a".repeat(200) }).q).toHaveLength(64);
  });
  it("validates list filters", () => {
    const p = parseSearchParams({ category: "arrows,../etc,Media", pack: ["tabler", "tabler"], license: "MIT,<script>" });
    expect(p.category).toEqual(["arrows"]);
    expect(p.pack).toEqual(["tabler"]);
    expect(p.license).toEqual(["MIT"]);
  });
});

describe("toQueryString", () => {
  it("round-trips state and omits defaults", () => {
    const p = parseSearchParams({ q: "home", style: "line", pack: "tabler,material", page: "3" });
    const qs = toQueryString(p);
    expect(qs).toBe("?q=home&style=line&pack=tabler%2Cmaterial&page=3");
    expect(parseSearchParams(Object.fromEntries(new URLSearchParams(qs)))).toEqual(p);
    expect(toQueryString(parseSearchParams({}))).toBe("");
  });
});
