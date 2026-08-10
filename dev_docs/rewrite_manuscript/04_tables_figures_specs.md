# 04 — Tables & Figures Specs (exact numbers, sources, output paths)

Every new or updated table/figure for the revision. All numbers below are taken from the
completed work-item reports (which were computed from the experiment outputs). During
implementation, each table must be regenerated from its source files by an analysis script —
never hand-typed (golden rule 1). The numbers here serve as the **acceptance check** for those
scripts.

---

## 1. Nash-MTL row — UPDATE `data/nyuv2/tables/nyuv2_main_table.tex`

**Source:** `outputs/nash_mtl/seed_{42,43,44}/csv_logs/nash_mtl_nyuv2_s{s}/metrics.csv`
(final epoch; verified seed 42: AbsRel 0.2298, RMSE 0.8242, mIoU 0.2891, Angle 28.74,
Within 0.2262, Total 1.9737).

| Metric | Value (mean ± std) |
|---|---|
| mIoU ↑ | 0.252 ± 0.027 |
| Abs Rel ↓ | 0.242 ± 0.009 |
| RMSE ↓ | 0.856 ± 0.029 |
| Angle ↓ | 30.18° ± 1.01° |
| Within 11.25° ↑ | 0.211 ± 0.011 |
| Total Loss ↓ | 2.071 ± 0.070 |
| Δ_M ↑ | **≈ −0.038 (must be computed by the analysis script from per-seed final metrics; do not hand-type)** |

Δ_M hand-check (means): mIoU −0.2610, AbsRel −0.0126, Angle +0.1601 → mean ≈ −0.038.
Because it is negative, present it as-is (no bold). Order rows: Static, Kendall, UWSO, PCGrad?? —
**No.** The NYUv2 main table currently lists Static, Kendall, UWSO, BPGS. Add Nash-MTL as the
last row (it is the weakest). Method label in table: `Nash-MTL`.

**Implementation:** add `nash_mtl` to `NYUV2_METHODS` in
`experiments/bpgs_analysis/analysis/common/constants.py`; stage the three Nash-MTL metrics CSVs
into the resolver's expected layout (either extend `resolve_nyuv2_path` or copy into
`data/nyuv2/final_output_versions/nash_mtl/seed_{s}/csv_logs/nash_mtl_nyuv2_s{s}/`); regenerate
table with the existing `table.py` pipeline.

---

## 2. Normalization ablation table — NEW `data/norm_ablation/tables/norm_ablation_table.tex`

**Source:** `experiment_results/exp_09_kendall_norm_ablation/20260724_113615/` (latest run dir).
**Seeds used in that run: 42, 123, 999 — see decision in `09_open_decisions.md` (preferred:
rerun with 42/43/44; if rerun, source paths change accordingly).**

Macro score by loss-scale factor (mean ± std, 3 seeds):

| Scale | BPGS | Kendall | Kendall+L1 |
|---|---|---|---|
| ×1 | 0.789 ± 0.018 | 0.788 ± 0.014 | 0.794 ± 0.017 |
| ×10 | 0.791 ± 0.015 | 0.781 ± 0.023 | 0.780 ± 0.022 |
| ×100 | 0.788 ± 0.016 | 0.734 ± 0.037 | 0.742 ± 0.029 |
| ×1000 | 0.785 ± 0.017 | 0.658 ± 0.042 | 0.689 ± 0.034 |

Scale sensitivity (×1 → ×1000): **BPGS −0.004 · Kendall −0.130 · Kendall+L1 −0.105**
(same metric as Table `tab:stress_rescaling`; the main rescaling table keeps its own 3-seed
result on seeds 42/43/44).

Caption draft:
> Normalization ablation on the pure loss-rescaling grid (macro score, mean ± std over 3 seeds).
> L1-normalizing Kendall's weights closes part of the gap at ×1000 but leaves a −0.105 scale
> sensitivity versus −0.004 for BPGS. [seed-set note per decision 09]

Placement: **Appendix B**. Label: `tab:norm_ablation`. Referenced from §5.1.

---

## 3. Stop-gradient ablation table — NEW `data/stop_gradient/tables/stop_gradient_table.tex`

**Source:** `experiment_results/12_nyuv2_stop_gradient/{split_stopgrad_on,split_stopgrad_off}/seed_{42,43,44}/csv_logs/bpgs_nyuv2_s{s}/metrics.csv`
(NYUv2 50% subset, 60 epochs; final epoch 59).

| Metric (epoch 59) | split ON (canonical) | split OFF (coupled) |
|---|---|---|
| θ_max (final) | **2.438 ± 0.014** | 3.993 ± 0.192 (+28%, 14× SD) |
| θ_max epoch 0 | 3.082 ± 0.017 | 3.109 ± 0.011 |
| val/segmentation_miou | 0.1983 | 0.1897 (−4.3%) |
| val/total_loss | 2.1278 | 2.1419 |
| val/depth_abs_rel | 0.2433 | 0.2452 |
| val/depth_rmse | 0.8433 | 0.8544 |
| val/normals_mean_angle | 29.412 | 29.019 |

Caption draft:
> Stop-gradient ablation on the NYUv2 50% subset (3 seeds, 60 epochs). Removing the stop-gradient
> from the uncertainty objective changes the dynamics qualitatively: θ_max grows +28% instead of
> settling, seed variance in θ_max increases 14×, and segmentation mIoU drops 4.3%.

Placement: **Appendix E**. Label: `tab:stop_gradient`. Referenced from §5.3.

---

## 4. Batch-size table — NEW `data/batch_size/tables/batch_size_table.tex`

**Source:** `experiment_results/11_nyuv2_batch_size/{batch_4,batch_8,batch_16}/seed_{42,43,44}/csv_logs/bpgs_nyuv2_s{s}/metrics.csv`
(NYUv2 50% subset, 60 epochs, canonical BPGS).

Seed-averaged final metrics per batch size (epoch 59):

| Metric | bs=4 | bs=8 | bs=16 | Across-bs CV |
|---|---|---|---|---|
| val/total_loss | 2.1468 | 2.1226 | 2.1507 | **0.58%** |
| val/depth_abs_rel | 0.2411 | 0.2421 | 0.2451 | **0.70%** |
| val/depth_rmse | 0.8643 | 0.8403 | 0.8490 | **1.17%** |
| val/normals_mean_angle | 29.400 | 29.223 | 29.754 | **0.75%** |
| val/segmentation_miou | 0.1955 | 0.1932 | 0.1810 | **3.35%** |
| val/pixel_acc | 0.5347 | 0.5382 | 0.5321 | **0.47%** |
| θ_max (final) | 2.396 ± 0.006 | 2.441 ± 0.020 | 2.589 ± 0.068 | — |

Caption draft:
> Batch-size sensitivity of canonical BPGS on the NYUv2 50% subset (3 seeds per batch size,
> 60 epochs). All validation metrics have across-batch-size CV below 3.5% (most below 1.2%);
> θ_max shifts modestly with batch size.

Placement: **Appendix E**. Label: `tab:batch_size`. Referenced from §5.4.

---

## 5. First-batch table — NEW `data/first_batch/tables/first_batch_table.tex`

**Source:** `experiment_results/10_nyuv2_first_batch/{loader_seed_1001,loader_seed_2001,loader_seed_3001}/seed_42/csv_logs/bpgs_nyuv2_s42/metrics.csv`
(NYUv2 50% subset, 60 epochs, fixed model seed, canonical BPGS).

| Metric (epoch 59) | seed 1001 | seed 2001 | seed 3001 | CV |
|---|---|---|---|---|
| val/total_loss | 2.1145 | 2.1040 | 2.1090 | **0.20%** |
| val/depth_abs_rel | 0.2385 | 0.2392 | 0.2411 | **0.46%** |
| val/depth_rmse | 0.8348 | 0.8302 | 0.8325 | **0.23%** |
| val/normals_mean_angle | 28.9205 | 28.8975 | 29.1069 | **0.32%** |
| val/normals_within_11_25 | 0.2274 | 0.2292 | 0.2261 | **0.56%** |
| val/segmentation_miou | 0.1912 | 0.1866 | 0.1952 | **1.84%** |
| val/pixel_acc | 0.5338 | 0.5366 | 0.5402 | **0.49%** |
| θ_max (final) | 2.4451 | 2.4382 | 2.4380 | 0.3% spread |

Caption draft:
> First-batch calibration sensitivity of canonical BPGS on the NYUv2 50% subset. Only the loader
> seed (the identity of the first observed batch) changes; all validation metrics have CV below
> 2% (most below 0.6%) and θ_max trajectories converge within 0.3% of each other.

Placement: **Appendix E**. Label: `tab:first_batch`. Referenced from §5.4.

---

## 6. Overhead table — NEW `data/overhead/tables/overhead_table.tex`

**Source:** `experiment_results/09_nyuv2_overhead/{bpgs,kendall}/seed_{42,43,44}/`
(NYUv2 50% subset, 60 epochs, single GPU; per-epoch wall-clock + peak CUDA memory logged via
callbacks — verify exact artifact layout during implementation; the WI-10 report is authoritative).

| Quantity | BPGS | Kendall | Difference |
|---|---|---|---|
| Per-epoch wall-clock (s) | 40.979 | 40.916 | **+0.15%** |
| Peak GPU memory (MB) | 3368.36 | 3339.34 | **+0.87%** |
| Total wall-clock, 60 epochs (s) | 2461.6 | 2457.9 | +3.7 s |
| Trainable parameters | 18,869,143 | 18,869,140 | +3 (the θ's) |

Per-seed values (time s / mem MB): BPGS 40.937/3368.68, 40.970/3367.74, 41.030/3368.68;
Kendall 40.915/3339.16, 40.893/3339.72, 40.941/3339.15.

Caption draft:
> Computational overhead of BPGS relative to Kendall on the NYUv2 50% subset (3 seeds, 60 epochs,
> single GPU): +0.15% wall-clock time and +0.87% peak GPU memory; the method adds T = 3 scalar
> uncertainty parameters.

Placement: **Appendix F**. Label: `tab:overhead`. Referenced from §5.6.

---

## 7. Saturation table — NEW `data/saturation/tables/saturation_table.tex`

**Source:** logged main-paper runs (WI-5; no new runs):
- NYUv2: `outputs/data/nyuv2/final_output_versions/bpgs/bpgs/`
- Yeast: `outputs/data/full_data/final_results/03_yeast_regime_check/bpgs/`
- RF1: `outputs/data/full_data/final_results/08_rf1_regime_check/bpgs/`
  (columns `train/bpgs/batch_mu`, `batch_sigma`, `log_var_i`, `theta_i`; reconstruct
  z_i = (s_i − μ)/σ̄).

| Dataset | T | τ_T | max \|z_i\|/τ_T (at epoch 0, seed, task) | final-epoch cap |
|---|---|---|---|---|
| NYUv2 | 3 | 1.5142 | 0.9327 (seed 43, task 2) | ≤ 0.84 |
| Yeast | 14 | 3.7056 | 0.7017 (seed 42, task 8) | ≤ 0.69 |
| RF1 | 8 | 2.7458 | 0.8937 (seed 44, task 2) | ≤ 0.89 |

Derived factors (state in caption or text): at the worst observed point σ(θ)(1−σ(θ)) ≈ 0.033
(13% of peak 0.25); by the final epochs ≈ 0.074 (30% of peak).

Caption draft:
> Closest observed approach to the saturation boundary across all logged main-paper runs. No run
> reaches the boundary; the closest point occurs at the auto-calibration epoch and every
> trajectory moves inward afterward.

Placement: **Appendix G**. Label: `tab:saturation`. Referenced from §3.4 and §6.

---

## 8. New figures

| Figure | Source | Content | Placement | Label |
|---|---|---|---|---|
| F-sg | wi-11 θ_max tables | θ_max vs epoch, split ON vs OFF (mean ± SD band) | Appendix E | `fig:stop_gradient_theta` |
| F-bs | wi-12 θ_max tables | θ_max vs epoch for bs 4/8/16 | Appendix E | `fig:batch_size_theta` |
| F-fb | wi-13 θ_max tables | θ_max vs epoch for loader seeds 1001/2001/3001 | Appendix E | `fig:first_batch_theta` |

Optional (space permitting, appendix only):
| F-norm | exp_09 summary | Macro score vs scale factor for BPGS/Kendall/Kendall+L1 (log x-axis) | Appendix B | `fig:norm_ablation` |

All figures to be generated by analysis scripts (matplotlib, same style as existing paper
figures: serif fonts, PDF output, consistent color palette). Check how existing figures are
stylized (`experiments/bpgs_analysis/analysis/studies/*/figures.py`) and reuse the style
helpers. Output paths: `working/paper/data/<study>/figures/pdf/<name>.pdf`.

---

## 9. Summary of new/updated files

```
working/paper/data/
  nyuv2/tables/nyuv2_main_table.tex          (UPDATE: + Nash-MTL row)
  norm_ablation/tables/norm_ablation_table.tex   (NEW)
  stop_gradient/tables/stop_gradient_table.tex   (NEW)
  stop_gradient/figures/pdf/stop_gradient_theta_max.pdf  (NEW)
  batch_size/tables/batch_size_table.tex          (NEW)
  batch_size/figures/pdf/batch_size_theta_max.pdf (NEW)
  first_batch/tables/first_batch_table.tex        (NEW)
  first_batch/figures/pdf/first_batch_theta_max.pdf (NEW)
  overhead/tables/overhead_table.tex              (NEW)
  saturation/tables/saturation_table.tex          (NEW)

analysis scripts (new or updated):
  experiments/bpgs_analysis/analysis/studies/nyuv2/           (UPDATE: nash_mtl)
  experiments/bpgs_analysis/analysis/studies/norm_ablation/   (NEW: extract/table)
  experiments/bpgs_analysis/analysis/studies/sensitivity/     (NEW: extract/table/figures —
     handles stop_gradient, batch_size, first_batch, overhead)
  experiments/bpgs_analysis/analysis/studies/saturation/      (NEW: extract/table)
```

## 10. Consistency traps (check during implementation)

1. **Rescaling table vs normalization-ablation table use different seed sets** (42/43/44 vs
   42/123/999) → BPGS ×1 reads 0.777 vs 0.789. Do not let the two tables sit side by side with
   unexplained differences (see `09_open_decisions.md`).
2. **Scale-stress table is 10-seed; rescaling table is 3-seed.** Captions must keep saying so.
3. **Ablation table uses 60 epochs on the 50% subset; main NYUv2 table uses 120 epochs on the
   full set.** New controlled studies also use the 50% subset — state it in every caption.
4. **Nash-MTL uses grad_clip=1.0** (its own config) — state in Appendix A so nobody assumes a
   uniform clip across methods.
5. **Δ_M for Nash-MTL is negative** (≈ −0.038) — bold/underline only positive best values.
6. All "≈" values (0.033, 0.074, −0.038) must be recomputed by scripts from raw data, not typed.
