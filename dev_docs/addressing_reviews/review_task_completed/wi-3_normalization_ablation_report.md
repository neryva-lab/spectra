# WI-3 Normalization Ablation Report

Date: 2026-07-24

## Scope

This report records the completed Kendall + L1-normalization ablation for WI-3 in:

- `outputs/exp_09_kendall_norm_ablation/`

The run grid covered:

- 4 loss-scale multipliers: `1`, `10`, `100`, `1000`
- 3 methods: `bpgs`, `kendall`, `kendall_norm`
- 3 seeds per setting

Total coverage: `36/36` runs complete.

## Integrity Check

The output tree is complete:

- All four multiplier directories are present.
- Each multiplier directory contains the full artifact set:
  - `metrics/summary.csv`
  - `metrics/results.csv`
  - `metrics/results.json`
  - `figures/`
  - `logs/`
- `latest_run.json` points to the final `20260724_113615` run directory.
- Aggregated summaries report `count=3` for each method at every multiplier.

## Results

Macro score by scale:

| Scale | BPGS | Kendall | Kendall + L1-norm |
| --- | --- | --- | --- |
| `×1` | `0.789 ± 0.018` | `0.788 ± 0.014` | `0.794 ± 0.017` |
| `×10` | `0.791 ± 0.015` | `0.781 ± 0.023` | `0.780 ± 0.022` |
| `×100` | `0.788 ± 0.016` | `0.734 ± 0.037` | `0.742 ± 0.029` |
| `×1000` | `0.785 ± 0.017` | `0.658 ± 0.042` | `0.689 ± 0.034` |

Scale sensitivity from `×1` to `×1000`:

- `bpgs`: `-0.004`
- `kendall`: `-0.130`
- `kendall_norm`: `-0.105`

## Review

The experiment supports the intended WI-3 conclusion:

- BPGS remains effectively flat across scale stress.
- Vanilla Kendall degrades sharply as the loss is rescaled.
- Kendall + L1-normalization is better than vanilla Kendall at the highest scale, but it still degrades materially and remains below BPGS.

So the data do **not** support the claim that L1-normalization alone explains BPGS robustness.

## Stability Notes

The training diagnostics are consistent with that conclusion:

- `bpgs` keeps train-loss variance low across scales.
- `kendall` and `kendall_norm` both become much less stable at higher multipliers.
- The largest gap appears at `×1000`, where Kendall_norm improves over Kendall but still trails BPGS.

## Interpretation Detail

For `kendall_norm`, the reported task weights are the normalized precision weights used on the network loss. The `0.5` factor remains part of the Kendall-style objective, but it does not change the fact that the normalized weights themselves sum to `1`.

## Verdict

WI-3 is complete and the run is usable for the rebuttal ledger.

Main takeaway:

- L1-normalization alone is not enough to recover BPGS-scale invariance.

