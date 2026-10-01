"use client";
import { isSafeSvg, sizedSvg } from "@/lib/svg";

export function IconSvgClient({ svg, size = 24, label, className }: { svg: string | null; size?: number; label?: string; className?: string }) {
  if (!isSafeSvg(svg)) return <span className={className} style={{ display: "inline-block", width: size, height: size }} />;
  return (
    <span
      className={`icon-svg inline-flex items-center justify-center ${className ?? ""}`}
      style={{ height: size }}
      dangerouslySetInnerHTML={{ __html: sizedSvg(svg, { size, label }) }}
    />
  );
}
