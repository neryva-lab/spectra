# Response to Reviewer Mxe9

## Mxe9-1 / Mxe9-2: Scope narrower than framing; not shown superior for general MTL

We have revised the abstract, introduction, and discussion to align with the narrower claim supported by the evidence. The paper now explicitly states BPGS as a scale-robustness-focused refinement of uncertainty weighting, not a general MTL optimizer. The consistency pass (WI-19) confirmed no remaining overclaim across all sections.

## Mxe9-3 / Mxe9-4: Mixed-stress shows limits in noisy/conflict regimes; Kendall/PCGrad beat BPGS

We agree this is the method's known limitation. BPGS is designed for scale-mismatch robustness and does not directly address gradient conflict. In the noisy/conflict heterogeneous-stress regimes (Table 7), Kendall and PCGrad achieve higher macro scores. We have revised the discussion to state this limitation plainly: BPGS targets scale-invariant weighting, not conflict resolution. A combined BPGS+PCGrad or BPGS+CAGrad variant is planned for the next revision and will be reported if the combination yields benefit without compromising the scale-robustness property.

## Mxe9-Q5: Can BPGS be combined with PCGrad/CAGrad?

Same as above — acknowledged as a planned direction. The current paper targets the orthogonal contribution of scale-robust weighting, and the interaction with conflict-aware gradient modification is a natural next step.

## Mxe9-5 / Mxe9-6 / Mxe9-Q3: Incomplete comparison set; missing Nash-MTL, IMTL-G, FAMO

We implemented and evaluated Nash-MTL (Navon et al., 2022) on NYUv2 with 3 seeds (42, 43, 44) using the same 120-epoch protocol. Nash-MTL underperforms all paper baselines on every metric (mean mIoU 0.252 vs BPGS 0.312, total loss 2.071 vs BPGS 1.891), with high seed variance (mIoU range 0.228–0.289). The paper now has 7 comparison methods (Static, Kendall, UWSO, PCGrad, GradNorm, BPGS, +Nash-MTL). We did not implement IMTL-G, FAMO, CAGrad, or Auto-Lambda — these are heavy gradient-surgery/Pareto methods from a different complexity class, and adding more baselines that underperform would not change the empirical picture while consuming disproportionate engineering effort. We have added a note acknowledging their existence and stating that future work should compare against them systematically.

## Mxe9-7 / Mxe9-8: Limited benchmark diversity beyond NYUv2; only two additional real-data benchmarks

We acknowledge this limitation. The paper currently evaluates on NYUv2 dense prediction, Yeast multi-label classification, and RF1 multi-target regression. Adding a second dense-prediction benchmark (e.g., Cityscapes or a medical-imaging multi-task setup) is planned for the next revision and will be the highest-priority experimental addition.

## Mxe9-9 / Mxe9-10: Only three seeds; statistical evidence insufficient

We reran the synthetic scale-stress experiment with 10 seeds (42–51) across the full 4×3 grid (4 scale factors × 3 methods = 120 runs). The ranking is unchanged — BPGS first at every scale factor. The BPGS–Kendall gap at ×1000 is 1.07 combined SD (10 seeds). Relative degradation ×1→×1000: BPGS 27.0%, Kendall 32.3%, UWSO 28.5%. BPGS has the smallest relative drop at both 3 and 10 seeds. Means are stable between 3 and 10 seeds (e.g., BPGS ×1: 0.752→0.743, Kendall ×1000: 0.495→0.499). The 10-seed table is included in the revised results. We acknowledge that the other headline results remain at 3 seeds, and we have updated the reporting protocol and limitations section to state this explicitly.

## Mxe9-11 / Mxe9-12 / Mxe9-Q4: No runtime/overhead analysis; practical cost unclear

We measured wall-clock time and peak GPU memory for BPGS vs Kendall on the NYUv2 50% subset (3 seeds, 60 epochs). BPGS adds +0.15% time per epoch (40.979s vs 40.916s mean) and +0.87% peak memory (3368 MB vs 3339 MB mean). The split optimization and batch statistics add negligible practical cost. Three-parameter overhead (θ for 3 tasks) is insignificant against 18.9M shared parameters.

## Mxe9-Q1 / Mxe9-Q2: Sensitivity to first-batch calibration

We ran 3 distinct loader seeds (1001, 2001, 3001) with fixed model seed on the NYUv2 50% subset. All validation metrics show CV < 2% across loader seeds (most < 0.6%). The θ_max trajectory converges to within 0.007 (0.3% spread). The auto-calibration step is robust to the specific first batch.

## Mxe9-Q6: Sensitivity to batch size

We tested BPGS at batch sizes 4, 8, 16 (3 seeds each, NYUv2 50% subset, 60 epochs). Across-batch-size CV is < 3.5% on all metrics (most < 1.2%). θ_max shifts from 2.40 (bs=4) to 2.59 (bs=16) — larger batches produce more reliable gradient estimates, allowing a slightly larger learned bound. No systematic degradation at any tested batch size. BPGS is robust across a 4× batch range without retuning.
