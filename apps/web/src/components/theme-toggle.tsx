"use client";
import { useEffect, useState } from "react";
import { UiIcon } from "./ui-icon";

type Theme = "light" | "dark" | "system";
const ORDER: Theme[] = ["system", "light", "dark"];

function apply(theme: Theme) {
  const dark = theme === "dark" || (theme === "system" && matchMedia("(prefers-color-scheme: dark)").matches);
  document.documentElement.classList.toggle("dark", dark);
}

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>("system");
  useEffect(() => {
    let stored: Theme = "system";
    try {
      stored = (localStorage.getItem("theme") as Theme) || "system";
    } catch {}
    setTheme(stored);
    const mq = matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => {
      let t: Theme = "system";
      try {
        t = (localStorage.getItem("theme") as Theme) || "system";
      } catch {}
      if (t === "system") apply("system");
    };
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);
  const next = ORDER[(ORDER.indexOf(theme) + 1) % ORDER.length];
  const label = { system: "System theme", light: "Light theme", dark: "Dark theme" }[theme];
  return (
    <button
      type="button"
      onClick={() => {
        setTheme(next);
        try {
          localStorage.setItem("theme", next);
        } catch {}
        apply(next);
      }}
      className="inline-flex h-9 items-center gap-1.5 rounded-lg px-2 text-sm text-muted hover:bg-surface-2 hover:text-text"
      aria-label={`${label}. Switch to ${next} theme`}
      title={`${label}. Click for ${next}`}
    >
      <UiIcon name={theme === "dark" ? "moon" : theme === "light" ? "sun" : "settings"} size={18} />
      <span className="hidden text-xs xl:inline">{theme === "system" ? "System" : theme === "light" ? "Light" : "Dark"}</span>
    </button>
  );
}

/** Inline script (runs before paint) so the stored theme never flashes. */
export const themeInitScript = `(function(){try{var t=localStorage.getItem('theme')||'system';var d=t==='dark'||(t==='system'&&matchMedia('(prefers-color-scheme: dark)').matches);if(d)document.documentElement.classList.add('dark')}catch(e){}})();`;
