import Link from "next/link";
import { Suspense } from "react";
import { AccountMenu } from "./account-menu";
import { HeaderSearch } from "./header-search";
import { Logo } from "./logo";
import { MobileNav } from "./mobile-nav";
import { ThemeToggle } from "./theme-toggle";

export const NAV = [
  { href: "/icons", label: "Icons" },
  { href: "/downloads", label: "Downloads" },
  { href: "/docs", label: "Docs" },
  { href: "/icons?style=brand", label: "Brands" },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-border bg-bg/90 backdrop-blur supports-[backdrop-filter]:bg-bg/75">
      <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:left-3 focus:top-3 focus:z-50 focus:rounded-lg focus:bg-surface focus:px-3 focus:py-2">
        Skip to content
      </a>
      <div className="mx-auto flex max-w-[1440px] flex-wrap items-center gap-x-3 gap-y-2 px-4 py-3 sm:px-6 md:h-16 md:flex-nowrap md:py-0">
        <MobileNav />
        <Link href="/" className="shrink-0 rounded-lg" aria-label="TypeIcon home">
          <Logo />
        </Link>
        <nav aria-label="Main" className="ml-4 hidden items-center gap-1 lg:flex">
          {NAV.map((n) => (
            <Link key={n.href} href={n.href} className="rounded-lg px-3 py-2 text-sm font-medium text-text-2 hover:bg-surface-2 hover:text-text">
              {n.label}
            </Link>
          ))}
        </nav>
        <div className="order-last w-full md:order-none md:mx-2 md:w-auto md:max-w-xl md:flex-1">
          <Suspense fallback={<div className="h-10" />}>
            <HeaderSearch />
          </Suspense>
        </div>
        <div className="ml-auto flex items-center gap-1">
          <ThemeToggle />
          <AccountMenu />
        </div>
      </div>
    </header>
  );
}
