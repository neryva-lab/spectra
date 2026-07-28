
## 1.  Anonymity violation

All of the identity and affiliation words cited in the reviews have been removed from `spectra/__init__.py`, `setup.py`, `pyproject.toml`, and `LICENSE`. And every `__author__` field now in the codebase reads "Anonymous."
  

## 2. Undocumented 100× gradient scale; equations don't describe optimizer; Eqs (5)–(10) wouldn't reproduce Table 2

The gradient scale on θ, `theta_grad_scale=100.0`, is an expected design choice. Because the uncertainty objective produces smaller gradients than the network objective, and the scale factor is there to compensate for this. The value is consistent across all code paths (`configs/method/bpgs.yaml:12`, `configs/empirical/bpgs/default.yaml:8`, `spectra/baselines/__init__.py:38`). And all the formalisation and equations would include this hyperparameter, so the method description matches the optimiser exactly.
  

## 3. Code-paper mismatches (hyperparams, selection metric, grad clip, stop-gradient notation, other)

  
All mismatches have been correctly resolved:

**NYUv2 hyperparams (120/8 vs 80/4):** The config file `configs/preset/nyuv2_bpgs.yaml` had stale values (80/4) that did not match the actual experiments (120/8). The study runner bypassed the config, so published results were unaffected, but anyone using `preset=nyuv2_bpgs` would get wrong settings. 
  
**Selection metric (val/total_loss vs val/miou):** The shared NYUv2 dataset default remains `val/total_loss (min)`. The final benchmark uses an explicit override of `val/miou (max)`. The mIoU is the standard segmentation metric on NYUv2 and appears in recent MTL work (GradNorm, PCGrad); therefore, the selection metric matches the primary evaluation criterion. mIoU also provides better method comparison (CV 8.9% vs 3.3%) and does not favour BPGS — Static has the highest mIoU (0.345 vs BPGS 0.311). Checkpoint quality differs by at most 0.0025 mIoU regardless of selection metric. Both settings would be documented in the appendix.


**Gradient clipping:** And the ablation appendix incorrectly stated that "gradient clipping 1.0" for BPGS ablation variants. They actually use `grad_clip=10.0` (from the method config). Only the Kendall variant uses 1.0. 
  

**Eq. (10) stop-gradient notation:** `sg[]` has been added to the μ(L) and σ̄(L) definitions, matching the `.detach()` calls in `spectra/core/bpgs.py:126-133`. The equations now state explicitly that batch statistics are detached from the graph.

  

**Other inconsistencies:** `configs/method/static.yaml` has been standardised to the same package pattern as other method configs.

  

## 4. No θ saturation analysis; boundedness of s ≠ learnability of θ; gradient factor can collapse; limitations section omits saturation

  
Yeah, it is right that boundedness of s does not guarantee learnability of θ at the boundary. And the sigmoid derivative σ(θ)(1−σ(θ)) shrinks as θ moves toward the boundary, reducing the effective gradient. To verify whether this is a practical problem or not, we analysed the logged runs across all three datasets.

  

The bounded latent coordinate z_i = (s_i − μ)/σ relative to the boundary radius τ_T:
  

- **NYUv2** (T=3, τ_T=1.514): max |z_i|/τ_T = 0.9327 (epoch 0, task 2, seed 43). By final epoch, ratios ≤ 0.84.

- **Yeast** (T=14, τ_T=3.706): max |z_i|/τ_T = 0.7017 (epoch 0, task 8, seed 42). By final epoch, ratios ≤ 0.69.

- **RF1** (T=8, τ_T=2.746): max |z_i|/τ_T = 0.8937 (epoch 0, task 2, seed 44). By the final epoch, ratios ≤ 0.89.

Based on this analysis, no run reaches the saturation boundary. The closest approach is always at epoch 0 (auto-calibration initialisation), and every trajectory moves inward from there. At the worst observed point (|z_i|/τ_T = 0.93, NYUv2 epoch 0), σ(θ) ≈ 0.966, so the derivative factor σ(θ)(1−σ(θ)) ≈ 0.033 — about 13% of its peak value of 0.25. By the final epoch (ratio ≤ 0.84), the factor rises to ≈ 0.074, roughly 30% of peak. The gradient remains meaningful throughout training.


We would definitely add this to the limitations section, mentioning the risk clearly: if a task's log-loss sat outside the bounded interval long enough, the gradient would decay, and recovery would be hard. However, in practice, the method stays well inside the learnable region, and the trajectories move away from the boundary, not toward it.

  

## 5. "Matches classical homoscedastic" claim misleading; same form ≠ same fixed-point; Kendall optimum reachable, BPGS not outside bound

  

We ran a controlled ablation to test whether L1-normalising Kendall's weights is enough to recover BPGS's robustness (36 runs: 4 scales × 3 methods × 3 seeds). Macro score (defined in §4):

  

| Scale | BPGS | Kendall | Kendall+L1 |

|-------|------|---------|------------|

| ×1    | 0.789±0.018 | 0.788±0.014 | 0.794±0.017 |

| ×10   | 0.791±0.015 | 0.781±0.023 | 0.780±0.022 |

| ×100  | 0.788±0.016 | 0.734±0.037 | 0.742±0.029 |

| ×1000 | 0.785±0.017 | 0.658±0.042 | 0.689±0.034 |

  

Scale sensitivity ×1→×1000: BPGS −0.004, Kendall −0.130, Kendall+L1 −0.105.


The L1-normalization would help the Kendall at ×1000; however, it does not close the gap that Kendall+L1 still degrades by −0.105, whereas BPGS degrades by −0.004. The bounded chart and the split optimisation each contribute independently. We verified the latter with a separate stop-gradient ablation (6 runs, bounded chart held constant): removing the stop-gradient causes θ_max to grow +28% instead of decaying, with 14× higher variance across seeds (SD 0.192 vs 0.014). So normalisation alone is not sufficient, and the stop-gradient has a measurable stabilising effect. The related work would now distinguish the fixed-point structure from the algebraic similarity of the objectives.

  

## 6. Narrow experimental scope

  
This is a fair point, and we understand it deeply. The current suite covers three task types — dense prediction (NYUv2), multi-label classification (Yeast), and multi-target regression (RF1) and synthetic stress tests. We were hoping to add more dense datasets due to different constraints; we could not achieve it. However, we can be certain that we plan to add Cityscapes in the revision, running BPGS and all baselines under the same experimental protocol.


## 7. Only three seeds

  
After the suggestion from the reviewer to address it, we reran the synthetic scale-stress experiment with 10 seeds (42–51) across the full 4×3 grid (120 runs total). And BPGS ranks first at all the scale factors, matching the 3-seed result. The gap at ×1000 is +1.07 combined SD vs Kendall. Relative degradation ×1→×1000: BPGS 27.0%, Kendall 32.3%, UWSO 28.5%. This means barely a shift between 3 and 10 seeds (BPGS ×1: 0.752→0.743; Kendall ×1000: 0.495→0.499). The 10-seed table would be in the revised results. The other headline results remain at 3 seeds, and this would be stated in the limitations section.


## 8. Robustness claim rests mainly on synthetic diagnostics; Table 4 admits not best on RF1

  
We understand it was our shortcoming. The RF1 framing would be corrected. The abstract would say "competitive" on RF1 instead of implying proximity to the best baseline. The results section would state explicitly that PCGrad leads on RMSE and MAE, and UWSO leads on mean R². The rescaling invariance is now backed by a formal proof (revised §3), not only by the synthetic result. All claims across the abstract, introduction, and discussion would be checked for consistency with the evidence.

  

## 9. BPGS is another option, not a paradigm shift


BPGS is not a paradigm shift, but it solves a specific failure mode. The reason we think it is still a useful contribution: loss-scale mismatch is a common practical problem that existing methods do not explicitly handle. Kendall degrades under rescaling (macro score drops −0.130 at ×1000), and gradient-surgery methods like PCGrad address conflict but not scale. BPGS fills that specific gap, and it does so cheaply (+0.15% time, +0.87% memory). The paper's positioning would be revised to reflect this. 
## 10. No single benchmark shows dominance; engineering refinement

  
Section 2 (Related Work) would be rewritten to scope the contribution. It now distinguishes three MTL lineages: (1) uncertainty weighting (Kendall, GradNorm, dynamic task prioritisation) — BPGS belongs here as a bounded/batch-aware variant; (2) gradient surgery (PCGrad, CAGrad) — BPGS does not touch gradient directions; (3) Pareto-style multi-objective methods (Sener–Koltun). The revised scope statement: "BPGS is best understood as a bounded, batch-aware refinement of uncertainty weighting that is designed to improve robustness to loss-scale mismatch." No broader claim is made.

## 11. Lacks comparison to recent SOTA (most recent ref from 2021)

  

Nash-MTL (Navon et al., 2022) has been added to the NYUv2 comparison (3 seeds, 120 epochs, same protocol). It achieves mIoU 0.252±0.027, AbsRel 0.242±0.009, Angle 30.18°±1.01°, Total Loss 2.071±0.070 with substantial seed variance (mIoU ranges from 0.228 to 0.289). The comparison now includes 7 methods.

CAGrad, IMTL-G, and FAMO were not implemented during this phase. We plan to add CAGrad in the revision. As it is the most requested baseline and operates on a different axis than BPGS (gradient conflict vs. scale mismatch). IMTL-G and FAMO are further targets.

  
## 12. Supplementary material poorly laid out

  

The appendix LaTeX has been restructured: the NeurIPS checklist is now separated from the substantive appendices by a page break, and the freed page-9 space carries the runtime/memory overhead analysis. This will be visible in the revised manuscript.