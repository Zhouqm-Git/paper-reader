# Empirical Paper Note Template

Use for papers with experiments: datasets, baselines, ablation studies, metrics.

<!-- This is a fill-in template. Replace all <...> placeholders. Sections marked OPTIONAL can be omitted if the paper doesn't cover that aspect. -->

---
type: source
source_type: paper
title: "<Full Paper Title>"
citekey: <citekey>
item_key: <ITEMKEY>
authors:
  - "<Author 1>"
  - "<Author 2>"
year: <YYYY>
venue: "<venue>"
url: "<url>"
pdf: "[[.raw/<citekey>/<citekey>.md]]"
status: seed
paper_type: empirical
key_claims:
  - "<Claim 1 — one sentence, distilled>"
  - "<Claim 2>"
  - "<Claim 3>"
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
| Problem | <strong/adequate/weak/unclear> | <page/table ref> |
| Method | | |
| Evidence | | |
| Reproducibility | | |
| Generalizability | | |
| Limitations | | |
| Positioning | | |
| Writing | | |

## Contribution

<!-- 2-4 paragraphs. What does this paper actually contribute? DO NOT retell the abstract.
     Each paragraph should have at least one page/table/figure reference. -->

<First contribution claim with evidence> (p.<N>).

<Second contribution> (Table <N>, p.<N>).

## Method

<!-- Core technical approach. Be precise: define key terms, state the main algorithm/architecture.
     If there's a key equation, include it as $LaTeX$. -->

<Method description with page refs>

$<key equation>$ (p.<N>)

## Evidence

<!-- This is the most important section for empirical papers. Read the main results table
     and ablation table carefully. Embed the GFM table directly (from resolve_anchor). -->

### Main Results

<1-2 paragraphs interpreting the main results table. What does it show? Is the improvement
real and significant, or marginal?>

<!-- Paste the GFM table here (from mineru_resolve_anchor markdownTable) *(Table N, p.N)* -->

| Method | Metric 1 | Metric 2 |
|---|---|---|
| ... | ... | ... |

### Ablations

<Does the ablation actually isolate the contribution? Or does removing any single component
barely hurt, suggesting the gains come from stacking tricks?> (Table <N>, p.<N>).

## Figures

<!-- Only embed figures that add information beyond text. Architecture diagrams and key
     result plots are worth it; decorative icons are not. Use the auto-merged figure paths. -->

![[attachments/papers/<citekey>/fig_<...>.png]]
*<1-3 sentence visual reading — what does this figure show and why does it matter?>*

## Strengths

<!-- What does this paper do well? Must have evidence references. -->

- <Strength 1> (p.<N>)
- <Strength 2> (Table <N>)

## Risks & Limitations

<!-- What concerns you? Be specific — not generic "more experiments needed". -->

- <Risk 1: e.g., evaluated on only one dataset> (p.<N>)
- <Risk 2: e.g., baseline is 2 years old> (Table <N>)
- <Does the paper acknowledge this limitation? If so, where? If not, that's a red flag.>

## Verdict

<!-- 1-2 paragraphs. Your overall judgment, backed by evidence.
     Address: is this paper worth building on? Worth citing? Worth replicating? -->

<Verdict with evidence>
