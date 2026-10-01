/**
 * @typeicon/vue: shared icon factory.
 *
 * Every generated icon module (e.g. `@typeicon/vue/line/home`) is a tiny
 * ESM file that calls `createIcon(name, iconNode, rootAttrs)`. This module
 * must stay small and must never import the catalog or any icon data.
 */
import { defineComponent, h, useId } from 'vue';
import type { DefineSetupFnComponent, VNode } from 'vue';

/** Attributes of one SVG element, using SVG (kebab-case) attribute names. */
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

/** Props accepted by every TypeIcon Vue icon. Other attributes fall through to `<svg>`. */
export interface IconProps {
  /** Rendered height in px (number) or any CSS length (string). Default `24`. */
  size?: number | string;
  /** Sets the CSS `color` of the icon; the artwork paints with `currentColor`. */
  color?: string;
  /** Overrides the root `stroke-width`; only applied to stroke-based icons. */
  strokeWidth?: number | string;
  /**
   * Accessible name. When set, the icon renders `role="img"`, a `<title>`
   * with a stable unique id and `aria-labelledby` pointing at it.
   */
  title?: string;
}

/** Any TypeIcon Vue icon component. */
export type IconComponent = DefineSetupFnComponent<IconProps>;

const SVG_NS = 'http://www.w3.org/2000/svg';
const PROP_NAMES = ['size', 'color', 'strokeWidth', 'title'] as const;

function toPascalCase(name: string): string {
  return name
    .split(/[^a-zA-Z0-9]+/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join('');
}

function renderNode(node: IconNodeElement): VNode {
  const children = node[2];
  return children && children.length > 0
    ? h(node[0], { ...node[1] }, children.map(renderNode))
    : h(node[0], { ...node[1] });
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
 * @param iconNode SVG children as `[tag, attrs, children?]` tuples (SVG attr names).
 * @param root     Root `<svg>` presentation attributes, including `viewBox`.
 */
export function createIcon(name: string, iconNode: IconNode, root: IconRootAttrs): IconComponent {
  const ratio = viewBoxRatio(root.viewBox);
  const isStroke = typeof root.stroke === 'string' && root.stroke !== 'none';

  return defineComponent<IconProps>(
    (props, { attrs, slots }) => {
      const titleId = useId();

      return () => {
        const size = props.size ?? 24;
        const title = props.title;
        const labelledByTitle = hasValue(title);
        const labelled =
          labelledByTitle || hasValue(attrs['aria-label']) || hasValue(attrs['aria-labelledby']);

        const width =
          ratio === 1
            ? size
            : typeof size === 'number'
              ? Math.round(size * ratio * 1000) / 1000
              : undefined;

        const svgAttrs: Record<string, unknown> = {
          xmlns: SVG_NS,
          width,
          height: size,
          ...root,
        };
        if (isStroke && hasValue(props.strokeWidth)) svgAttrs['stroke-width'] = props.strokeWidth;
        if (hasValue(props.color)) svgAttrs.color = props.color;
        if (labelled) {
          svgAttrs.role = 'img';
          if (labelledByTitle) svgAttrs['aria-labelledby'] = titleId;
        } else {
          svgAttrs['aria-hidden'] = 'true';
          svgAttrs.focusable = 'false';
        }
        Object.assign(svgAttrs, attrs);

        const children: (VNode | VNode[] | undefined)[] = [];
        if (labelledByTitle) children.push(h('title', { id: titleId }, title));
        for (const node of iconNode) children.push(renderNode(node));
        const extra = slots.default?.();
        if (extra) children.push(extra);

        return h('svg', svgAttrs, children);
      };
    },
    {
      name: toPascalCase(name) || 'TypeIconIcon',
      props: PROP_NAMES as unknown as (keyof IconProps)[],
      inheritAttrs: false,
    },
  );
}
