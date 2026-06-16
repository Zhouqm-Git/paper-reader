---
name: paper-wiki
description: "Legacy standalone paper-reader package. Use only to redirect paper reading, Zotero PDF parsing, MinerU evidence extraction, paper wiki indexing, cross-paper QA, or paper comparison work to the canonical Zotero-aware implementation in mineru-zotero-mcp/skills/paper-wiki and the claude-obsidian paper-wiki adapter."
---

# paper-reader Legacy Redirect

This standalone package has been migrated.

Use the canonical implementation instead:

```text
../mineru-zotero-mcp/skills/paper-wiki
../mineru-zotero-mcp/commands/paper-wiki.md
../mineru-zotero-mcp/agents/paper-wiki-ingest.md
../claude-obsidian/skills/paper-wiki
```

The active architecture is Zotero-aware:

```text
.raw/<doc_id>/                                           MinerU parse/cache artifacts
attachments/papers/<doc_id>/                             visible figures/captures
wiki/sources/zotero/index.md                             all indexed papers
wiki/sources/zotero/lib-<libraryID>/index.md             one Zotero library index
wiki/sources/zotero/lib-<libraryID>/items/<item_key>.md   canonical paper source page
wiki/sources/zotero/lib-<libraryID>/collections/.../index.md
                                                          Zotero collection folder indexes
wiki/questions/<slug>.md                                 cross-paper answers
wiki/comparisons/<slug>.md                               comparison matrices
```

Do not use this package's old `notes/` layout for claude-obsidian vaults. Do not create a second paper wiki outside `mineru-zotero-mcp` and `claude-obsidian`.
