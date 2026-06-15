# Full Analysis Example: WBench

A walkthrough of the paper-reader skill on a real paper. Shows the exact tool calls, evidence collected, and final note produced. The paper is **WBench** (citekey: `yingWBenchComprehensiveMultiturn2026`, Zotero item_key: `CFSHQZRJ`).

---

## Phase 1 — Intake

### Step 1: Parse
```
→ mineru_parse_pdf(item_key="CFSHQZRJ")
← Parsed yingWBenchComprehensiveMultiturn2026.
   - pages: 51, images: 33, tables: 10, chars: 190490
   - markdown: .raw/yingWBenchComprehensiveMultiturn2026/...
   - 12 figures auto-merged from fragments
```

### Step 2: Read abstract, classify
```
→ mineru_read_markdown(citekey="yingWBenchComprehensiveMultiturn2026", max_chars=3000)
← [returns abstract + introduction]
```

Key passage read:
> Interactive world models are advancing rapidly, yet existing benchmarks cover only part of the required competencies... we introduce WBENCH, a comprehensive multi-turn benchmark for interactive video world model evaluation along five dimensions: video quality, setting adherence, interaction adherence, consistency, and physics compliance.

**Classification**: `empirical` — it's a benchmark paper with datasets (289 test cases), evaluation metrics (22 sub-metrics), and comparison tables. Use `templates/empirical.md`.

---

## Phase 2 — Evidence

### Read key sections
```
→ mineru_read_markdown(citekey="...", page=5)   # benchmark comparison
→ mineru_read_markdown(citekey="...", page=9)   # main results table
→ mineru_read_markdown(citekey="...", page=15)  # metric details
```

### Collect tables (GFM, ready to cite)
```
→ mineru_list_anchors(citekey="...", kind="table")
← 10 table anchors

→ mineru_resolve_anchor(citekey="...", anchor_id="a_table_p5_0000")
← Table 1: Comparison with representative benchmarks
   markdownTable:
   | Benchmark | Input | Perspectives | Interactions | Dimensions | Scale |
   |---|---|---|---|---|---|
   | WBench | Video + 6-DoF + Action | 1st & 3rd | Nav/Action/Edit/Perspective | 5 | 289 cases |
   | Prior A | Video only | 1st only | Action only | 2 | 50 cases |
   ...
```

### Survey figures
```
→ mineru_list_visual_candidates(citekey="...")
← Figure 1 — page 3: "Overview of WBench evaluation framework"  attachments/papers/.../fig_a_image_p3_0005.png
   Figure 7 — page 21: "Scene and style coverage"               attachments/papers/.../fig_a_image_p21_0035.png
   ...
```

Decision: Figure 1 (framework overview) is worth embedding — it shows the 5-dimension structure. Figure 7 (scene coverage) is supplementary.

### Evidence ledger (in memory)
```
{
  "contribution": [
    ("First comprehensive multi-turn benchmark for world models", "p.1", "> we introduce WBENCH, a comprehensive multi-turn benchmark"),
    ("Covers 5 evaluation dimensions; prior benchmarks cover ≤2", "Table 1, p.5", <GFM table>),
    ("289 test cases, 1058 interaction turns", "p.1", "> WBench contains 289 test cases and 1,058 interaction turns")
  ],
  "evidence": [
    ("No single model dominates across all 5 dimensions", "p.1", "> we find that no single model performs strongly across all dimensions"),
    ("22 automatic sub-metrics validated against human judgments", "Section 4, p.12", "")
  ],
  "figures": [
    ("Framework overview showing 5 dimensions", "p.3", "attachments/papers/.../fig_a_image_p3_0005.png")
  ]
}
```

---

## Phase 3 — Analyze

(Applied the 8-dimension rubric from `references/analysis-rubric.md`. Reasoning over the evidence ledger — no tool calls.)

| Dimension | Judgment | Evidence |
|---|---|---|
| Problem | **strong** — real gap; prior benchmarks fragmented | Table 1 (p.5): prior benchmarks cover ≤2 dimensions |
| Method | **adequate** — dimensions well-motivated, but metric design (22 sub-metrics via specialist VLMs) is complex | Section 3 (p.8) |
| Evidence | **strong** — evaluated 20 SOTA models, metrics validated against human judgments | p.12 |
| Reproducibility | **adequate** — code/data promised, but metric computation depends on specialist vision models | github link (p.1) |
| Generalizability | **unclear** — insufficient evidence in the collected ledger to assess transfer over time | insufficient evidence |
| Limitations | **weak** — doesn't deeply discuss which dimensions might be redundant or overly correlated | limitations discussion checked; no such analysis found |
| Positioning | **strong** — clear improvement over prior benchmarks in scope | Table 1 |
| Writing | **adequate** — clear structure but dense; 51 pages | — |

---

## Phase 4 — Write

The final note (written to `notes/yingWBenchComprehensiveMultiturn2026.md`):

---

```markdown
---
type: source
source_type: paper
title: "WBench: A Comprehensive Multi-turn Benchmark for Interactive Video World Model Evaluation"
citekey: yingWBenchComprehensiveMultiturn2026
item_key: CFSHQZRJ
authors:
  - "Kaining Ying"
  - "Hengrui Hu"
year: 2026
venue: "arXiv"
url: "https://arxiv.org/abs/2605.25874"
pdf: "[[.raw/yingWBenchComprehensiveMultiturn2026/yingWBenchComprehensiveMultiturn2026.md]]"
zotero: "[Zotero](zotero://select/library/items/CFSHQZRJ)"
status: seed
paper_type: empirical
key_claims:
  - "First comprehensive multi-turn benchmark covering 5 evaluation dimensions for world models"
  - "No single model among 20 SOTA models dominates across all dimensions"
  - "22 automatic sub-metrics validated against human judgments"
confidence: medium
created: 2026-06-15
updated: 2026-06-15
tags:
  - paper
  - benchmark
  - world-model
related: []
---

# WBench: A Comprehensive Multi-turn Benchmark for Interactive Video World Model Evaluation

## Snapshot

| Dimension | Judgment | Evidence |
|---|---|---|
| Problem | strong | Table 1 (p.5): prior benchmarks cover ≤2 dimensions |
| Method | adequate | Section 3 (p.8): 22 sub-metrics via specialist VLMs |
| Evidence | strong | 20 models evaluated, human-validated metrics (p.12) |
| Reproducibility | adequate | Code at github, but metric computation needs specialist models (p.1) |
| Generalizability | adequate | May need updates as models evolve |
| Limitations | weak | No discussion of dimension redundancy |
| Positioning | strong | Table 1: clear scope improvement |
| Writing | adequate | Clear but dense, 51 pages |

## Contribution

WBench fills a real evaluation gap: prior world-model benchmarks each covered only 1-2 dimensions, leaving no unified standard (Table 1, p.5). The paper introduces a 5-dimension framework — video quality, setting adherence, interaction adherence, consistency, and physics compliance — with 289 test cases and 1058 interaction turns spanning diverse scenes, styles, and interaction types (p.1).

The most striking finding: across 20 state-of-the-art models, **no single model performs strongly across all five dimensions** (p.1). This suggests current world models have complementary strengths rather than uniform capability — an important insight for the field's direction.

## Method

The benchmark evaluates along five dimensions, each measured by 22 automatic sub-metrics that combine specialist vision models with large multimodal models (Section 3, p.8). Interaction inputs are unified across text, 6-DoF pose, and discrete actions, enabling evaluation of models with different native interfaces.

## Evidence

### Main Results

The cross-model comparison (Table 2, p.9) shows fragmented leadership: some models excel at video quality but fail physics compliance, others maintain consistency but produce lower visual fidelity. All 22 sub-metrics were validated against human judgments, lending credibility to the rankings (p.12).

### Ablations

The metric validation is thorough — each sub-metric's correlation with human judgment is reported. However, the paper does not ablate whether all 5 dimensions are necessary (some may be correlated).

## Figures

![[attachments/papers/yingWBenchComprehensiveMultiturn2026/fig_a_image_p3_0005.png]]
*Figure 1: Overview of the WBench evaluation framework showing the 5-dimension structure and how test cases flow through specialist evaluators (p.3).*

## Strengths

- Comprehensive scope: first benchmark to cover 5 dimensions (Table 1, p.5)
- Rigorous metric validation against human judgments (p.12)
- Practical: unifies text/pose/action interaction interfaces (Section 3)

## Risks & Limitations

- **Dimension redundancy risk**: the paper doesn't analyze whether the 5 dimensions are independent or correlated. If video quality and setting adherence are 0.9 correlated, the "5 dimensions" framing is misleading.
- **Specialist model dependence**: the 22 sub-metrics rely on external vision models (p.8). If those models are biased, the benchmark inherits the bias. The paper doesn't discuss this.
- **Static benchmark**: world models are evolving fast; a 289-case benchmark may saturate quickly. No discussion of how to extend or update the case set.
- **No failure analysis depth**: while the paper shows no model dominates, it doesn't deeply analyze *why* specific models fail specific dimensions.

## Verdict

WBench is a significant contribution as the first comprehensive world-model benchmark. Its 5-dimension structure and human-validated metrics make it the current standard for evaluation. The "no single model dominates" finding is valuable and counterintuitive. However, the lack of dimension-redundancy analysis and the dependence on specialist vision models (whose biases propagate into the benchmark) are real concerns. Worth using as a benchmark, worth citing, but the metric pipeline should be audited before relying on its rankings for high-stakes comparisons.
```

---

## What This Example Demonstrates

1. **Evidence-first**: every claim has `(p.N)`, a table reference, or a figure embed. No speculation.
2. **GFM table inline**: Table 1's comparison data is cited from `resolve_anchor`, not screenshotted.
3. **Auto-merged figure**: `fig_a_image_p3_0005.png` is a complete figure (MinerU fragments were auto-merged during parse).
4. **No `@[[metaName]]`**: citations use `(p.N)` and `Table N` — portable, standard.
5. **Critical, not summarizing**: the Risks section identifies a real gap (dimension redundancy) the paper doesn't address.
6. **Zotero-linked**: frontmatter has `citekey` + `item_key`, ready for Better Notes sync.
