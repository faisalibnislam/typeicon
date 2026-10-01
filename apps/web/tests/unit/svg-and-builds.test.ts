import { describe, expect, it } from "vitest";
import { coloredSvg, isSafeSvg, sizedSvg, transformedSvg } from "@/lib/svg";
import { buildCacheKey, slugify } from "@/lib/builds";

const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M1 1h2v2z"/></svg>';

describe("svg safety", () => {
  it("accepts sanitized catalog SVG", () => expect(isSafeSvg(svg)).toBe(true));
  it.each([
    '<svg><script>alert(1)</script></svg>',
    '<svg onload="x()"></svg>',
    '<svg><a href="https://x"></a></svg>',
    '<svg><foreignObject/></svg>',
    '<svg><use xlink:href="#a"/></svg>',
    '<svg style="fill:url(https://x)"></svg>',
    "<div></div>",
    null,
  ])("rejects %s", (bad) => expect(isSafeSvg(bad as string)).toBe(false));
  it("sizes and labels", () => {
    expect(sizedSvg(svg, { size: 32 })).toContain('width="32" height="32" aria-hidden="true" focusable="false"');
    expect(sizedSvg(svg, { size: 32, label: 'Home "x"' })).toContain('role="img" aria-label="Home x"');
    const wide = svg.replace("0 0 24 24", "0 0 48 24");
    expect(sizedSvg(wide, { size: 24 })).toContain('width="48" height="24"');
  });
  it("applies transform and colour only when requested", () => {
    expect(transformedSvg(svg, { rotate: 0, flipX: false, flipY: false })).toBe(svg);
    expect(transformedSvg(svg, { rotate: 90, flipX: true, flipY: false })).toContain('transform="translate(12 12) rotate(90) scale(-1 1) translate(-12 -12)"');
    expect(coloredSvg(svg, "#ff0000")).toContain('fill="#ff0000"');
    expect(coloredSvg(svg, "red; x")).toBe(svg);
  });
});

describe("build cache keys", () => {
  const items = [
    { variantId: "a", svgSha256: "1" },
    { variantId: "b", svgSha256: "2" },
  ] as never[];
  it("is order independent and changes with any input", () => {
    const base = { scope: "public", slug: "x", formats: ["otf", "css"], items, release: "0.1.0" };
    const k = buildCacheKey(base);
    expect(buildCacheKey({ ...base, items: [...items].reverse(), formats: ["css", "otf"] })).toBe(k);
    expect(buildCacheKey({ ...base, scope: "private:u1" })).not.toBe(k);
    expect(buildCacheKey({ ...base, slug: "y" })).not.toBe(k);
    expect(buildCacheKey({ ...base, release: "0.2.0" })).not.toBe(k);
    expect(buildCacheKey({ ...base, items: [items[0], { variantId: "b", svgSha256: "3" }] as never[] })).not.toBe(k);
  });
  it("slugifies project names safely", () => {
    expect(slugify("Acme Dashboard!!")).toBe("acme-dashboard");
    expect(slugify("../../etc")).toBe("etc");
    expect(slugify("***")).toBe("subset");
  });
});
