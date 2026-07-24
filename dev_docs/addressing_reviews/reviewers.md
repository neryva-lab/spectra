# Review Inventory

Source: [openreview.md](C:\Users\Hellx\Documents\Programming\python\Project\iron\bc\SPECTRA\dev_docs\review\openreview.md)

Purpose:
- Neutral tracking document for reviewer and meta-review points.
- This file records only what was raised in the reviews.
- It does not contain rebuttal text or response plans.

Tracking fields:
- `Status`: `Open` / `In progress` / `Resolved`
- `Owner`: optional later assignment
- `Notes`: optional later bookkeeping only

## Meta Review

Reviewer/role: Area Chair `zptV`

Overall assessment:
- The paper is judged below the acceptance threshold in its current form.
- The central concern is the limited depth and insight of the methodological contribution.
- The review agrees with the reviewers that the paper is not yet sufficiently motivated or positioned.

Issues raised:
- **MR-1**: Section 3 is presented mainly as a sequence of formulas, with insufficient intuition.
- **MR-2**: The paper does not sufficiently justify the specific design choices in the method.
- **MR-3**: The relationship to existing techniques is not explained clearly enough.
- **MR-4**: The choice in Eq. (4) is not explained.
- **MR-5**: Positioning relative to prior work is limited.
- **MR-6**: The empirical evaluation is narrow.
- **MR-7**: The results are modest.
- **MR-8**: The paper does not yet establish problem motivation strongly enough.
- **MR-9**: The paper does not yet establish novelty strongly enough.
- **MR-10**: The paper does not yet establish significance strongly enough.

Context (not an issue to resolve, kept for reference):
- The AC explicitly invites a future resubmission and states the reviews are intended to be constructive for that purpose.

## Reviewer Mxe9

Metadata:
- Quality: `3` (good)
- Clarity: `4` (excellent)
- Significance: `3` (good)
- Originality: `3` (good)
- Rating: `3` borderline reject
- Confidence: `3`

Positive observations:
- The paper addresses a practical problem in multi-task learning.
- The controlled stress tests are informative because they directly target the failure mode.
- The rescaling experiments are seen as convincing evidence for the central claim.
- The NYUv2 results are viewed as competitive on some key metrics.
- The ablation study is considered informative.

Issues raised:
- **Mxe9-1**: The scope of the contribution is narrower than the framing suggests.
- **Mxe9-2**: The method is supported for scale robustness, but not shown to be superior for general multi-task optimization.
- **Mxe9-3**: The heterogeneous mixed-stress experiments show limitations in noisy and conflict regimes.
- **Mxe9-4**: Kendall and PCGrad perform better than BPGS in those noisy/conflict regimes.
- **Mxe9-5**: The comparison set is incomplete.
- **Mxe9-6**: Recent methods such as Nash-MTL, IMTL-G, and FAMO are missing.
- **Mxe9-7**: The experimental evaluation is relatively limited beyond NYUv2.
- **Mxe9-8**: Only two additional real-data benchmarks are included.
- **Mxe9-9**: Results are reported using only three random seeds.
- **Mxe9-10**: The statistical evidence may be insufficient for fine-grained ranking claims.
- **Mxe9-11**: No runtime or computational overhead analysis is provided.
- **Mxe9-12**: The practical cost of the added calibration and split-optimization steps is unclear.

Questions raised:
- **Mxe9-Q1**: How sensitive is the method to the first-batch calibration procedure?
- **Mxe9-Q2**: Would a different initial batch lead to substantially different uncertainty trajectories?
- **Mxe9-Q3**: Has BPGS been evaluated against newer MTL methods such as Nash-MTL, IMTL-G, or FAMO?
- **Mxe9-Q4**: Can runtime and memory overhead be reported relative to Kendall weighting?
- **Mxe9-Q5**: Can BPGS be combined with conflict-aware methods such as PCGrad or CAGrad?
- **Mxe9-Q6**: How sensitive is the method to batch size, given the dependence on batch statistics?

Limitations called out:
- The authors are seen as transparent about the scope of the contribution.
- The review says BPGS should mainly be interpreted as a solution to loss-scale mismatch, not as a general multi-task optimization framework.
- The limited benchmark diversity, incomplete comparison set, and three-seed evaluation reduce confidence in broader applicability.

Formatting / anonymity concerns:
- None raised. Reviewer states no major formatting or anonymity violations were identified.

## Reviewer AqnD

Metadata:
- Quality: `2` (not good)
- Clarity: `2` (not good)
- Significance: `2` (not good)
- Originality: `2` (not good)
- Rating: `2` reject
- Confidence: `4`

Summary of the review:
- BPGS is characterized as Kendall-style uncertainty weighting plus two modifications: a bounded chart and split optimization.
- The reviewer treats the work as an incremental refinement rather than a major conceptual advance.

Issues raised:
- **AqnD-1**: The code contains a 100x gradient scaling on `theta` that is not described in the paper.
- **AqnD-2**: The published equations do not fully describe the actual optimizer used in code.
- **AqnD-3**: Reproducing the method from Eqs. (5)-(10) would not reproduce Table 2 as implemented.
- **AqnD-4**: The paper does not analyze `theta` saturation.
- **AqnD-5**: The paper proves that `s` is bounded, but does not address whether `theta` remains learnable at the boundary.
- **AqnD-6**: The review argues that once the latent variable saturates, the gradient factor can collapse and recovery may be impossible.
- **AqnD-7**: The statement that the method "matches classical homoscedastic uncertainty weighting" is seen as misleading.
- **AqnD-8**: The reviewer argues that matching algebraic form is not the same as matching fixed-point structure.
- **AqnD-9**: The reviewer claims Kendall's optimum is reachable, whereas BPGS's is not when the target lies outside the bounded interval.
- **AqnD-10**: The paper and code disagree on NYUv2 hyperparameters, including `120/8` versus `80/4`.
- **AqnD-11**: The paper and code disagree on the validation selection metric, including `val/total_loss` versus hard-coded `val/miou`.
- **AqnD-12**: The paper and code disagree on gradient clipping details.
- **AqnD-13**: These mismatches matter because the paper's central claim concerns reproducibility under scale mismatch.
- **AqnD-14**: The experimental scope is narrow: one dense-prediction benchmark, two tabular benchmarks, and synthetic stress tests.
- **AqnD-15**: Only three seeds are used.
- **AqnD-16**: The abstract's emphasis on robustness is seen as supported mainly by synthetic rescaling diagnostics, even though Table 4 itself honestly reports BPGS is not best on RF1.
- **AqnD-17**: Eq. (10) is said to omit the stop-gradient on batch statistics that the text describes.
- **AqnD-18**: The paper and released code disagree in non-trivial places beyond the main optimizer description.
- **AqnD-19**: The supplementary material is poorly laid out, with figures wedged into the NeurIPS checklist.
- **AqnD-20**: The method is viewed as another option among many adaptive weighting schemes, not a paradigm shift.
- **AqnD-21**: No single benchmark shows BPGS clearly dominating.
- **AqnD-22**: The paper lacks comparison against stronger or more recent SOTA methods.
- **AqnD-23**: The reviewer characterizes the contribution as engineering refinement rather than conceptual novelty.

Additional comments captured in the review:
- **AqnD-C1**: The reviewer argues that boundedness of `s` does not imply learnability of `theta`.
- **AqnD-C2**: The review says Section 6 lists limitations but omits the boundary-saturation issue.

Limitations called out:
- The code/paper mismatches are treated as substantive.
- The formatting/layout of the supplementary material is treated as a paper-quality issue.

Formatting / anonymity concerns:
- **AqnD-F1**: The reviewer states the released code repository violates NeurIPS double-blind anonymity requirements: `spectra/__init__.py` contains the author's real name, and the `LICENSE`, `setup.py`, and `pyproject.toml` files identify the affiliation as "Neryva Lab." This is independently actionable and unrelated to the scientific content of the paper.

## Reviewer MKod

Metadata:
- Quality: `2` (not good)
- Clarity: `2` (not good)
- Significance: `2` (not good)
- Originality: `2` (not good)
- Rating: `2` reject
- Confidence: `4`

Positive observations:
- **MKod-S1**: The problem is well-motivated - sensitivity of adaptive weighting methods to arbitrary loss scaling is a realistic concern in dense prediction and heterogeneous multi-output learning.
- **MKod-S2**: The method is simple but intuitive - it modifies the uncertainty parameterization rather than introducing complex gradient surgery or multi-objective optimization; the bounded sigmoid chart is seen as an intuitive mechanism against precision collapse/explosion.
- **MKod-S3**: The synthetic loss-rescaling experiment is convincing - BPGS is near-invariant from x1 to x1000 (macro score about 0.777-0.778) while Kendall degrades substantially (0.780 -> 0.637).

Issues raised:
- **MKod-1**: BPGS is largely a constrained reparameterization of Kendall-style uncertainty weighting with batch-wise affine normalization, rather than a fundamentally new weighting objective or optimization strategy; the paper's own text (re: Eq. 10) states the objective "matches the scalar uncertainty objective used by classical homoscedastic uncertainty weighting," differing only in the chart mapping - the reviewer sees the conceptual gap from Kendall as narrower than the paper's presentation implies.
- **MKod-2**: The main formal statement is only batch-conditional boundedness; deeper properties such as invariance guarantees or convergence characteristics of the split objective are not analyzed.
- **MKod-3**: Reliance on batch statistics (log-loss mean/std) introduces potential sensitivity to batch size, with no explicit analysis of this dependency.
- **MKod-4**: The role of stop-gradient, while motivated, is not ablated independently from the bounded/batch-aware chart.
- **MKod-5**: The paper does not compare against several recent strong baselines, including CAGrad, Nash-MTL, and Auto-Lambda, leaving it unclear whether BPGS offers advantages beyond older uncertainty-weighting and gradient-surgery approaches.
- **MKod-6**: Only one dense-prediction benchmark (NYUv2) is tested at full scale; claims of real-world competitiveness rest heavily on a single well-studied dataset.
- **MKod-7**: No computational overhead analysis is provided - BPGS introduces additional computation via batch-wise log-loss statistics, normalization, and a separate uncertainty optimization step, but runtime/memory overhead is not quantified.
- **MKod-8**: Presentation issue - several figures and results are interleaved with the NeurIPS checklist in the appendix, making the supplementary material harder to follow; page 9 has substantial unused space that could have held clearer experimental details or additional analysis.

Questions raised:
- None beyond the issues above; the review directs readers to the Weaknesses section for detail.

Limitations called out:
- The reviewer views the small benchmark suite and three-seed evaluation as core shortcomings rather than peripheral caveats.
- The reviewer describes the authors' acknowledgment of these limitations as appreciated but somewhat defensive, and states it does not substitute for stronger empirical validation.

Formatting / anonymity concerns:
- None raised (marked N/A in the review).
