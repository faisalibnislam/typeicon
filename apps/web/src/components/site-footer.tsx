import Link from "next/link";
import { LogoMark } from "./logo";

const COLS: [string, [string, string][]][] = [
  ["Library", [["/icons", "All icons"], ["/categories", "Categories"], ["/icons?style=brand", "Brands"], ["/styles/line", "Styles"], ["/packs", "Sources"]]],
  ["Use", [["/downloads", "Downloads"], ["/docs/desktop", "Desktop fonts"], ["/docs/web", "Web"], ["/docs/figma", "Figma"]]],
  ["Project", [["/licenses", "Licenses"], ["/changelog", "Changelog"], ["/docs/compatibility", "Compatibility"], ["/docs/accessibility", "Accessibility"]]],
];

export function SiteFooter() {
  return (
    <footer className="mt-24 border-t border-border">
      <div className="mx-auto grid max-w-[1440px] gap-10 px-4 py-12 sm:px-6 md:grid-cols-[1.4fr_repeat(3,1fr)]">
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <LogoMark size={24} />
            <span className="font-semibold tracking-tight">TypeIcon</span>
          </div>
          <p className="max-w-xs text-sm text-muted">
            Icons you can type. Original keyword ligature fonts, SVGs and components, plus a separate brand-logo set.
          </p>
        </div>
        {COLS.map(([title, links]) => (
          <div key={title}>
            <h2 className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted">{title}</h2>
            <ul className="space-y-2">
              {links.map(([href, label]) => (
                <li key={href}>
                  <Link href={href} className="text-sm text-text-2 hover:text-accent">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </footer>
  );
}
