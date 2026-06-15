# Frontmatter Schema for Paper Notes

Every paper note starts with flat YAML frontmatter. No nested objects (Obsidian Properties UI requires flat structure).

## Full Schema

```yaml
---
type: source
source_type: paper
title: "Full Paper Title"
citekey: smith2024              # BetterBibTeX citation key — primary key for wikilinks
item_key: AB12CD34              # Zotero 8-char item key — for zotero-mcp calls
authors:
  - "First Author"
  - "Second Author"
year: 2024
venue: "NeurIPS"               # conference/journal, or "arXiv" for preprints
url: "https://arxiv.org/abs/..."
pdf: "[[raw/smith2024/smith2024.md]]"   # link to MinerU-parsed markdown
status: seed                    # seed | developing | mature | evergreen
paper_type: empirical           # empirical | theoretical | survey | system
key_claims:
  - "First key claim in one sentence"
  - "Second key claim"
confidence: medium              # high | medium | low — your confidence in the judgment
created: 2026-06-15
updated: 2026-06-15
tags:
  - paper
  - <topic-tag>
related:                        # wikilinks to other paper notes
  - "[[other2023]]"
---
```

## Field Rules

| Field | Required | Notes |
|---|---|---|
| `type` | ✅ | Always `source` |
| `source_type` | ✅ | Always `paper` |
| `title` | ✅ | Full paper title in quotes |
| `citekey` | ✅ | BBT citation key; used as filename and wikilink target |
| `item_key` | ✅ | Zotero item key; needed for `zotero_create_note` etc. |
| `authors` | ✅ | List of full names |
| `year` | ✅ | 4-digit year |
| `venue` | ✅ | Conference/journal name, or `arXiv` |
| `url` | ✅ | Paper URL |
| `pdf` | ✅ | Wikilink to the parsed markdown in `raw/` |
| `status` | ✅ | `seed` on first write; advance as you revisit |
| `paper_type` | ✅ | Determines which template was used |
| `key_claims` | ✅ | 2-4 one-sentence claims (not summary — your distilled claims) |
| `confidence` | optional | How confident are you in your judgment? Default `medium` |
| `created` / `updated` | ✅ | `YYYY-MM-DD`; update `updated` on every edit |
| `tags` | ✅ | Start with `paper`, add topic tags |
| `related` | optional | Wikilinks to related papers in the vault |

## Status Lifecycle

- **seed**: first pass, note exists but may be incomplete
- **developing**: real content, evidence-backed, but not yet comprehensive
- **mature**: comprehensive analysis, well-linked to other papers
- **evergreen**: unlikely to need updates (foundational paper you fully understand)

## Better Notes Compatibility

When Better Notes Auto-Sync is enabled, it injects an additional `$version` field into the frontmatter during the first sync:

```yaml
$version: 42
```

**Do not manually edit or remove `$version`** — it drives Better Notes' bidirectional conflict detection (MD5 + version comparison). If the field is present, leave it; if absent (no sync configured), don't add it.
