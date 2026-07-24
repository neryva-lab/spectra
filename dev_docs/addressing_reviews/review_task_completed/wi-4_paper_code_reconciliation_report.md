# WI-4 Paper/Code Reconciliation Report

Date: 2026-07-24

## Scope

WI-4 reconciles the paper text and configuration files with the released implementation for the
NYUv2 benchmark and the reproducibility appendix.

The goal was not to change benchmark behavior broadly, but to make the final benchmark settings
explicit where they belong and keep shared defaults stable. This report has been updated to reflect
the current state of the repository, including the later documentation follow-up for the NYUv2
subset preparation notes.

## Decisions Taken

1. Kept the shared NYUv2 dataset default as:
   - `selection_metric: val/total_loss`
   - `selection_mode: min`

2. Kept the final NYUv2 benchmark explicit in the study overrides:
   - `train.selection_metric=val/miou`
   - `train.selection_mode=max`
   - `batch_augmentation=cpu`
   - `train.deterministic=true`
   - `train.deterministic_warn_only=true`

3. Kept the NYUv2 ablation on the dataset default selection rule and documented that choice
   explicitly in the appendix.

This is the correct reconciliation because it preserves the ablation setup while making the final
benchmark settings fully explicit.

## Files Updated

- `docs/bpgs_formalization.md`
- `configs/preset/nyuv2_bpgs.yaml`
- `configs/method/static.yaml`
- `working/paper/appendix/A_reproducibility_details.tex`
- `docs/studies.md`
- `dev_docs/temp/resolved.md`

## What Changed

- Added detached-statistics notation to the BPGS formalization so the equations match the code.
- Documented `theta_grad_scale=100.0` in the formalization notes.
- Standardized the static method config to the same package pattern as the other method configs.
- Reconciled the NYUv2 appendix text so it now states:
  - final benchmark runs use `val/miou` selection in max mode
  - final benchmark runs use deterministic execution with CPU batch augmentation
  - the ablation uses the dataset default `val/total_loss` / `min`
- Kept the shared NYUv2 dataset default unchanged at `val/total_loss` / `min`.
- Documented the NYUv2 subset preparation details in `docs/studies.md`.

## Review Notes

The shared NYUv2 default remains `val/total_loss` / `min`; the final study uses an explicit
override to `val/miou` / `max`. That keeps the ablation and any other default NYUv2 runs stable
while still matching the final benchmark configuration.

## Status

WI-4 reconciliation is reflected in the current repository state.
