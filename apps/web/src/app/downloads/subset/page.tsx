import type { Metadata } from "next";
import { SubsetBuilder } from "@/components/downloads/subset-builder";

export const metadata: Metadata = { title: "Build a subset", description: "Generate a small font kit with only the icons you need.", alternates: { canonical: "/downloads/subset" } };

export default function SubsetPage() {
  return (
    <div className="mx-auto max-w-[1300px] px-4 pb-24 pt-8 sm:px-6">
      <h1 className="text-2xl font-semibold tracking-tight">Build a subset</h1>
      <p className="mb-8 mt-1 max-w-2xl text-sm text-text-2">
        Generate fonts that contain only your selected icons, with their keywords and aliases, plus CSS and SVGs. Builds run in a background worker and are cached, so an identical build is reused.
      </p>
      <SubsetBuilder />
    </div>
  );
}
