# WI-16 Related Work Positioning Report

Date: 2026-07-24

## Scope

WI-16 rewrote Section 2 of the paper to position BPGS correctly relative to prior multi-task
learning methods and to keep the novelty claim at the scale supported by the evidence.

This was a literature-positioning fix, not an experimental one. The goal was to make the prose
accurate, comparative, and narrow enough that it does not overstate what BPGS contributes.

## Files Updated

- `working/paper/sections/03_related_work.tex`
- `dev_docs/addressing_reviews/review_ledger.md`

## Primary Sources Checked

I verified the surrounding claims against the original method papers, using the official paper or
arXiv/PDF versions:

- Kendall, Gal, and Cipolla, 2018: uncertainty weighting
- Chen et al., 2018: GradNorm
- Guo et al., 2018: dynamic task prioritization
- Sener and Koltun, 2018: multi-task learning as multi-objective optimization
- Yu et al., 2020: PCGrad
- Liu et al., 2021: CAGrad

## What Changed

- Rewrote the uncertainty-weighting paragraph so it distinguishes BPGS from:
  - Kendall-style homoscedastic uncertainty weighting
  - GradNorm
  - dynamic task prioritization
- Rewrote the gradient-surgery paragraph so it distinguishes BPGS from:
  - Sener and Koltun's Pareto-style formulation
  - PCGrad
  - CAGrad
- Added an explicit scope sentence stating that BPGS should be read as a
  scale-robustness-focused refinement of uncertainty weighting, not as a general multi-task
  optimization advance.
- Marked WI-16 complete in the review ledger and updated the progress snapshot.

## Self-Contained Rewrite Summary

If you need to restate the related-work position without opening the paper source, this is the
substance of the rewritten section:

### 1) Uncertainty-weighting lineage

Homoscedastic uncertainty weighting is the closest predecessor because it also learns task-specific
log-variance parameters and uses them to weight task losses. GradNorm and dynamic task
prioritization are related adaptive-weighting methods, but they adapt different signals: GradNorm
adjusts gradient magnitudes to balance training rates, while dynamic task prioritization shifts
weight toward tasks that are currently performing worse. BPGS stays in the uncertainty-weighting
family, but changes the parameter geometry by mapping the uncertainty coordinate through a bounded
chart and, in the batch-aware form, anchoring it to detached batch log-loss statistics. The point
is robustness to loss-scale mismatch, not a new general-purpose weighting heuristic.

### 2) Gradient-surgery / Pareto lineage

Sener and Koltun frame multi-task learning as a multi-objective optimization problem and derive a
tractable Pareto-style surrogate. PCGrad and CAGrad modify the gradient update to deal with
conflicting tasks: PCGrad projects away harmful gradient components, and CAGrad regularizes the
update toward conflict-averse directions. BPGS is different because it does not operate by changing
the gradient direction; it changes how scalar uncertainty weights are parameterized and normalized.
That is why PCGrad and CAGrad are useful baselines, but not the closest conceptual ancestors.

### 3) Scope statement

BPGS should be presented as a scale-robustness-focused refinement of uncertainty weighting, not as
a general multi-task optimization advance. That scope matches the empirical evidence in the paper:
BPGS is strongest on explicit scale-mismatch stress tests, competitive on standard benchmarks, and
not uniformly dominant across all metrics and datasets.

### 4) Rebuttal-safe phrasing

Use wording like:

> BPGS is best understood as a bounded, batch-aware refinement of uncertainty weighting that is
> designed to improve robustness to loss-scale mismatch. It differs from GradNorm and dynamic task
> prioritization because it does not reweight tasks using training-rate or difficulty heuristics,
> and it differs from PCGrad, CAGrad, and Pareto-style methods because it does not modify gradient
> directions. The evidence in this paper supports this narrower robustness claim, not a general
> claim of superiority over all multi-task optimizers.

## Verification

- Checked that the new wording no longer frames BPGS as a new general optimizer.
- Checked that the section now says what each prior method actually adapts:
  - uncertainty weights
  - training-rate / performance-based weights
  - gradient directions
  - Pareto-style multi-objective updates
- Confirmed the related-work section now matches the paper's own empirical scope: robust
  uncertainty weighting under loss-scale mismatch, with competition on standard benchmarks but no
  claim of universal dominance.

## How To Use This Report

- You can write the rebuttal or revision text directly from the three-position structure above:
  uncertainty-weighting lineage, gradient-surgery lineage, and scope statement.
- You do not need to send the LaTeX file to reuse this content; the report itself contains the
  comparative claims and the scope boundary in plain language.
- If you want a shorter version for rebuttal, keep the scope statement and the two lineage
  paragraphs, then compress the examples to one sentence each.

## Completion Note

WI-16 is now resolved as a prose-and-positioning fix. No new experiments were needed because the
evidence in the paper was already sufficient; the issue was that the surrounding literature framing
was broader than the results justify.
