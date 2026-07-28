# Response to Reviewer Mxe9

## Mxe9-1 / Mxe9-2: Scope narrower than framing; not shown superior for general MTL

We have revised the abstract, introduction, and discussion to align with the narrower claim supported by the evidence. The paper now explicitly states BPGS as a scale-robustness-focused refinement of uncertainty weighting, not a general MTL optimizer. For example, the abstract now states BPGS is "competitive" on RF1 rather than the original phrasing that implied near-parity with the leading baseline on RMSE and MAE. A final consistency pass confirmed no remaining overclaim across all sections.

## Mxe9-3 / Mxe9-4 / Mxe9-Q5: Mixed-stress shows limits in noisy/conflict regimes; Kendall/PCGrad beat BPGS; can BPGS combine with conflict-aware methods?

We agree this is the method's known limitation, and it is instructive to examine the specific numbers. In the heterogeneous mixed-stress study (Table 7), the macro scores across three regimes are:

| Regime   | Kendall | PCGrad | BPGS |
|----------|---------|--------|------|
| Clean    | 0.687±0.010 | **0.688±0.016** | 0.679±0.017 |
| Noisy    | **0.659±0.007** | 0.656±0.007 | 0.641±0.013 |
| Conflict | **0.664±0.012** | 0.660±0.011 | 0.652±0.012 |

BPGS trails Kendall by 0.018 (noisy) and 0.012 (conflict) in macro score. However, BPGS achieves the best worst-task score in the clean regime (0.301 vs Kendall 0.267 and PCGrad 0.274), while UWSO collapses entirely (worst-task score 0.000 across all regimes).

The pattern is consistent with BPGS's design: it stabilises scalar task weights against scale mismatch but does not modify gradient directions. When the primary challenge shifts from scale mismatch to gradient conflict or noise injection, methods that operate on the gradient (PCGrad, Kendall's implicit conflict handling) have an architectural advantage that BPGS does not claim to address.

This is a complementary limitation, not a contradiction. BPGS and conflict-aware methods target orthogonal failure modes — scale mismatch vs. gradient interference. A combined BPGS+PCGrad or BPGS+CAGrad variant, where BPGS handles the weighting and PCGrad/CAGrad modifies the gradient direction, is a natural next step. We have revised the discussion to state this limitation and the complementary-methods framing explicitly.

## Mxe9-5 / Mxe9-6 / Mxe9-Q3: Incomplete comparison set; missing Nash-MTL, IMTL-G, FAMO

We implemented and evaluated Nash-MTL (Navon et al., 2022) on NYUv2 with 3 seeds (42, 43, 44) using the same 120-epoch protocol. Results: mIoU 0.252±0.027, AbsRel 0.242±0.009, Angle 30.18°±1.01°, Total Loss 2.071±0.070. Nash-MTL underperforms all paper baselines on every metric, with high seed variance (mIoU range 0.228–0.289). The paper now compares against 7 methods (Static, Kendall, UWSO, PCGrad, GradNorm, BPGS, Nash-MTL).

We did not implement CAGrad, IMTL-G, FAMO, or Auto-Lambda within the rebuttal window. These methods are architecturally distinct from Nash-MTL — CAGrad modifies gradient directions, FAMO uses a fast adaptive multi-objective formulation — and Nash-MTL's underperformance on our setup does not predict theirs. We commit to including CAGrad in the revised manuscript, as it is the most frequently requested baseline and is complementary to BPGS's scale-robustness focus. IMTL-G and FAMO remain as additional comparison targets.

## Mxe9-7 / Mxe9-8: Limited benchmark diversity beyond NYUv2; only two additional real-data benchmarks

We acknowledge this limitation. The current evaluation covers three distinct task types — dense prediction (NYUv2), multi-label classification (Yeast), and multi-target regression (RF1) — which provides breadth across task structures. However, the dense-prediction category has only one representative. Adding Cityscapes as a second dense-prediction benchmark is our highest-priority experimental addition for the revised manuscript; we will run BPGS and all baselines under the same protocol used for NYUv2. We note that the current three-benchmark suite already spans a wider range of task structures (dense prediction, multi-label classification, multi-target regression) than many MTL papers that evaluate on NYUv2 alone.

## Mxe9-9 / Mxe9-10: Only three seeds; statistical evidence insufficient

We reran the synthetic scale-stress experiment with 10 seeds (42–51) across the full 4×3 grid (4 scale factors × 3 methods = 120 runs). The ranking is unchanged — BPGS first at every scale factor. The BPGS–Kendall gap at ×1000 is 1.07 combined SD (10 seeds). Relative degradation ×1→×1000: BPGS 27.0%, Kendall 32.3%, UWSO 28.5%. BPGS has the smallest relative drop at both 3 and 10 seeds. Means are stable between 3 and 10 seeds (e.g., BPGS ×1: 0.752→0.743, Kendall ×1000: 0.495→0.499). The 10-seed table is included in the revised results. We acknowledge that the other headline results remain at 3 seeds, and we have updated the reporting protocol and limitations section to state this explicitly.

## Mxe9-11 / Mxe9-12 / Mxe9-Q4: No runtime/overhead analysis; practical cost unclear

We measured wall-clock time and peak GPU memory for BPGS vs Kendall on the NYUv2 50% subset (3 seeds, 60 epochs). BPGS adds +0.15% time per epoch (40.979s vs 40.916s mean) and +0.87% peak memory (3368 MB vs 3339 MB mean). The split optimization and batch statistics add negligible practical cost. Three-parameter overhead (θ for 3 tasks) is insignificant against 18.9M shared parameters.

## Mxe9-Q1 / Mxe9-Q2: Sensitivity to first-batch calibration

We ran 3 distinct loader seeds (1001, 2001, 3001) with fixed model seed on the NYUv2 50% subset. All validation metrics show CV < 2% across loader seeds (most < 0.6%). The θ_max trajectory converges to within 0.007 (0.3% spread). The auto-calibration step is robust to the specific first batch.

## Mxe9-Q6: Sensitivity to batch size

We tested BPGS at batch sizes 4, 8, 16 (3 seeds each, NYUv2 50% subset, 60 epochs). Across-batch-size CV is < 3.5% on all metrics (most < 1.2%). θ_max shifts from 2.40 (bs=4) to 2.59 (bs=16) — larger batches produce more reliable gradient estimates, allowing a slightly larger learned bound. No systematic degradation at any tested batch size. BPGS is robust across a 4× batch range without retuning.
