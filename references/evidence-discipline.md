# Evidence Discipline: Anti-Hallucination Rules

The single most important rule in paper-reader: **never write a claim you cannot point to a specific source for.** This prevents the LLM from fabricating plausible-sounding but false statements about the paper.

## The Golden Rule

> Every claim in the note MUST be backed by a source you actually read:
> - a **page number**: `(p.3)` referencing content from `mineru_read_markdown`
> - a **table**: GFM content from `mineru_resolve_anchor`
> - a **figure**: image path from `mineru_list_visual_candidates`
> - a **block quote**: `> original text (p.5)` — the actual words from the paper

## What Counts as Evidence

| Source type | How to cite | Example |
|---|---|---|
| Text you read | `(p.N)` page reference | "The model uses dual encoders (p.3)." |
| Exact words | Block quote + page | `> We propose a novel loss function (p.4)` |
| Table data | Inline GFM table + `Table N` label | See table below *(Table 2, p.6)* |
| Figure | Embed + 1-3 sentence visual reading | `![[raw/.../fig.png]]` + "The architecture shows..." |
| Equation | `$LaTeX$` + page | "The loss is $L = L_{ce} + \lambda L_{reg}$ (p.4)." |

## What Does NOT Count as Evidence

- ❌ "The paper likely..." / "It probably..." — speculation without page ref
- ❌ "According to the authors..." — vague, no specific location
- ❌ Paraphrasing the abstract — you must read the actual method section
- ❌ "Standard techniques such as..." — unless you read them on a specific page
- ❌ Numbers without source — "achieves 95% accuracy" must cite the exact table

## The Evidence Ledger

Before writing any section of the note, you must have already collected the evidence in Phase 2:

```
evidence_ledger = {
  "contribution": [
    ("Introduces PoSE training for context window extension", "p.1", "> we propose Positional Skip-wisE (PoSE) training"),
    ("Extends LLaMA to 128k tokens with 2k training window", "p.1", "> successfully extended the LLaMA model to 128k tokens")
  ],
  "evidence": [
    ("PoSE matches Full-length fine-tuning at 1/8 memory", "Table 1", <GFM table>),
  ],
  ...
}
```

**If you cannot fill an entry with a real source, leave that dimension blank rather than fabricate.** A note with "Risks: insufficient evidence to assess" is honest and correct. A note with fabricated risks is worse than useless.

## Self-Audit (end of Phase 4)

Before finishing, scan every paragraph of your note:

1. Does each claim have `(p.N)`, a table reference, a figure embed, or a block quote?
2. Are there any sentences starting with "likely", "probably", "presumably", "seems to"? → remove or add evidence.
3. Are any numbers (accuracy, parameters, sizes) without a table/page source? → remove or cite.
4. Are strengths/risks/conclusion sections each backed by at least one reference? → if not, note is incomplete.

## Density Threshold

A note is **failed** (needs rework) if any of these sections has zero evidence references:
- Strengths
- Risks & Limitations
- Verdict

These are judgment sections — if you can't point to evidence for your judgment, you haven't read deeply enough. Go back to Phase 2.
