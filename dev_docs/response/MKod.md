# Response to Reviewer MKod

## MKod-1: Largely a constrained reparameterization of Kendall + normalization

To test this directly, we ran a Kendall + L1-normalization ablation (36 runs: 4 loss scales × 3 methods × 3 seeds). Macro score (defined in §4):

| Scale | BPGS | Kendall | Kendall+L1 |
|-------|------|---------|------------|
| ×1    | 0.789±0.018 | 0.788±0.014 | 0.794±0.017 |
| ×10   | 0.791±0.015 | 0.781±0.023 | 0.780±0.022 |
| ×100  | 0.788±0.016 | 0.734±0.037 | 0.742±0.029 |
| ×1000 | 0.785±0.017 | 0.658±0.042 | 0.689±0.034 |

Scale sensitivity ×1→×1000: BPGS −0.004, Kendall −0.130, Kendall+L1 −0.105.

L1-normalization helps Kendall under rescaling but does not close the gap — at ×1000, Kendall+L1 still drops −0.105 where BPGS drops −0.004. A separate stop-gradient ablation (6 runs, bounded chart held constant) shows the split-optimization piece: without the stop-gradient, θ_max grows +28% instead of settling, with 14× higher seed variance (SD 0.192 vs 0.014) and a 4.3% mIoU drop. The normalization ablation and the stop-gradient ablation together show that BPGS is more than Kendall + normalization. The related work now distinguishes the fixed-point structure from the algebraic similarity of the objectives.

## MKod-2: Deeper properties (invariance, convergence) not analyzed

**Invariance proof.** Under uniform rescaling of all task losses by c>0: μ(L) shifts by log(c), σ̄(L) stays the same (it is a centered moment), z_i(θ_i) is unchanged, so s_i shifts by log(c). The raw precision ω_i = exp(−s_i) scales by 1/c, and after normalization α_i = ω_i / Σω_j the common factor cancels. The normalized task weights α_i are exactly invariant. Table 1 confirms this empirically. Auto-calibration preserves invariance too, because the standardized coordinates (log L_i − μ)/σ̄ do not change under the additive log(c) shift.

**Saturation analysis.** We checked the logged runs on NYUv2 (T=3, τ_T=1.514), Yeast (T=14, τ_T=3.706), and RF1 (T=8, τ_T=2.746). The highest observed |z_i|/τ_T ratio is 0.9327 (NYUv2, epoch 0, seed 43, task 2). Every trajectory moves inward from the initialization point — none reaches the boundary. At the worst point (ratio 0.93), σ(θ)(1−σ(θ)) ≈ 0.033, about 13% of its peak. By end of training (ratio ≤ 0.84), it rises to ≈ 0.074 (30% of peak). The gradient stays meaningful. The limitations section now discusses the theoretical saturation risk and gives these quantified margins.

## MKod-3: Batch-size sensitivity not analyzed

Tested at batch sizes 4, 8, 16 (3 seeds each, NYUv2 50% subset, 60 epochs). CV across batch sizes stays below 3.5% on all validation metrics (most below 1.2%). θ_max shifts from 2.40 (bs=4) to 2.59 (bs=16), consistent with larger batches producing more stable statistics. No degradation at any tested size.

## MKod-4: Stop-gradient role not ablated independently

We ablated the stop-gradient in isolation, keeping the bounded chart and batch-aware calibration fixed (6 runs: 2 variants × 3 seeds, NYUv2 50% subset):

- **With stop-gradient (canonical):** θ_max decays from 3.08→2.44 (epoch 0→59), converging to 2.438±0.014.
- **Without stop-gradient:** θ_max grows from 3.11→3.99 (+28%), seed variance 14× higher (SD 0.192 vs 0.014).

mIoU drops 4.3% (0.198→0.190) without the stop-gradient. The dynamics are qualitatively different — without decoupling, the backward pass pushes the uncertainty scale upward monotonically instead of letting it settle. The stop-gradient is doing real work.

## MKod-5: Missing CAGrad, Nash-MTL, Auto-Lambda

Nash-MTL (Navon et al., 2022) has been run on NYUv2 with the standard protocol (3 seeds, 120 epochs). Results: mIoU 0.252±0.027, AbsRel 0.242±0.009, Angle 30.18°±1.01°, Total Loss 2.071±0.070. It underperforms every existing baseline, with mIoU ranging from 0.228 to 0.289 across seeds.

CAGrad, Auto-Lambda, IMTL-G, and FAMO were not run in the rebuttal period. They work on different principles — CAGrad projects conflicting gradients, Auto-Lambda meta-learns task weights — so Nash-MTL's result is not informative about them. We plan to add CAGrad in the revision since it is the most commonly requested and addresses gradient conflict, which is a different problem from the scale mismatch that BPGS targets. The others are further targets.

## MKod-6: Only one dense-prediction benchmark (NYUv2)

Yes, the dense-prediction coverage is thin — NYUv2 is the only entry. The suite does cover three task types (dense prediction, multi-label classification, multi-target regression), which is broader than many MTL papers, but we agree a second dense-prediction benchmark would strengthen the evaluation. Cityscapes is the plan for the revision.

## MKod-7: No computational overhead analysis

On the NYUv2 50% subset (3 seeds, 60 epochs), BPGS adds +0.15% wall-clock time (40.979s vs 40.916s per epoch) and +0.87% peak GPU memory (3368 MB vs 3339 MB) compared to Kendall. Three extra θ parameters against 18.9M shared parameters. The cost is trivial.

## MKod-8: Figures wedged into checklist, unused page-9 space

The appendix LaTeX has been reorganised: the NeurIPS checklist is separated from the substantive appendices by a page break. The page-9 space now carries the runtime/memory overhead table. This will show in the revised manuscript.
