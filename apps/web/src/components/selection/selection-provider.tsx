"use client";
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

export interface SelectedIcon {
  designId: string;
  name: string;
  style: "filled" | "line" | "rounded" | "thin" | "brand";
  source: string;
  svg: string | null;
}

interface SelectionApi {
  items: SelectedIcon[];
  has: (designId: string, style: string) => boolean;
  toggle: (item: SelectedIcon) => void;
  add: (items: SelectedIcon[]) => void;
  remove: (designId: string, style: string) => void;
  clear: () => void;
  max: number;
}

const KEY = "typeicon:selection:v1";
const MAX = 500;
const Ctx = createContext<SelectionApi | null>(null);

export function SelectionProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<SelectedIcon[]>([]);
  useEffect(() => {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) setItems((JSON.parse(raw) as SelectedIcon[]).slice(0, MAX));
    } catch {}
    const onStorage = (e: StorageEvent) => {
      if (e.key === KEY && e.newValue) {
        try {
          setItems(JSON.parse(e.newValue));
        } catch {}
      }
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);
  const persist = useCallback((next: SelectedIcon[]) => {
    setItems(next);
    try {
      localStorage.setItem(KEY, JSON.stringify(next));
    } catch {}
  }, []);
  const api = useMemo<SelectionApi>(() => {
    const key = (d: string, s: string) => `${d}:${s}`;
    const set = new Set(items.map((i) => key(i.designId, i.style)));
    return {
      items,
      max: MAX,
      has: (d, s) => set.has(key(d, s)),
      toggle: (item) =>
        persist(
          set.has(key(item.designId, item.style))
            ? items.filter((i) => key(i.designId, i.style) !== key(item.designId, item.style))
            : [...items, item].slice(0, MAX),
        ),
      add: (more) => persist([...items, ...more.filter((m) => !set.has(key(m.designId, m.style)))].slice(0, MAX)),
      remove: (d, s) => persist(items.filter((i) => key(i.designId, i.style) !== key(d, s))),
      clear: () => persist([]),
    };
  }, [items, persist]);
  return <Ctx.Provider value={api}>{children}</Ctx.Provider>;
}

export function useSelection(): SelectionApi {
  const v = useContext(Ctx);
  if (!v) throw new Error("useSelection outside SelectionProvider");
  return v;
}
