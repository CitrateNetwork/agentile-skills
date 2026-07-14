#!/usr/bin/env python3
"""Validation harness for agentile-skills (SKILLS-S0 WP-3).

Canonical test command:  python3 scripts/validate.py

Checks, in order:
  1. marketplace.json / plugin.json schema + cross-consistency
  2. SKILL.md frontmatter lint (name == directory, trigger-phrase description)
  3. Rule-12 frontmatter on every .agentile/ doc
  4. Vendored-template integrity vs templates.lock (catches in-place edits)
  5. Vendored-template drift vs the agentile skeleton (local checkouts only;
     skipped in CI where the skeleton is not present)
  6. Cited workspace paths in citrate-federation plugin skills exist
     (local checkouts only; skipped in CI where the workspace is not present)
  7. Sprint-close completeness: every completed sprint has RETRO.md and a
     journal whose frontmatter `sprint:` matches the sprint's ID

Exit 0 = all checks pass. Exit 1 = at least one failure.
Every individual assertion is one counted check; the final count is the
repo's test-count ratchet axis (Rule 2).
"""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKELETON_TEMPLATES = ROOT.parent / "agentile" / ".agentile" / "templates"
TRIGGER_RE = re.compile(r"\bUse (when|at|after)\b")

results = []  # (ok, label, detail)


def check(ok, label, detail=""):
    results.append((bool(ok), label, detail))


def frontmatter(path):
    """Parse the simple 'key: value' YAML subset between --- markers."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return None  # unterminated block


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ── 1. marketplace + plugin metadata ────────────────────────────────
mp_path = ROOT / ".claude-plugin" / "marketplace.json"
try:
    mp = json.loads(mp_path.read_text(encoding="utf-8"))
except Exception as e:  # noqa: BLE001 - report, don't crash the harness
    check(False, "marketplace.json parses", str(e))
    mp = {"plugins": []}
else:
    check(True, "marketplace.json parses")
    for field in ("name", "owner", "metadata", "plugins"):
        check(field in mp, f"marketplace.json has '{field}'")

for entry in mp.get("plugins", []):
    pname = entry.get("name", "<unnamed>")
    for field in ("name", "version", "description", "source"):
        check(field in entry, f"marketplace plugin '{pname}' has '{field}'")
    src = ROOT / entry.get("source", "")
    check(src.is_dir(), f"plugin '{pname}' source dir exists", str(src))
    pj_path = src / ".claude-plugin" / "plugin.json"
    check(pj_path.is_file(), f"plugin '{pname}' has plugin.json")
    if pj_path.is_file():
        try:
            pj = json.loads(pj_path.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            check(False, f"plugin '{pname}' plugin.json parses", str(e))
        else:
            check(True, f"plugin '{pname}' plugin.json parses")
            check(pj.get("name") == pname, f"plugin '{pname}' name matches marketplace entry")
            check(
                pj.get("version") == entry.get("version"),
                f"plugin '{pname}' version matches marketplace entry",
                f"{pj.get('version')} vs {entry.get('version')}",
            )

# ── 2. SKILL.md frontmatter lint ────────────────────────────────────
skill_files = sorted(ROOT.glob("plugins/*/skills/*/SKILL.md"))
check(len(skill_files) > 0, "at least one SKILL.md found", f"found {len(skill_files)}")
for sf in skill_files:
    rel = sf.relative_to(ROOT)
    fm = frontmatter(sf)
    check(fm is not None, f"{rel}: frontmatter present and terminated")
    if fm is None:
        continue
    dirname = sf.parent.name
    check(fm.get("name") == dirname, f"{rel}: name matches directory", f"{fm.get('name')!r} vs {dirname!r}")
    desc = fm.get("description", "")
    check(len(desc) > 0, f"{rel}: description non-empty")
    check(TRIGGER_RE.search(desc), f"{rel}: description is a trigger condition ('Use when/at/after')")
    check(len(desc) <= 1024, f"{rel}: description <= 1024 chars", f"{len(desc)} chars")

# every skills/* directory must contain a SKILL.md
for d in sorted(ROOT.glob("plugins/*/skills/*")):
    if d.is_dir():
        check((d / "SKILL.md").is_file(), f"{d.relative_to(ROOT)}: contains SKILL.md")

# ── 3. Rule-12 frontmatter on .agentile docs ────────────────────────
for doc in sorted((ROOT / ".agentile").rglob("*.md")):
    rel = doc.relative_to(ROOT)
    fm = frontmatter(doc)
    check(fm is not None, f"{rel}: Rule-12 frontmatter present")
    if fm is None:
        continue
    for field in ("created", "branch", "author", "status"):
        check(field in fm and fm[field], f"{rel}: frontmatter '{field}' set")

# ── 4. vendored templates match templates.lock ──────────────────────
lock_path = ROOT / "templates.lock"
check(lock_path.is_file(), "templates.lock exists")
locked = {}
if lock_path.is_file():
    for line in lock_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            digest, rel = line.split(None, 1)
            locked[rel.strip()] = digest

vendored = sorted(ROOT.glob("plugins/*/skills/*/*_TEMPLATE.md"))
check(len(vendored) > 0, "vendored templates found", f"found {len(vendored)}")
for t in vendored:
    rel = str(t.relative_to(ROOT))
    check(rel in locked, f"{rel}: listed in templates.lock")
    if rel in locked:
        check(
            sha256(t) == locked[rel],
            f"{rel}: matches templates.lock (no in-place edits)",
            "re-vendor from the agentile skeleton and regenerate the lock",
        )
for rel in locked:
    check((ROOT / rel).is_file(), f"templates.lock entry exists on disk: {rel}")

# ── 5. drift vs skeleton (local only) ───────────────────────────────
if SKELETON_TEMPLATES.is_dir():
    for t in vendored:
        upstream = SKELETON_TEMPLATES / t.name
        check(upstream.is_file(), f"skeleton has {t.name}")
        if upstream.is_file():
            check(
                t.read_bytes() == upstream.read_bytes(),
                f"{t.relative_to(ROOT)}: byte-identical to skeleton",
                "upstream template changed — re-vendor and bump plugin version",
            )
else:
    print("note: agentile skeleton not found; drift-vs-skeleton checks skipped (CI mode)")

# ── 6. cited workspace paths in federation-plugin skills (local only) ─
# Backticked tokens containing '/' in citrate-federation SKILL.md files are
# treated as workspace-path citations and must exist under the workspace root
# (the parent directory holding citrate-labs' repos). Tokens with placeholders
# (<...>), globs, URLs, or generic per-repo .agentile/ paths are skipped.
WORKSPACE = ROOT.parent
CITED_RE = re.compile(r"`([^`\s]+/[^`\s]*)")

if (WORKSPACE / "citrate-federation").is_dir():
    for sf in sorted(ROOT.glob("plugins/citrate-federation/skills/*/SKILL.md")):
        rel = sf.relative_to(ROOT)
        seen = set()
        for m in CITED_RE.finditer(sf.read_text(encoding="utf-8")):
            cand = m.group(1).rstrip(".,;:")
            if cand in seen:
                continue
            seen.add(cand)
            if any(t in cand for t in ("<", ">", "*", "://")):
                continue
            if cand.startswith((".agentile/", "git@", "~")):
                continue
            p = cand[len("citrate-labs/"):] if cand.startswith("citrate-labs/") else cand
            check(
                (WORKSPACE / p).exists(),
                f"{rel}: cited path exists: {cand}",
                f"not found under {WORKSPACE}",
            )
else:
    print("note: federation workspace not found; cited-path checks skipped (CI mode)")

# ── 7. sprint-close completeness (journal-per-sprint tripwire) ──────
journal_sprints = set()
for j in (ROOT / ".agentile" / "docs" / "journals").glob("*.md"):
    fm = frontmatter(j)
    if fm and fm.get("sprint"):
        journal_sprints.add(fm["sprint"])

for sprint_dir in sorted((ROOT / ".agentile" / "sprints" / "completed").glob("*/*/")):
    rel = sprint_dir.relative_to(ROOT)
    check((sprint_dir / "RETRO.md").is_file(), f"{rel}: RETRO.md present")
    sprint_md = sprint_dir / "SPRINT.md"
    check(sprint_md.is_file(), f"{rel}: SPRINT.md present")
    if sprint_md.is_file():
        fm = frontmatter(sprint_md) or {}
        sprint_id = fm.get("sprint")
        check(bool(sprint_id), f"{rel}: SPRINT.md frontmatter has sprint id")
        if sprint_id:
            check(
                sprint_id in journal_sprints,
                f"{rel}: journal exists for sprint {sprint_id}",
                "minimum one journal per sprint — see agentile:journal",
            )

# ── report ──────────────────────────────────────────────────────────
failures = [r for r in results if not r[0]]
for ok, label, detail in results:
    if not ok:
        print(f"FAIL  {label}" + (f"  [{detail}]" if detail else ""))
print(f"\n{len(results) - len(failures)}/{len(results)} checks passed")
sys.exit(1 if failures else 0)
