# System Paper Note Template

Use for papers describing a system design: architecture, engineering tradeoffs, performance benchmarks.

---
type: source
source_type: paper
title: "<Full Paper Title>"
citekey: <citekey>
item_key: <ITEMKEY>
authors:
  - "<Author 1>"
year: <YYYY>
venue: "<venue>"
url: "<url>"
pdf: "[[.raw/<citekey>/<citekey>.md]]"
status: seed
paper_type: system
key_claims:
  - "<System capability or performance claim>"
  - "<Design choice and its justification>"
confidence: medium
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags:
  - paper
  - system
  - <domain-tag>
related: []
---

# <Title>

## Snapshot

| Dimension | Judgment | Evidence |
|---|---|---|
| Problem | | |
| Architecture soundness | | |
| Performance evidence | | |
| Reproducibility (deployability) | | |
| Engineering tradeoffs | | |
| Scalability | | |
| Positioning | | |
| Writing | | |

## System Overview

<!-- What system is built? What problem does it solve? What are the key design goals? -->

<System description with page refs>

## Architecture

<!-- Describe the key components and how they interact. Embed an architecture diagram if available. -->

![[attachments/papers/<citekey>/fig_<...>.png]]
*<Architecture overview — label the key components> (p.<N>)*

<Component-by-component description with page refs>

## Design Tradeoffs

<!-- What engineering decisions were made and why? This is the heart of a system paper. -->

| Decision | Choice | Rationale | Alternative considered |
|---|---|---|---|
| <decision 1> | <choice> | <why> | <alt> (p.<N>) |

## Performance

<!-- Embed the benchmark table. Focus on: what's the throughput/latency? At what scale? -->

<!-- GFM table from resolve_anchor *(Table N)* -->

| Workload | Metric | Result |
|---|---|---|
| ... | ... | ... |

<Analysis: is the performance impressive? At what cost (compute, complexity)?> (p.<N>).

## Strengths

- <Engineering strength> (p.<N>)
- <Performance strength> (Table <N>)

## Risks & Limitations

<!-- System papers often hide complexity. What concerns you about deploying this? -->

- <Operational complexity: e.g., requires 5 dependent services> (p.<N>)
- <Hardware dependence: only works on specific accelerators/networks>
- <Benchmarks may not reflect real workloads>

## Verdict

<Would you deploy this? Build on it? Is the engineering reusable beyond this specific system?>
