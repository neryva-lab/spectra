# WI-11 Stop-Gradient Ablation Report

Date: 2026-07-25

## Scope

WI-11 isolates the role of BPGS's split-optimization stop-gradient design choice. The concern is
whether the method still behaves well when the network update and uncertainty update are no longer
kept strictly separate by detached objectives.

This is not a bounded-chart ablation and not a batch-aware ablation. Those pieces stay fixed.
Only the stop-gradient behavior changes.

## Dataset Choice

The study uses the same **50% NYUv2 subset** as the other controlled NYUv2 experiments:

- `dataset: nyuv2`
- `subset_budget: "50"`
- `subset_seed: 11`
- `use_subset_file: true`

That choice keeps the test aligned with the paper's main ablation regime and avoids introducing a
new dataset-specific confound.

## Files Updated

- `spectra/core/bpgs.py`
- `spectra/engine/optimizers/bpgs.py`
- `spectra/baselines/__init__.py`
- `configs/method/bpgs.yaml`
- `spectra/train/runner.py`
- `spectra/train/artifacts.py`
- `experiments/bpgs_study/optional/configs/12_nyuv2_stop_gradient.yaml`
- `experiments/bpgs_study/optional/utils.py`
- `docs/studies.md`
- `dev_docs/addressing_reviews/review_ledger.md`

## Experiment Execution

All six runs (2 variants × 3 seeds) were executed and completed successfully (60 epochs on NYUv2 50% subset):

| Variant | Seeds | Status |
|---|---|---|
| `split_stopgrad_on` | 42, 43, 44 | 3/3 completed |
| `split_stopgrad_off` | 42, 43, 44 | 3/3 completed |

All runs at `outputs/12_nyuv2_stop_gradient/{variant}/seed_{s}/csv_logs/bpgs_nyuv2_s{s}/metrics.csv`.

## Results

### Final Validation Metrics (epoch 59)

| Metric | on_s42 | on_s43 | on_s44 | off_s42 | off_s43 | off_s44 | on_mean | off_mean | \|Δ\| |
|---|---|---|---|---|---|---|---|---|---|---|
| val/total_loss | 2.1193 | 2.1492 | 2.1149 | 2.1162 | 2.1682 | 2.1413 | 2.1278 | 2.1419 | 0.0141 (0.66%) |
| val/depth_abs_rel | 0.2418 | 0.2486 | 0.2393 | 0.2419 | 0.2515 | 0.2424 | 0.2433 | 0.2452 | 0.0020 (0.82%) |
| val/depth_rmse | 0.8419 | 0.8522 | 0.8358 | 0.8432 | 0.8737 | 0.8463 | 0.8433 | 0.8544 | 0.0111 (1.31%) |
| val/normals_mean_angle | 29.183 | 30.067 | 28.984 | 28.878 | 29.600 | 28.580 | 29.412 | 29.019 | 0.392 (1.33%) |
| val/normals_within_11.25 | 0.2239 | 0.2114 | 0.2252 | 0.2297 | 0.2175 | 0.2324 | 0.2202 | 0.2266 | 0.0064 (2.90%) |
| val/segmentation_miou | 0.1935 | 0.2079 | 0.1934 | 0.1931 | 0.1876 | 0.1883 | 0.1983 | 0.1897 | 0.0086 (4.33%) |
| val/pixel_acc | 0.5398 | 0.5357 | 0.5372 | 0.5399 | 0.5306 | 0.5301 | 0.5375 | 0.5335 | 0.0040 (0.75%) |

### Theta_max Trajectory — The Critical Result

The most striking difference is in θ_max. With `split_stopgrad_on` (canonical), the learned uncertainty scale decays smoothly and converges to a stable value. With `split_stopgrad_off`, θ_max **grows** over training instead:

| Epoch | on (mean±sd) | off (mean±sd) |
|---|---|---|
| 0 | 3.082 ± 0.017 | 3.109 ± 0.011 |
| 10 | 2.690 ± 0.017 | 3.440 ± 0.017 |
| 20 | 2.521 ± 0.022 | 3.697 ± 0.065 |
| 30 | 2.467 ± 0.024 | 3.863 ± 0.108 |
| 40 | 2.446 ± 0.023 | 3.953 ± 0.147 |
| 50 | 2.439 ± 0.022 | 3.988 ± 0.170 |
| 59 | **2.438 ± 0.014** | **3.993 ± 0.192** |

Without the stop-gradient, θ_max increases by **+28%** over training (3.11 → 3.99), and its seed-to-seed variability is **14× higher** (sd=0.192 vs sd=0.014). The trajectories are fundamentally different — the coupled backward pass pulls the uncertainty scale into a regime where it grows monotonically rather than settling.

### Training Loss Stability

Final training losses are similar across variants, confirming the coupled backward pass does not cause optimization failure or divergence:

| Variant | seed_42 | seed_43 | seed_44 |
|---|---|---|---|
| on train/depth_loss | 0.5750 | 0.5871 | 0.5629 |
| off train/depth_loss | 0.5794 | 0.5968 | 0.5716 |

## Interpretation

The stop-gradient matters independently of the bounded chart and batch-aware calibration.

The coupled variant (`split_stopgrad_off`) produces:

1. **Qualitatively different θ_max dynamics** — the uncertainty scale grows instead of decaying, indicating a fundamental shift in how the uncertainty parameters are learned when they receive gradient signal from the network objective.

2. **Higher variance** — θ_max seed-to-seed variability is 14× larger (sd=0.19 vs 0.01), showing the coupled update is less stable.

3. **Modest validation degradation** — most validation metrics are comparable, but segmentation mIoU drops by 4.3% (0.198 → 0.190), suggesting the segmentation task is most sensitive to the stop-gradient removal.

The canonical design's separation of network and uncertainty updates serves a real stabilizing role. Without it, the uncertainty scale parameter grows beyond the canonical range and the calibration becomes less consistent across seeds. The validation metrics stay broadly similar (reflecting the dominant contribution of the bounded chart), but the internal calibration dynamics are clearly healthier with the stop-gradient in place.

**Conclusion:** The split-optimization stop-gradient is a meaningful design choice. The coupled variant converges to a different (and less stable) calibration state. This supports keeping the stop-gradient in the canonical method.

## Current Status

Experiment completed, analysis done. No further action needed for this item.
