# WI-17 Method Intuition and Motivation Report

Date: 2026-07-24

## Scope

WI-17 added plain-language motivation to Section 3 of the paper so the method is explained in
terms of design intent, not only equations.

The fix does not change the method. It explains why the bounded chart, batch-conditioning, first
batch calibration, and split optimization are used, and why the boundedness statement matters for
robustness.

## Files Updated

- `working/paper/sections/02_method.tex`
- `dev_docs/addressing_reviews/review_ledger.md`

## What Was Added

### 1) Problem setup motivation

I added a short paragraph explaining that the design goal is not to replace task weighting
altogether, but to make it less fragile when task losses differ in numerical scale or units. The
new text states that an unconstrained uncertainty parameter can drift too far too quickly, which is
why the method deliberately constrains the coordinate and ties it to the current batch statistics.

### 2) Canonical chart motivation

I added explanation for why the chart is bounded and batch-aware:

- the uncertainty variable should still adapt, but should not be free to drift to extreme values
  just because the raw losses are numerically large or small
- centering on the batch mean and scaling by the batch spread makes the coordinate relative to the
  current batch rather than tied to an absolute loss level
- the bounded sigmoid map keeps the learnable coordinate inside a finite range, which makes the
  resulting precision easier to control and reason about

### 3) First-batch calibration motivation

I added a paragraph clarifying that first-batch calibration is a practical initialization choice,
not a separate claim of optimality. The motivation is to place the uncertainty coordinates in a
sensible range before training begins so the model does not waste early iterations recovering from
an arbitrary starting point.

### 4) Split-optimization motivation

I added explicit plain-language motivation for the two-pass design:

- the network pass should treat task weights as fixed coefficients for the main update
- the uncertainty pass should update the weights from current losses without directly reshaping the
  network gradient in the same step
- separating the passes makes the difference between "how to update the model" and "how to update
  the weights" explicit

### 5) Batch-conditional boundedness motivation

I added a concluding paragraph explaining why the boundedness property is worth stating:

- it does not prove the method is best
- it does show that the learned weights stay numerically well-behaved on a fixed batch
- the corresponding precision cannot explode or collapse without limit within that batch
- this makes the robustness claim concrete rather than abstract

## Self-Contained Rewrite Summary

If you need to restate the method motivation without opening the LaTeX source, this is the core
message of the rewritten section:

> BPGS is designed to make uncertainty weighting less fragile under loss-scale mismatch. The
> bounded chart prevents the latent uncertainty coordinate from drifting to extreme values, the
> batch statistics make the coordinate relative to the current batch rather than to an arbitrary
> absolute loss scale, first-batch calibration provides a sensible starting point, and the split
> optimization keeps the network update and the uncertainty update conceptually separate. The
> boundedness statement is included because it explains why the induced precision stays within a
> finite range for a fixed batch.

## Verification

- Checked that the new paragraphs appear immediately around the formulas they explain.
- Checked that the wording stays descriptive rather than promotional.
- Checked that the new prose does not introduce any new empirical or theoretical claim beyond what
  the method already supports.
- Confirmed that the section now answers the reviewer concern that the method read like a sequence
  of formulas without enough motivation.

## Completion Note

WI-17 is now resolved as a prose-and-explanation fix. No experiments were needed because the change
was purely about clarifying the rationale for the existing method design.
