"use client";
import { useEffect, useState } from "react";

export interface PreviewPrefs {
  size: number;
  color: string | null; // null = currentColor (theme text)
}
const KEY = "typeicon:preview:v1";

export function usePreviewPrefs(): [PreviewPrefs, (p: Partial<PreviewPrefs>) => void] {
  const [prefs, setPrefs] = useState<PreviewPrefs>({ size: 28, color: null });
  useEffect(() => {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) setPrefs((p) => ({ ...p, ...JSON.parse(raw) }));
    } catch {}
  }, []);
  return [
    prefs,
    (p) =>
      setPrefs((cur) => {
        const next = { ...cur, ...p };
        try {
          localStorage.setItem(KEY, JSON.stringify(next));
        } catch {}
        return next;
      }),
  ];
}
