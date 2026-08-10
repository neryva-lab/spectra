# 00 — Executive Overview: Manuscript Rewrite Plan (Post-Review Revision)

**Date:** 2026-08-11
**Status:** Plan (not yet implemented)
**Inputs consumed:** `dev_docs/review/openreview.md` (3 reviews + AC meta-review),
`dev_docs/response/*.md` (the 4 submitted rebuttal responses),
`dev_docs/addressing_reviews/review_ledger.md` + all 17 `review_task_completed/*.md` reports,
`working/paper/**` (current manuscript source, tables, figures, appendices, compiled PDF).

---

## 1. Purpose of this document set

This directory contains the complete, itemized rewrite plan for the BPGS manuscript before the
next submission. The plan answers four questions:

1. **What** content is added/changed/moved (per section, per table, per figure, per reference).
2. **Why** each change exists (which reviewer issue / atomic ledger item it resolves).
3. **Where** each piece of evidence lands (main 9-page text vs. unlimited appendix), subject to
   the NeurIPS rule that *the paper must stand alone without the appendix*.
4. **How** the change is implemented and verified (which scripts produce which `.tex` files,
   how the PDF is rebuilt, and what consistency checks must pass).

---

## 2. The situation (what the reviewers said, condensed)

Three reviewers + one AC. Verdicts: 2/2/3 with an AC meta-review leaning reject. The **core
complaint is consistent across all of them**:

> The method is an incremental re-parameterization of Kendall's uncertainty weighting; the
> technical core is under-developed (formulas without intuition, unexplained constants, no formal
> properties beyond trivial boundedness); the evaluation is narrow (few benchmarks, few seeds,
> no modern baselines, no overhead analysis); and the paper's framing over-claims relative to
> the evidence.

Concrete failure-level findings (AqnD): an undocumented `theta_grad_scale=100.0` meant the
published equations did not describe the actual optimizer; several paper/code mismatches;
a saturation failure mode of the bounded sigmoid was never analyzed; the "matches classical
homoscedastic weighting" claim conflates algebraic form with fixed-point structure.

## 3. What was already done (during the rebuttal window) — the raw material we now write up

All of the following *exist as completed work* (see `dev_docs/addressing_reviews/review_task_completed/`).
The manuscript rewrite is the job of turning these into paper content:

| Work item | Result | Paper status today |
|---|---|---|
| WI-1 anonymity scrub | Code repo anonymized | N/A (repo, not paper) |
| WI-2 invariance proof | **Exact invariance of normalized weights under uniform rescaling, proven algebraically** | **NOT in paper — must be added as a Proposition** |
| WI-3 Kendall+L1 ablation | 36 runs: L1-normalization alone does NOT recover BPGS robustness (−0.105 vs −0.004) | **NOT in paper — must be added (appendix table + main-text paragraph)** |
| WI-4 paper/code reconciliation | Configs fixed; selection metric, grad-clip, `theta_grad_scale` documented | Partially in appendix A; **`theta_grad_scale` still missing from main text/appendix** |
| WI-5 saturation check | No run approaches the boundary; max `|z_i|/τ_T` = 0.93; gradients stay meaningful | **NOT in paper — must be added (method + limitations + appendix table)** |
| WI-6 τ_T justification | `√(T−1)` derived via Cauchy–Schwarz on the standardized vector; +0.1 is a safety margin | **NOT in paper — derivation must be added** |
| WI-7 10-seed scale stress | Table updated, already in paper (`tab:stress_scale`, 10 seeds) | **DONE** |
| WI-8 RF1 language | Abstract/intro/results corrected | **DONE** |
| WI-9 Nash-MTL baseline | Implemented + run on NYUv2 (3 seeds): mIoU 0.252±0.027 (weakest), high seed variance | **NOT in paper — must be added (NYUv2 table row + text)** |
| WI-10 runtime/memory | +0.15% time, +0.87% memory vs Kendall | **NOT in paper — must be added** |
| WI-11 stop-grad ablation | Without stop-grad: θ_max +28%, 14× seed variance, mIoU −4.3% | **NOT in paper — must be added** |
| WI-12 batch-size sensitivity | bs 4/8/16: across-bs CV < 3.5% | **NOT in paper — must be added** |
| WI-13 first-batch sensitivity | 3 loader seeds: CV < 2%; θ_max converges within 0.3% | **NOT in paper — must be added** |
| WI-16 related-work positioning | Section rewritten; scoped to "bounded, batch-aware refinement of uncertainty weighting" | **DONE (minor: add Nash-MTL mention)** |
| WI-17 method intuition prose | Motivation paragraphs added | **DONE (may need slight tightening for space)** |
| WI-18 appendix layout | Plan written, **not implemented** | **OPEN — implement now** |
| WI-19 consistency pass | Confirmed wording aligned | **DONE (re-run at end of this rewrite)** |
| WI-14 BPGS×conflict-aware | Not run; discussion-only resolution | **OPEN — resolve in Discussion** |
| WI-15 Cityscapes | Not run | **OPEN — state as future work, do not promise** |

## 4. The rewrite strategy (rationale)

**Central narrative shift.** The paper's center of gravity moves from
"a robust weighting method with decent results" to:

> **BPGS is the uncertainty-weighting rule whose normalized weights are *provably* invariant to
> uniform loss rescaling, whose components are each *individually justified and ablated*, and
> which delivers this robustness with negligible overhead and without benchmark loss.**

Three pillars carry this narrative:

1. **Formal pillar (answers AC's "limited technical depth", AqnD-8/9, MKod-2):**
   a new Proposition (invariance under uniform rescaling) with a compact proof, plus the derived
   τ_T bound (answers MR-4 / Eq-4 question). The boundedness property is kept but framed as one
   of two formal properties, not the only one.

2. **Non-triviality pillar (answers "incremental over Kendall", AqnD-7, MKod-1, MR-9):**
   the Kendall+L1 ablation shows normalization alone cannot reproduce the robustness
   (−0.105 vs −0.004 degradation), and the stop-gradient ablation shows the split optimization
   does real work (θ_max +28% and 14× variance without it). Together these demonstrate the two
   "twists" each contribute beyond the algebraic form being similar to Kendall.

3. **Trust/accountability pillar (answers AqnD's reproducibility complaints, Mxe9's questions):**
   full documentation of `theta_grad_scale`, selection metric, grad-clip, hyperparameters;
   saturation analysis with quantified margins; batch-size and first-batch sensitivity studies;
   runtime/memory measurement; and honest limitations.

**Honesty rule (applies everywhere):** every claim must match table-level evidence. No
"competitive near-parity" phrasing for RF1, no implication that the noisy/conflict regimes are
won, no promise of Cityscapes. This was the strongest thread in the AC meta-review.

## 5. Placement policy (main text vs appendix)

NeurIPS 2026: 9 pages main content; references/appendices/checklist unlimited; the paper must
stand alone without the appendix.

| Content | Placement | Justification |
|---|---|---|
| Invariance Proposition + proof | **Main (§3.5)** | It *is* the central methodological claim — cannot be appendix-only |
| τ_T derivation | **Main (§3.2)** | Directly answers "why this constant"; a few lines |
| `theta_grad_scale` note | **Main (§3.3) + appendix A detail** | AqnD: equations must describe the optimizer |
| Saturation analysis (summary) | **Main (§3.4) + appendix table** | Explains the boundedness claim's limits; summary is 3–4 sentences |
| Saturation full table | **Appendix** | Supporting evidence |
| Kendall+L1 ablation (summary) | **Main (§4.1) + appendix table** | The main-text paragraph carries the conclusion; full table in appendix |
| Stop-grad ablation (summary) | **Main (§4.3) + appendix table/figure** | Same pattern |
| Batch-size + first-batch sensitivity | **Main (§4.4, one paragraph) + appendix** | Robustness checks, not core claims |
| Runtime/memory | **Main (§4.4 or §4.5, few sentences) + appendix table** | Same pattern |
| Nash-MTL | **Main (table row + sentences; related work)** | A comparison baseline is main-text material |
| Mixed-stress regime discussion | **Main (§6)** | Honest scoping + future-work positioning (WI-14) |
| All full experimental details | **Appendix A** | Standard practice |

## 6. Where the paper stands on page budget (measured, not guessed)

The compiled PDF (`build/main.pdf`, last built 2026-05-07, before the WI-7 10-seed update) is
only a provisional layout baseline: its build auxiliary data still records the scale-stress
table as 3-seed, while the current source records the completed 10-seed table. Rebuild before
treating page counts or float positions as authoritative. The provisional baseline shows
References beginning on page 8, suggesting roughly **~1.5 pages** of headroom, but this must
be remeasured after the source/data reconciliation.

Estimated additions: **~1.3 pages** (see `07_page_budget_and_space_reclamation.md`). This is
feasible *if* we reclaim ~0.2–0.3 pages by tightening existing prose (the method motivation
paragraphs added for the rebuttal can be compressed) and by keeping new tables out of the main
text. A prioritized fallback-cut list is in file 07 in case the build overflows.

## 7. Files in this plan

| File | Contents |
|---|---|
| `01_issue_to_change_matrix.md` | Every atomic issue (MR-*, Mxe9-*, AqnD-*, MKod-*, TA-*) → the concrete change that resolves it → placement |
| `02_section_by_section_rewrite_plan.md` | Per-section edit instructions, in reading order |
| `03_technical_content_drafts.md` | Draft text: Proposition 1 + proof, τ_T derivation, saturation paragraph, grad-scale note |
| `04_tables_figures_specs.md` | Every new/updated table and figure: exact numbers, sources, output paths |
| `05_appendix_restructure.md` | Appendix reorganization (WI-18) + checklist separation |
| `06_references_update.md` | New bibliography entries (Nash-MTL, IMTL-G, FAMO, Auto-Lambda) |
| `07_page_budget_and_space_reclamation.md` | Page accounting + fallback cuts |
| `08_execution_order.md` | Ordered implementation steps with build/verification gates |
| `09_open_decisions.md` | D1 is resolved as a required 42/43/44 rerun (with an explicit fallback); WI-14/WI-15 remain parked as discussion/future-work decisions |

## 8. Golden rules for the implementation phase

1. **No number enters the paper that is not in a verified source file.** Every table is generated
   from the experiment outputs by an analysis script (or is a hard-coded static table with the
   source path recorded in the file header comment).
2. **Build after every section change** (`.\build.ps1`) and check: compiles clean, ≤ 9 main pages,
   no overfull boxes that break layout, no dangling `\ref`/`\cite`.
3. **Run the WI-19 consistency pass** (abstract ↔ intro ↔ results ↔ discussion ↔ limitations)
   as the final gate.
4. **Do not add claims** beyond what the data supports; where a reviewer-facing statement is
   softened, soften the abstract/intro at the same time so the whole paper tells one story.
5. **Keep the anonymity discipline**: no author names, no affiliation, no links to the real repo
   in the manuscript.
