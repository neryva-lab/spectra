

## MR-1 / MR-2: Section 3 presented as a sequence of formulas; design choices not sufficiently justified

Section 3 now explains the motivation behind each design choice:

- **Bounded chart.** The latent uncertainty coordinate is kept within a finite interval to prevent drift when task losses differ in scale. The boundary radius τ_T = √(T−1) + 0.1 comes from the tight coordinate bound on a population-standardised T-vector, plus a small safety margin.
- **Batch-aware conditioning.** Centring on the batch log-loss mean and scaling by the batch spread makes the coordinate relative to the current batch. This gives the rescaling invariance (see MR-9).
- **First-batch calibration.** The uncertainty coordinates are initialised from the first batch so the optimiser starts in a sensible region instead of recovering from arbitrary initial values.
- **Split optimisation.** The network step treats task weights as constants; the uncertainty step adjusts weights from current losses without reshaping the network gradient. An ablation confirms this matters: without the stop-gradient, θ_max grows +28% instead of decaying, with 14× higher seed variance.

## MR-3 / MR-5: Relationship to existing techniques not explained; positioning relative to prior work limited

Section 2 has been rewritten around three MTL lineages:

1. **Uncertainty weighting** (Kendall et al., GradNorm, dynamic task prioritisation) — BPGS fits here as a bounded, batch-aware variant. It shares Kendall's learned-log-variance foundation but uses a different parameterisation geometry and fixed-point structure.
2. **Gradient surgery** (PCGrad, CAGrad) — BPGS does not touch gradient directions; it operates on scalar weights only, so it does not handle gradient conflict. Conflict-aware methods are complementary.
3. **Pareto-style multi-objective methods** (Sener–Koltun, Nash-MTL) — These solve a per-step multi-objective subproblem. BPGS does not need per-task gradient extraction or game-theoretic solvers.

Revised scope statement: "BPGS is best understood as a bounded, batch-aware refinement of uncertainty weighting that is designed to improve robustness to loss-scale mismatch."

## MR-4: Choice in Eq. (4) not explained

The boundary radius τ_T = √(T−1) + 0.1 is now derived. Let z_i = (log L_i − μ)/σ̄ be the standardised log-loss coordinate for T tasks. Since Σz_i = 0 and (1/T)Σz_i² = 1, a Cauchy–Schwarz argument gives the tight bound |z_i| ≤ √(T−1). The +0.1 is a safety margin that keeps the inverse-sigmoid calibration away from the exact boundary, where the map becomes numerically fragile.

## MR-6 / MR-7 / MR-8 / MR-10: Empirical evaluation narrow; results modest; problem motivation and significance not established strongly enough

Steps taken:

- **10-seed replication.** The synthetic scale-stress experiment was rerun with 10 seeds (120 runs). BPGS ranks first at every scale factor; the gap at ×1000 is +1.07 combined SD vs Kendall.
- **Nash-MTL baseline.** Implemented and evaluated (2022). We plan to add CAGrad.
- **Four new ablations.** Batch-size sensitivity (9 runs, CV < 3.5%), first-batch calibration (3 runs, CV < 2%), stop-gradient isolation (6 runs, 14× variance difference), and Kendall+L1-normalisation (36 runs — L1-norm alone does not recover the invariance).
- **Runtime numbers.** +0.15% time and +0.87% memory vs Kendall.
- **Invariance proof.** The normalised BPGS weights are exactly invariant under uniform loss rescaling — an algebraic property, not an empirical observation.

The framing has also been corrected: BPGS is now presented as a targeted scale-robustness refinement, the RF1 wording says "competitive," and Cityscapes is planned as a second dense-prediction benchmark.

## MR-9: Novelty not established strongly enough

Two results address this:

1. **Invariance proof.** The normalised BPGS weights are exactly invariant under uniform rescaling — a property that Kendall's unconstrained parameterisation does not share. Table 1 confirms it.
2. **Normalisation ablation.** L1-normalising Kendall's weights reduces degradation but does not close the gap (−0.105 vs −0.004 at ×1000). The bounded chart and split optimisation each contribute beyond normalisation.

BPGS is not a paradigm shift. It is a principled fix to a specific failure mode of uncertainty weighting.

