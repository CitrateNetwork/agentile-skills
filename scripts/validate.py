#!/usr/bin/env python3
"""Validation harness for agentile-skills (SKILLS-S0 WP-3).

Canonical test command:  python3 scripts/validate.py

Checks, in order:
  1. marketplace.json / plugin.json schema + cross-consistency, and every
     author.url / owner url resolves inside the CitrateNetwork org (AGS-B-006)
  2. SKILL.md frontmatter lint (name == directory, trigger-phrase description)
  3. Rule-12 frontmatter on every .agentile/ doc
  4. Vendored-template integrity vs templates.lock (catches in-place edits)
  5. Vendored-template drift vs the agentile skeleton (armed by an adjacent
     `agentile` checkout; when absent the family is emitted as SKIP entries
     that still count toward the denominator — AGS-B-004)
  6. Cited workspace paths in citrate-federation plugin skills exist. Armed
     ONLY by an explicit `--workspace <path>`; without it the citations are
     still enumerated and emitted as SKIP entries (so the denominator is
     stable and no stray sibling directory can arm the check — AGS-B-004)
  7. Sprint-close completeness: every completed sprint has RETRO.md and a
     journal whose frontmatter `sprint:` matches the sprint's ID
  8. Skill-body content gate: no skill body may ship credential-file paths,
     shell-exfiltration idioms, or destructive commands without an explicit
     `<!-- canon-allow -->` marker on the line (AGS-B-003)
  9. Check-count ratchet: the number of checks must not fall below
     `checks.baseline` (AGS-B-007). Regenerate deliberately with
     `--update-baseline` after a reviewed change to the check set.

Flags:
  --workspace <path>   arm §6 against a real federation workspace root
  --require-full       exit 1 if any check family was skipped
  --update-baseline    rewrite checks.baseline to the current check count

Exit 0 = all checks pass. Exit 1 = at least one failure (or a skip under
--require-full). Skipped checks are counted in the denominator and reported
separately, so a green line always states which families actually ran.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRIGGER_RE = re.compile(r"\bUse (when|at|after)\b")

# ── argv ────────────────────────────────────────────────────────────
ARGS = sys.argv[1:]
REQUIRE_FULL = "--require-full" in ARGS
UPDATE_BASELINE = "--update-baseline" in ARGS
WORKSPACE_ARG = None
if "--workspace" in ARGS:
    i = ARGS.index("--workspace")
    if i + 1 < len(ARGS):
        WORKSPACE_ARG = Path(ARGS[i + 1]).resolve()

# An adjacent `agentile` checkout is the upstream skeleton source for §5.
SKELETON_TEMPLATES = ROOT.parent / "agentile" / ".agentile" / "templates"

results = []  # (state, label, detail) — state is True | False | "skip"


def check(ok, label, detail=""):
    results.append((bool(ok), label, detail))


def skip(label, detail=""):
    results.append(("skip", label, detail))


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


def in_citrate_org(url):
    """True iff a GitHub URL resolves inside github.com/CitrateNetwork."""
    if not isinstance(url, str):
        return False
    m = re.match(r"^https://github\.com/([^/]+)", url.strip())
    return bool(m) and m.group(1).lower() == "citratenetwork"


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
    # AGS-B-006: an org-owned marketplace must not point provenance at a
    # personal account. owner.url (if present) must be inside the org.
    owner_url = (mp.get("owner") or {}).get("url")
    if owner_url is not None:
        check(in_citrate_org(owner_url),
              "marketplace.json owner.url is inside CitrateNetwork",
              str(owner_url))

for entry in mp.get("plugins", []):
    pname = entry.get("name", "<unnamed>")
    for field in ("name", "version", "description", "source"):
        check(field in entry, f"marketplace plugin '{pname}' has '{field}'")
    # AGS-B-006: author.url is the identity a consumer follows to decide
    # whether to trust the plugin; it must resolve to the publishing org.
    author_url = (entry.get("author") or {}).get("url")
    if author_url is not None:
        check(in_citrate_org(author_url),
              f"marketplace plugin '{pname}' author.url is inside CitrateNetwork",
              str(author_url))
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
            pj_author_url = (pj.get("author") or {}).get("url")
            if pj_author_url is not None:
                check(in_citrate_org(pj_author_url),
                      f"plugin '{pname}' plugin.json author.url is inside CitrateNetwork",
                      str(pj_author_url))

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

# ── 5. drift vs skeleton ────────────────────────────────────────────
# Armed by an adjacent `agentile` checkout. When it is absent the family is
# emitted as SKIP entries — one per (exists, byte-identical) assertion per
# vendored template — so the denominator is identical in every environment
# and a green line names what did not run (AGS-B-004).
skeleton_present = SKELETON_TEMPLATES.is_dir()
for t in vendored:
    rel = t.relative_to(ROOT)
    if skeleton_present:
        upstream = SKELETON_TEMPLATES / t.name
        check(upstream.is_file(), f"skeleton has {t.name}")
        if upstream.is_file():
            check(
                t.read_bytes() == upstream.read_bytes(),
                f"{rel}: byte-identical to skeleton",
                "upstream template changed — re-vendor and bump plugin version",
            )
        else:
            skip(f"{rel}: byte-identical to skeleton", "skeleton missing this template")
    else:
        skip(f"skeleton has {t.name}", "no adjacent agentile checkout")
        skip(f"{rel}: byte-identical to skeleton", "no adjacent agentile checkout")
if not skeleton_present:
    print("note: agentile skeleton not found; drift-vs-skeleton checks SKIPPED "
          "(counted, run with an adjacent `agentile` checkout to arm)")

# ── 6. cited workspace paths in federation-plugin skills ─────────────
# Backticked tokens containing '/' in citrate-federation SKILL.md files are
# treated as workspace-path citations. Existence is verified ONLY against an
# explicit --workspace <path>; without the flag each citation is emitted as a
# SKIP (never auto-armed off an ambient sibling directory — AGS-B-004). The
# citation set is enumerated the same way in both modes, so the denominator
# does not move with the filesystem.
CITED_RE = re.compile(r"`([^`\s]+/[^`\s]*)")
workspace_armed = WORKSPACE_ARG is not None and WORKSPACE_ARG.is_dir()

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
        if workspace_armed:
            p = cand[len("citrate-labs/"):] if cand.startswith("citrate-labs/") else cand
            check(
                (WORKSPACE_ARG / p).exists(),
                f"{rel}: cited path exists: {cand}",
                f"not found under {WORKSPACE_ARG}",
            )
        else:
            skip(f"{rel}: cited path exists: {cand}", "no --workspace given")
if not workspace_armed:
    print("note: no --workspace given; federation cited-path checks SKIPPED "
          "(counted, pass --workspace <path> to arm)")

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

# ── 8. skill-body content gate (AGS-B-003) ──────────────────────────
# Skill bodies become instructions in a consumer's agent session. Frontmatter
# lint (§2) never looks at the body. This gate fails the harness if a body
# ships a credential-file path, a shell-exfiltration idiom, or a destructive
# command. A line may opt out with an explicit `<!-- canon-allow -->` marker,
# which is the reviewed record that a human decided the mention is legitimate.
DANGER_PATTERNS = [
    (r"~/\.aws\b", "home AWS credentials path"),
    (r"~/\.ssh\b", "home SSH key path"),
    (r"~/\.gnupg\b", "home GnuPG key path"),
    (r"~/\.config/gh\b", "home gh credential path"),
    (r"\baws/credentials\b", "AWS credentials file"),
    (r"\bid_rsa\b", "private SSH key file"),
    (r"\bid_ed25519\b", "private SSH key file"),
    (r"curl\b[^\n|]*\|\s*(ba)?sh\b", "curl piped into a shell"),
    (r"wget\b[^\n|]*\|\s*(ba)?sh\b", "wget piped into a shell"),
    (r"base64\s+-d[^\n|]*\|\s*(ba)?sh\b", "base64-decoded payload piped into a shell"),
    (r"\beval\s*\$\(", "eval of a command substitution"),
    (r"rm\s+-rf\s+[~/]", "destructive rm -rf on an absolute/home path"),
]
DANGER_RE = [(re.compile(p, re.IGNORECASE), why) for p, why in DANGER_PATTERNS]
ALLOW_MARKER = "canon-allow"

for sf in skill_files:
    rel = sf.relative_to(ROOT)
    body_lines = sf.read_text(encoding="utf-8").splitlines()
    hits = []
    for lineno, line in enumerate(body_lines, start=1):
        if ALLOW_MARKER in line:
            continue
        for rx, why in DANGER_RE:
            if rx.search(line):
                hits.append(f"{rel}:{lineno} {why}")
    check(not hits, f"{rel}: body has no ungated dangerous idiom",
          "; ".join(hits) if hits else "")

# ── 9. check-count ratchet (AGS-B-007) ──────────────────────────────
# The denominator is stable across environments (§5/§6 skips are counted), so
# it is a real ratchet: it must never silently drop. Regenerate deliberately
# with --update-baseline after a reviewed change to the check set.
baseline_path = ROOT / "checks.baseline"
pre_ratchet_total = len(results)
if UPDATE_BASELINE:
    baseline_path.write_text(f"{pre_ratchet_total}\n", encoding="utf-8")
    print(f"checks.baseline updated to {pre_ratchet_total}.")

baseline = None
if baseline_path.is_file():
    txt = baseline_path.read_text(encoding="utf-8").strip()
    if txt.isdigit():
        baseline = int(txt)
if baseline is None:
    skip("check-count ratchet vs checks.baseline", "checks.baseline missing or unreadable")
else:
    check(pre_ratchet_total >= baseline,
          f"check count {pre_ratchet_total} >= baseline {baseline} (ratchet)",
          "check count fell below baseline — this is a ratchet, it must not go down")

# ── report ──────────────────────────────────────────────────────────
failures = [r for r in results if r[0] is False]
skipped = [r for r in results if r[0] == "skip"]
passed = [r for r in results if r[0] is True]

for state, label, detail in results:
    if state is False:
        print(f"FAIL  {label}" + (f"  [{detail}]" if detail else ""))

mode = "full" if not skipped else "partial"
print(f"\nmode={mode} checks={len(results)} passed={len(passed)} "
      f"failed={len(failures)} skipped={len(skipped)}")
print(f"{len(passed)}/{len(results)} checks passed"
      + (f", {len(skipped)} skipped" if skipped else ""))

exit_bad = bool(failures) or (REQUIRE_FULL and bool(skipped))
if REQUIRE_FULL and skipped:
    print(f"--require-full: {len(skipped)} check(s) were skipped; failing.")
sys.exit(1 if exit_bad else 0)
