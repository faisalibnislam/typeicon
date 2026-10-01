"use client";
import { createContext, useContext, useMemo, useState } from "react";

/** The icons currently visible in a grid, so the icon modal can step to the previous/next result. */
export interface ResultEntry {
  name: string;
  style: string | null;
}
interface Api {
  entries: ResultEntry[];
  setEntries: (e: ResultEntry[]) => void;
}
const Ctx = createContext<Api>({ entries: [], setEntries: () => undefined });

export function ResultsNavProvider({ children }: { children: React.ReactNode }) {
  const [entries, setEntries] = useState<ResultEntry[]>([]);
  const api = useMemo(() => ({ entries, setEntries }), [entries]);
  return <Ctx.Provider value={api}>{children}</Ctx.Provider>;
}

export const useResultsNav = () => useContext(Ctx);
