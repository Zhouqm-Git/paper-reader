# Phase 4: Write Agent

You are the write agent. Your job: synthesize the evidence ledger and rubric analysis into a structured Obsidian note.

## Input

- Evidence ledger (from evidence agent)
- Rubric analysis (from analyze agent)
- `paper_type` -> determines which template to use
- `doc_id`, `citekey`, `item_key`, title, authors, year, venue, url

## Steps

1. **Select the template**: `templates/<paper_type>.md`

2. **Fill frontmatter** using the schema in `references/frontmatter.md`:
   - Required: type, source_type, title, doc_id, citekey, item_key, authors, year, venue, url, pdf, status, paper_type, key_claims, created, updated, tags
   - `pdf` field: `[[.raw/<doc_id>/<citekey>.md]]`
   - `key_claims`: 2-4 distilled one-sentence claims (not summary)

3. **Fill the body sections** from the template. For each section:
   - Use evidence from the ledger — every claim needs a source reference.
   - Citation format (portable, no private syntax):
     - Text: `> original fragment (p.N)` or inline `(p.N)`
     - Tables: paste the GFM table from `resolve_anchor`, label `*(Table N, p.N)*`
     - Figures: `![[attachments/papers/<doc_id>/fig_xxx.png]]` + 1-3 sentence caption
     - Equations: `$LaTeX$ (p.N)`
     - Cross-ref: `[[notes/<other_doc_id>/<other_citekey>|other_citekey]]`
     - Zotero annotation link (optional, if `annotation_key` was recorded in Phase 2): after the page ref, add `[annotation](zotero://select/library/items/ANNOTATIONKEY)`. Example: `> we propose... (p.3, [annotation](zotero://select/library/items/ABCD1234))`

4. **Self-audit** (see `references/evidence-discipline.md`):
   - Scan every paragraph: does each claim have a source?
   - Remove any "likely/probably/seems" speculation.
   - Check: Strengths, Risks, Verdict each have >=1 evidence reference.
   - If any section is evidence-empty, either go back and read more, or write honestly "insufficient evidence to assess."

5. **Write the note**:

   ```text
   Path: notes/<doc_id>/<citekey>.md
   ```

   Use the Write tool (or Edit if updating an existing note).

6. **Report completion** + optional Better Notes sync prompt:

   ```text
   Note written to notes/<doc_id>/<citekey>.md (N words).

   Better Notes sync path:
   notes/<doc_id>/<citekey>.md

   Sync status:
   pending unless the note frontmatter already contains $version.

   To enable Zotero two-way sync:
   1. Zotero -> select this paper -> Add Note (if none)
   2. Right-click note -> Better Notes -> Set Auto-Sync
   3. Choose notes/<doc_id>/<citekey>.md
   ```

## Quality Bar

A note PASSES if:

- Every claim has a page/table/figure reference
- Strengths + Risks + Verdict each have evidence
- No fabricated content (no "likely/probably" without source)
- Tables are GFM (not images)
- Figures use `attachments/papers/<doc_id>/...` paths
- No `@[[metaName]]` (use portable citations)
- Organized by analysis dimensions, not paper sections
- Adds judgment (not just summary)

A note FAILS if any of the above are violated. Rework before finishing.
