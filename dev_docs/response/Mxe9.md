# Response to Reviewer Mxe9

## Mxe9-1 / Mxe9-2: Scope narrower than framing; not shown superior for general MTL

The framing has been tightened. The abstract, introduction, and discussion now present BPGS as a scale-robustness refinement of uncertainty weighting rather than a general MTL method. Concretely, the abstract previously implied near-parity with the best baseline on RF1 — it now says "competitive." We went through every section to remove overclaims.

## Mxe9-3 / Mxe9-4 / Mxe9-Q5: Mixed-stress shows limits in noisy/conflict regimes; Kendall/PCGrad beat BPGS; can BPGS combine with conflict-aware methods?

Yes, this is a genuine limitation. The numbers from the heterogeneous mixed-stress study (Table 7) show it clearly:

| Regime   | Kendall | PCGrad | BPGS |
|----------|---------|--------|------|
| Clean    | 0.687±0.010 | **0.688±0.016** | 0.679±0.017 |
| Noisy    | **0.659±0.007** | 0.656±0.007 | 0.641±0.013 |
| Conflict | **0.664±0.012** | 0.660±0.011 | 0.652±0.012 |

BPGS trails Kendall by 0.018 (noisy) and 0.012 (conflict) in macro score. On the other hand, BPGS has the best worst-task score in the clean regime (0.301 vs Kendall 0.267 and PCGrad 0.274), while UWSO collapses to 0.000 across all regimes.

This fits what BPGS actually does: it stabilises scalar task weights against scale imbalance, but it does not modify gradients. When the problem shifts to gradient conflict or noise, methods that work directly on the gradient (PCGrad, Kendall through its unconstrained parameterization) have a structural edge. BPGS was not designed for that regime and does not claim to solve it.

The practical implication is that BPGS and conflict-aware methods like PCGrad or CAGrad address different failure modes. A combined approach — BPGS for the weighting, PCGrad/CAGrad for the gradient — is a natural direction, and the discussion now states this.

## Mxe9-5 / Mxe9-6 / Mxe9-Q3: Incomplete comparison set; missing Nash-MTL, IMTL-G, FAMO

Nash-MTL (Navon et al., 2022) has been run on NYUv2 with the same 120-epoch, 3-seed protocol. Results: mIoU 0.252±0.027, AbsRel 0.242±0.009, Angle 30.18°±1.01°, Total Loss 2.071±0.070. It falls below every existing baseline, with high variance across seeds (mIoU spans 0.228–0.289). The comparison now covers 7 methods (Static, Kendall, UWSO, PCGrad, GradNorm, BPGS, Nash-MTL).

CAGrad, IMTL-G, FAMO, and Auto-Lambda were not run during the rebuttal period. They work differently from Nash-MTL — CAGrad projects gradients to reduce inter-task conflict, FAMO uses a fast multi-objective formulation — so Nash-MTL's poor result on our setup says nothing about theirs. We intend to add CAGrad in the revision since it is the most requested and targets a different problem (gradient conflict) than BPGS (scale mismatch). IMTL-G and FAMO are on the list as well.

## Mxe9-7 / Mxe9-8: Limited benchmark diversity beyond NYUv2; only two additional real-data benchmarks

Fair criticism. The current suite does cover three different task types — dense prediction (NYUv2), multi-label classification (Yeast), and multi-target regression (RF1) — but only one of those is a dense-prediction benchmark. Cityscapes is the obvious addition and is our top priority for the revision. That said, the breadth across task types (dense prediction, classification, regression) is already wider than many MTL papers that evaluate on NYUv2 alone.

## Mxe9-9 / Mxe9-10: Only three seeds; statistical evidence insufficient

We reran the synthetic scale-stress experiment with 10 seeds (42–51) across the full 4×3 grid (120 runs total). BPGS ranks first at every scale factor, same as with 3 seeds. The gap at ×1000 is +1.07 combined SD vs Kendall. Relative degradation ×1→×1000: BPGS 27.0%, Kendall 32.3%, UWSO 28.5%. Means barely change between 3 and 10 seeds (BPGS ×1: 0.752→0.743; Kendall ×1000: 0.495→0.499). The 10-seed table is in the revision. The other headline results stay at 3 seeds — the limitations section now says so.

## Mxe9-11 / Mxe9-12 / Mxe9-Q4: No runtime/overhead analysis; practical cost unclear

Measured on the NYUv2 50% subset (3 seeds, 60 epochs). BPGS adds +0.15% wall-clock time per epoch (40.979s vs 40.916s for Kendall) and +0.87% peak GPU memory (3368 MB vs 3339 MB). Three extra θ parameters on top of 18.9M shared parameters. The overhead is negligible.

## Mxe9-Q1 / Mxe9-Q2: Sensitivity to first-batch calibration

Three loader seeds (1001, 2001, 3001) with fixed model seed, NYUv2 50% subset. All validation metrics have CV < 2% across loader seeds (most < 0.6%). The θ_max trajectory converges to within 0.007 (0.3% spread). The choice of first batch does not meaningfully affect the final result.

## Mxe9-Q6: Sensitivity to batch size

Tested at batch sizes 4, 8, 16 (3 seeds each, NYUv2 50% subset, 60 epochs). CV across batch sizes is < 3.5% on all metrics (most < 1.2%). θ_max shifts from 2.40 (bs=4) to 2.59 (bs=16), which makes sense — larger batches give more stable gradient estimates. No degradation at any tested size. BPGS works across a 4× batch range without retuning.
