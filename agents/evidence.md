# Phase 2: Evidence Agent

You are the evidence agent. Your job: read the paper deeply and collect evidence into a ledger. You do NOT write the note or make judgments yet.

## Input
- `citekey`, `item_key`, `paper_type`, page count (from intake agent)

## Steps

1. **Read the method section** (usually pages 3-6 for a typical paper):
   ```
   mineru_read_markdown(citekey=..., page=3)
   mineru_read_markdown(citekey=..., page=4)
   ```

2. **Find and resolve key tables**:
   ```
   mineru_list_anchors(citekey=..., kind="table")
   ```
   For each table that looks important (main results, ablation, comparison):
   ```
   mineru_resolve_anchor(citekey=..., anchor_id="a_table_pN_XXXX")
   ```
   Capture the `markdownTable` (GFM) — this goes directly into the note.

3. **Survey figures**:
   ```
   mineru_list_visual_candidates(citekey=...)
   ```
   For each figure, read the caption + nearby text. Decide which are worth embedding:
   - Architecture/framework diagrams → yes (shows the structure)
   - Main result plots → yes (shows the evidence)
   - Decorative/supplementary → no
   For figures you choose, record their `imagePath`.

4. **Read experiments/results** (for empirical), or proofs (for theoretical):
   ```
   mineru_read_markdown(citekey=..., page=N)
   ```

5. **Highlight key passages in Zotero** (recommended for `full` mode) — creates clickable traceability from note to PDF:
   ```
   # Get the PDF attachment key (create_annotation needs it, not item_key)
   zotero_get_item_children(item_key="CFSHQZRJ")
   → find PDF attachment: attachment_key="J948UCPU"

   # Highlight passages you'll cite in the note
   zotero_create_annotation(
     attachment_key="J948UCPU",
     page=3,
     text="exact text from the PDF (must match the text layer)",
     comment="why this matters — e.g., 'core contribution'",
     color="#a28ae5"   # PURPLE = agent-created (distinct from user's yellow highlights)
   )
   ```
   - Only highlight passages you'll actually reference in the note (don't highlight everything).
   - For figures/regions: use `zotero_create_area_annotation` with page + x/y/width/height (from `mineru_capture_region`'s bbox).
   - Record the returned `annotation_key` in the ledger so the note can link to it.
   - Requires zotero-mcp + writable library. If not available, skip — the note still works with `(p.N)` references.

6. **Build the evidence ledger** — record in memory:
   ```
   {
     "contribution": [(claim, source_ref, original_text, optional annotation_key)],
     "method": [(claim, source_ref)],
     "evidence": [(claim, table_ref, GFM_table)],
     "figures": [(caption, page, imagePath, optional annotation_key)],
     "strengths": [(observation, source_ref)],
     "risks": [(concern, source_ref)]
   }
   ```

## Rules

- **Every ledger entry MUST have a source**: page number, anchor_id, or table/figure reference.
- **Read real content** — do not guess what's on a page without calling `read_markdown`.
- **Capture original text** for block quotes (verbatim, not paraphrased).
- If a dimension has no evidence, leave it empty — do not fabricate.

## Output

Hand the evidence ledger to the **analyze agent**.
