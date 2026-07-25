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

## What Was Done

- Added support in the training runner for explicit `train.devices`, `train.accelerator`, and
  `train.strategy` overrides so sensitivity studies can be pinned to a single GPU when needed.
- Recorded those device-selection fields in the run metadata.
- Added a new optional study definition, `11_nyuv2_batch_size`, that:
  - uses canonical BPGS
  - keeps the model seed fixed at `42`, `43`, and `44`
  - uses the NYUv2 50% subset from the ablation
  - varies only `train.batch_size`
  - pins training to a single device with `train.devices=1`
- Registered the study in the optional study list and documented it in `docs/studies.md`.
- Updated the review ledger so WI-12 is tracked as in progress rather than open-ended.

## Study Design

The study is configured to answer one question:

> Does BPGS stay stable when the mini-batch size changes?

To keep that question isolated, the study holds the dataset, seed, and method constant while
testing three batch sizes around the paper default of 8:

- `batch_4`
- `batch_8`
- `batch_16`

Each run uses:

- `method.s_mode=batch_aware`
- `method.init_mode=auto_calibrate`
- `train.batch_size=<varies>`
- `train.devices=1`
- `train.deterministic=true`
- `train.save_ckpt=false`
- `train.early_stop=false`

The single-device guard matters here. Without it, multi-GPU execution could change the effective
batch regime and turn this into a distributed-training confound instead of a true batch-size
sensitivity test.

## Validation

The study planner was dry-run after the scaffold was added, and it now emits exactly nine runs:

- `batch_4` with seeds `42`, `43`, `44`
- `batch_8` with seeds `42`, `43`, `44`
- `batch_16` with seeds `42`, `43`, `44`

Dry-run command:

```bash
python experiments/bpgs_study/run.py --study 11_nyuv2_batch_size --dry-run
```

## How To Interpret Results Later

When the runs are executed, the result should be read as a robustness check rather than a retuning
exercise. If BPGS remains stable across `4`, `8`, and `16`, that weakens the batch-statistics
sensitivity objection. If the results shift materially, that should be reported honestly as a
limitation of the method's dependence on batch statistics.

## Current Status

The batch-size sensitivity scaffold is ready, but the actual runs have not been executed in this
task. No performance outcome is claimed here.
