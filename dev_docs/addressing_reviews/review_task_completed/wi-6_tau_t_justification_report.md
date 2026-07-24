# WI-6 tau_T Justification Report

Date: 2026-07-24

Scope:
- Justify the choice `tau_T = sqrt(T - 1) + 0.1` used in Eq. (4).
- Keep the claim narrow and implementation-aligned.

Primary sources checked:
- Local implementation note: [docs/bpgs_formalization.md](C:\Users\Hellx\Documents\Programming\python\Project\iron\bc\SPECTRA\docs\bpgs_formalization.md)
- Local code: [spectra/core/bpgs.py](C:\Users\Hellx\Documents\Programming\python\Project\iron\bc\SPECTRA\spectra\core\bpgs.py)

Relevant implementation detail:
- The batch-aware path computes `mu(L)` as the mean of detached log-losses.
- It computes `sigma_bar(L)` with `log_losses.std(unbiased=False).clamp(min=1e-4)`.
- Auto-calibration uses the standardized coordinate `(log(L_i) - mu(L)) / sigma_bar(L)` and then clamps it to `[-tau_T, tau_T]`.

## Mathematical justification

Let

`z_i = (log(L_i) - mu(L)) / sigma_bar(L)`

for a batch of `T` tasks, using the population-standard-deviation convention implemented in code.

Then the standardized vector has:

`sum_i z_i = 0`

and

`(1/T) sum_i z_i^2 = 1`.

Equivalently,

`sum_i z_i^2 = T`.

To find the largest possible coordinate magnitude, set one coordinate to `|z_1| = M`. The remaining `T - 1` coordinates must sum to `-M`. By the equality case of Cauchy-Schwarz, the smallest possible sum of squares of those remaining coordinates occurs when they are all equal, i.e.

`z_2 = ... = z_T = -M / (T - 1)`.

Then

`sum_i z_i^2 >= M^2 + (T - 1) * (M / (T - 1))^2`

`= M^2 * T / (T - 1)`.

Since `sum_i z_i^2 = T`, it follows that

`M^2 <= T - 1`,

so

`|z_i| <= sqrt(T - 1)`.

This bound is tight: equality is achieved by the configuration above.

## Interpretation

- `sqrt(T - 1)` is the mathematically justified radius for the standardized coordinate under the same population-variance convention used by the implementation.
- The `+ 0.1` term is a small numerical safety margin.
- Its role is to keep the clamp and inverse-sigmoid calibration away from the exact boundary, where the inverse map would become numerically fragile.

## What to say in the paper or rebuttal

- The `sqrt(T - 1)` term is not arbitrary.
- It comes from the tight coordinate bound on a population-standardized `T`-vector.
- The `+ 0.1` term is a practical buffer, not a theoretically essential constant.
- The report should not claim the buffer is derived; only the `sqrt(T - 1)` part is derived.

## Completion note

This report is intended for internal tracking only. It records the rationale for `tau_T` in a way that matches the code and avoids overstating the theoretical claim.
