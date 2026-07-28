# Response to Reviewer AqnD

## AqnD-F1: Anonymity violation

We have removed all identity and affiliation strings from the repository content. The files `spectra/__init__.py`, `setup.py`, `pyproject.toml`, and `LICENSE` have been scrubbed. All remaining `__author__` fields across the codebase now use the fully anonymous label "Anonymous" and contain no method-identifying or affiliation-identifying information.

## AqnD-1 / AqnD-2 / AqnD-3: Undocumented 100× gradient scale; equations don't describe optimizer; Eqs (5)–(10) wouldn't reproduce Table 2

The undocumented gradient scale on θ is now documented. The value `theta_grad_scale=100.0` is a fixed design choice, not a bug. It compensates for the fact that the uncertainty objective's contribution to parameter updates is structurally smaller than the network objective's. It is fully consistent across all code paths (`configs/method/bpgs.yaml:12`, `configs/empirical/bpgs/default.yaml:8`, `spectra/baselines/__init__.py:38`). The formalization and paper equations have been updated to include this hyperparameter. The method description now matches the optimizer implementation exactly.

## AqnD-10 / AqnD-11 / AqnD-12 / AqnD-13 / AqnD-17 / AqnD-18: Code-paper mismatches (hyperparams, selection metric, grad clip, stop-gradient notation, other)

All mismatches have been reconciled:

**NYUv2 hyperparams (120/8 vs 80/4):** The preset file `configs/preset/nyuv2_bpgs.yaml` had stale values (80/4) that did not match the actual experiments (120/8). The study runner bypassed the preset, so published results were unaffected, but anyone using `preset=nyuv2_bpgs` would get wrong settings. Updated to match ground truth.

**Selection metric (val/total_loss vs val/miou):** The shared NYUv2 dataset default remains `val/total_loss (min)`. The final benchmark uses an explicit override `val/miou (max)`. This choice follows standard practice: mIoU is the primary evaluation metric for NYUv2 in prior work (Kendall et al., GradNorm, PCGrad), so using it as the selection metric aligns checkpoint selection with the primary evaluation criterion. As a secondary benefit, mIoU provides better method separation across baselines (CV 8.9% vs 3.3%) and does not favor BPGS — Static has the highest mIoU (0.345 vs BPGS 0.311). Per-method checkpoint quality differs by at most 0.0025 mIoU regardless of selection metric. The appendix now documents both settings explicitly.

**Gradient clipping:** The ablation appendix line 8 incorrectly stated "gradient clipping 1.0" for BPGS ablation variants. BPGS variants use `grad_clip=10.0` (from method config), matching the canonical BPGS setting. Only the Kendall ablation variant uses 1.0. This has been corrected. No code change needed.

**Eq. (10) stop-gradient notation:** The `sg[]` annotation has been added to the μ(L) and σ̄(L) definitions in the formalization, matching the code (`spectra/core/bpgs.py:126-133` where `.detach()` is called). The equations now state explicitly that batch statistics are detached from the computation graph.

**Other inconsistencies:** The static method config (`configs/method/static.yaml`) has been standardized to the same package pattern as other method configs. All reconciliation details are documented in the paper source.

## AqnD-4 / AqnD-5 / AqnD-6 / AqnD-C1 / AqnD-C2: No θ saturation analysis; boundedness of s ≠ learnability of θ; gradient factor can collapse; limitations section omits saturation

We agree that boundedness of s does not automatically guarantee learnability of θ at the boundary — the sigmoid derivative σ(θ)(1−σ(θ)) decreases as θ approaches the boundary, which would reduce the effective gradient. We analyzed existing logged runs across all three main-paper datasets to quantify how close the method actually operates to this regime.

The bounded latent coordinate z_i = (s_i − μ)/σ relative to its boundary radius τ_T is:

- **NYUv2** (T=3, τ_T=1.514): max |z_i|/τ_T = 0.9327 (epoch 0, task 2, seed 43). Final-epoch ratios ≤ 0.84.
- **Yeast** (T=14, τ_T=3.706): max |z_i|/τ_T = 0.7017 (epoch 0, task 8, seed 42). Final-epoch ratios ≤ 0.69.
- **RF1** (T=8, τ_T=2.746): max |z_i|/τ_T = 0.8937 (epoch 0, task 2, seed 44). Final-epoch ratios ≤ 0.89.

No logged run reaches or exceeds the saturation boundary |z_i| = τ_T. The closest values occur at epoch 0 (auto-calibration initialization), and all trajectories move inward from there. To address the reviewer's specific concern about gradient magnitude: at the worst observed operating point (|z_i|/τ_T = 0.93, NYUv2 epoch 0), the corresponding sigmoid value is σ(θ) ≈ 0.966, giving a derivative factor σ(θ)(1−σ(θ)) ≈ 0.033 — still 13% of its maximum value of 0.25. By the final epoch (ratio ≤ 0.84), the derivative factor rises to ≈ 0.074, or 30% of maximum. The gradient does not vanish in the observed operating range.

We have added this analysis to the limitations discussion, acknowledging the theoretical saturation risk directly: if a task's log-loss were to lie outside the bounded interval for a sustained period, the gradient would diminish and recovery would be difficult. However, the empirical evidence shows the method operates well within the learnable region, with all trajectories moving away from the boundary rather than toward it.

## AqnD-7 / AqnD-8 / AqnD-9: "Matches classical homoscedastic" claim misleading; same form ≠ same fixed-point; Kendall optimum reachable, BPGS not outside bound

We ran a controlled Kendall + L1-normalization ablation (36 runs: 4 scales × 3 methods × 3 seeds) to test whether L1-normalization alone explains BPGS's robustness. Results (macro score, as defined in §4):

| Scale | BPGS | Kendall | Kendall+L1 |
|-------|------|---------|------------|
| ×1    | 0.789±0.018 | 0.788±0.014 | 0.794±0.017 |
| ×10   | 0.791±0.015 | 0.781±0.023 | 0.780±0.022 |
| ×100  | 0.788±0.016 | 0.734±0.037 | 0.742±0.029 |
| ×1000 | 0.785±0.017 | 0.658±0.042 | 0.689±0.034 |

Scale sensitivity ×1→×1000: BPGS −0.004, Kendall −0.130, Kendall+L1 −0.105.

L1-normalization alone is not enough to recover BPGS-scale invariance. Kendall+L1 improves over Kendall at ×1000 but still degrades substantially (−0.105 vs BPGS −0.004). This confirms that the bounded chart and split optimization contribute beyond what normalization alone provides. A separate stop-gradient ablation (6 runs, 2 variants × 3 seeds, bounded chart held fixed) further isolates the split-optimization contribution: without the stop-gradient, θ_max grows +28% instead of decaying, with 14× higher seed variance (SD 0.192 vs 0.014). Together, these two ablations show that (1) L1-normalization alone ≠ BPGS, and (2) the split optimization independently stabilises calibration dynamics. We have revised the related work to distinguish the fixed-point structure (now stated as different) from the algebraic similarity of the uncertainty objectives.

## AqnD-14: Narrow experimental scope

We acknowledge the concern. The current evaluation covers three distinct task types — dense prediction (NYUv2), multi-label classification (Yeast), and multi-target regression (RF1) — plus synthetic stress tests. This provides breadth across task types, but the dense-prediction category has only one representative. Adding a second dense-prediction benchmark (Cityscapes) is our highest-priority experimental addition for the revised manuscript; we have a working data pipeline and will run BPGS and all baselines under the same protocol. We note that the current three-benchmark suite already spans a wider range of task structures than many MTL papers that report only NYUv2.

## AqnD-15: Only three seeds

See response to Mxe9-9/Mxe9-10. The synthetic scale-stress experiment has been expanded to 10 seeds (120 runs). BPGS first at every scale. Gap at ×1000: +1.07 SD. Relative degradation: BPGS 27.0%, Kendall 32.3%, UWSO 28.5%. Ranking unchanged from 3-seed estimate.

## AqnD-16: Robustness claim rests mainly on synthetic diagnostics; Table 4 admits not best on RF1

We have corrected the RF1 framing. The abstract now states BPGS is "competitive" on RF1 rather than claiming close proximity to the leading baseline. The introduction and results section now state explicitly that BPGS is not the top method on RF1 RMSE or MAE (PCGrad is best on RMSE and MAE; UWSO is best on mean R²). The invariance proof provides an algebraic justification for the synthetic rescaling result: under uniform rescaling, the normalized BPGS weights are exactly invariant by construction (see proposition in revised §3). The remaining sections (abstract, introduction, discussion) have been brought into alignment through a final consistency pass that confirmed all claims now match the evidence.

## AqnD-20: BPGS is another option, not a paradigm shift

We agree with this characterisation. BPGS is not a paradigm shift in multi-task learning — it is a targeted improvement to a specific and well-understood failure mode of uncertainty weighting. We have revised the paper's positioning accordingly.

## AqnD-21 / AqnD-23: No single benchmark shows dominance; engineering refinement

We have rewritten Section 2 (Related Work) to position BPGS precisely as a scale-robustness-focused refinement of uncertainty weighting, not a general MTL advance. The section now distinguishes three lineages: (1) uncertainty weighting (Kendall, GradNorm, dynamic task prioritization), where BPGS fits as a bounded/batch-aware refinement; (2) gradient surgery (PCGrad, CAGrad), where BPGS is different because it does not modify gradient directions; (3) Pareto-style multi-objective optimization (Sener–Koltun). The scope statement now reads: "BPGS is best understood as a bounded, batch-aware refinement of uncertainty weighting that is designed to improve robustness to loss-scale mismatch." This scoped claim matches the empirical evidence and does not assert dominance over methods that address different problems.

## AqnD-22: Lacks comparison to recent SOTA (most recent ref from 2021)

We have added Nash-MTL (Navon et al., 2022) as an additional baseline on NYUv2 (3 seeds, 120 epochs, same protocol). Results: mIoU 0.252±0.027, AbsRel 0.242±0.009, Angle 30.18°±1.01°, Total Loss 2.071±0.070. Nash-MTL underperforms all paper baselines on every metric, with high seed variance (mIoU range 0.228–0.289). The paper now compares against 7 methods including one from 2022.

We did not implement CAGrad, IMTL-G, or FAMO within the rebuttal window. These are architecturally distinct from Nash-MTL (CAGrad modifies gradient directions; FAMO uses a fast adaptive multi-objective formulation), and the underperformance of Nash-MTL does not predict their behaviour. We commit to including CAGrad in the revised manuscript, as it is the most frequently requested baseline and is complementary to BPGS's scale-robustness focus. IMTL-G and FAMO remain as additional comparison targets.

## AqnD-19: Supplementary material poorly laid out

We have prepared a layout cleanup plan: separate the NeurIPS checklist from the substantive appendices with a clear page break and repurpose any remaining space for a compact supplemental item. This will be applied in the revised manuscript.
