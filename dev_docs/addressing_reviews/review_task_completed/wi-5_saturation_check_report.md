# WI-5 Saturation Check Report

Date: 2026-07-24

Scope:
- Check whether the bounded latent coordinate approaches the clamp boundary in the logged main-paper runs.
- Use existing epoch logs only; no new training runs were needed.

What was analyzed:
- NYUv2 BPGS runs from `outputs/data/nyuv2/final_output_versions/bpgs/bpgs`
- Yeast BPGS runs from `outputs/data/full_data/final_results/03_yeast_regime_check/bpgs`
- RF1 BPGS runs from `outputs/data/full_data/final_results/08_rf1_regime_check/bpgs`

Logged quantities used:
- `train/bpgs/batch_mu`
- `train/bpgs/batch_sigma`
- `train/bpgs/log_var_i`
- `train/bpgs/theta_i`

Reconstruction:
- The bounded latent coordinate was reconstructed as
  `z_i = (s_i - mu) / sigma`,
  where `s_i` is the logged `train/bpgs/log_var_i`.
- The boundary radius is
  `tau_T = sqrt(T - 1) + 0.1`.

Results:

- **NYUv2** (`T = 3`, `tau_T = 1.5142`)
  - Maximum observed `|z_i| / tau_T`: `0.9327`
  - Worst case: `seed_43`, `epoch_0`, task `2`, `z_i = -1.4123`
  - Final-epoch ratios remained below the maximum and stayed below `0.84`

- **Yeast** (`T = 14`, `tau_T = 3.7056`)
  - Maximum observed `|z_i| / tau_T`: `0.7017`
  - Worst case: `seed_42`, `epoch_0`, task `8`, `z_i = 2.6000`
  - Final-epoch ratios remained below the maximum and stayed below `0.69`

- **RF1** (`T = 8`, `tau_T = 2.7458`)
  - Maximum observed `|z_i| / tau_T`: `0.8937`
  - Worst case: `seed_44`, `epoch_0`, task `2`, `z_i = 2.4540`
  - Final-epoch ratios remained below the maximum and stayed below `0.89`

Conclusion:
- No logged main-paper run reaches or exceeds the saturation boundary `|z_i| = tau_T`.
- The closest values occur at the first recorded epoch, which is consistent with auto-calibration placing the initial point near the intended chart scale.
- There is no evidence of sustained boundary locking or post-initialization collapse in the stored runs.

What to say in the rebuttal or revision:
- The method uses an explicitly bounded latent coordinate.
- In the logged NYUv2, Yeast, and RF1 runs, the coordinate remains strictly inside the bound.
- The closest observed points are below the clamp boundary, so the concern is about explainability of the design choice, not an observed saturation failure.

Completion note:
- This report documents the WI-5 saturation check using existing logs only.
