"""Permanent codepoint registry (append-only) and global name/alias collision checks.

assets/registry/codepoints.json is committed and is the source of truth for PUA
assignments. Codepoints are stored as integers. An assignment is never changed or reused
for a different subject within a namespace; removed/deprecated subjects keep theirs.
"""
from __future__ import annotations

import json
from pathlib import Path

NAMESPACE_RANGES = {
    # namespace kind -> (base, limit)
    "core": (0xF0000, 65534),  # Plane 15 Supplementary PUA-A
    "pack": (0x100000, 61440),  # Plane 16 Supplementary PUA-B (each pack is its own family)
    "kit": (0x10F000, 4094),  # custom uploads, per kit
}
CORE_BMP_BASE, CORE_BMP_LIMIT = 0xE000, 6400  # BMP PUA mirror for the first 6,400 Core concepts


class RegistryError(RuntimeError):
    pass


def _kind(namespace: str) -> str:
    return namespace.split(":", 1)[0]


class CodepointRegistry:
    def __init__(self, path: Path):
        self.path = path
        if path.exists():
            self.doc = json.loads(path.read_text())
        else:
            self.doc = {"version": 1, "namespaces": {}}
        self._original = json.dumps(self.doc, sort_keys=True)
        self.new_assignments: list[tuple[str, str, int]] = []

    def namespace(self, ns: str) -> dict:
        spaces = self.doc["namespaces"]
        if ns not in spaces:
            base, limit = NAMESPACE_RANGES[_kind(ns)]
            spaces[ns] = {"base": base, "limit": limit, "assignments": {}}
        return spaces[ns]

    def get(self, ns: str, subject: str) -> int | None:
        return self.doc["namespaces"].get(ns, {}).get("assignments", {}).get(subject)

    def allocate(self, ns: str, subjects: list[str]) -> dict[str, int]:
        """Assign codepoints to subjects that lack one, in the given (deterministic) order."""
        space = self.namespace(ns)
        assigned: dict[str, int] = space["assignments"]
        used = set(assigned.values())
        if len(used) != len(assigned):
            raise RegistryError(f"{ns}: duplicate codepoints in registry")
        nxt = max(used) + 1 if used else space["base"]
        out = {}
        for subj in subjects:
            if subj in assigned:
                out[subj] = assigned[subj]
                continue
            if nxt >= space["base"] + space["limit"]:
                raise RegistryError(f"{ns}: codepoint range exhausted")
            assigned[subj] = nxt
            self.new_assignments.append((ns, subj, nxt))
            out[subj] = nxt
            nxt += 1
        return out

    @staticmethod
    def bmp_mirror(ns: str, codepoint: int) -> int | None:
        if ns != "core":
            return None
        n = codepoint - NAMESPACE_RANGES["core"][0]
        return CORE_BMP_BASE + n if 0 <= n < CORE_BMP_LIMIT else None

    def retire(self, ns: str, reason: str, date: str) -> None:
        """Move a namespace (e.g. a removed source) to `retired`. Its assignments are kept as history."""
        space = self.doc["namespaces"].pop(ns, None)
        if space is not None:
            self.doc.setdefault("retired", {})[ns] = {**space, "retiredAt": date, "reason": reason}

    def check_append_only(self, previous: dict) -> list[str]:
        """Compare against a previous registry document; report changed/reused assignments."""
        problems = []
        for ns, space in previous.get("namespaces", {}).items():
            if ns in self.doc.get("retired", {}):
                space_now = self.doc["retired"][ns]["assignments"]
                if space_now != space.get("assignments", {}):
                    problems.append(f"{ns}: retired namespace history was modified")
                continue
            cur = self.doc["namespaces"].get(ns, {}).get("assignments", {})
            for subj, cp in space.get("assignments", {}).items():
                if subj not in cur:
                    problems.append(f"{ns}: assignment for {subj} was removed")
                elif cur[subj] != cp:
                    problems.append(f"{ns}: {subj} changed U+{cp:X} -> U+{cur[subj]:X}")
            inv: dict[int, str] = {}
            for subj, cp in cur.items():
                if cp in inv:
                    problems.append(f"{ns}: U+{cp:X} assigned to both {inv[cp]} and {subj}")
                inv[cp] = subj
        return problems

    def save(self) -> bool:
        cur = json.dumps(self.doc, sort_keys=True)
        if cur == self._original:
            return False
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Stable, reviewable formatting: one assignment per line, sorted by codepoint.
        lines = ['{', '  "version": 1,', '  "$comment": "Append-only. Never edit or reuse an assignment. Codepoints are integers.",', '  "namespaces": {']
        spaces = self.doc["namespaces"]
        for i, ns in enumerate(sorted(spaces)):
            sp = spaces[ns]
            lines.append(f'    {json.dumps(ns)}: {{"base": {sp["base"]}, "limit": {sp["limit"]}, "assignments": {{')
            items = sorted(sp["assignments"].items(), key=lambda kv: kv[1])
            for j, (subj, cp) in enumerate(items):
                lines.append(f'      {json.dumps(subj)}: {cp}' + ("," if j < len(items) - 1 else ""))
            lines.append("    }}" + ("," if i < len(spaces) - 1 else ""))
        lines.append("  }" + ("," if self.doc.get("retired") else ""))
        if self.doc.get("retired"):
            lines.append('  "retired": ' + json.dumps(self.doc["retired"], sort_keys=True))
        lines += ["}"]
        self.path.write_text("\n".join(lines) + "\n")
        self._original = cur
        return True


class NameRegistry:
    """Global collision registry for canonical names and aliases, per namespace."""

    def __init__(self):
        self.owner: dict[tuple[str, str], tuple[str, str]] = {}  # (ns,name) -> (design, kind)
        self.errors: list[str] = []

    def claim(self, ns: str, name: str, design: str, kind: str) -> bool:
        key = (ns, name)
        if key in self.owner and self.owner[key][0] != design:
            other = self.owner[key]
            self.errors.append(f"{ns}: {kind} {name!r} of {design} collides with {other[1]} of {other[0]}")
            return False
        self.owner[key] = (design, kind)
        return True
