import { isSafeSvg, sizedSvg } from "@/lib/svg";
import { cn } from "@/lib/cn";

/** Render a catalog SVG inline (inherits currentColor). Unsafe or missing markup renders nothing. */
export function IconSvg({ svg, size = 24, label, className }: { svg: string | null; size?: number; label?: string; className?: string }) {
  if (!isSafeSvg(svg)) return <span className={cn("inline-block", className)} style={{ width: size, height: size }} />;
  return (
    <span
      className={cn("icon-svg inline-flex items-center justify-center", className)}
      style={{ height: size }}
      dangerouslySetInnerHTML={{ __html: sizedSvg(svg, { size, label }) }}
    />
  );
}
