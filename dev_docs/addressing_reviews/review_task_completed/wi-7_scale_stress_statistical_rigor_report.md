# WI-7 Scale-Stress Statistical Rigor Report

Date: 2026-07-24

## Scope

WI-7 strengthens the statistical footing of the synthetic scale-stress result by rerunning the
scale-stress grid with 10 seeds instead of 3 and updating the paper source to match.

The goal is not to claim a formal significance result. The goal is to make the scale-stress
comparison less fragile and to keep the narrative aligned with the stronger 10-seed estimate.

## Files Updated

- `experiments/bpgs_study/stress/configs/02_synthetic_scale_stress.yaml`
- `working/paper/data/stress/scale/tables/scale_stress_scale_table.tex`
- `working/paper/data/stress/combined/tables/degradation_table.tex`
- `working/paper/sections/04_results.tex`
- `working/paper/sections/03_experimental_setup.tex`
- `working/paper/sections/05_discussion_limitations.tex`
- `dev_docs/addressing_reviews/review_ledger.md`

## What Was Done

- Expanded the synthetic scale-stress seed list from `[42, 43, 44]` to `[42, 43, 44, 45, 46, 47,
  48, 49, 50, 51]`.
- Executed the full grid:
  - 4 scale factors: `x1`, `x10`, `x100`, `x1000`
  - 3 methods: `BPGS`, `Kendall`, `UWSO`
  - 10 seeds per setting
- Recomputed the macro-score table and the relative degradation summary.
- Updated the paper source so the scale-stress table, related prose, and reporting protocol now
  reflect the 10-seed rerun.

## Results

Macro score by scale:

| Variant | BPGS mean | BPGS std | Kendall mean | Kendall std | UWSO mean | UWSO std |
|---------|-----------|----------|--------------|-------------|-----------|----------|
| x1      | 0.7433    | 0.0183   | 0.7378       | 0.0171      | 0.6901    | 0.0343   |
| x10     | 0.6159    | 0.0390   | 0.6071       | 0.0376      | 0.6041    | 0.0404   |
| x100    | 0.5468    | 0.0318   | 0.5218       | 0.0304      | 0.5254    | 0.0347   |
| x1000   | 0.5427    | 0.0322   | 0.4993       | 0.0246      | 0.4935    | 0.0243   |

Stability relative to the original 3-seed estimate:

| Variant | BPGS 3s | BPGS 10s | Kendall 3s | Kendall 10s | UWSO 3s | UWSO 10s |
|---------|---------|----------|------------|-------------|---------|----------|
| x1      | 0.7522  | 0.7433   | 0.7419     | 0.7378      | 0.7109  | 0.6901   |
| x10     | 0.6141  | 0.6159   | 0.6164     | 0.6071      | 0.6024  | 0.6041   |
| x100    | 0.5310  | 0.5468   | 0.5070     | 0.5218      | 0.5092  | 0.5254   |
| x1000   | 0.5282  | 0.5427   | 0.4947     | 0.4993      | 0.4855  | 0.4935   |

The ranking is unchanged: BPGS remains first at every scale factor.

BPGS vs Kendall gap in combined standard deviations (10 seeds):

- x1: `+0.22 SD`
- x10: `+0.16 SD`
- x100: `+0.57 SD`
- x1000: `+1.07 SD`

Relative degradation from x1 to x1000:

| Method | 3 seeds | 10 seeds |
|--------|---------|----------|
| BPGS   | 29.8%   | 27.0%    |
| Kendall| 33.3%   | 32.3%    |
| UWSO   | 31.7%   | 28.5%    |

BPGS has the smallest relative drop at both 3 and 10 seeds.

## Interpretation

- The 10-seed rerun strengthens the directional case at the largest perturbation.
- The updated paper wording should describe the result as favorable and more stable, but still as a
  comparison of means and variability rather than a formal significance test.
- The paper source has been updated so the table, the main-results narrative, the reporting protocol,
  and the limitations discussion all agree on the seed count.

## Completion Note

All 120 runs completed successfully. Results are stored at `outputs/02_synthetic_scale_stress/`.
The paper source now reflects the 10-seed rerun for the scale-stress table, while the other
headline results remain aggregated over three seeds.
