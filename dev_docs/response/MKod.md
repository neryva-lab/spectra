# Response to Reviewer MKod

## MKod-1: Largely a constrained reparameterization of Kendall + normalization

We ran a controlled Kendall + L1-normalization ablation (36 runs: 4 loss scales × 3 methods × 3 seeds) to test whether L1-normalization alone explains BPGS's robustness. Results:

| Scale | BPGS | Kendall | Kendall+L1 |
|-------|------|---------|------------|
| ×1    | 0.789±0.018 | 0.788±0.014 | 0.794±0.017 |
| ×10   | 0.791±0.015 | 0.781±0.023 | 0.780±0.022 |
| ×100  | 0.788±0.016 | 0.734±0.037 | 0.742±0.029 |
| ×1000 | 0.785±0.017 | 0.658±0.042 | 0.689±0.034 |

Scale sensitivity ×1→×1000: BPGS −0.004, Kendall −0.130, Kendall+L1 −0.105.

L1-normalization alone does not recover BPGS-scale invariance. At ×1000, Kendall+L1 (−0.105) improves over vanilla Kendall (−0.130) but still trails BPGS (−0.004) by an order of magnitude. The bounded chart and split optimization do independent work beyond normalization. We have revised the related work to position BPGS as a bounded, batch-aware refinement with a different fixed-point structure from Kendall, while acknowledging the algebraic similarity of the uncertainty objectives.

## MKod-2: Deeper properties (invariance, convergence) not analyzed

**Invariance proof:** Under uniform rescaling of all task losses by c>0: μ(L) shifts by log(c), σ̄(L) is unchanged (centered moment), z_i(θ_i) is unchanged, so s_i shifts by log(c). The raw precision ω_i = exp(−s_i) scales by 1/c, and the normalization α_i = ω_i / Σω_j cancels the common factor. Therefore the normalized task weights α_i are exactly invariant under uniform rescaling. This is an algebraic property of the construction — Table 1 confirms it empirically. First-batch auto-calibration also preserves invariance because the standardized coordinates (log L_i − μ)/σ̄ are unchanged by the additive log(c) shift.

**Saturation analysis:** We analyzed existing logs across NYUv2 (T=3, τ_T=1.514), Yeast (T=14, τ_T=3.706), and RF1 (T=8, τ_T=2.746). The maximum observed |z_i|/τ_T ratio is 0.9327 (NYUv2, epoch 0, seed 43, task 2). All trajectories move inward from the initial auto-calibration point. No logged run reaches the saturation boundary. The limitations section now discusses the theoretical saturation risk alongside the negative empirical finding.

## MKod-3: Batch-size sensitivity not analyzed

We tested BPGS at batch sizes 4, 8, 16 (3 seeds each, NYUv2 50% subset, 60 epochs). Across-batch-size CV on all validation metrics is < 3.5% (most < 1.2%). The learned θ_max shifts from 2.40 (bs=4) to 2.59 (bs=16), consistent with larger batches providing more reliable gradient estimates. No systematic degradation at any tested size. BPGS is robust across a 4× batch range without retuning.

## MKod-4: Stop-gradient role not ablated independently

We ablated the split-optimization stop-gradient while keeping the bounded chart and batch-aware calibration fixed (6 runs: 2 variants × 3 seeds, NYUv2 50% subset). Results:

- **With stop-gradient (canonical):** θ_max decays from 3.08→2.44 (epoch 0→59), converging to 2.438±0.014.
- **Without stop-gradient:** θ_max grows from 3.11→3.99 (+28%), with 14× higher seed variance (SD 0.192 vs 0.014).

Validation metrics are broadly similar, but mIoU drops 4.3% (0.198→0.190) without stop-gradient. The internal calibration dynamics are fundamentally different — the coupled backward pass pulls the uncertainty scale into a regime where it grows monotonically rather than settling. The split-optimization stop-gradient is a meaningful design choice that stabilizes the calibration.

## MKod-5: Missing CAGrad, Nash-MTL, Auto-Lambda

We implemented Nash-MTL (Navon et al., 2022) on NYUv2 (3 seeds, 120 epochs). Results: mIoU 0.252±0.027, AbsRel 0.242±0.009, Angle 30.18°±1.01°, Total Loss 2.071±0.070. Nash-MTL underperforms all paper baselines on every metric, with high seed variance (mIoU range 0.228–0.289). The paper now has 7 comparison methods. CAGrad, Auto-Lambda, and IMTL-G were not implemented — they belong to a different method class (gradient surgery / learned loss functions) and the marginal return of adding further underperforming baselines to an already 7-method comparison is low. A note acknowledging their existence is added.

## MKod-6: Only one dense-prediction benchmark (NYUv2)

Acknowledged. Adding a second dense-prediction benchmark (Cityscapes or a medical-imaging multi-task setup) is the highest-priority experimental addition for the next revision.

## MKod-7: No computational overhead analysis

We measured BPGS vs Kendall on the NYUv2 50% subset (3 seeds, 60 epochs). BPGS adds +0.15% wall-clock time per epoch (40.979s vs 40.916s) and +0.87% peak GPU memory (3368 MB vs 3339 MB). The split optimization, batch statistics, and 3 extra θ parameters add negligible overhead against the 18.9M shared parameter model.

## MKod-8: Figures wedged into checklist, unused page-9 space

We have prepared a layout cleanup plan to separate the NeurIPS checklist from the substantive appendices with a clear page break, and to use the page-9 space for a compact supplemental item. Paper edits cannot be uploaded during the rebuttal window; this will be applied before any future submission.
