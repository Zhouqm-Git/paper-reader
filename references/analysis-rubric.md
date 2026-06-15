# Analysis Rubric: 8 Dimensions for Technical Papers

Score the paper across these 8 dimensions. Each dimension gets 1-3 sentences of judgment backed by evidence (page/table/figure). This is not a checklist — it's a framework for critical thinking.

## The 8 Dimensions

### 1. Problem Clarity / Motivation
- Is the problem precisely defined?
- Why does it matter? Who benefits from a solution?
- Is it a real problem or a manufactured one?
- **Red flag**: vague problem statement, no clear use case, "we explore..." without stakes.

### 2. Method Soundness / Novelty
- Is the approach technically correct (not just plausible)?
- What's genuinely new vs. incremental combination of existing techniques?
- Are the key assumptions stated and justified?
- **Red flag**: method described only at high level, no formal definition, "novel" without comparison to prior art.

### 3. Evidence Strength
- Do the experiments actually test the central claims?
- Are baselines fair and current (not 3-year-old weak baselines)?
- Are ablations isolating the contribution, or just stacking tricks?
- For theory: are proofs correct and complete? Are bounds tight?
- **Red flag**: only toy experiments, missing baselines, no error bars, no ablation of the core component.

### 4. Reproducibility
- Is there code? Is it usable (not just a README)?
- Are hyperparameters, data splits, compute requirements stated?
- Could a competent grad student reproduce the main result in a month?
- **Red flag**: no code, "details in supplementary" but supplementary is thin, unspecified training details.

### 5. Generalizability / Transfer Risk
- Will this work on different datasets/domains/scales?
- Is the method tied to a specific architecture, dataset, or hardware?
- Are there theoretical reasons it should (or shouldn't) generalize?
- **Red flag**: evaluated on one dataset, one architecture, one scale; no discussion of limitations.

### 6. Limitations Honesty
- Does the paper acknowledge its own weaknesses?
- Are failure cases shown, not just success cases?
- Is the "future work" section honest about what doesn't work yet?
- **Red flag**: no limitations section, cherry-picked examples, sweeping claims without caveats.

### 7. Positioning (vs Prior Work)
- How does this improve on the closest prior work?
- Is the comparison fair (same setting, same data, same compute)?
- Is related work thorough, or does it ignore inconvenient prior art?
- **Red flag**: "to the best of our knowledge, the first..." without checking, missing obviously relevant citations.

### 8. Writing Quality
- Is the paper clearly written? Could a target-audience reader follow it?
- Are figures and tables informative (not decorative)?
- Is the structure logical?
- **Red flag**: dense walls of text, figures without captions, notation introduced but never defined.

---

## Scoring Guide

For the Snapshot table in the note, give each dimension a brief judgment (not a number):

| Label | Meaning |
|---|---|
| **strong** | This dimension is a clear strength of the paper |
| **adequate** | Acceptable but unremarkable |
| **weak** | This is a real concern |
| **unclear** | Not enough information to judge (be honest) |

## How to Apply

Don't go dimension-by-dimension mechanically. Instead:

1. After reading the full paper (Phase 2), form an overall impression.
2. Identify the 2-3 dimensions where the paper is strongest and weakest.
3. Write detailed judgment for those (with evidence).
4. For the remaining dimensions, write shorter judgments.
5. The Snapshot table captures all 8 at a glance; the body sections go deep on the important ones.

## Paper-Type Adjustments

- **empirical**: weight Evidence Strength and Reproducibility highest.
- **theoretical**: weight Method Soundness and Generalizability highest; "Evidence" = proof quality.
- **survey**: weight Positioning and Writing highest; "Evidence" = coverage breadth.
- **system**: weight Reproducibility and Method Soundness highest; "Evidence" = benchmark results.
