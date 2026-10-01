import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ResultsNavProvider } from "@/components/catalog/results-nav";
import { SelectionProvider } from "@/components/selection/selection-provider";
import { SelectionTray } from "@/components/selection/selection-tray";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { themeInitScript } from "@/components/theme-toggle";
import "./globals.css";

const sans = Geist({ variable: "--font-sans-ui", subsets: ["latin"], display: "swap" });
const mono = Geist_Mono({ variable: "--font-mono-ui", subsets: ["latin"], display: "swap" });

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3107";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: { default: "TypeIcon: icons you can type", template: "%s · TypeIcon" },
  description:
    "Search icons, copy SVG and code, and install desktop fonts whose OpenType ligatures turn keywords like home or search into icons.",
  alternates: { canonical: "/" },
  openGraph: { siteName: "TypeIcon", type: "website" },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f7f7f5" },
    { media: "(prefers-color-scheme: dark)", color: "#0d0d0f" },
  ],
};

export default function RootLayout({ children, modal }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${sans.variable} ${mono.variable}`} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeInitScript }} />
      </head>
      <body className="min-h-dvh bg-bg font-sans text-text antialiased">
        <SelectionProvider>
          <ResultsNavProvider>
            <SiteHeader />
            <main id="main" className="min-h-[60vh]">
              {children}
            </main>
            <SiteFooter />
            <SelectionTray />
            {modal}
          </ResultsNavProvider>
        </SelectionProvider>
      </body>
    </html>
  );
}
