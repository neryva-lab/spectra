# Response to Area Chair (Meta-Review)

We thank the Area Chair for the detailed and constructive feedback. We address each concern below, with references to the specific revisions and new evidence that have been produced since the original submission.

## MR-1 / MR-2: Section 3 presented as a sequence of formulas; design choices not sufficiently justified

We have added plain-language motivation paragraphs throughout Section 3 that explain *why* each design choice exists, not only *what* it computes:

- **Bounded chart:** The latent uncertainty coordinate is constrained to prevent drift to extreme values when task losses differ in numerical scale. The boundary radius τ_T = √(T−1) + 0.1 is derived from the tight coordinate bound on a population-standardized T-vector (the √(T−1) term), with a small numerical safety margin (+0.1).
- **Batch-aware conditioning:** Centering on the batch log-loss mean and scaling by the batch spread makes the coordinate relative to the current batch rather than tied to an absolute loss level. This is the mechanism that provides exact rescaling invariance (see MR-9 below).
- **First-batch calibration:** A practical initialization choice that places the uncertainty coordinates in a sensible range before training begins, so the model does not waste early iterations recovering from an arbitrary starting point.
- **Split optimization:** The network update treats task weights as fixed coefficients; the uncertainty update adjusts weights from current losses without reshaping the network gradient in the same step. This separation stabilises calibration dynamics — an independent ablation shows that without the stop-gradient, θ_max grows +28% instead of decaying, with 14× higher seed variance.

## MR-3 / MR-5: Relationship to existing techniques not explained; positioning relative to prior work limited

Section 2 (Related Work) has been rewritten to position BPGS precisely within three lineages:

1. **Uncertainty weighting** (Kendall et al., GradNorm, dynamic task prioritization): BPGS fits as a bounded, batch-aware refinement. It shares the learned-log-variance foundation with Kendall but uses a different parameterization geometry and a different fixed-point structure.
2. **Gradient surgery** (PCGrad, CAGrad): BPGS does not modify gradient directions — it operates on scalar task weights only. This is why it does not address gradient conflict, and why conflict-aware methods are complementary rather than competing.
3. **Pareto-style multi-objective optimization** (Sener–Koltun, Nash-MTL): These methods solve a multi-objective subproblem at each step. BPGS is simpler — it does not require per-task gradient extraction or game-theoretic solvers.

The scope statement now reads: "BPGS is best understood as a bounded, batch-aware refinement of uncertainty weighting that is designed to improve robustness to loss-scale mismatch."

## MR-4: Choice in Eq. (4) not explained

The boundary radius τ_T = √(T−1) + 0.1 is now derived in the revised Section 3. Let z_i = (log L_i − μ)/σ̄ be the standardized log-loss coordinate for T tasks under the population-standard-deviation convention used in the implementation. Since Σz_i = 0 and (1/T)Σz_i² = 1, the constraint Σz_i² = T together with a Cauchy–Schwarz argument yields the tight bound |z_i| ≤ √(T−1). The +0.1 term is a numerical safety margin that keeps the inverse-sigmoid calibration away from the exact boundary where the map would become numerically fragile. This derivation is now stated explicitly in the paper.

## MR-6 / MR-7 / MR-8 / MR-10: Empirical evaluation narrow; results modest; problem motivation and significance not established strongly enough

We have taken several concrete steps to strengthen the empirical and analytical foundation:

- **Expanded statistical rigor:** The synthetic scale-stress experiment has been rerun with 10 seeds (120 total runs). BPGS ranks first at every scale factor; the gap at ×1000 is +1.07 combined SD vs Kendall.
- **New baseline:** Nash-MTL (2022) has been implemented and evaluated. We commit to adding CAGrad in the revised manuscript.
- **New ablations:** Batch-size sensitivity (9 runs, CV < 3.5%), first-batch calibration sensitivity (3 runs, CV < 2%), stop-gradient isolation (6 runs, 14× variance difference), and Kendall+L1-normalization (36 runs, showing L1-norm alone does not recover BPGS invariance).
- **Runtime analysis:** BPGS adds +0.15% time and +0.87% memory vs Kendall — negligible overhead.
- **Invariance proof:** A formal proposition now proves that the normalized BPGS weights are exactly invariant under uniform loss rescaling, grounding the synthetic result in an algebraic property rather than an empirical observation alone.
- **Cityscapes benchmark:** Planned as the highest-priority addition for the revised manuscript.

We have also revised the framing to match the evidence: the abstract, introduction, and discussion now consistently present BPGS as a targeted scale-robustness refinement, not a general MTL advance. The RF1 framing has been corrected to state "competitive" rather than implying near-parity with the leading baseline.

## MR-9: Novelty not established strongly enough

We address novelty through two complementary results:

1. **Invariance proof:** The normalized BPGS weights are exactly invariant under uniform rescaling — an algebraic property of the construction, not shared by Kendall's unconstrained parameterization. This is verified empirically in Table 1.
2. **Normalization ablation:** L1-normalizing Kendall's weights reduces degradation under rescaling but does not recover BPGS's near-perfect invariance (−0.105 vs −0.004 at ×1000 scale). This confirms that the bounded chart and split optimization contribute beyond simple normalization.

We do not claim that BPGS represents a paradigm shift. Its novelty is targeted: a principled solution to a specific, well-documented failure mode of uncertainty weighting.

---

We are grateful to the AC and all three reviewers for the thorough and constructive feedback. We believe the revisions — new experiments, a formal invariance proof, honest reframing of scope, and full paper-code reconciliation — substantially address the concerns raised.
