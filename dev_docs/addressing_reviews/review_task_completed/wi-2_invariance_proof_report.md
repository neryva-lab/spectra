# WI-2 Invariance Proof Report

Date: 2026-07-24

Scope:
- Formalize the rescaling-invariance result for the batch-aware BPGS weighting rule.
- Keep the claim narrow: the exact invariant is the normalized task weighting rule, not an overbroad statement about every optimizer-side effect.

Primary sources checked:
- Local implementation note: [docs/bpgs_formalization.md](C:\Users\Hellx\Documents\Programming\python\Project\iron\bc\SPECTRA\docs\bpgs_formalization.md)
- Local code: [spectra/core/bpgs.py](C:\Users\Hellx\Documents\Programming\python\Project\iron\bc\SPECTRA\spectra\core\bpgs.py)
- Kendall et al., 2018: [arXiv:1705.07115](https://arxiv.org/abs/1705.07115)
- Recent normalization-based uncertainty weighting context: [arXiv:2408.07985](https://arxiv.org/abs/2408.07985)

Mathematical statement:

Let `L_i(w) >= 0` be the task losses for `i = 1,...,T`. Define a uniform rescaling by a constant `c > 0`:

`L_i'(w) = c * L_i(w)`.

In the batch-aware BPGS path, the log-loss statistics are

`mu(L) = (1/T) sum_i log(max(L_i, eps_log))`

and

`sigma_bar(L) = max( std(log(max(L_i, eps_log))), eps_std )`.

The latent coordinate and log-variance are

`z_i(theta_i) = tau_T * (2 * sigmoid(theta_i) - 1)`

`s_i(theta_i; L) = mu(L) + sigma_bar(L) * z_i(theta_i)`.

The network weights are

`omega_i = exp(-s_i)`

`alpha_i = omega_i / sum_j omega_j`.

## Proposition

For any `c > 0`, if all task losses are uniformly rescaled by `c`, then the normalized BPGS weights `alpha_i` are unchanged in the standard operating regime where the `eps_log` and `eps_std` clamps do not bind:

`alpha_i(L') = alpha_i(L)` for all `i`.

If first-batch auto-calibration is used, the initialized `theta_i` values are also unchanged under the same uniform rescaling of that calibration batch.

## Proof

Let `L_i' = c * L_i`. Then, assuming the numerical clamps are inactive on the relevant losses and batch statistics,

`log(max(L_i', eps_log)) = log(c) + log(max(L_i, eps_log))`

for the regime where the clamp is inactive on the rescaled values, which is the intended regime for the derivation and the one used in the formalization note.

Therefore:

`mu(L') = mu(L) + log(c)`.

Because adding the same constant to every log-loss does not change the centered deviations, the standard deviation is unchanged:

`sigma_bar(L') = sigma_bar(L)`.

The latent coordinate `z_i(theta_i)` depends only on `theta_i`, so it is unchanged by rescaling the losses:

`z_i(theta_i; L') = z_i(theta_i; L)`.

Hence

`s_i(theta_i; L') = mu(L') + sigma_bar(L') * z_i(theta_i)`

`= mu(L) + log(c) + sigma_bar(L) * z_i(theta_i)`

`= s_i(theta_i; L) + log(c)`.

So the raw precision rescales as

`omega_i(L') = exp(-s_i(L')) = exp(-(s_i(L) + log(c))) = omega_i(L) / c`.

Finally, the normalization cancels the common factor:

`alpha_i(L') = (omega_i(L) / c) / sum_j (omega_j(L) / c) = omega_i(L) / sum_j omega_j(L) = alpha_i(L)`.

This proves exact invariance of the normalized task weights under uniform rescaling.

For the first-batch auto-calibration path, the same cancellation holds because the standardized log-loss values

`(log(L_i) - mu(L)) / sigma_bar(L)`

are invariant to adding `log(c)` to every log-loss. Therefore the initial `theta_i` values computed from the first batch are unchanged as well.

## Interpretation for the paper

- The proof supports a narrow claim: the BPGS weighting rule is exactly invariant at the level of normalized task weights under uniform rescaling, provided the numerical safeguards are inactive.
- The empirical Table 1 result should be presented as a confirmation of this algebraic property, not as the only evidence for it.
- The claim should not be overstated as a general optimizer-invariance theorem unless the optimizer and learning-rate effects are separately controlled.
- If the clamp floors ever activate, exact invariance can weaken, so the rebuttal text should keep the theorem scoped to the intended operating regime.

## Notes from literature review

- Kendall et al. establish uncertainty-based task weighting as a learned-weighting framework for heterogeneous task losses.
- More recent uncertainty-weighting work also normalizes uncertainty-derived weights, which is consistent with the general idea that normalization can stabilize learned task weights.
- The WI-2 proof here is therefore not a novelty claim by itself; it is a correctness and presentation fix that should be stated cleanly in the rebuttal text.

## Completion note

This report is intended for internal tracking only. It captures the proof needed for WI-2 and the exact scope of the invariant that should be used later in the rebuttal.
