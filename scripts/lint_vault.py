#!/usr/bin/env python3
"""Lint a paper-wiki vault for missing links between notes, raw artifacts, and embeds."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

from build_indexes import _read_frontmatter

_EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]")
_REQUIRED = ("type", "source_type", "title", "doc_id", "citekey", "item_key", "status", "paper_type")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint paper-wiki vault consistency.")
    parser.add_argument("--vault", default=os.environ.get("VAULT_ROOT"), help="Obsidian vault root")
    args = parser.parse_args()
    if not args.vault:
        raise SystemExit("VAULT_ROOT is not set; pass --vault")
    vault = Path(args.vault).expanduser()
    if not vault.is_dir():
        raise SystemExit(f"Vault does not exist: {vault}")

    issues = lint(vault)
    print(render_report(issues))
    return 1 if any(i[0] == "FAIL" for i in issues) else 0


def lint(vault: Path) -> list[tuple[str, str, str]]:
    issues: list[tuple[str, str, str]] = []
    notes = _canonical_notes(vault)
    if not notes:
        issues.append(("WARN", "notes", "no canonical notes under notes/lib-*/*/*.md"))
    for note in notes:
        _lint_note(vault, note, issues)

    if not (vault / "notes" / "_index.md").is_file():
        issues.append(("WARN", "notes/_index.md", "missing; run scripts/build_indexes.py"))
    return issues


def render_report(issues: list[tuple[str, str, str]]) -> str:
    counts = {s: sum(1 for i in issues if i[0] == s) for s in ("OK", "WARN", "FAIL")}
    lines = [
        "# paper-wiki lint",
        "",
        f"Summary: {counts['OK']} OK, {counts['WARN']} WARN, {counts['FAIL']} FAIL",
        "",
        "| Status | Check | Detail |",
        "|---|---|---|",
    ]
    for status, check, detail in issues:
        lines.append(f"| {status} | {_table(check)} | {_table(detail)} |")
    return "\n".join(lines)


def _canonical_notes(vault: Path) -> list[Path]:
    notes = vault / "notes"
    if not notes.is_dir():
        return []
    return sorted(p for p in notes.glob("lib-*/*/*.md") if p.name != "index.md")


def _lint_note(vault: Path, note: Path, issues: list[tuple[str, str, str]]) -> None:
    rel = note.relative_to(vault).as_posix()
    fm = _read_frontmatter(note)
    missing = [key for key in _REQUIRED if not fm.get(key)]
    if missing:
        issues.append(("FAIL", rel, "missing frontmatter: " + ", ".join(missing)))
    else:
        issues.append(("OK", rel, "frontmatter complete"))

    doc_id = str(fm.get("doc_id") or "/".join(note.relative_to(vault / "notes").parts[:2]))
    raw_dir = vault / ".raw" / doc_id
    if not raw_dir.is_dir():
        issues.append(("FAIL", rel, f"missing raw artifacts: .raw/{doc_id}"))
    elif not (raw_dir / "anchors.json").is_file():
        issues.append(("FAIL", rel, f"missing anchors: .raw/{doc_id}/anchors.json"))
    else:
        issues.append(("OK", rel, f"raw artifacts present: .raw/{doc_id}"))

    try:
        text = note.read_text(encoding="utf-8")
    except OSError as e:
        issues.append(("FAIL", rel, f"cannot read note: {e}"))
        return
    for embed in _EMBED_RE.findall(text):
        target = vault / embed
        if not target.exists():
            issues.append(("FAIL", rel, f"missing embed: {embed}"))


def _table(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
