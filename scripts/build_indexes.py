#!/usr/bin/env python3
"""Build paper-wiki index notes from MinerU .raw metadata and canonical notes."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass
class Paper:
    doc_id: str
    citekey: str
    item_key: str
    library_id: str
    title: str
    year: str
    venue: str
    status: str
    tags: list[str]
    note_path: str
    has_note: bool
    has_raw: bool


def main() -> int:
    parser = argparse.ArgumentParser(description="Build paper-wiki index notes.")
    parser.add_argument("--vault", default=os.environ.get("VAULT_ROOT"), help="Obsidian vault root")
    parser.add_argument("--library-id", help="Only build one library index")
    parser.add_argument("--dry-run", action="store_true", help="Print target files without writing")
    args = parser.parse_args()

    if not args.vault:
        raise SystemExit("VAULT_ROOT is not set; pass --vault")
    vault = Path(args.vault).expanduser()
    if not vault.is_dir():
        raise SystemExit(f"Vault does not exist: {vault}")

    papers = load_papers(vault)
    if args.library_id:
        papers = [p for p in papers if p.library_id == str(args.library_id)]

    writes = build_indexes(vault, papers, dry_run=args.dry_run)
    for target in writes:
        print(target)
    return 0


def load_papers(vault: Path) -> list[Paper]:
    raw_docs = _load_raw_docs(vault)
    note_docs = _load_note_docs(vault)
    doc_ids = sorted(set(raw_docs) | set(note_docs))
    papers = [_merge_paper(doc_id, raw_docs.get(doc_id, {}), note_docs.get(doc_id, {})) for doc_id in doc_ids]
    return sorted(papers, key=lambda p: (p.library_id, p.year, p.citekey), reverse=True)


def build_indexes(vault: Path, papers: list[Paper], *, dry_run: bool = False) -> list[str]:
    notes_dir = vault / "notes"
    targets: list[tuple[Path, str]] = [(notes_dir / "_index.md", render_index("All Papers", "all", papers))]

    by_library: dict[str, list[Paper]] = defaultdict(list)
    for paper in papers:
        by_library[paper.library_id or "unknown"].append(paper)
    for library_id, library_papers in sorted(by_library.items()):
        targets.append((
            notes_dir / "libraries" / f"lib-{library_id}" / "index.md",
            render_index(f"Library lib-{library_id}", f"library:lib-{library_id}", library_papers),
        ))

    written = []
    for path, content in targets:
        written.append(path.relative_to(vault).as_posix())
        if dry_run:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return written


def render_index(title: str, scope: str, papers: list[Paper]) -> str:
    today = date.today().isoformat()
    lines = [
        "---",
        "type: index",
        f'title: "{title}"',
        f'scope: "{scope}"',
        f"updated: {today}",
        "tags:",
        "  - paper-index",
        "---",
        "",
        f"# {title}",
        "",
        f"Updated: {today}",
        "",
        "## Papers",
        "",
        "| Paper | Year | Venue | Status | Tags | Zotero |",
        "|---|---:|---|---|---|---|",
    ]
    for paper in papers:
        tags = ", ".join(paper.tags)
        zotero = f"[Zotero](zotero://select/library/items/{paper.item_key})" if paper.item_key else ""
        lines.append(
            f"| [[{paper.note_path}|{_table(paper.citekey)}]] | {_table(paper.year)} | "
            f"{_table(paper.venue)} | {_table(paper.status)} | {_table(tags)} | {zotero} |"
        )

    missing_notes = [p for p in papers if not p.has_note]
    missing_raw = [p for p in papers if not p.has_raw]
    lines.extend(["", "## Gaps", ""])
    if not missing_notes and not missing_raw:
        lines.append("- None.")
    else:
        if missing_notes:
            lines.append("- Parsed but no canonical note:")
            lines.extend(f"  - `{p.doc_id}` citekey=`{p.citekey}`" for p in missing_notes)
        if missing_raw:
            lines.append("- Note but no parse artifacts:")
            lines.extend(f"  - `{p.note_path}`" for p in missing_raw)
    lines.append("")
    return "\n".join(lines)


def _load_raw_docs(vault: Path) -> dict[str, dict[str, Any]]:
    raw = vault / ".raw"
    docs: dict[str, dict[str, Any]] = {}
    if not raw.is_dir():
        return docs
    for meta_file in raw.glob("**/meta.json"):
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
        except Exception:
            continue
        doc_id = str(meta.get("doc_id") or meta_file.parent.relative_to(raw).as_posix())
        docs[doc_id] = meta
    return docs


def _load_note_docs(vault: Path) -> dict[str, dict[str, Any]]:
    notes = vault / "notes"
    docs: dict[str, dict[str, Any]] = {}
    if not notes.is_dir():
        return docs
    for note in notes.glob("lib-*/*/*.md"):
        if note.name == "index.md":
            continue
        frontmatter = _read_frontmatter(note)
        doc_id = str(frontmatter.get("doc_id") or "/".join(note.relative_to(notes).parts[:2]))
        frontmatter["note_path"] = note.relative_to(vault).as_posix()
        docs[doc_id] = frontmatter
    return docs


def _merge_paper(doc_id: str, raw: dict[str, Any], note: dict[str, Any]) -> Paper:
    citekey = str(note.get("citekey") or raw.get("citekey") or doc_id.rsplit("/", 1)[-1])
    item_key = str(note.get("item_key") or raw.get("item_key") or doc_id.rsplit("/", 1)[-1])
    library_id = str(note.get("library_id") or raw.get("library_id") or _library_from_doc_id(doc_id))
    note_path = str(note.get("note_path") or f"notes/{doc_id}/{citekey}.md")
    status = str(note.get("status") or ("missing-note" if not note else "seed"))
    return Paper(
        doc_id=doc_id,
        citekey=citekey,
        item_key=item_key,
        library_id=library_id,
        title=str(note.get("title") or raw.get("title") or citekey),
        year=str(note.get("year") or raw.get("year") or ""),
        venue=str(note.get("venue") or raw.get("venue") or ""),
        status=status,
        tags=_as_list(note.get("tags")),
        note_path=note_path,
        has_note=bool(note),
        has_raw=bool(raw),
    )


def _read_frontmatter(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    return _parse_simple_yaml(text[4:end])


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(_clean_scalar(line[4:]))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        value = value.strip()
        data[current_key] = [] if value == "" else _clean_scalar(value)
    return data


def _clean_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if str(v)]
    return [str(value)]


def _library_from_doc_id(doc_id: str) -> str:
    first = doc_id.split("/", 1)[0]
    return first.removeprefix("lib-")


def _table(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
