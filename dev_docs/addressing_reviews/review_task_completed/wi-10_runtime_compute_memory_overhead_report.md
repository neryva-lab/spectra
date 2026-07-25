# WI-10 Runtime, Compute, and Memory Overhead Report

Date: 2026-07-25
experiment_results\09_nyuv2_overhead
## Scope

WI-10 measures the practical runtime and memory overhead of BPGS relative to Kendall
uncertainty weighting on the same 50% NYUv2 subset used by the ablation study.

## Experimental Setup

- Dataset: NYUv2, 50% subset (398 of 795 training images)
- Methods: BPGS (canonical, batch-aware, auto-calibrate) vs Kendall
- Epochs: 60
- Seeds: 42, 43, 44
- Hardware: Single GPU (cuda:0)
- Deterministic: true
- Metric collected per epoch: wall-clock time, peak CUDA memory
- 6 runs total (2 methods x 3 seeds)

## Results

### Per-epoch wall-clock time

| Seed | BPGS (s) | Kendall (s) | Difference |
|------|----------|-------------|------------|
| 42   | 40.937   | 40.915     | +0.022s  |
| 43   | 40.970   | 40.893     | +0.077s  |
| 44   | 41.030   | 40.941     | +0.089s  |
| **Mean** | **40.979** | **40.916** | **+0.063s** |

BPGS adds **0.15%** wall-clock time per epoch vs. Kendall — well within measurement noise
(per-epoch std is ~0.18-0.21s for both methods).

### Peak GPU memory

| Seed | BPGS (MB) | Kendall (MB) | Difference |
|------|-----------|--------------|------------|
| 42   | 3368.68   | 3339.16     | +29.52 MB  |
| 43   | 3367.74   | 3339.72     | +28.02 MB  |
| 44   | 3368.68   | 3339.15     | +29.53 MB  |
| **Mean** | **3368.36** | **3339.34** | **+29.02 MB** |

BPGS adds **0.87%** peak GPU memory vs. Kendall.

### Total wall-clock (60 epochs)

| Seed | BPGS (s) | Kendall (s) |
|------|----------|-------------|
| 42   | 2459.6   | 2458.4      |
| 43   | 2461.0   | 2456.3      |
| 44   | 2464.3   | 2459.0      |
| **Mean** | **2461.6** | **2457.9** | **+3.7s** |

### Parameter count

Both methods use the same model architecture: 18,869,140 trainable parameters.
BPGS adds 3 extra parameters (theta values for 3 tasks).

## Conclusion

BPGS introduces negligible overhead compared to Kendall:

- **Time:** +0.15% per epoch (the split optimization adds no meaningful wall-clock cost)
- **Memory:** +0.87% peak GPU memory (the batch statistics and theta parameters use minimal additional storage)

These results are consistent across all three seeds. The overhead is small enough that it should
not be a practical concern for anyone considering BPGS.

## Files Updated

- `spectra/engine/callbacks.py`
- `spectra/train/runner.py`
- `spectra/train/artifacts.py`
- `experiments/bpgs_study/optional/utils.py`
- `experiments/bpgs_study/optional/configs/09_nyuv2_overhead.yaml`
- `docs/studies.md`
- `dev_docs/addressing_reviews/review_ledger.md`
