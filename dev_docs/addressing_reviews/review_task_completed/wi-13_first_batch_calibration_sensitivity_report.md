# WI-13 First-Batch Calibration Sensitivity Report

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

## What Was Done

- Added a dedicated `train.loader_seed` knob to the data module so the training shuffle order can
  be changed without changing the model seed.
- Kept validation loading separate, with its existing deterministic seed path unchanged.
- Recorded `loader_seed` and `val_loader_seed` in the run metadata so the batch-order condition is
  captured alongside the rest of the training configuration.
- Added a new optional study definition, `10_nyuv2_first_batch`, that:
  - uses canonical BPGS
  - keeps the model seed fixed at `42`
  - uses the NYUv2 50% subset from the ablation
  - varies only the training loader seed across three runs
- Registered the study in the optional study list and documented it in `docs/studies.md`.

## Study Design

The study is configured to answer one question:

> If the first observed batch changes, do the learned uncertainty trajectories change materially?

To keep that question isolated, the study holds everything constant except the training loader
seed. The three planned runs are:

- `loader_seed_1001` with `seed=42`
- `loader_seed_2001` with `seed=42`
- `loader_seed_3001` with `seed=42`

Each run uses the same canonical BPGS settings:

- `method.s_mode=batch_aware`
- `method.init_mode=auto_calibrate`
- `train.loader_seed=<varies>`
- `train.deterministic=true`
- `train.save_ckpt=false`
- `train.early_stop=false`

## Validation

The study planner was dry-run after the scaffold was added, and it now emits exactly three runs.
Only the loader seed changes across them; the model seed stays fixed.

Dry-run command:

```bash
python experiments/bpgs_study/run.py --study 10_nyuv2_first_batch --dry-run
```

## How To Interpret Results Later

When the runs are executed, the comparison should focus on whether the trajectory curves and final
metrics remain stable across loader seeds. If the curves track closely, the first-batch concern is
small. If they diverge, that sensitivity should be reported honestly as a limitation of the
auto-calibration step.

## Current Status

The experiment scaffold is ready, but the actual three runs have not yet been executed in this
task. No outcome is claimed here.
