import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  const base = (process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3107").replace(/\/$/, "");
  return {
    rules: [
      {
        userAgent: "*",
        allow: ["/", "/icons", "/icons/"],
        // Filter permutations, private areas and APIs are not indexed; canonical pages are.
        disallow: ["/api/", "/admin", "/account", "/kits", "/collections", "/sign-in", "/sign-up", "/icons?", "/downloads/subset"],
      },
    ],
    sitemap: [`${base}/sitemap-index.xml`],
  };
}
