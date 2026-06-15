# Theoretical Paper Note Template

Use for papers with formal definitions, theorems, proofs, complexity analysis.

---
type: source
source_type: paper
title: "<Full Paper Title>"
doc_id: <doc_id>
citekey: <citekey>
item_key: <ITEMKEY>
library_id: <libraryID>
authors:
  - "<Author 1>"
year: <YYYY>
venue: "<venue>"
url: "<url>"
pdf: "[[.raw/<doc_id>/<citekey>.md]]"
status: seed
paper_type: theoretical
key_claims:
  - "<Theorem/Result 1 — one sentence>"
  - "<Theorem/Result 2>"
confidence: medium
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags:
  - paper
  - <topic-tag>
related: []
---

# <Title>

## Snapshot

| Dimension | Judgment | Evidence |
|---|---|---|
| Problem | | |
| Method | | |
| Evidence (proof quality) | | |
| Reproducibility | | |
| Generalizability | | |
| Limitations | | |
| Positioning | | |
| Writing | | |

## Contribution

<!-- What new theoretical result does this paper establish? State it precisely. -->

<Main result statement> (Theorem <N>, p.<N>).

## Setup & Definitions

<!-- Define the problem formally. Introduce notation. State assumptions. -->

<Definitions with page refs. Key notation:>

$<key definition or notation>$ (p.<N>)

**Assumptions:**
- <Assumption 1> (p.<N>)
- <Assumption 2>

## Main Results

<!-- For each key theorem/lemma: state it, sketch the proof idea (not full proof), assess correctness. -->

### Theorem <N> (<informal name>)

> **Statement:** <precise statement in your own words> (p.<N>)

**Proof sketch:** <the core idea in 2-3 sentences. What technique? What's the key insight?>

**Assessment:** <Is the proof correct and complete? Are the bounds tight? Did you spot gaps?>

### Theorem <N+1>

> **Statement:** ... (p.<N>)

## Evidence

<!-- For theory papers, "evidence" = do the theoretical results hold empirically?
     Is there an experimental section? Do the bounds match practice? -->

<Experimental validation discussion> (p.<N>, Table <N>).

## Strengths

- <Theoretical strength: e.g., tight bound, novel technique> (p.<N>)

## Risks & Limitations

<!-- Theory papers often have strong assumptions. Are they realistic? -->

- <Assumption limitation: e.g., assumes i.i.d. data which rarely holds> (p.<N>)
- <Gap between theory and practice: bound is loose by factor of N>

## Verdict

<Is this a foundational result? Will it be cited in 5 years? Is the proof technique reusable?>
