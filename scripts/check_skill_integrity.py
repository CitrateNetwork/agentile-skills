#!/usr/bin/env python3
"""Integrity gate over executable skill content (AGS-B-001).

The product of this repo is instruction text that runs inside a consumer's
agent session. Before this gate, nothing in the repo hashed, signed, or
otherwise pinned the 13 `SKILL.md` files: an unreviewed edit to any of them —
a compromised maintainer token, a poisoned agent push — shipped to every
installation on the next marketplace refresh with nothing to detect it.

This check pins every `plugins/*/skills/*/SKILL.md` by SHA-256 in
`skills.lock`. A content change that is not accompanied by a matching,
deliberately-regenerated lock entry fails the harness, so a silent edit to
executable content cannot pass CI. It is deliberately a SEPARATE lock from
`templates.lock` (which covers the inert `*_TEMPLATE.md` scaffolds): this one
guards the text that becomes instructions.

Usage:
  scripts/check_skill_integrity.py            # verify (CI); exit 1 on drift
  scripts/check_skill_integrity.py --update   # regenerate skills.lock after a
                                              # reviewed, intentional edit

Regenerating the lock is a reviewed act: the diff to skills.lock is the
record that a human/agent looked at the content change. Pair it with
CODEOWNERS + branch protection so the regeneration itself is reviewed.

Exit codes:
  0 — every SKILL.md is covered and matches skills.lock
  1 — a SKILL.md is uncovered, changed, or the lock references a missing file
  2 — usage error
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK_PATH = ROOT / "skills.lock"
SKILL_GLOB = "plugins/*/skills/*/SKILL.md"

HEADER = (
    "# sha256 of every executable SKILL.md (AGS-B-001 integrity gate).\n"
    "# Regenerate ONLY after a reviewed, intentional content change:\n"
    "#   scripts/check_skill_integrity.py --update\n"
    "# A drift between a SKILL.md and this file fails the validation harness.\n"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def skill_files() -> list[Path]:
    return sorted(ROOT.glob(SKILL_GLOB))


def parse_lock() -> dict[str, str]:
    locked: dict[str, str] = {}
    if not LOCK_PATH.is_file():
        return locked
    for line in LOCK_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, rel = line.split(None, 1)
        locked[rel.strip()] = digest
    return locked


def write_lock(files: list[Path]) -> None:
    lines = [HEADER]
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        lines.append(f"{sha256(f)}  {rel}\n")
    LOCK_PATH.write_text("".join(lines), encoding="utf-8")


def main() -> int:
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    files = skill_files()
    if not files:
        print("ERROR: no SKILL.md files found; refusing to write an empty lock.",
              file=sys.stderr)
        return 2

    if args and args[0] == "--update":
        write_lock(files)
        print(f"skills.lock regenerated over {len(files)} SKILL.md file(s).")
        return 0
    if args:
        print(f"ERROR: unknown argument {args[0]!r}", file=sys.stderr)
        return 2

    locked = parse_lock()
    if not locked:
        print("BLOCKER: skills.lock is missing or empty. Generate it with")
        print("  scripts/check_skill_integrity.py --update")
        return 1

    on_disk = {f.relative_to(ROOT).as_posix(): f for f in files}
    problems: list[str] = []

    for rel, path in on_disk.items():
        if rel not in locked:
            problems.append(f"UNCOVERED: {rel} has no entry in skills.lock")
        elif sha256(path) != locked[rel]:
            problems.append(f"CHANGED:   {rel} does not match skills.lock")
    for rel in locked:
        if rel not in on_disk:
            problems.append(f"MISSING:   skills.lock entry {rel} is not on disk")

    if problems:
        print(f"BLOCKER: {len(problems)} skill-integrity violation(s):")
        for p in problems:
            print(f"  - {p}")
        print()
        print("Executable skill content changed without a matching lock update.")
        print("If the change is intentional and reviewed, regenerate the lock:")
        print("  scripts/check_skill_integrity.py --update")
        return 1

    print(f"OK: {len(files)} SKILL.md file(s) match skills.lock.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
