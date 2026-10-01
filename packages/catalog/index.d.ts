// @typeicon/catalog: type declarations.
import type { IconName, CoreIconName } from './dist/names.js';

export type { IconName, CoreIconName };

export type TypeIconSource = 'typeicon-core' | 'simple-icons';
export type TypeIconStyle = 'filled' | 'line' | 'rounded' | 'thin' | 'brand';
export type TypeIconArea = 'core' | 'brands';
export type TypeIconFramework = 'react' | 'vue';

export interface TypeIconIconStyle {
  variantId: string;
  nativeStyle: string;
  nativeLabel: string;
  /** Release-relative path, e.g. `svg/typeicon-core/line/home.svg`. */
  svg: string;
  /** Sprite reference, e.g. `sprites/typeicon-core-line.svg#typeicon-line-home`. */
  sprite: string;
  fontFamily: string | null;
  fontSupported: boolean;
  svgSha256: string;
  sourceSha256: string;
}

export interface TypeIconIcon {
  name: string;
  id: string;
  source: TypeIconSource;
  area: TypeIconArea;
  concept: string;
  keywords: string[];
  aliases: string[];
  tags: string[];
  /** Extra search terms: synonyms, use cases and common queries. */
  searchTerms: string[];
  /** Plain-language description of the drawing and where it is used. */
  context: string | null;
  categories: string[];
  isBrand: boolean;
  codepoint: number | null;
  codepointHex: string | null;
  bmpCodepoint: number | null;
  /** SPDX identifier (or LicenseRef) of the icon's source licence. */
  license: string;
  derivedFrom: { name: string; transform: string } | null;
  styles: Partial<Record<TypeIconStyle, TypeIconIconStyle>>;
}

export interface TypeIconFamilyFile {
  name: string;
  bytes: number;
  sha256: string;
}

export interface TypeIconFamily {
  slug: string;
  family: string;
  postscriptName: string;
  source: TypeIconSource;
  area: TypeIconArea;
  style: TypeIconStyle;
  cssClass: string;
  part: string | number | null;
  glyphs: number;
  keywords: number;
  files: Partial<Record<'otf' | 'ttf' | 'woff2' | 'woff', TypeIconFamilyFile>>;
  [key: string]: unknown;
}

/** Compact entry of `@typeicon/catalog/names.json`. */
export interface TypeIconNameEntry {
  name: IconName;
  source: TypeIconSource;
  area: TypeIconArea;
  styles: TypeIconStyle[];
}

export declare const SOURCES: readonly TypeIconSource[];
export declare const STYLES: readonly TypeIconStyle[];

export declare function isValidIconName(name: unknown): name is string;
export declare function getIcon(name: IconName): Promise<TypeIconIcon>;
export declare function getIcon(name: string): Promise<TypeIconIcon | undefined>;
export declare function findIcon(
  icons: readonly TypeIconIcon[],
  name: string,
  options?: { matchAliases?: boolean },
): TypeIconIcon | undefined;
export declare function iconSubpath(icon: TypeIconIcon, style: TypeIconStyle): string | undefined;
export declare function iconImportPath(
  icon: TypeIconIcon,
  style: TypeIconStyle,
  framework?: TypeIconFramework,
): string | undefined;
export declare function svgImportPath(icon: TypeIconIcon, style: TypeIconStyle): string | undefined;
