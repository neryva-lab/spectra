# WI-10 Runtime, Compute, and Memory Overhead Setup Report

Date: 2026-07-24

## Scope

WI-10 addresses the reviewer concern that BPGS may impose extra runtime or memory cost relative
to Kendall weighting. The setup here is intentionally lightweight: it uses the same 50% NYUv2
subset as the ablation study rather than the full NYUv2 training set, and it compares only
Kendall versus BPGS.

The goal of this work item is to make the overhead measurement reproducible and cheap to run, not
to broaden the benchmark footprint.

## Files Updated

- `spectra/engine/callbacks.py`
- `spectra/train/runner.py`
- `spectra/train/artifacts.py`
- `experiments/bpgs_study/optional/utils.py`
- `experiments/bpgs_study/optional/configs/09_nyuv2_overhead.yaml`
- `docs/studies.md`

## What Was Done

- Added a `RuntimeOverheadCallback` that records:
  - per-epoch wall-clock time
  - peak CUDA memory allocated during each epoch
  - trainable and total parameter counts
  - device metadata
- Wired that callback into the training runner behind a new `train.measure_overhead` flag so it
  only activates for studies that explicitly request it.
- Extended `run_summary.json` so the new overhead metrics are preserved alongside the existing
  fit summary.
- Added a new optional study definition, `09_nyuv2_overhead`, with:
  - the same 50% NYUv2 subset used by the ablation study
  - Kendall and BPGS as the only two variants
  - deterministic settings
  - checkpointing and early stopping disabled
  - minimal progress logging
- Documented the new study in `docs/studies.md` so the benchmark is discoverable.

## Measurement Design

The overhead study is configured to answer a narrow question:

1. run Kendall and BPGS on the same 50% NYUv2 subset
2. keep the training budget identical across both methods
3. record training-epoch wall-clock and peak GPU memory from the run summary
4. compare the aggregate statistics across the three seeds

This setup avoids introducing a second experimental axis. It is enough to quantify practical cost
without turning the study into a full benchmark sweep.

## Run Configuration

The new study definition is:

- `experiments/bpgs_study/optional/configs/09_nyuv2_overhead.yaml`

Key settings:

- `subset_budget: "50"`
- `subset_seed: 11`
- `use_subset_file: true`
- `epochs: 60`
- `seeds: [42, 43, 44]`
- `early_stop: false`
- `train.measure_overhead: true`
- `train.save_ckpt: false`
- `train.early_stop: false`

The configuration is deliberately aligned with the ablation subset instead of the full dataset.

## How To Run

Dry-run the study plan first:

```bash
python experiments/bpgs_study/run.py --study 09_nyuv2_overhead --dry-run
```

Then execute it normally when GPU resources are available.

The resulting run summaries will be written under the study output tree, and the overhead metrics
will be available in each run's `run_summary.json` under the `runtime_overhead` key.

The study planner was dry-run after the config cleanup, and it now emits exactly six runs:

- `kendall` seeds `42`, `43`, `44`
- `bpgs` seeds `42`, `43`, `44`

## Current Status

The infrastructure for WI-10 is in place, but the actual Kendall-vs-BPGS timing/memory runs have
not yet been executed in this task. No results are claimed here.
