"use client";
import { useEffect } from "react";
import { type ResultEntry, useResultsNav } from "./results-nav";

/** Records the icons visible on a server-rendered grid so the icon modal can step through them. */
export function RegisterResults({ entries }: { entries: ResultEntry[] }) {
  const { setEntries } = useResultsNav();
  const key = entries.map((e) => `${e.name}:${e.style}`).join("|");
  useEffect(() => {
    setEntries(entries);
  }, [key]); // eslint-disable-line react-hooks/exhaustive-deps
  return null;
}
