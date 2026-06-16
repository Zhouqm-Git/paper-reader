# Paper Knowledge Base

## Design

The vault uses three layers:

```text
.raw/<doc_id>/                 MinerU parsed source/cache; hidden from users
attachments/papers/<doc_id>/   visible images/captures embedded by notes
notes/                         user-facing paper wiki
```

`notes/<doc_id>/<citekey>.md` is the only canonical paper note. Everything else is an index, question, or comparison page that links back to canonical notes.

## Index Pages

Create link-only indexes:

- `notes/_index.md`: master catalog of all canonical paper notes.
- `notes/libraries/lib-<libraryID>/index.md`: one page per Zotero library.
- `notes/collections/<collection-path>/index.md`: one page per Zotero collection path when collection metadata is available.
- `notes/<doc_id>/index.md`: optional landing page for one paper folder.

Index pages should include:

- scope and update timestamp
- paper table: title, citekey, year, venue, status, tags, note link, Zotero link
- synthesis links: related question/comparison pages
- gaps: missing notes, missing parse artifacts, weak evidence, outdated notes

Do not duplicate paper-note bodies into indexes.

Use `scripts/build_indexes.py` for the default all-papers and per-library indexes:

```bash
python3 scripts/build_indexes.py --vault "$VAULT_ROOT"
python3 scripts/build_indexes.py --vault "$VAULT_ROOT" --library-id 1
```

The script overwrites generated `notes/_index.md` and `notes/libraries/lib-*/index.md`. Keep manual narrative in question/comparison pages, not in generated indexes.

## Cross-Paper Questions

For questions like "which papers compare BM25 and dense retrievers":

1. Use `mineru_list_documents` to establish the candidate set.
2. Use `mineru_search_evidence` with the user's terms and synonyms.
3. Resolve strong anchors with `mineru_resolve_anchor`.
4. Read canonical notes for interpretation.
5. Write `notes/questions/<slug>.md` with answer, evidence table, and open gaps.

Each claim needs at least one link to a canonical paper note and a page/anchor reference.

## Comparisons

For comparisons across papers, write `notes/comparisons/<slug>.md`.

Use matrices when the axis is stable:

- methods compared
- datasets
- baselines
- metrics
- ablations
- limitations
- reproducibility artifacts

If a cell is not supported by evidence, write `not found`, not a guess.

## Zotero Organization

Zotero item identity is `doc_id = lib-<libraryID>/<item_key>`. This prevents collisions across libraries and keeps parsed artifacts stable.

Zotero collections are views, not identity. The same paper may appear in multiple collections, so collection pages should link to the same canonical note.

## PageIndex Decision

Do not make PageIndex a default dependency.

Use existing MinerU anchors first when the task is:

- single-paper note writing
- finding passages/tables/figures by keyword
- cross-paper evidence search
- Zotero annotation from page/bbox/text anchors

Consider PageIndex only as an optional experiment when:

- a single document is very long and section hierarchy matters more than block anchors
- the PDF has a meaningful table of contents
- the user asks for reasoning over sections rather than exact evidence blocks

If adopted later, store PageIndex outputs under `.raw/<doc_id>/pageindex/` and expose them as optional navigation metadata. Do not replace `.raw/<doc_id>/anchors.json`.
