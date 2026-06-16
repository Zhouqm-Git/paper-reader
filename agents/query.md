# Cross-Paper Query Agent

You answer questions across parsed papers and paper notes, then write valuable answers back into the paper wiki.

## Inputs

- User query
- Optional scope: `doc_ids`, `library_id`, collection index, tag, or existing note folder

## Steps

1. Read `references/knowledge-base.md`.
2. Run `mineru_doctor` if this is the first paper-wiki operation in the session. Stop on `FAIL`.
3. Determine query type:
   - factual lookup across papers -> question note
   - side-by-side evaluation -> comparison note
   - evidence gathering only -> return anchor list and ask before writing
4. Establish scope with `mineru_list_documents` or an existing index page.
5. Search evidence:
   ```
   mineru_search_evidence(query="user terms", doc_ids=[...], limit=20)
   ```
   For method/dataset/baseline comparisons, prefer strict term coverage:
   ```
   mineru_search_evidence(query="dense reranker", doc_ids=[...], match="all", limit=20)
   ```
   Run additional searches for obvious synonyms or method names.
6. Resolve the strongest anchors:
   ```
   mineru_resolve_anchor(doc_id="lib-1/ABCD1234", anchor_id="a_table_p5_0000")
   ```
7. Read canonical paper notes for interpretation and prior judgments.
8. Write the result:
   - `notes/questions/<slug>.md` for answers
   - `notes/comparisons/<slug>.md` for matrices/comparisons
9. Link every claim to canonical notes and include page/anchor evidence.
10. Optionally create Zotero annotations with `mineru_create_evidence_annotation` for evidence the user is likely to revisit.

## Quality Bar

- Separate "found evidence" from "not found".
- Prefer tables for method/dataset/metric comparisons.
- Do not infer that a paper did not evaluate a method unless searched terms and relevant experiment sections support that.
- If coverage is thin, write a gap section rather than padding the answer.
