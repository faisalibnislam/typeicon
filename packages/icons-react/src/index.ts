/**
 * @typeicon/react: shared icon factory.
 *
 * Every generated icon module (e.g. `@typeicon/react/line/home`) is a tiny
 * ESM file that calls `createIcon(name, iconNode, rootAttrs)`. This module
 * must stay small and must never import the catalog or any icon data.
 */
import { createElement, forwardRef, useId } from 'react';
import type {
  ForwardRefExoticComponent,
  ReactElement,
  ReactNode,
  RefAttributes,
  SVGProps,
} from 'react';

/** Attributes of one SVG element, using React (camelCase) attribute names. */
export type IconNodeAttrs = Readonly<Record<string, string | number>>;

/** One SVG child element: `[tagName, attrs]` or `[tagName, attrs, children]`. */
export type IconNodeElement =
  | readonly [tag: string, attrs: IconNodeAttrs]
  | readonly [tag: string, attrs: IconNodeAttrs, children: IconNode];

/** Compact, serialisable representation of an icon's SVG children. */
export type IconNode = readonly IconNodeElement[];

/** Presentation attributes of the root `<svg>` (always includes `viewBox`). */
export interface IconRootAttrs {
  readonly viewBox: string;
  readonly [attr: string]: string | number;
}

type NativeSvgProps = Omit<
  SVGProps<SVGSVGElement>,
  'ref' | 'color' | 'strokeWidth' | 'width' | 'height' | 'children'
>;

/** Props accepted by every TypeIcon icon. */
export interface IconBaseProps extends NativeSvgProps {
  /** Rendered height in px (number) or any CSS length (string). Default `24`. */
  size?: number | string;
  /** Sets the CSS `color` of the icon; the artwork paints with `currentColor`. */
  color?: string;
  /**
   * Accessible name. When set, the icon renders `role="img"`, a `<title>`
   * with a stable unique id and `aria-labelledby` pointing at it.
   */
  title?: string;
  /** Extra SVG content appended after the icon artwork. */
  children?: ReactNode;
}

/** Props of stroke-based icons (Core line/rounded, Tabler outline). */
export interface StrokeIconProps extends IconBaseProps {
  /** Overrides the root `stroke-width` (in viewBox units). */
  strokeWidth?: number | string;
}

/** Props union accepted by the runtime component. */
export type IconProps = StrokeIconProps;

/** A fill-based icon component (no `strokeWidth` prop). */
export type FilledIconComponent = ForwardRefExoticComponent<
  IconBaseProps & RefAttributes<SVGSVGElement>
>;

/** A stroke-based icon component (accepts `strokeWidth`). */
export type StrokeIconComponent = ForwardRefExoticComponent<
  StrokeIconProps & RefAttributes<SVGSVGElement>
>;

/** Any TypeIcon React icon component. */
export type IconComponent = FilledIconComponent | StrokeIconComponent;

const SVG_NS = 'http://www.w3.org/2000/svg';

function toPascalCase(name: string): string {
  return name
    .split(/[^a-zA-Z0-9]+/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join('');
}

function renderNode(node: IconNodeElement): ReactElement {
  const children = node[2];
  return children && children.length > 0
    ? createElement(node[0], node[1], ...children.map(renderNode))
    : createElement(node[0], node[1]);
}

function viewBoxRatio(viewBox: string): number {
  const parts = viewBox.trim().split(/[\s,]+/).map(Number);
  const width = parts[2];
  const height = parts[3];
  if (!width || !height || !Number.isFinite(width / height)) return 1;
  return width / height;
}

function hasValue(value: unknown): boolean {
  return value !== undefined && value !== null && value !== '' && value !== false;
}

/**
 * Create an icon component from its compact SVG node description.
 *
 * @param name     Icon name (catalog `name`, e.g. `home`, `tabler-home`).
 * @param iconNode SVG children as `[tag, attrs, children?]` tuples (React attr names).
 * @param root     Root `<svg>` presentation attributes, including `viewBox`.
 */
export function createIcon(
  name: string,
  iconNode: IconNode,
  root: IconRootAttrs,
): StrokeIconComponent {
  // Element trees are immutable, so they are built once and reused per render.
  const artwork = iconNode.map(renderNode);
  const ratio = viewBoxRatio(root.viewBox);
  const isStroke = typeof root.stroke === 'string' && root.stroke !== 'none';

  const Icon = forwardRef<SVGSVGElement, StrokeIconProps>(function TypeIconIcon(props, ref) {
    const { size = 24, color, strokeWidth, title, children, ...rest } = props;
    const titleId = useId();

    const labelledByTitle = hasValue(title);
    const labelled =
      labelledByTitle || hasValue(rest['aria-label']) || hasValue(rest['aria-labelledby']);

    const height = size;
    // Non-square viewBoxes keep their aspect ratio. String sizes (CSS lengths)
    // leave width to the browser, which derives it from the viewBox.
    const width =
      ratio === 1 ? size : typeof size === 'number' ? Math.round(size * ratio * 1000) / 1000 : undefined;

    const svgProps: Record<string, unknown> = {
      xmlns: SVG_NS,
      width,
      height,
      ...root,
    };
    if (isStroke && hasValue(strokeWidth)) svgProps.strokeWidth = strokeWidth;
    if (hasValue(color)) svgProps.color = color;
    if (labelled) {
      svgProps.role = 'img';
      if (labelledByTitle) svgProps['aria-labelledby'] = titleId;
    } else {
      svgProps['aria-hidden'] = 'true';
      svgProps.focusable = 'false';
    }
    Object.assign(svgProps, rest);
    svgProps.ref = ref;

    return createElement(
      'svg',
      svgProps,
      labelledByTitle ? createElement('title', { id: titleId }, title) : null,
      ...artwork,
      children,
    );
  });

  Icon.displayName = toPascalCase(name) || 'TypeIconIcon';
  return Icon;
}
