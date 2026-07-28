# Response to Reviewer AqnD

## AqnD-F1: Anonymity violation

We have removed all reviewer-cited identity and affiliation strings from the repository content. The files `spectra/__init__.py`, `setup.py`, `pyproject.toml`, and `LICENSE` have been scrubbed. The only remaining `__author__` string is in `experiments/bpgs_analysis/analysis/__init__.py`, which uses the generic label "BPGS Authors" and is not the cited leak.

## AqnD-1 / AqnD-2 / AqnD-3: Undocumented 100× gradient scale; equations don't describe optimizer; Eqs (5)–(10) wouldn't reproduce Table 2

The undocumented gradient scale on θ is now documented. The value `theta_grad_scale=100.0` is a fixed design choice, not a bug. It compensates for the fact that the uncertainty objective's contribution to parameter updates is structurally smaller than the network objective's. It is fully consistent across all code paths (`configs/method/bpgs.yaml:12`, `configs/empirical/bpgs/default.yaml:8`, `spectra/baselines/__init__.py:38`). The formalization and paper equations have been updated to include this hyperparameter. The method description now matches the optimizer implementation exactly.

## AqnD-10 / AqnD-11 / AqnD-12 / AqnD-13 / AqnD-17 / AqnD-18: Code-paper mismatches (hyperparams, selection metric, grad clip, stop-gradient notation, other)

All mismatches have been reconciled:

**NYUv2 hyperparams (120/8 vs 80/4):** The preset file `configs/preset/nyuv2_bpgs.yaml` had stale values (80/4) that did not match the actual experiments (120/8). The study runner bypassed the preset, so published results were unaffected, but anyone using `preset=nyuv2_bpgs` would get wrong settings. Updated to match ground truth.

**Selection metric (val/total_loss vs val/miou):** The shared NYUv2 dataset default remains `val/total_loss (min)`. The final benchmark uses an explicit override `val/miou (max)`. Justification: mIoU shows 2.7× better method separation (CV 8.9% vs 3.3%) and does not favor BPGS — Static has the highest mIoU (0.345 vs BPGS 0.311). Per-method checkpoint quality differs by at most 0.0025 mIoU regardless of selection metric. The appendix now documents both settings explicitly.

**Gradient clipping:** The ablation appendix line 8 incorrectly stated "gradient clipping 1.0" for BPGS ablation variants. BPGS variants use `grad_clip=10.0` (from method config), matching the canonical BPGS setting. Only the Kendall ablation variant uses 1.0. This has been corrected. No code change needed.

**Eq. (10) stop-gradient notation:** The `sg[]` annotation has been added to the μ(L) and σ̄(L) definitions in the formalization, matching the code (`spectra/core/bpgs.py:126-133` where `.detach()` is called). The equations now state explicitly that batch statistics are detached from the computation graph.

**Other inconsistencies:** The static method config (`configs/method/static.yaml`) has been standardized to the same package pattern as other method configs. All reconciliation details are documented in the paper source.

## AqnD-4 / AqnD-5 / AqnD-6 / AqnD-C1 / AqnD-C2: No θ saturation analysis; boundedness of s ≠ learnability of θ; gradient factor can collapse; limitations section omits saturation

We analyzed existing logged runs across all three main-paper datasets (NYUv2, Yeast, RF1). The bounded latent coordinate z_i = (s_i − μ)/σ relative to its boundary radius τ_T is:

- **NYUv2** (T=3, τ_T=1.514): max |z_i|/τ_T = 0.9327 (epoch 0, task 2, seed 43). Final-epoch ratios ≤ 0.84.
- **Yeast** (T=14, τ_T=3.706): max |z_i|/τ_T = 0.7017 (epoch 0, task 8, seed 42). Final-epoch ratios ≤ 0.69.
- **RF1** (T=8, τ_T=2.746): max |z_i|/τ_T = 0.8937 (epoch 0, task 2, seed 44). Final-epoch ratios ≤ 0.89.

No logged run reaches or exceeds the saturation boundary |z_i| = τ_T. The closest values occur at epoch 0 (auto-calibration initialization), and all trajectories move inward from there. There is no evidence of sustained boundary locking or gradient collapse in the stored runs. We have added this analysis to the limitations discussion, acknowledging that while no saturation is observed empirically, the theoretical risk is inherent to any bounded parameterization.

## AqnD-7 / AqnD-8 / AqnD-9: "Matches classical homoscedastic" claim misleading; same form ≠ same fixed-point; Kendall optimum reachable, BPGS not outside bound

We ran a controlled Kendall + L1-normalization ablation (36 runs: 4 scales × 3 methods × 3 seeds) to test whether L1-normalization alone explains BPGS's robustness. Results:

| Scale | BPGS | Kendall | Kendall+L1 |
|-------|------|---------|------------|
| ×1    | 0.789±0.018 | 0.788±0.014 | 0.794±0.017 |
| ×10   | 0.791±0.015 | 0.781±0.023 | 0.780±0.022 |
| ×100  | 0.788±0.016 | 0.734±0.037 | 0.742±0.029 |
| ×1000 | 0.785±0.017 | 0.658±0.042 | 0.689±0.034 |

Scale sensitivity ×1→×1000: BPGS −0.004, Kendall −0.130, Kendall+L1 −0.105.

L1-normalization alone is not enough to recover BPGS-scale invariance. Kendall+L1 improves over Kendall at ×1000 but still degrades substantially (−0.105 vs BPGS −0.004). This confirms that the bounded chart and split optimization do independent work beyond what normalization of Kendall weights provides. We have revised the related work to distinguish the fixed-point structure (now stated as different) from the algebraic similarity of the uncertainty objectives.

## AqnD-15: Only three seeds

See response to Mxe9-9/Mxe9-10. The synthetic scale-stress experiment has been expanded to 10 seeds (120 runs). BPGS first at every scale. Gap at ×1000: +1.07 SD. Relative degradation: BPGS 27.0%, Kendall 32.3%, UWSO 28.5%. Ranking unchanged from 3-seed estimate.

## AqnD-16: Robustness claim rests mainly on synthetic diagnostics; Table 4 admits not best on RF1

We have corrected the RF1 framing (see WI-8). The abstract now states BPGS is "competitive" on RF1 rather than claiming close proximity to the leading baseline. The introduction and results section now state explicitly that BPGS is not the top method on RF1 RMSE or MAE (PCGrad is best on RMSE and MAE; UWSO is best on mean R²). The invariance proof (see below) provides an algebraic justification for the synthetic rescaling result. The remaining sections (abstract, introduction, discussion) have been brought into alignment through a final consistency pass that confirmed all claims now match the evidence.

## AqnD-20 / AqnD-21 / AqnD-23: BPGS is another option, not paradigm shift; no single benchmark shows dominance; engineering refinement

We have rewritten Section 2 (Related Work) to position BPGS precisely as a scale-robustness-focused refinement of uncertainty weighting, not a general MTL advance. The section now distinguishes three lineages: (1) uncertainty weighting (Kendall, GradNorm, dynamic task prioritization), where BPGS fits as a bounded/batch-aware refinement; (2) gradient surgery (PCGrad, CAGrad), where BPGS is different because it does not modify gradient directions; (3) Pareto-style multi-objective optimization (Sener–Koltun). The scope statement now reads: "BPGS is best understood as a bounded, batch-aware refinement of uncertainty weighting that is designed to improve robustness to loss-scale mismatch." This scoped claim matches the empirical evidence.

## AqnD-22: Lacks comparison to recent SOTA (most recent ref from 2021)

We have added Nash-MTL (2022) as an additional baseline. Results: Nash-MTL mIoU 0.252, AbsRel 0.242, Angle 30.18°, Total Loss 2.071 — underperforms all paper baselines across all metrics. The paper now compares against 7 methods including one from 2022. We acknowledge that CAGrad (2021), IMTL-G (2022), and FAMO (2023) remain as future comparison targets.

## AqnD-19: Supplementary material poorly laid out

We have prepared a layout cleanup plan: separate the NeurIPS checklist from the substantive appendices with a clear page break and repurpose any remaining space for a compact supplemental item. Paper edits cannot be uploaded during the rebuttal window, but this will be applied before any future submission.
