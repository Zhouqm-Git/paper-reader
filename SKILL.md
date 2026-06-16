---
name: paper-reader
description: "Read a Zotero paper via MinerU and write a structured analysis note in the Obsidian vault. Parses the PDF, collects evidence (text/tables/figures), highlights key passages as Zotero annotations, analyzes by rubric, then synthesizes a note. Triggers on: read this paper, analyze this paper, write a note for this paper, review this paper, paper-reader."
---

# paper-reader: Evidence-Grounded Paper Reading

Read a Zotero paper end-to-end via MinerU, judge it by a technical rubric, and write a structured analysis note — every claim backed by a real page reference, GFM table, figure, or clickable Zotero annotation.

**Single source of truth for paper notes**: the note lives in the Obsidian vault at `notes/<doc_id>/<citekey>.md`. `doc_id` is the MinerU parse identity returned by `mineru_parse_pdf` (`lib-<libraryID>/<item_key>`), not the citekey. MinerU parse/cache artifacts live in hidden `.raw/<doc_id>/`; user-facing figure and region images live in `attachments/papers/<doc_id>/`. Better Notes (optional) mirrors the note back to Zotero for backup and search. Zotero annotations (highlights) created during analysis are clickable from the note via `zotero://` links.

## Prerequisites

- **mineru-zotero-mcp** server: `mineru_parse_pdf`, `mineru_read_markdown`, `mineru_list_anchors`, `mineru_resolve_anchor`, `mineru_list_visual_candidates`, `mineru_create_evidence_annotation`, `mineru_capture_region`, `mineru_check_quota`, `mineru_parse_batch`.
- **zotero-mcp** server: `zotero_create_annotation`, `zotero_create_area_annotation`, `zotero_get_item_children`, `zotero_get_annotations`, `zotero_create_note`, `zotero_search_by_citation_key`.
- Vault root set via `VAULT_ROOT` env. Papers parse to `.raw/<doc_id>/`; figures/captures go to `attachments/papers/<doc_id>/`; notes go to `notes/<doc_id>/<citekey>.md`.
- Obsidian syntax follows the [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) `obsidian-markdown` skill if installed; otherwise standard OFM.

---

## The 4-Phase Workflow

```
Phase 1: INTAKE     parse the PDF, read the abstract, classify the paper type
Phase 2: EVIDENCE   read deeply, collect tables/figures/text, highlight in Zotero
Phase 3: ANALYZE    judge each rubric dimension with evidence backing
Phase 4: WRITE      synthesize the note from the template, write to vault
```

The golden rule across all phases: **never write a claim you cannot point to a page, table, figure, or annotation for.** See [`references/evidence-discipline.md`](references/evidence-discipline.md).

---

### Phase 1 — Intake

**Goal**: get the paper parsed and classified.

1. **Parse**:
   ```
   mineru_parse_pdf(item_key="CFSHQZRJ")
   # or
   mineru_parse_pdf(citekey="smith2024")
   ```
   Confirm and record the returned `doc_id`, `cached: True/False`, page count, table count. If an item key is ambiguous across Zotero libraries, re-run with `library_id=<id>`.

2. **Read the opening** to classify:
   ```
   mineru_read_markdown(doc_id="lib-1/CFSHQZRJ", max_chars=4000)
   ```
   Look at abstract + introduction. Determine `paper_type`:
   - **empirical**: has datasets, baselines, ablation studies, metrics tables
   - **theoretical**: has definitions, theorems, proofs, complexity analysis
   - **survey**: reviews many papers, has taxonomy/comparison tables
   - **system**: describes a system design, engineering tradeoffs, benchmarks

3. **Select template** from `templates/<paper_type>.md`. If unsure, default to `empirical.md`.

4. Record in your working memory: `doc_id`, `citekey`, `item_key`, `paper_type`, `title`, page count.

> For batch: run `mineru_check_quota` first, then `mineru_parse_batch`.

---

### Phase 2 — Evidence

**Goal**: collect real evidence AND leave Zotero highlights on the PDF. Do NOT write the note yet. Do NOT fabricate.

1. **Read deeply** — page by page or by section:
   ```
   mineru_read_markdown(doc_id="lib-1/CFSHQZRJ", page=3)
   mineru_read_markdown(doc_id="lib-1/CFSHQZRJ", page=5)
   ```

2. **Find key tables** — tables are GFM markdown (not images), ready to cite:
   ```
   mineru_list_anchors(doc_id="lib-1/CFSHQZRJ", kind="table")
   mineru_resolve_anchor(doc_id="lib-1/CFSHQZRJ", anchor_id="a_table_p6_0000")
   → returns markdownTable (GFM) — capture this for the note
   ```

3. **Survey figures** — the figure catalog gives caption + location + path:
   ```
   mineru_list_visual_candidates(doc_id="lib-1/CFSHQZRJ")
   → each figure already merged (fragments auto-joined during parse)
   → decide which figures are worth embedding (use caption + nearby text)
   ```
   For figures you want in the note, note their `imagePath` (e.g. `attachments/papers/lib-1/CFSHQZRJ/fig_a_image_p3_0005.png`).

4. **Highlight key passages in Zotero** (recommended for `full` mode) — creates clickable traceability from note to PDF:
   ```
   # Use anchor ids gathered from mineru_list_anchors / mineru_resolve_anchor.
   # Text/list anchors become text highlights; image/table/equation anchors become area annotations.
   mineru_create_evidence_annotation(
     doc_id="lib-1/CFSHQZRJ",
     anchor_id="a_text_p3_0002",
     comment="core method — cite in contribution section",
     mode="auto"
   )
   ```
   Only highlight passages/regions you'll actually reference in the note. The tool resolves the Zotero PDF `attachment_key`, page, text, and bbox automatically.

   **Annotation color convention** — the agent MUST use a distinct color so its highlights are visually separable from the user's own:

   | Color | Hex | Who |
   |---|---|---|
   | **Purple** | `#a28ae5` | **Agent** (default for `mineru_create_evidence_annotation`) |
   | Yellow | `#ffd400` | User (Zotero default) |
   | Red | `#ff6666` | User (important) |
   | Green | `#5fb236` | User |

   This way the user can instantly tell agent highlights from their own in Zotero. Override only if the user explicitly asks for a different color.

5. **Build the evidence ledger** in memory:
   ```
   {
     "contribution":  [(claim, "p.2", "original text fragment", "ANNOTATIONKEY")],
     "evidence":      [(claim, "Table 1", GFM table content)],
     "figures":       [(caption, "p.5", imagePath, optional annotation_key)],
     "strengths":     [(observation, "p.N", optional annotation_key)],
     "risks":         [(concern, "p.N")]
   }
   ```
   Every entry MUST have a source. If you created a Zotero annotation, record its `annotation_key` so the note can link back to it.

> See [`references/evidence-discipline.md`](references/evidence-discipline.md) for the anti-hallucination rules.

---

### Phase 3 — Analyze

**Goal**: judge the paper across rubric dimensions. No tools called — pure reasoning over the evidence ledger.

Score each of the 8 dimensions (see [`references/analysis-rubric.md`](references/analysis-rubric.md)):

| Dimension | What to ask |
|---|---|
| Problem clarity | Is the problem well-defined? Why does it matter? |
| Method soundness | Is the approach technically correct? Novel? |
| Evidence strength | Do experiments/proofs actually support the claims? |
| Reproducibility | Could someone reproduce this? Code? Data? Hyperparams? |
| Generalizability | Will this transfer beyond the specific setting? |
| Limitations honesty | Does the paper acknowledge its own weaknesses? |
| Positioning | How does it improve on prior work? Is the comparison fair? |
| Writing quality | Is it clearly written? Are figures/tables informative? |

For each dimension: write 1-3 sentences of judgment + attach evidence (page/table/figure/annotation).

---

### Phase 4 — Write

**Goal**: synthesize the note from the template and write it to the vault.

1. **Fill the template** (`templates/<paper_type>.md`). Every section must have evidence.

2. **Citation format** (portable, no private syntax):
   - Text evidence: `> original fragment (p.3)` — blockquote with page
   - Tables: inline the GFM table directly (from `resolve_anchor`)
   - Figures: `![[attachments/papers/<doc_id>/fig_xxx.png]]` — Obsidian embed of the auto-merged figure
   - Equations: `$LaTeX$` inline (from anchor `textFormat`)
   - Cross-reference: use the note path or alias, e.g. `[[notes/lib-1/CFSHQZRJ/smith2024|smith2024]]`
   - **Zotero deep links** (clickable in Obsidian — opens Zotero and navigates):
     - Jump to paper item: `[Zotero](zotero://select/library/items/ITEMKEY)` — use `item_key` from frontmatter
     - Jump to an annotation: `(p.3, [annot](zotero://select/library/items/ANNOTATIONKEY))` — use the annotation key from Phase 2
     - These work because Zotero registers the `zotero://` URL scheme system-wide

3. **Frontmatter** — use the schema in [`references/frontmatter.md`](references/frontmatter.md). Required: `doc_id`, `citekey`, `item_key`, `paper_type`, `key_claims`, `status`.

4. **Write to vault**:
   ```
   notes/<doc_id>/<citekey>.md
   ```

5. **Optional — Zotero sync** (tell the user, don't auto-do it):
   > "Note written to `notes/<doc_id>/<citekey>.md`. To enable Zotero two-way sync via Better Notes: open Zotero → select this paper's note → right-click → Better Notes → Set Auto-Sync → choose `notes/<doc_id>/<citekey>.md`."

---

## Available MCP Tools

### mineru-zotero-mcp (parsing + evidence extraction)

| Tool | Phase | Purpose |
|---|---|---|
| `mineru_parse_pdf` | Intake | Parse one Zotero PDF → `.raw/<doc_id>/` + `attachments/papers/<doc_id>/` |
| `mineru_parse_batch` | Intake | Batch parse (checks quota first) |
| `mineru_check_quota` | Intake | Estimate remaining MinerU quota |
| `mineru_read_markdown` | Intake, Evidence | Read parsed md by `doc_id`, optionally by page |
| `mineru_list_anchors` | Evidence | List text/image/table/equation anchors by `doc_id` |
| `mineru_resolve_anchor` | Evidence | Get one anchor's detail by `doc_id` (tables → GFM) |
| `mineru_list_visual_candidates` | Evidence | Figure catalog by `doc_id` (caption + path + context) |
| `mineru_create_evidence_annotation` | Evidence | Create a Zotero annotation from `doc_id + anchor_id` |
| `mineru_capture_region` | Evidence | Render a formula/table/text region as PNG under `attachments/papers/<doc_id>/` |

### zotero-mcp (annotations + notes + metadata)

| Tool | Phase | Purpose |
|---|---|---|
| `zotero_get_item_children` | Evidence | Low-level fallback: get attachment_key |
| `zotero_create_annotation` | Evidence | Low-level fallback: highlight a text passage |
| `zotero_create_area_annotation` | Evidence | Low-level fallback: box a PDF region |
| `zotero_get_annotations` | Evidence | Read existing Zotero annotations |
| `zotero_create_note` | Write | Create a Zotero note item (for Better Notes sync) |
| `zotero_search_by_citation_key` | Intake | Look up item_key from a citekey |

**Division of labor**: mineru-zotero-mcp parses + extracts evidence and provides `mineru_create_evidence_annotation` as the high-level bridge from anchors to Zotero annotations. zotero-mcp still owns the low-level Zotero writes, notes, metadata, and search.

---

## Modes

- **full** (default): complete deep read + Zotero highlights + 8-dimension analysis. Use for papers central to your research.
- **quick**: read abstract + intro + conclusion + main table only. 300-800 word note, skip annotation creation. Use for surveying many papers.
- **figures**: focus on `list_visual_candidates` + figure analysis. Use for papers where the figures ARE the contribution.

---

## Anti-Patterns

- ❌ **Retelling the abstract**. The note must add judgment, not summarize.
- ❌ **Writing claims without page/table/figure references**. Every claim needs evidence.
- ❌ **Using `@[[metaName]]`** (old CiteFlow syntax). Use `(p.3)`, an Obsidian note link, or `![[path]]`.
- ❌ **Section-by-section paraphrase**. Organize by analysis dimensions, not paper sections.
- ❌ **Embedding raw HTML tables**. Use GFM pipe tables. Only fall back to HTML for >500-cell complex tables.
- ❌ **Using yellow `#ffd400` for agent annotations**. Use `mineru_create_evidence_annotation`'s purple default `#a28ae5` so user can distinguish.

---

## File Map

```
SKILL.md                              ← you are here (main workflow)
references/
  frontmatter.md                      ← YAML schema for paper notes
  evidence-discipline.md              ← anti-hallucination rules
  analysis-rubric.md                  ← 8-dimension scoring criteria
  better-notes-sync.md                ← Zotero two-way sync setup + conflict handling
templates/
  empirical.md                        ← experiment papers (datasets/baselines/ablations)
  theoretical.md                      ← theory papers (definitions/theorems/proofs)
  survey.md                           ← survey papers (taxonomy/comparison/trends)
  system.md                           ← system papers (architecture/engineering)
  better-notes-zotero-template.yaml   ← Better Notes Item template (Zotero-side)
examples/
  full-analysis-example.md            ← walkthrough on a real paper (WBench)
agents/
  intake.md                           ← Phase 1 prompt
  evidence.md                         ← Phase 2 prompt (includes Zotero highlighting)
  analyze.md                          ← Phase 3 prompt
  write.md                            ← Phase 4 prompt (includes zotero:// links)
```
