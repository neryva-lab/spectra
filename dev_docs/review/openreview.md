OpenReview
.net
Search articles, authors and reviews...
Notifications7
Activity
Tasks
Krishna Subedi 
back arrowGo to NeurIPS 2026 Conference homepage
Bounded Precision-Geometry Scaling for Robust Multi-Task Learning under Loss Scale Mismatch
Download PDF
Krishna Subedi 
05 May 2026 (modified: 28 May 2026)
NeurIPS 2026 Conference Submission
Conference, Senior Area Chairs, Area Chairs, Reviewers, Authors
Revisions
CC BY 4.0
Abstract:
Multi-task learning often combines objectives with different numerical scales, which can destabilise uncertainty-based loss weighting. We propose Bounded Precision-Geometry Scaling (BPGS), a split uncertainty-weighting method that maps each task’s latent uncertainty coordinate through a bounded sigmoid chart and, in its batch-aware form, expresses task log-variances in detached batch log-loss coordinates with first-batch calibration. We evaluate BPGS on synthetic stress tests, NYUv2 dense prediction, Yeast multi-label classification, and RF1 multi-target regression. Under pure post-hoc loss rescaling, BPGS keeps macro score nearly unchanged from ×1 to ×1000 (0.777 to 0.778), whereas Kendall-style uncertainty weighting drops from 0.780 to 0.637. On NYUv2, BPGS attains the best depth absolute relative error (0.223), the best depth RMSE (0.790), and the lowest total loss (1.891) among the compared methods. In an NYUv2 ablation, the batch-aware variants avoid the severe degradation of the stateless auto-calibrated variant, and the canonical batch-aware form improves depth and surface-normal metrics over Kendall. On Yeast and RF1, BPGS remains competitive beyond synthetic stress settings, achieving the best Yeast micro-F1 (0.616) and RF1 RMSE and MAE within 0.562 and 0.450 of the leading baseline. These results support BPGS as a robust uncertainty-weighting method when loss-scale mismatch is a primary concern.

Checklist Confirmation: I confirm that I have included a paper checklist in the paper PDF.
Responsible Reviewing: We acknowledge the responsible reviewing obligations as authors.
Primary Area: Optimization (e.g., convex and non-convex, stochastic, robust)
Secondary Area: Deep learning advancements (e.g., architectures, optimizers, representation learning)
Contribution Type: General: Most submissions will fall into this type.
Academic Integrity: I acknowledge that I have read the NeurIPS Handbook and commit to adhering to all policies in the Handbook (https://neurips.cc/Conferences/2026/MainTrackHandbook), the NeurIPS Code of Conduct and the NeurIPS Academic Integrity Policy.
LLM Usage: Editing (e.g., grammar, spelling, word choice)
Declaration: I confirm that the above information is accurate.
Reviewer Nomination:  Krishna Subedi
Submission Number: 36721
Discussion
Filter by reply type...
Filter by author...
Search keywords...

Sort: Newest First
4 / 4 replies shown
Add:
Meta Review of Submission36721 by Area Chair zptV
Meta Reviewby Area Chair zptV23 Jul 2026, 03:36 (modified: 24 Jul 2026, 00:26)Senior Area Chairs, Area Chairs, Authors, Reviewers Submitted, Program Chairs, Area Chair zptVRevisions
Metareview:
This submission raises many concerns across the reviews. After reading the paper, I largely agree with these concerns and with the overall assessment that the paper, in its current form, falls below the NeurIPS acceptance threshold. The central issue across reviews, which I agree with, is the limited depth and insight of the methodological contribution. Section 3, which should constitute the technical core of the paper, is presented largely as a sequence of formulas, with insufficient intuition, motivation, or justification for the specific design choices and their relationship to existing techniques. The unexplained choice in Eq. (4), also highlighted by the reviewers, is one concrete example. More broadly, the limited methodological justification and positioning relative to prior work, together with the narrow empirical evaluation and modest results, make it difficult to establish the problem motivation as well as sufficient novelty and significance. The reviews provide detailed and constructive feedback, and I encourage the authors to engage carefully with the specific comments when preparing a future resubmission. I hope this feedback will be useful in strengthening both the technical development and the empirical support for the work.

Add:
Official Review of Submission36721 by Reviewer Mxe9
Official Reviewby Reviewer Mxe925 Jun 2026, 18:49 (modified: 23 Jul 2026, 22:53)Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Authors, Reviewer Mxe9Revisions
Summary:
This paper addresses loss-scale mismatch in multi-task learning, a setting where task losses differ substantially in magnitude and can destabilize adaptive weighting methods. The authors propose Bounded Precision-Geometry Scaling (BPGS), a modification of uncertainty-based loss weighting that constrains the uncertainty parameters through a bounded sigmoid parameterization and introduces batch-aware calibration together with split optimization. The method is evaluated on synthetic scale-perturbation experiments, the NYUv2 dense prediction benchmark, and two tabular multi-task datasets (Yeast and RF1). The clearest evidence for the method comes from the loss-rescaling experiments, where BPGS remains stable under extreme scale changes while Kendall-style weighting degrades.

Contribution Type: General: Most submissions will fall into this type.
Strengths And Weaknesses:
Strengths • The paper addresses a practical and well-motivated problem in multi-task learning. Sensitivity to loss-scale mismatch is a common issue in adaptive weighting methods, yet it is rarely isolated and studied directly. • I found the controlled stress tests more informative than the standard benchmark results, because they directly test the failure mode the method is designed for. This makes it easier to determine whether the observed improvements stem from better scale handling rather than from benchmark-specific effects. • The rescaling experiments provide convincing evidence for the central claim. Under pure post-hoc loss rescaling, BPGS remains nearly unchanged (0.777 → 0.778), whereas Kendall-style uncertainty weighting degrades substantially (0.780 → 0.637). This result directly supports the proposed bounded parameterization. • On NYUv2, BPGS achieves the best depth Abs Rel (0.223), the best depth RMSE (0.790), and the lowest total validation loss (1.891) among the compared methods. These results suggest that the additional robustness is not obtained at the cost of noticeably weaker benchmark performance. • The ablation study is informative and helps identify which components of the method matter in practice. The severe degradation of the stateless auto-calibrated variant (mIoU 0.058, total loss 6.142) provides evidence that the batch-aware formulation is a meaningful component rather than a minor implementation detail.

Weaknesses • The scope of the contribution is narrower than the broader framing initially suggests. The experiments convincingly demonstrate robustness to loss-scale mismatch, but they do not establish superiority for general multi-task optimization. The paper itself notes that BPGS should be interpreted primarily as a scale-robust weighting method rather than a general solution to heterogeneous task interactions. • The heterogeneous mixed-stress experiments reveal limitations of the approach. In the noisy and conflict regimes, Kendall and PCGrad achieve higher macro scores than BPGS, suggesting that the method does not directly address gradient interference or task conflict. • The comparison against prior work is incomplete. Several influential recent multi-task learning methods, including Nash-MTL, IMTL-G, and FAMO, are not included in the empirical evaluation. As a result, it is difficult to assess the relative position of BPGS with respect to more recent approaches in the MTL literature. • The experimental evaluation remains relatively limited. Beyond NYUv2, only two additional real-data benchmarks are included, which restricts the evidence for generalization across domains. • Most reported results are aggregated over only three random seeds. While sufficient to reveal large performance differences, this level of statistical evidence may not be adequate to support fine-grained ranking claims when competing methods perform similarly. • The paper does not provide a dedicated runtime or computational overhead analysis despite introducing additional calibration and split-optimization steps. The absence of hardware and efficiency measurements makes the practical cost of the method difficult to assess.

Quality: 3: good
Clarity: 4: excellent
Significance: 3: good
Originality: 3: good
Questions:
How sensitive is the method to the first-batch calibration procedure? Would a different initial batch lead to substantially different uncertainty trajectories?
Have the authors evaluated BPGS against more recent MTL methods such as Nash-MTL, IMTL-G, or FAMO? If so, could those results be included?
Can the authors provide runtime and memory overhead measurements relative to Kendall weighting?
The paper demonstrates strong robustness to scale mismatch, but performance is weaker in conflict and noisy regimes. Can BPGS be combined with conflict-aware methods such as PCGrad or CAGrad?
How sensitive is the method to batch size, given that the uncertainty parameterization explicitly depends on batch statistics?
Limitations:
The authors are generally transparent about the scope of their contribution and acknowledge that BPGS is primarily a solution to loss-scale mismatch rather than a general multi-task optimization framework. However, some limitations remain underexplored. In particular, the experimental evaluation is limited in benchmark diversity, the comparison against recent MTL baselines is incomplete, and most results are reported using only three random seeds. These issues do not undermine the central claim of scale robustness, but they reduce confidence in the broader applicability of the method.

Rating: 3: Borderline reject: Technically solid paper where reasons to reject, e.g., limited evaluation, outweigh reasons to accept, e.g., good evaluation. Please use sparingly.
Confidence: 3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.
Ethical Concerns: NO or VERY MINOR ethics concerns only
Paper Formatting Concerns:
I did not identify any major formatting or anonymity violations.

Code Of Conduct Acknowledgement: Yes
Responsible Reviewing Acknowledgement: Yes
Add:
Official Review of Submission36721 by Reviewer AqnD
Official Reviewby Reviewer AqnD25 Jun 2026, 10:14 (modified: 23 Jul 2026, 22:53)Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Authors, Reviewer AqnDRevisions
Summary:
BPGS = Kendall's homoscedastic uncertainty weighting + two twists:

Bounded chart: replace the unconstrained log-variance ²
 with 
, anchoring per-task log-variance to the current batch loss statistics.
Split optimization: network step uses sg[α] (stop-grad on weights); θ step uses sg[L] and sg[batch stats]. Two passes, two objectives.
That's it. Everything else is standard.

Contribution Type: General: Most submissions will fall into this type.
Strengths And Weaknesses:
Quality
Methodology has gaps the paper doesn't surface:

The 100× GradScale on 
 (in code, not in the paper) means the published equations don't describe the actual optimizer. Anyone reproducing from Eqs (5)-(10) will not get Table 2.
No analysis of θ saturation. Seciton 3.4 proves s is bounded but never asks whether 
 can be learned at the boundary. The 
 factor in 
 goes to zero — the paper is silent on this.
"Matches classical homoscedastic uncertainty weighting" (line 99-100) is misleading. Same algebraic form ≠ same fixed-point structure. Kendall's optimum ²
 is reachable; BPGS's isn't when 
 sits outside the bounded interval.
Code-paper mismatches on hyperparameters (NYUv2 120/8 vs 80/4, selection_metric val/total_loss vs hard-coded val/miou, grad_clip differences) — these matter because the central claim is reproducibility under scale mismatch.
Empirical scope is narrow: one dense-prediction benchmark (NYUv2) + two tabular (Yeast/RF1) + synthetic stress tests. Three seeds. Table 4 honestly admits BPGS is not best on RF1; that's commendable, but the abstract still leads with "robust" — the robustness claim only really lands on the synthetic rescaling diagnostic.
Clarity
Overall, the high-level narrative is followable. That said, three things stood out:

The equations and the prose don't always line up — Eq. (10), for instance, omits the sg on the batch statistics that the text explicitly says are detached.
The paper and the released code disagree in non-trivial places (hyperparameters, selection metric, an undocumented 100× gradient scaling on θ ).
The layout is rough — supplementary figures end up wedged inside the NeurIPS checklist.
Significance
Loss-scale mismatch is a real practical issue in multi-task setups. A bounded uncertainty parameterization is a reasonable response. But:

The community has many adaptive weighting schemes already; BPGS slots in as another option, not a paradigm shift.
There is no single benchmark where BPGS dominates.
The paper lacks comparison against SOTA methods in the field — the most recent reference is from 2021.
Originality
Wrapping Kendall's objective in a batch-conditional bounded chart and (trivially) showing s stays in a finite interval — this reads as an honest engineering refinement, not a conceptual breakthrough.

Quality: 2: not good
Clarity: 2: not good
Significance: 2: not good
Originality: 2: not good
Questions:
See above. The following are additional comments.

Equation (5) squashes 
 through a sigmoid into a bounded interval, 
. One line of calculus shows:

 

Once 
 saturates, this factor is essentially zero and 
 can't come back. If a task's log-loss sits outside the bounded interval, 
 gets pinned at the boundary for good — the classic failure mode of any bounded reparameterization.

Section 3.4 makes a big deal of "s is bounded" as the key formal property. But s being bounded ≠ 
 being learnable. Those are two different statements. Section 6 lists three limitations and conveniently skips this one.

Limitations:
The paper and the released code disagree in non-trivial places (hyperparameters, selection metric, an undocumented 100× gradient scaling on θ ).
The layout is rough — supplementary figures end up wedged inside the NeurIPS checklist.
Rating: 2: Reject: For instance, a paper with technical flaws, weak evaluation, inadequate reproducibility and incompletely addressed ethical considerations.
Confidence: 4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.
Ethical Concerns: NO or VERY MINOR ethics concerns only
Paper Formatting Concerns:
This submission's released code repository violates NeurIPS double-blind anonymity requirements: spectra/init.py contains the author's real name, and the LICENSE, setup.py, and pyproject.toml all identify the affiliation as "Neryva Lab".

Code Of Conduct Acknowledgement: Yes
Responsible Reviewing Acknowledgement: Yes
Add:
Official Review of Submission36721 by Reviewer MKod
Official Reviewby Reviewer MKod22 Jun 2026, 20:13 (modified: 23 Jul 2026, 22:53)Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Authors, Reviewer MKodRevisions
Summary:
This work addresses the central challenge of numerical scale heterogeneity in multi-task learning. The method introduces a bounded sigmoid parameterization of task uncertainty and a batch-aware log-variance chart to stabilize adaptive task weighting under severe loss-scale mismatch. Empirically, BPGS shows near-invariance under pure post-hoc loss rescaling and competitive to strong performance on NYUv2, remains stable in ablations that highlight the importance of batch-aware coordinates, and performs competitively on Yeast and RF1 outside synthetic stress settings.

Contribution Type: General: Most submissions will fall into this type.
Strengths And Weaknesses:
Strength

[S1] Well-motivated problem: This paper targets a practical issue in multi-task learning. Adaptive weighting methods can become highly sensitive to arbitrary loss scaling. This is a realistic concern in dense prediction and heterogeneous multi-output learning, and the motivation is clearly articulated.

[S2] Simple but intuitive method: BPGS modifies the uncertainty parameterization rather than introducing complex gradient surgery or multi-objective optimization. The bounded sigmoid chart provides an intuitive mechanism for preventing unbounded precision collapse/explosion.

[S3] Strong synthetic evidence: The synthetic loss-rescaling experiment is convincing. BPGS remains nearly invariant from 
 to 
 scaling (macro score ≈ 0.777–0.778), while Kendall degrades substantially (0.780 → 0.637). This directly supports the claimed robustness under pure scale perturbations.

Weakness

[W1] Limited methodological novelty:

(W1-1) Conceptually, BPGS can largely be viewed as a constrained reparameterization of Kendall et al. [2] style uncertainty weighting with batch-wise affine normalization. Rather than introducing a fundamentally new weighting objective or optimization strategy, the main contribution lies in bounding the uncertainty coordinates to improve robustness against loss-scale mismatch. Notably, the paper itself acknowledges that the uncertainty objective (Eq. 10) "matches the scalar uncertainty objective used by classical homoscedastic uncertainty weighting," differing only in the chart mapping from 
 to 
. While practically effective, this feels incremental relative to prior work on constrained task weighting and loss normalization, and the conceptual gap from Kendall et al. [2] is narrower than the presentation implies.

(W1-2) The main formal statement is batch-conditional boundedness, which is intuitive from the sigmoid mapping. Deeper properties (e.g., invariance guarantees, convergence characteristics of the split objective) are not analyzed.

[W2] Limited experiments:

(W2-1) Reliance on batch statistics (log-loss mean/std) introduces potential variance/sensitivity to batch size, no explicit analysis explores this dependency.

(W2-2) The role of stop-gradient, while motivated, is not ablated independently from the bounded/batch-aware chart.

(W2-3) Limited comparisons with recent MTL methods. The paper does not compare against several recent strong baselines, including CAGrad, Nash-MTL, and Auto-Lambda etc. As a result, the empirical evidence is insufficient to determine whether BPGS offers advantages beyond outdated uncertainty-weighting and gradient-surgery approaches.

(W2-4) Only one dense-prediction benchmark (NYUv2) is tested at full scale. Claims about real-world competitiveness rest heavily on a single well-studied dataset. Testing on at least one additional dense-prediction benchmark (e.g., CityScapes, or a medical imaging multi-task setup) would substantially strengthen the generalization claim.

(W2-5) No computational overhead analysis. BPGS introduces additional computation through batch-wise log-loss statistics, normalization, and a separate uncertainty optimization step, yet the paper does not quantify the associated runtime or memory overhead. This omission makes it difficult to assess the practical efficiency and scalability of the method.

Minor Weakness

[MW1] Presentation issues: Several figures and experimental results are interleaved with the NeurIPS checklist section in the appendix, which makes the supplementary material harder to follow. Separating scientific content (figures/tables) from checklist responses would improve readability and reduce confusion. Additionally, page 9 contains substantial unused space, which could have been better utilized for clearer experimental details, additional analysis, or stronger baseline comparisons.

Quality: 2: not good
Clarity: 2: not good
Significance: 2: not good
Originality: 2: not good
Questions:
Please refer the Weakness part.

Limitations:
Although the authors acknowledge several limitations, many of these correspond to core shortcomings of the paper rather than peripheral caveats. For example, the small benchmark suite and limited statistical evaluation (only three seeds) significantly restrict the ability to assess generality and robustness. Their acknowledgment is appreciated, yet merely listing these issues in the limitations section feels somewhat defensive and does not substitute for stronger empirical validation.

Rating: 2: Reject: For instance, a paper with technical flaws, weak evaluation, inadequate reproducibility and incompletely addressed ethical considerations.
Confidence: 4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.
Ethical Concerns: NO or VERY MINOR ethics concerns only
Paper Formatting Concerns:
N/A

Code Of Conduct Acknowledgement: Yes
Responsible Reviewing Acknowledgement: Yes
Add:
About OpenReview
Contact
FAQ
Hosting a Venue
Sponsors
Terms of Use / Privacy Policy
All Venues
Donate
News
OpenReview is a long-term project to advance science through improved peer review with legal nonprofit status. We gratefully acknowledge the support of the OpenReview Sponsors. © 2026 OpenReview

