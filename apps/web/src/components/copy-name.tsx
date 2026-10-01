"use client";
import { useRef, useState } from "react";
import { cn } from "@/lib/cn";

/** The icon name as a button: one click copies it and shows a short "Copied" tooltip. */
export function CopyName({ name, as: Tag = "h1", className }: { name: string; as?: "h1" | "h2"; className?: string }) {
  const [state, setState] = useState<"idle" | "copied" | "error">("idle");
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  async function copy() {
    try {
      await navigator.clipboard.writeText(name);
      setState("copied");
    } catch {
      setState("error");
    }
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => setState("idle"), 1600);
  }
  return (
    <Tag className="relative m-0">
      <button
        type="button"
        onClick={copy}
        title="Click to copy the name"
        aria-description="Copies the name to the clipboard"
        className={cn("cursor-copy rounded-md font-mono font-semibold tracking-tight text-text hover:text-accent focus-visible:text-accent", className)}
      >
        {name}
      </button>
      <span
        role="status"
        aria-live="polite"
        className={cn(
          "pointer-events-none absolute -top-7 left-0 whitespace-nowrap rounded-md bg-text px-2 py-0.5 font-sans text-xs font-medium text-bg shadow transition-opacity",
          state === "idle" ? "opacity-0" : "opacity-100",
        )}
      >
        {state === "error" ? "Copy failed. Select the name to copy it." : state === "copied" ? "Copied" : ""}
      </span>
    </Tag>
  );
}
