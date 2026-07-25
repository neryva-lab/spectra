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

## What Was Changed

- Added a `split_stop_gradient` flag to the BPGS method config, with the canonical default set to
  `true`.
- Wired that flag into the BPGS weighter so the canonical path detaches:
  - the normalized network-update weights
  - the raw losses inside the uncertainty objective
- Extended the BPGS optimizer engine so that when `split_stop_gradient=false`, it uses a coupled
  update path:
  - one backward pass on the sum of the network and uncertainty objectives
  - both optimizers stepped from that shared gradient signal
- Added a new optional study, `12_nyuv2_stop_gradient`, with two variants:
  - `split_stopgrad_on`
  - `split_stopgrad_off`
- Kept the bounded chart, batch-aware parameterization, batch size, seed schedule, and NYUv2
  subset fixed across both variants.

## Study Design

The study answers one question:

> Does the split-optimization stop-gradient matter independently of the bounded/batch-aware chart?

To isolate that question, the study holds everything else constant:

- canonical BPGS
- batch-aware chart
- auto-calibration
- batch size 8
- single-device execution
- same 50% NYUv2 subset
- seeds `42`, `43`, and `44`

The two variants differ only in `method.split_stop_gradient`:

- `split_stopgrad_on`: `true`
- `split_stopgrad_off`: `false`

## Why The Engine Change Was Necessary

This ablation needed more than a config toggle. A pure config change would only alter where tensors
are detached, but it would still leave the original two-pass update structure in place. To make the
ablation faithful, the optimizer engine now switches to a coupled backward pass when the flag is
disabled.

That makes the comparison meaningful:

- canonical BPGS keeps network and uncertainty updates separated
- the ablated variant lets the two objectives interact through a shared backward pass

## Validation

The study planner was dry-run after the scaffold was added, and it now emits exactly six runs:

- `split_stopgrad_on` with seeds `42`, `43`, `44`
- `split_stopgrad_off` with seeds `42`, `43`, `44`

Dry-run command:

```bash
python experiments/bpgs_study/run.py --study 12_nyuv2_stop_gradient --dry-run
```

## How To Interpret Results Later

When the runs are executed, the result should be read as a design-choice check. If the coupled
variant is materially worse or less stable, that supports the need for the split-optimization
stop-gradient. If the variants are similar, the stop-gradient is likely a weaker contributor than
the bounded chart or batch-aware calibration.

## Current Status

The stop-gradient ablation scaffold is ready, but the actual six runs have not been executed in this
task. No performance outcome is claimed here.
