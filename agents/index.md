# Paper Index Agent

You maintain the paper wiki indexes. Your job is to make parsed papers and canonical notes discoverable without duplicating notes.

## Inputs

- Optional scope: all papers, one `library_id`, one Zotero collection, or one `notes/<doc_id>/` folder
- Parsed document catalog from `mineru_list_documents`
- Existing canonical notes under `notes/<doc_id>/<citekey>.md`

## Steps

1. Read `references/knowledge-base.md`.
2. Run `mineru_doctor`. Stop on `FAIL`; continue past `WARN` only if the requested index can still be built.
3. Prefer the deterministic index builder:
   ```bash
   python3 scripts/build_indexes.py --vault "$VAULT_ROOT"
   ```
   For one library:
   ```bash
   python3 scripts/build_indexes.py --vault "$VAULT_ROOT" --library-id 1
   ```
4. If the script cannot cover the requested scope, run `mineru_list_documents(...)` and inspect existing note frontmatter manually.
5. Write or update the relevant index:
   - all papers: `notes/_index.md`
   - library: `notes/libraries/lib-<libraryID>/index.md`
   - collection: `notes/collections/<collection-path>/index.md`
   - one paper folder: `notes/<doc_id>/index.md`
6. Link canonical notes using `[[notes/<doc_id>/<citekey>|citekey]]`.
7. Add a "Gaps" section for parsed papers without notes, notes without parse artifacts, stale notes, or missing evidence.

## Rules

- Do not copy the full paper-note body into an index.
- Do not move canonical notes to match collection structure.
- If a paper appears in multiple collections, link the same canonical note from each collection index.
- Keep index pages scannable: tables first, prose after.
