#!/usr/bin/env python3
"""Structural checks for the skill: local Markdown links resolve, and every
eval case has exactly one rubric section. Run from anywhere: python3 scripts/check.py"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
LINK = re.compile(r"\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.S | re.M)


def check_links() -> list[str]:
    errors = []
    for md in sorted(ROOT.glob("**/*.md")):
        if ".git" in md.parts or ".claude" in md.parts:
            continue
        text = FENCE.sub("", md.read_text(encoding="utf-8"))
        for target in LINK.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if not (md.parent / path).exists():
                errors.append(f"{md.relative_to(ROOT)}: broken link {target}")
    return errors


def check_evals() -> list[str]:
    errors = []
    with open(EVALS / "universal-engineering-standard.prompts.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ids = [r["id"] for r in rows]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"prompts.csv: duplicate id {dup}")
    for r in rows:
        if r["should_trigger"] not in ("true", "false"):
            errors.append(f"prompts.csv: {r['id']} should_trigger must be true or false")
        if not r["prompt"].strip():
            errors.append(f"prompts.csv: {r['id']} has an empty prompt")
    sections = re.findall(r"^## (\S+)\s*$", (EVALS / "behavior-rubric.md").read_text(encoding="utf-8"), re.M)
    for dup in sorted({s for s in sections if sections.count(s) > 1}):
        errors.append(f"behavior-rubric.md: duplicate section {dup}")
    for missing in sorted(set(ids) - set(sections)):
        errors.append(f"behavior-rubric.md: no section for case {missing}")
    for extra in sorted(set(sections) - set(ids)):
        errors.append(f"behavior-rubric.md: section {extra} has no case")
    return errors


if __name__ == "__main__":
    errors = check_links() + check_evals()
    for e in errors:
        print(e, file=sys.stderr)
    print(f"{len(errors)} error(s)")
    sys.exit(1 if errors else 0)
