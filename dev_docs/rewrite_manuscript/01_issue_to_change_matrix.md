# 01 — Issue → Change Matrix (full traceability)

Every atomic issue raised by the AC meta-review (MR-*), the three reviewers (Mxe9-*, AqnD-*, MKod-*),
and the internal technical analysis (TA-*; **not from an official reviewer**) is mapped to the
concrete manuscript change that resolves it, plus where the change lands.

**Placement keys:** `M#` = main-text section number (of the revised paper), `A#` = appendix
section letter, `T#` = table file in `working/paper/data/`, `F#` = figure, `BIB` = references.

Legend for status: `NEW` = change is not yet in the manuscript; `PART` = partially present;
`DONE` = already in manuscript; `N/A` = not a paper change (repo/tooling only).

---

## A. Meta-review (Area Chair zptV)

| ID | Issue | Resolving change | Placement | Status |
|---|---|---|---|---|
| MR-1 | §3 is a sequence of formulas, insufficient intuition | Motivation prose already added (WI-17); keep; tighten to recover space; add plain-language lead-in to each new formal result (Prop. 1, τ_T) | M3 | PART |
| MR-2 | Design choices not justified | τ_T derivation (WI-6); grad-scale rationale; first-batch calibration already justified; invariance proof justifies the batch-aware chart design itself | M3.2, M3.3, M3.5 | PART→NEW |
| MR-3 | Relationship to existing techniques unclear | Related work already rewritten (WI-16); add Nash-MTL/IMTL-G/FAMO/Auto-Lambda positioning sentence | M2 | PART |
| MR-4 | Choice in Eq. (4) unexplained | τ_T derivation paragraph (WI-6) | M3.2 | NEW |
| MR-5 | Positioning vs prior work limited | Same as MR-3; scope sentence already present | M2 | PART |
| MR-6 | Empirical evaluation narrow | Nash-MTL baseline; 4 new controlled studies (WI-3/11/12/13); 10-seed scale stress; runtime study (WI-10); honest future-work statement (Cityscapes) | M4, A-E | PART→NEW |
| MR-7 | Results modest | Do not inflate; reframe as *targeted* results; the invariance Proposition + non-triviality ablations raise the contribution's perceived depth without overclaiming | M3.5, M4 | NEW |
| MR-8 | Problem motivation not established | Keep existing intro motivation; add one sentence on real-world prevalence of scale mismatch (dense prediction + tabular); no overclaiming | M1 | PART |
| MR-9 | Novelty not established | **Invariance Proposition (WI-2)** + Kendall+L1 ablation (WI-3) + stop-grad ablation (WI-11) | M3.5, M5.1, M5.3 | NEW |
| MR-10 | Significance not established | Overhead study (WI-10) shows the fix is cheap; scale-invariance is a desirable property in deployed pipelines | M5.6, A-F | NEW |

## B. Reviewer Mxe9

| ID | Issue | Resolving change | Placement | Status |
|---|---|---|---|---|
| Mxe9-1 | Scope narrower than framing | Framing already corrected (WI-19); re-verify in final pass | M1, M6 | DONE |
| Mxe9-2 | Not shown superior for general MTL | Explicit "we do not claim general superiority" statement (already present); keep | M1, M6 | DONE |
| Mxe9-3 | Mixed-stress limits in noisy/conflict regimes | New Discussion paragraph: explain why (scalar weights only, no gradient surgery); combination with PCGrad/CAGrad as future work (WI-14 resolution) | M6 | NEW |
| Mxe9-4 | Kendall/PCGrad beat BPGS in noisy/conflict | Report numbers honestly (already in Table 7/heterogeneous); add interpretation sentence | M4.1, M6 | PART |
| Mxe9-5 | Comparison set incomplete | Nash-MTL added to NYUv2 table + text | M4.2, T-nyuv2, BIB | NEW |
| Mxe9-6 | Missing Nash-MTL, IMTL-G, FAMO | Nash-MTL evaluated; IMTL-G/FAMO positioned as future work in Discussion + related work mention | M2, M4.2, M6 | NEW |
| Mxe9-7 | Limited evaluation beyond NYUv2 | Acknowledge; Cityscapes future work (WI-15); do not promise results | M6 | NEW |
| Mxe9-8 | Only two additional real-data benchmarks | Same as Mxe9-7 | M6 | NEW |
| Mxe9-9 | Only three seeds | 10-seed scale stress already in paper; state seed counts for every new study; keep 3-seed statement in limitations | M4.3, A-A | PART |
| Mxe9-10 | Statistical evidence insufficient for fine-grained ranking | Existing "comparison of means, not formal significance test" wording; extend to new studies | M4.1, M6 | PART |
| Mxe9-11 | No runtime/overhead analysis | Overhead study (WI-10) paragraph + table | M5.6, A-F | NEW |
| Mxe9-12 | Practical cost unclear | Same as Mxe9-11 | M5.6, A-F | NEW |
| Mxe9-Q1 | Sensitivity to first-batch calibration | First-batch sensitivity study (WI-13) | M5.4, A-E | NEW |
| Mxe9-Q2 | Different first batch → different trajectories? | θ_max convergence evidence (WI-13) | M5.4, A-E | NEW |
| Mxe9-Q3 | Evaluated against Nash-MTL/IMTL-G/FAMO? | Nash-MTL yes; others future work | M4.2, M6 | NEW |
| Mxe9-Q4 | Runtime/memory vs Kendall? | WI-10 table | M5.6, A-F | NEW |
| Mxe9-Q5 | Can BPGS combine with PCGrad/CAGrad? | Discussion: complementary failure modes; future work (WI-14) | M6 | NEW |
| Mxe9-Q6 | Sensitivity to batch size? | Batch-size study (WI-12) | M5.4, A-E | NEW |

## C. Reviewer AqnD

| ID | Issue | Resolving change | Placement | Status |
|---|---|---|---|---|
| AqnD-1 | Undocumented 100× gradient scale on θ | Document `theta_grad_scale=100` in §3.3 + rationale + appendix A | M3.3, A-A | NEW |
| AqnD-2 | Equations don't describe actual optimizer | Same as AqnD-1; also state detached-statistics notation already present (sg[] added) | M3.3, M3.2 | PART |
| AqnD-3 | Eqs. would not reproduce Table 2 | Full reproducibility block in appendix A: configs, selection metric, grad-clip, grad-scale, seeds | A-A | PART |
| AqnD-4 | No θ saturation analysis | Saturation analysis (WI-5) summary in §3.4 + table in appendix | M3.4, A-G | NEW |
| AqnD-5 | s bounded ≠ θ learnable | Explicit paragraph: boundedness is necessary but not sufficient for learnability; quantified margins | M3.4, M6 | NEW |
| AqnD-6 | Gradient factor can collapse at saturation | Report the derivative factor σ(θ)(1−σ(θ)) values (13% → 30% of peak) | M3.4, A-G | NEW |
| AqnD-7 | "Matches classical homoscedastic" misleading | Reword Eq. (10) comment: same algebraic form, different fixed-point structure; cite normalization ablation | M3.3, M4.1 | NEW |
| AqnD-8 | Same algebraic form ≠ same fixed-point | Explicit fixed-point discussion + Kendall+L1 ablation | M3.3, M4.1 | NEW |
| AqnD-9 | Kendall's optimum reachable, BPGS's not outside bound | Acknowledge in §3.4/limitations; empirical counter-evidence: no run reaches boundary | M3.4, M6 | NEW |
| AqnD-10 | NYUv2 hyperparam mismatch (120/8 vs 80/4) | Config fixed (WI-4); appendix A states final settings explicitly | A-A | DONE |
| AqnD-11 | Selection metric mismatch (total_loss vs miou) | Appendix A documents val/miou override for final benchmark, val/total_loss for ablation | A-A | DONE |
| AqnD-12 | Gradient clipping mismatch | Appendix A documents clip 10.0 (BPGS) vs 1.0 (Kendall ablation) | A-A | DONE |
| AqnD-13 | Mismatches undercut reproducibility | Covered by AqnD-3 + AqnD-10..12; add explicit "reproducibility reconciliation" sentence in appendix A intro | A-A | NEW |
| AqnD-14 | Narrow experimental scope | Nash-MTL + 4 new studies; future work statement | M4, A | NEW |
| AqnD-15 | Only three seeds | 10-seed scale stress (done); explicit per-study seed reporting | M4.3, A-A | PART |
| AqnD-16 | Robustness claim rests mainly on synthetic; RF1 not best | Invariance Proposition (formal, not empirical) + RF1 wording already fixed | M3.5, M5.5 | PART |
| AqnD-17 | Eq. (10) omits sg on batch statistics | sg[L_i] in Eq. (10) done (WI-4); sg on the μ(L)/σ̄(L) definitions still to add (02 §3.2) | M3.2, M3.3 | PART |
| AqnD-18 | Paper/code disagree elsewhere | Config standardization (WI-4) + appendix A documentation | A-A | DONE |
| AqnD-19 | Supplementary poorly laid out | Appendix restructure (WI-18): page break before checklist; new appendices | A, 05 | NEW |
| AqnD-20 | BPGS is another option, not a paradigm shift | Scope statement already in paper; keep; reinforce with "cheap fix for a specific failure mode" framing | M2, M6 | PART |
| AqnD-21 | No single benchmark dominance | Already stated ("results do not support a stronger statement"); keep | M5.5 | DONE |
| AqnD-22 | Lacks recent SOTA comparison | Nash-MTL added; IMTL-G/FAMO/CAGrad future work | M4.2, M6 | NEW |
| AqnD-23 | Engineering refinement, not conceptual novelty | Non-triviality pillar (invariance + Kendall+L1 + stop-grad ablations) | M3.5, M4.1, M4.3 | NEW |
| AqnD-C1 | Boundedness of s ≠ learnability of θ | Same as AqnD-5 | M3.4, M6 | NEW |
| AqnD-C2 | Limitations omit saturation issue | Add to limitations | M6 | NEW |
| AqnD-F1 | Anonymity violation in repo | Repo scrubbing (WI-1) still pending; URL appears in three paper locations — see 09 D8 | N/A | OPEN |

## D. Reviewer MKod

| ID | Issue | Resolving change | Placement | Status |
|---|---|---|---|---|
| MKod-1 | Constrained reparameterization of Kendall + normalization | Kendall+L1 ablation (WI-3) + related-work fixed-point discussion (WI-16) | M4.1, M2 | NEW |
| MKod-2 | Deeper properties not analyzed | Invariance Proposition + saturation analysis | M3.4, M3.5 | NEW |
| MKod-3 | Batch-size sensitivity | WI-12 study | M5.4, A-E | NEW |
| MKod-4 | Stop-gradient not ablated independently | WI-11 study | M4.3, A-E | NEW |
| MKod-5 | Missing CAGrad, Nash-MTL, Auto-Lambda | Nash-MTL added; CAGrad/Auto-Lambda future work statement | M4.2, M6 | NEW |
| MKod-6 | Only one dense-prediction benchmark | Cityscapes future work (WI-15); acknowledge honestly | M6 | NEW |
| MKod-7 | No computational overhead analysis | WI-10 study | M5.6, A-F | NEW |
| MKod-8 | Figures wedged in checklist, page-9 space | Appendix restructure (WI-18) | A, 05 | NEW |

## E. Technical analysis items (internal, not reviewer-sourced)

| ID | Issue | Resolving change | Placement | Status |
|---|---|---|---|---|
| TA-1 | Table 1 invariance is an algebraic identity, not emergent | Reframe Table 1 as empirical confirmation of Proposition 1; proof in main text | M3.5, M4.1 | NEW |
| TA-2 | Unknown if bounded chart adds value beyond L1-norm | Kendall+L1 ablation | M4.1, A-B | NEW |
| TA-3 | Table 5 gaps within ~1 SD at 3 seeds | 10-seed rerun already in paper; wording already says "comparison of means" | M4.1 | DONE |
| TA-4 | Abstract RF1 framing obscured last-place RMSE/MAE | Already fixed (WI-8) | M1, M5.5 | DONE |
| TA-5 | τ_T has no derivation | τ_T derivation | M3.2 | NEW |
| TA-6 | No empirical check of boundary approach | Saturation analysis | M3.4, A-G | NEW |

---

## F. Coverage check against the ledger

Ledger totals: 68 atomic issues (MR 10 + Mxe9 18 + AqnD 26 + MKod 8 + TA 6 = 68). Breakdown
(verified by scan, 2026-08-11): Mxe9-18 = Mxe9-1..12 from `reviewers.md` + Mxe9-Q1..Q6;
AqnD-26 = AqnD-1..23 + AqnD-C1 + AqnD-C2 + AqnD-F1. `reviewers.md` contains 56 distinct IDs
(strict numeric scan: 53); the ledger adds TA-1..6. All 68 entries map to rows above (MR in
§A, Mxe9 in §B, AqnD in §C, MKod in §D, TA in §E) — verified programmatically 53/53 + 59/59.
After implementation, re-run the ledger checklist (update `review_ledger.md` statuses) and
confirm 19/19 WI items closed or explicitly parked.

## G. Anything NOT going into the paper (deliberately)

| Item | Why not |
|---|---|
| The full 120-run 10-seed raw table for scale stress | Already represented by `tab:stress_scale` (10-seed) — no change |
| Nash-MTL alpha-trajectory figure | Useful but not needed; one sentence in text + appendix note suffices (space) |
| Detailed σ̄/μ trajectory figures per task | Saturation table + existing weight-dynamics figure cover the analysis |
| Per-seed breakdown tables for every benchmark | Standard practice is mean±std; per-seed data in code repo |
| BPGS×PCGrad combination results | Not run; discussion-only (WI-14 decision, see 09_open_decisions.md) |
| Cityscapes numbers | Not run; future-work statement only (WI-15) |
