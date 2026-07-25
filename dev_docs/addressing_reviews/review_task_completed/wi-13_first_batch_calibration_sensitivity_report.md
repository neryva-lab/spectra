# WI-13 First-Batch Calibration Sensitivity Report
experiment_results\10_nyuv2_first_batch
Date: 2026-07-25

## Scope

WI-13 addresses the reviewer concern that BPGS auto-calibrates from the first observed training
batch, so its trajectories might depend on which batch arrives first. The purpose of this item is
to isolate that question cleanly.

The setup is intentionally narrow:

- keep the dataset fixed
- keep the model seed fixed
- change only the training loader seed

That way, the experiment tests first-batch sensitivity rather than overall randomness in the full
training pipeline.

## Dataset Choice

The study uses the same **50% NYUv2 subset** as the ablation study:

- `dataset: nyuv2`
- `subset_budget: "50"`
- `subset_seed: 11`
- `use_subset_file: true`

This is the correct dataset choice for WI-13 because the question is about canonical BPGS on the
same training regime where first-batch auto-calibration already matters.

## Files Updated

- `spectra/data/datamodule.py`
- `spectra/train/artifacts.py`
- `experiments/bpgs_study/optional/configs/10_nyuv2_first_batch.yaml`
- `experiments/bpgs_study/optional/utils.py`
- `docs/studies.md`
- `dev_docs/addressing_reviews/review_ledger.md`

## Experiment Execution

All three runs were executed and completed successfully (60 epochs on NYUv2 50% subset, canonical BPGS):

| Run | Command | Status |
|---|---|---|
| `loader_seed_1001` | `python run.py --study 10_nyuv2_first_batch --variant loader_seed_1001` | Completed (60 epochs) |
| `loader_seed_2001` | `python run.py --study 10_nyuv2_first_batch --variant loader_seed_2001` | Completed (60 epochs) |
| `loader_seed_3001` | `python run.py --study 10_nyuv2_first_batch --variant loader_seed_3001` | Completed (60 epochs) |

All runs are at `outputs/10_nyuv2_first_batch/{variant}/seed_42/csv_logs/bpgs_nyuv2_s42/metrics.csv`.

## Results

### Final Validation Metrics (epoch 59)

| Metric | seed_1001 | seed_2001 | seed_3001 | Mean | Std | CV |
|---|---|---|---|---|---|---|
| val/total_loss | 2.1145 | 2.1040 | 2.1090 | 2.1092 | 0.0043 | 0.20% |
| val/depth_abs_rel | 0.2385 | 0.2392 | 0.2411 | 0.2396 | 0.0011 | 0.46% |
| val/depth_rmse | 0.8348 | 0.8302 | 0.8325 | 0.8325 | 0.0019 | 0.23% |
| val/normals_mean_angle | 28.9205 | 28.8975 | 29.1069 | 28.9750 | 0.0938 | 0.32% |
| val/normals_within_11.25 | 0.2274 | 0.2292 | 0.2261 | 0.2276 | 0.0013 | 0.56% |
| val/segmentation_miou | 0.1912 | 0.1866 | 0.1952 | 0.1910 | 0.0035 | 1.84% |
| val/segmentation_pixel_acc | 0.5338 | 0.5366 | 0.5402 | 0.5369 | 0.0026 | 0.49% |
| val/miou | 0.1912 | 0.1866 | 0.1952 | 0.1910 | 0.0035 | 1.84% |

### Trajectory Stability (θ_max)

The learned uncertainty scale θ_max converges smoothly and indistinguishably across all three loader seeds:

| Epoch | seed_1001 | seed_2001 | seed_3001 |
|---|---|---|---|
| 0 | 3.2716 | 3.2700 | 3.2700 |
| 10 | 2.8365 | 2.7928 | 2.7958 |
| 20 | 2.5851 | 2.5646 | 2.5599 |
| 30 | 2.4892 | 2.4782 | 2.4711 |
| 40 | 2.4569 | 2.4517 | 2.4492 |
| 50 | 2.4469 | 2.4406 | 2.4398 |
| 59 | 2.4451 | 2.4382 | 2.4380 |

All three trajectories follow the same exponential decay pattern and converge to within 0.007 of each other (0.3% relative spread).

## Interpretation

The data answers the question clearly:

> **Changing the first observed batch does NOT materially change the learned uncertainty trajectories.**

The coefficient of variation (CV) across all validation metrics is well under 2%, with most metrics (total_loss, depth_abs_rel, depth_rmse, normals_mean_angle, pixel_acc) under 0.6%. The segmentation mIoU shows slightly higher variation at 1.84% CV, which is consistent with the known sensitivity of this task on the 50% subset and still well within acceptable bounds.

This confirms that the auto-calibration step is robust to the specific batch that arrives first. The batch-conditional boundedness mechanism in BPGS does not create a dependency on the initial shuffle order.

## Current Status

Experiment completed, analysis done. No further action needed for this item.
