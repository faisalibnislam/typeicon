/** TypeIcon mark: a keycap whose letters resolve into a glyph, which is what a ligature does. */
export function LogoMark({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" aria-hidden="true" focusable="false">
      <rect x="1.5" y="1.5" width="29" height="29" rx="8" fill="var(--text)" />
      <path d="M7.5 9.5h11M13 9.5V23" fill="none" stroke="var(--bg)" strokeWidth="3" strokeLinecap="butt" strokeLinejoin="miter" />
      <rect x="19.5" y="15" width="5" height="8" rx="1" fill="var(--accent)" />
      <circle cx="22" cy="10.5" r="2.25" fill="var(--accent)" />
    </svg>
  );
}

export function Logo() {
  return (
    <span className="inline-flex items-center gap-2">
      <LogoMark />
      <span className="text-[17px] font-semibold tracking-[-0.02em] text-text">TypeIcon</span>
    </span>
  );
}
