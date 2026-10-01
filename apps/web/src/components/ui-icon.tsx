import { uiIcons } from "@/generated/ui-icons";

/** Site chrome icons, rendered from TypeIcon Core's own canonical SVGs. */
export function UiIcon({
  name,
  variant = "line",
  size = 20,
  className,
  label,
}: {
  name: string;
  variant?: "line" | "filled";
  size?: number;
  className?: string;
  label?: string;
}) {
  const icon = uiIcons[`${variant}/${name}`];
  if (!icon) return null;
  const { attrs, body } = icon;
  return (
    <svg
      viewBox={attrs.viewBox}
      width={size}
      height={size}
      fill={attrs.fill}
      stroke={attrs.stroke}
      strokeWidth={attrs["stroke-width"]}
      strokeLinecap={attrs["stroke-linecap"] as "butt" | undefined}
      strokeLinejoin={attrs["stroke-linejoin"] as "miter" | undefined}
      className={className}
      role={label ? "img" : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
      focusable="false"
      dangerouslySetInnerHTML={{ __html: body }}
    />
  );
}
