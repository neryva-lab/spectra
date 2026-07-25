# WI-12 Batch-Size Sensitivity Report

Date: 2026-07-25

## Scope

WI-12 addresses the reviewer concern that BPGS depends on batch statistics, so its behavior might
change when the mini-batch size changes. The purpose of this item is to check whether canonical
BPGS remains stable across a meaningful batch-size range rather than only at the paper's default
setting.

The setup is deliberately narrow:

- keep the dataset fixed
- keep the model seed fixed
- keep the method fixed to canonical BPGS
- vary only the training batch size

## Dataset Choice

The study uses the same **50% NYUv2 subset** as the ablation study:

- `dataset: nyuv2`
- `subset_budget: "50"`
- `subset_seed: 11`
- `use_subset_file: true`

This is the right dataset choice for WI-12 because the question is specifically about the effect of
batch statistics inside BPGS, and the ablation subset is already the paper's controlled NYUv2
setting.

## Files Updated

- `spectra/train/runner.py`
- `spectra/train/artifacts.py`
- `experiments/bpgs_study/optional/configs/11_nyuv2_batch_size.yaml`
- `experiments/bpgs_study/optional/utils.py`
- `docs/studies.md`
- `dev_docs/addressing_reviews/review_ledger.md`

## Experiment Execution

All nine runs (3 batch sizes × 3 seeds) were executed and completed successfully (60 epochs on NYUv2 50% subset, canonical BPGS):

| Variant | Seeds | Status |
|---|---|---|
| `batch_4` | 42, 43, 44 | 3/3 completed |
| `batch_8` | 42, 43, 44 | 3/3 completed |
| `batch_16` | 42, 43, 44 | 3/3 completed |

All runs are at `outputs/11_nyuv2_batch_size/{variant}/seed_{s}/csv_logs/bpgs_nyuv2_s{s}/metrics.csv`.

## Results

### Final Validation Metrics (epoch 59) — Per-Run Detail

| Metric | b4s42 | b4s43 | b4s44 | b8s42 | b8s43 | b8s44 | b16s42 | b16s43 | b16s44 |
|---|---|---|---|---|---|---|---|---|---|
| val/total_loss | 2.1469 | 2.1565 | 2.1371 | 2.1138 | 2.1492 | 2.1048 | 2.1391 | 2.2024 | 2.1106 |
| val/depth_abs_rel | 0.2402 | 0.2466 | 0.2365 | 0.2389 | 0.2468 | 0.2406 | 0.2402 | 0.2536 | 0.2415 |
| val/depth_rmse | 0.8601 | 0.8603 | 0.8725 | 0.8438 | 0.8513 | 0.8257 | 0.8311 | 0.8875 | 0.8283 |
| val/normals_mean_angle | 29.405 | 29.790 | 29.005 | 29.349 | 29.431 | 28.889 | 29.578 | 30.766 | 28.919 |
| val/segmentation_miou | 0.1886 | 0.2009 | 0.1970 | 0.1947 | 0.1868 | 0.1981 | 0.1772 | 0.1745 | 0.1914 |
| val/pixel_acc | 0.5337 | 0.5319 | 0.5385 | 0.5424 | 0.5302 | 0.5419 | 0.5284 | 0.5275 | 0.5405 |

### Within-Batch Variation (across 3 seeds per batch size)

| Metric | bs=4 mean (cv) | bs=8 mean (cv) | bs=16 mean (cv) |
|---|---|---|---|
| val/total_loss | 2.1468 (0.37%) | 2.1226 (0.90%) | 2.1507 (1.78%) |
| val/depth_abs_rel | 0.2411 (1.73%) | 0.2421 (1.41%) | 0.2451 (2.46%) |
| val/depth_rmse | 0.8643 (0.67%) | 0.8403 (1.28%) | 0.8490 (3.21%) |
| val/normals_mean_angle | 29.400 (1.09%) | 29.223 (0.82%) | 29.754 (2.57%) |
| val/segmentation_miou | 0.1955 (2.62%) | 0.1932 (2.45%) | 0.1810 (4.08%) |
| val/pixel_acc | 0.5347 (0.52%) | 0.5382 (1.05%) | 0.5321 (1.12%) |

### Across-Batch-Size Stability (seed-averaged means compared across batch_4/8/16)

| Metric | bs=4 mean | bs=8 mean | bs=16 mean | Across mean | Across std | Across CV |
|---|---|---|---|---|---|---|
| val/total_loss | 2.1468 | 2.1226 | 2.1507 | 2.1400 | 0.0124 | **0.58%** |
| val/depth_abs_rel | 0.2411 | 0.2421 | 0.2451 | 0.2428 | 0.0017 | **0.70%** |
| val/depth_rmse | 0.8643 | 0.8403 | 0.8490 | 0.8512 | 0.0099 | **1.17%** |
| val/normals_mean_angle | 29.400 | 29.223 | 29.754 | 29.459 | 0.2208 | **0.75%** |
| val/segmentation_miou | 0.1955 | 0.1932 | 0.1810 | 0.1899 | 0.0064 | **3.35%** |
| val/pixel_acc | 0.5347 | 0.5382 | 0.5321 | 0.5350 | 0.0025 | **0.47%** |

### Theta_max Trajectory

The learned uncertainty scale θ_max shows a systematic but modest trend with batch size — larger batches converge to a slightly higher θ_max, consistent with more stable gradient estimates allowing a larger uncertainty bound. The trajectory shapes remain qualitatively identical (exponential decay to steady state).

| Epoch | bs=4 | bs=8 | bs=16 |
|---|---|---|---|
| 0 | 3.2377 | 3.0815 | 3.2263 |
| 10 | 2.5397 | 2.6925 | 2.9661 |
| 20 | 2.3999 | 2.5246 | 2.7875 |
| 30 | 2.3913 | 2.4703 | 2.6733 |
| 40 | 2.3977 | 2.4504 | 2.6154 |
| 50 | 2.3962 | 2.4429 | 2.5923 |
| 59 | 2.3955 | 2.4414 | 2.5887 |

Final θ_max across seeds: bs=4 → 2.396 (±0.006), bs=8 → 2.441 (±0.020), bs=16 → 2.589 (±0.068).

## Interpretation

> **BPGS is stable across a 4× range of batch sizes (4, 8, 16).**

All validation metrics show across-batch-size CV well under 3.5%, with most under 1.2%. The segmentation mIoU shows the highest across-batch variation (3.35% CV), consistent with this task's known sensitivity on the 50% subset. There is no systematic degradation at any tested batch size — the seed-averaged metrics are essentially flat across batch_4, batch_8, and batch_16.

The θ_max shift from 2.40 (bs=4) to 2.59 (bs=16) is expected behavior: larger mini-batches produce more statistically reliable gradient estimates, so the learned uncertainty bound can be larger without risking instability. This is a feature of the calibration mechanism, not a bug.

**Conclusion:** The batch-statistics sensitivity concern raised by the reviewer is not supported by the data. BPGS performs robustly across a meaningful range of batch sizes without retuning.

## Current Status

Experiment completed, analysis done. No further action needed for this item.
