# Response to Reviewer AqnD

## AqnD-F1: Anonymity violation

All identity and affiliation strings cited by the reviewer have been removed from `spectra/__init__.py`, `setup.py`, `pyproject.toml`, and `LICENSE`. Every `__author__` field in the codebase now reads "Anonymous."

## AqnD-1 / AqnD-2 / AqnD-3: Undocumented 100× gradient scale; equations don't describe optimizer; Eqs (5)–(10) wouldn't reproduce Table 2

The gradient scale on θ is now documented in the paper. `theta_grad_scale=100.0` is a deliberate design choice — the uncertainty objective produces structurally smaller gradients than the network objective, and the scale factor compensates for this. The value is consistent across all code paths (`configs/method/bpgs.yaml:12`, `configs/empirical/bpgs/default.yaml:8`, `spectra/baselines/__init__.py:38`). The formalization and equations now include this hyperparameter, so the method description matches the optimizer exactly.

## AqnD-10 / AqnD-11 / AqnD-12 / AqnD-13 / AqnD-17 / AqnD-18: Code-paper mismatches (hyperparams, selection metric, grad clip, stop-gradient notation, other)

All mismatches have been reconciled:

**NYUv2 hyperparams (120/8 vs 80/4):** The preset file `configs/preset/nyuv2_bpgs.yaml` had stale values (80/4) that did not match the actual experiments (120/8). The study runner bypassed the preset, so published results were unaffected, but anyone using `preset=nyuv2_bpgs` would get wrong settings. Fixed.

**Selection metric (val/total_loss vs val/miou):** The shared NYUv2 dataset default remains `val/total_loss (min)`. The final benchmark uses an explicit override `val/miou (max)`. mIoU is the standard segmentation metric on NYUv2 and is prominently reported in recent MTL work (GradNorm, PCGrad), so the selection metric matches the primary evaluation criterion. mIoU also provides better method separation (CV 8.9% vs 3.3%) and does not favor BPGS — Static has the highest mIoU (0.345 vs BPGS 0.311). Checkpoint quality differs by at most 0.0025 mIoU regardless of selection metric. Both settings are now documented in the appendix.

**Gradient clipping:** The ablation appendix incorrectly stated "gradient clipping 1.0" for BPGS ablation variants. They actually use `grad_clip=10.0` (from method config). Only the Kendall variant uses 1.0. Corrected in the text. No code change needed.

**Eq. (10) stop-gradient notation:** `sg[]` has been added to the μ(L) and σ̄(L) definitions, matching the `.detach()` calls in `spectra/core/bpgs.py:126-133`. The equations now state explicitly that batch statistics are detached from the graph.

**Other inconsistencies:** `configs/method/static.yaml` has been standardized to the same package pattern as other method configs.

## AqnD-4 / AqnD-5 / AqnD-6 / AqnD-C1 / AqnD-C2: No θ saturation analysis; boundedness of s ≠ learnability of θ; gradient factor can collapse; limitations section omits saturation

The reviewer is right that boundedness of s does not guarantee learnability of θ at the boundary. The sigmoid derivative σ(θ)(1−σ(θ)) shrinks as θ moves toward the boundary, reducing the effective gradient. To check whether this is a practical problem, we examined the logged runs across all three datasets.

The bounded latent coordinate z_i = (s_i − μ)/σ relative to the boundary radius τ_T:

- **NYUv2** (T=3, τ_T=1.514): max |z_i|/τ_T = 0.9327 (epoch 0, task 2, seed 43). By final epoch, ratios ≤ 0.84.
- **Yeast** (T=14, τ_T=3.706): max |z_i|/τ_T = 0.7017 (epoch 0, task 8, seed 42). By final epoch, ratios ≤ 0.69.
- **RF1** (T=8, τ_T=2.746): max |z_i|/τ_T = 0.8937 (epoch 0, task 2, seed 44). By final epoch, ratios ≤ 0.89.

No run reaches the saturation boundary. The closest approach is always at epoch 0 (auto-calibration initialization), and every trajectory moves inward from there. At the worst observed point (|z_i|/τ_T = 0.93, NYUv2 epoch 0), σ(θ) ≈ 0.966, so the derivative factor σ(θ)(1−σ(θ)) ≈ 0.033 — about 13% of its peak value of 0.25. By the final epoch (ratio ≤ 0.84), the factor rises to ≈ 0.074, roughly 30% of peak. The gradient remains meaningful throughout training.

We have added this to the limitations section, stating the risk clearly: if a task's log-loss sat outside the bounded interval long enough, the gradient would decay and recovery would be hard. But in practice, the method stays well inside the learnable region, and the trajectories move away from the boundary, not toward it.

## AqnD-7 / AqnD-8 / AqnD-9: "Matches classical homoscedastic" claim misleading; same form ≠ same fixed-point; Kendall optimum reachable, BPGS not outside bound

We ran a controlled ablation to test whether L1-normalizing Kendall's weights is enough to recover BPGS's robustness (36 runs: 4 scales × 3 methods × 3 seeds). Macro score (defined in §4):

| Scale | BPGS | Kendall | Kendall+L1 |
|-------|------|---------|------------|
| ×1    | 0.789±0.018 | 0.788±0.014 | 0.794±0.017 |
| ×10   | 0.791±0.015 | 0.781±0.023 | 0.780±0.022 |
| ×100  | 0.788±0.016 | 0.734±0.037 | 0.742±0.029 |
| ×1000 | 0.785±0.017 | 0.658±0.042 | 0.689±0.034 |

Scale sensitivity ×1→×1000: BPGS −0.004, Kendall −0.130, Kendall+L1 −0.105.

L1-normalization helps Kendall at ×1000 but does not close the gap — Kendall+L1 still degrades by −0.105 where BPGS degrades by −0.004. The bounded chart and the split optimization each contribute independently. We verified the latter with a separate stop-gradient ablation (6 runs, bounded chart held constant): removing the stop-gradient causes θ_max to grow +28% instead of decaying, with 14× higher variance across seeds (SD 0.192 vs 0.014). So normalization alone is not sufficient, and the stop-gradient has a measurable stabilising effect. The related work now distinguishes the fixed-point structure from the algebraic similarity of the objectives.

## AqnD-14: Narrow experimental scope

Fair point. The current suite covers three task types — dense prediction (NYUv2), multi-label classification (Yeast), and multi-target regression (RF1) — plus synthetic stress tests. That spans more task types than many MTL papers that report only NYUv2, but the dense-prediction category has only one representative. We plan to add Cityscapes in the revision, running BPGS and all baselines under the same experimental protocol.

## AqnD-15: Only three seeds

We reran the synthetic scale-stress experiment with 10 seeds (42–51) across the full 4×3 grid (120 runs total). BPGS ranks first at every scale factor, matching the 3-seed result. The gap at ×1000 is +1.07 combined SD vs Kendall. Relative degradation ×1→×1000: BPGS 27.0%, Kendall 32.3%, UWSO 28.5%. Means barely shift between 3 and 10 seeds (BPGS ×1: 0.752→0.743; Kendall ×1000: 0.495→0.499). The 10-seed table is in the revised results. The other headline results remain at 3 seeds — this is now stated in the limitations section.

## AqnD-16: Robustness claim rests mainly on synthetic diagnostics; Table 4 admits not best on RF1

The RF1 framing has been corrected. The abstract now says "competitive" on RF1 instead of implying close proximity to the best baseline. The results section states explicitly that PCGrad leads on RMSE and MAE, and UWSO leads on mean R². The rescaling invariance is now backed by a formal proof (revised §3), not only by the synthetic result. All claims across the abstract, introduction, and discussion have been checked for consistency with the evidence.

## AqnD-20: BPGS is another option, not a paradigm shift

Agreed. BPGS is not a paradigm shift — it solves a specific failure mode. The reason we think it is still a useful contribution: loss-scale mismatch is a common practical problem that existing methods do not explicitly handle. Kendall degrades under rescaling (macro score drops −0.130 at ×1000), gradient-surgery methods like PCGrad address conflict but not scale. BPGS fills that particular gap, and it does so cheaply (+0.15% time, +0.87% memory). The paper's positioning has been revised to reflect this.

## AqnD-21 / AqnD-23: No single benchmark shows dominance; engineering refinement

Section 2 (Related Work) has been rewritten to scope the contribution. It now distinguishes three MTL lineages: (1) uncertainty weighting (Kendall, GradNorm, dynamic task prioritization) — BPGS belongs here as a bounded/batch-aware variant; (2) gradient surgery (PCGrad, CAGrad) — BPGS does not touch gradient directions; (3) Pareto-style multi-objective methods (Sener–Koltun). The revised scope statement: "BPGS is best understood as a bounded, batch-aware refinement of uncertainty weighting that is designed to improve robustness to loss-scale mismatch." No broader claim is made.

## AqnD-22: Lacks comparison to recent SOTA (most recent ref from 2021)

Nash-MTL (Navon et al., 2022) has been added to the NYUv2 comparison (3 seeds, 120 epochs, same protocol). It achieves mIoU 0.252±0.027, AbsRel 0.242±0.009, Angle 30.18°±1.01°, Total Loss 2.071±0.070 — below all existing baselines, with substantial seed variance (mIoU ranges from 0.228 to 0.289). The comparison now includes 7 methods.

CAGrad, IMTL-G, and FAMO were not implemented during the rebuttal period. These differ from Nash-MTL in design (CAGrad works on gradient directions, FAMO uses a fast multi-objective formulation), so Nash-MTL's result does not speak to theirs. We plan to add CAGrad in the revision — it is the most requested baseline and operates on a different axis than BPGS (gradient conflict vs. scale mismatch). IMTL-G and FAMO are further targets.

## AqnD-19: Supplementary material poorly laid out

The appendix LaTeX has been restructured: the NeurIPS checklist is now separated from the substantive appendices by a page break, and the freed page-9 space carries the runtime/memory overhead analysis. This will be visible in the revised manuscript.
