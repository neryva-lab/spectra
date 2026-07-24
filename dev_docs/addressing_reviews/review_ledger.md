# Review Ledger — BPGS Revision Tracking

**Purpose:** A single checkbox-based tracker covering every issue raised across the AC meta-review,
all three official reviews (Mxe9, AqnD, MKod), and six additional technical findings surfaced by
directly reading the submitted PDF (labeled `TA-#`, for "Technical Analysis" — these are **not**
from an official reviewer; keep that distinction if any of this language ends up in a future
rebuttal or cover letter).

**How to use this file:**
- **Section 1** is where you actually work. Pick one unchecked `WI-#` item at a time, do it, check
  it off, update its `Status` line.
- **Section 2** is a full atomic log of every individual point anyone raised, each pointing back to
  the `WI-#` that resolves it. It exists purely so nothing gets dropped — you shouldn't need to
  work from it directly, only consult it if you want to double-check a specific reviewer's exact
  point before closing out a work item.
- Check boxes with `[x]` when done. Feel free to change `Status: Open` to `Status: In Progress` or
  add a note (e.g. `Status: Done — see exp_09_normalization_ablation`).

**Progress snapshot (update manually as you go):**
- Work items: 2 / 19 complete
- Atomic issues addressed: 0 / 68

---

## Section 1 — Work Items

### Tier 0 — Independent, no dependencies, do first

- [x] **WI-1. Scrub the anonymity violation from the code repository.**
  Remove the real author name from `spectra/__init__.py` and the "Neryva Lab" affiliation from
  `LICENSE`, `setup.py`, and `pyproject.toml`. Check git history too — editing the files alone
  leaves old commits exposed; a fresh orphan branch or new anonymized repo is safer.
  **Resolves:** AqnD-F1
  **Status:** Done - repo content scrubbed; see `dev_docs/addressing_reviews/review_task_complete_report/wi-1_anonymity_fix_report.md`

---

### Tier 1 — Foundational (the outcome of these determines how much of the rest changes)

- [x] **WI-2. Formalize the rescaling-invariance result as a proven proposition, not an empirical table.**
  Add a numbered proposition + short proof: under uniform rescaling, μ(L) shifts by log c, ς̄(L) is
  unchanged (centered moment), z_i(θ_i) is untouched, so s_i shifts uniformly and the L1-normalization
  in Eq. 8 cancels it exactly — BPGS is *exactly* invariant to uniform rescaling by construction.
  Reframe Table 1 as confirmatory evidence of the proposition, not as the primary empirical claim.
  **Resolves:** MR-1 (partial), MR-9 (partial), MKod-2 (partial), AqnD-16 (partial), TA-1
  **Status:** Done - proof report written; see `dev_docs/addressing_reviews/review_task_completed/wi-2_invariance_proof_report.md`

- [ ] **WI-3. Re-run the Kendall + L1-normalization ablation correctly.**
  Requirements for a valid version of this experiment:
  - Full ×1 / ×10 / ×100 / ×1000 grid — not a single endpoint.
  - Same metric as Table 1 (macro score) — not a different metric set (R², RMSE, Total Val Loss).
  - ≥3 seeds, reported as mean ± std, so gaps can be checked against noise.
  - A ×1 (no rescaling) run included, to rule out an untuned-hyperparameter confound driving any
    apparent degradation rather than a real scale-robustness effect.
  Use the result to determine whether the bounded/batch-aware chart adds value beyond plain
  normalization — this is the single result that determines how the paper's contribution should be
  framed going forward.
  **Resolves:** MKod-1, AqnD-7, AqnD-8, AqnD-9, AqnD-23, TA-2
  **Status:** Open (a first attempt was made but had methodological gaps — see prior notes; needs redo)

---

### Tier 2 — Scientific correctness fixes

- [ ] **WI-4. Reconcile the paper's equations/text with the actual released code.**
  Specifically: the undocumented 100× gradient scale on θ; the NYUv2 hyperparameter mismatch
  (paper vs. code disagree on epoch/batch settings, reported as 120/8 vs 80/4); the validation
  selection metric (`val/total_loss` in text vs. hard-coded `val/miou` in code); gradient-clipping
  value differences; and the missing stop-gradient notation on batch statistics in Eq. (10). Either
  update the equations/text to match what the code does, or update the code to match the paper and
  rerun any affected experiments (this affects Table 2 specifically, per AqnD).
  **Resolves:** AqnD-1, AqnD-2, AqnD-3, AqnD-10, AqnD-11, AqnD-12, AqnD-13, AqnD-17, AqnD-18
  **Status:** Open

- [x] **WI-5. Analyze and document θ / z_i saturation behavior empirically.**
  Add a companion analysis to the existing Figure 7 (task-weight dynamics): plot the underlying
  θ_i or z_i values (not just the derived α_i weight) across all main-paper runs (NYUv2, Yeast,
  RF1), and report whether any task's z_i approaches ±τ_T within the tested epoch budgets. Report
  the outcome either way, with a specific named conclusion rather than a generic "no convergence
  guarantees" statement.
  **Resolves:** AqnD-4, AqnD-5, AqnD-6, AqnD-C1, AqnD-C2, MKod-2 (partial), TA-6
  **Status:** Done - saturation check report written; see `dev_docs/addressing_reviews/review_task_completed/wi-5_saturation_check_report.md`

- [x] **WI-6. Derive or explicitly justify τ_T (Eq. 4).**
  Either derive why `τ_T = √(T−1) + 0.1` is the correct functional form, or state plainly that it's
  a heuristic choice and support that with a small sensitivity sweep (e.g., τ_T scaled by 0.5×, 1×,
  2× the current value) showing the method isn't fragile to this specific constant.
  **Resolves:** MR-4, TA-5
  **Status:** Done - justification report written; see `dev_docs/addressing_reviews/review_task_completed/wi-6_tau_t_justification_report.md`

- [ ] **WI-7. Increase statistical rigor on the scale-stress result (Table 5) and reframe the claim to match it.**
  Every current BPGS-vs-Kendall gap in Table 5 is smaller than one combined standard deviation at
  3 seeds (largest gap, at ×1000, is ~0.94 combined SD — still under one). Either run more seeds
  specifically on this grid, report per-seed values so a real paired test is possible, or reframe
  the text to something like "directionally favorable at the largest perturbation, not statistically
  distinguished from Kendall at 3 seeds" instead of claiming a clear win.
  **Resolves:** Mxe9-9, Mxe9-10, AqnD-15, TA-3
  **Status:** Open

- [ ] **WI-8. Fix the RF1 reporting language in the abstract and §5.4.**
  Replace "RF1 RMSE and MAE within 0.562 and 0.450 of the leading baseline" with an accurate
  statement — BPGS has the *worst* RMSE (30.158) and *worst* MAE (23.548) of all six compared
  methods on RF1 (though second-best on R², behind UWSO). State this plainly rather than in a
  near-parity framing.
  **Resolves:** AqnD-16 (partial), TA-4
  **Status:** Open

---

### Tier 3 — Expand the evidence base

- [ ] **WI-9. Add modern MTL baselines.**
  At minimum Nash-MTL and FAMO — the most-repeated ask, raised independently by all three
  reviewers. Add IMTL-G, CAGrad, and Auto-Lambda if time allows.
  **Resolves:** Mxe9-5, Mxe9-6, Mxe9-Q3, AqnD-22, MKod-5
  **Status:** Open

- [ ] **WI-10. Add runtime / compute / memory overhead analysis relative to Kendall.**
  Report wall-clock and memory overhead introduced by the batch-wise log-loss statistics,
  normalization, and the separate uncertainty-objective optimization pass.
  **Resolves:** Mxe9-11, Mxe9-12, Mxe9-Q4, MKod-7
  **Status:** Open

- [ ] **WI-11. Ablate the stop-gradient design choice independently from the bounded/batch-aware chart.**
  Isolate whether the split-optimization stop-gradient is doing independent work, rather than only
  ever reporting it bundled with the rest of the method.
  **Resolves:** MKod-4
  **Status:** Open

- [ ] **WI-12. Run a batch-size sensitivity analysis.**
  The method depends directly on batch statistics (μ(L), ς̄(L)); test how results change across a
  meaningful range of batch sizes.
  **Resolves:** Mxe9-Q6, MKod-3
  **Status:** Open

- [ ] **WI-13. Run a first-batch calibration sensitivity analysis.**
  Test whether a different first observed batch leads to substantially different learned
  uncertainty trajectories, given the method's first-batch auto-calibration step.
  **Resolves:** Mxe9-Q1, Mxe9-Q2
  **Status:** Open

- [ ] **WI-14. Investigate combining BPGS with conflict-aware methods, or explain the noisy/conflict-regime weakness directly.**
  Either test a BPGS+PCGrad or BPGS+CAGrad combination, or add explicit discussion of why BPGS
  underperforms Kendall and PCGrad specifically in the noisy and conflict heterogeneous-stress
  regimes (Table 7).
  **Resolves:** Mxe9-3, Mxe9-4, Mxe9-Q5
  **Status:** Open

- [ ] **WI-15. Add a second dense-prediction benchmark beyond NYUv2.**
  Cityscapes or a medical-imaging multi-task setup, per MKod's specific suggestion. Also
  contributes to the broader "narrow benchmark diversity" concern raised by Mxe9 and AqnD.
  **Resolves:** MKod-6; contributes to Mxe9-7, Mxe9-8, AqnD-14
  **Status:** Open

---

### Tier 4 — Writing, positioning, presentation

- [ ] **WI-16. Rewrite Section 2 (Related Work) positioning.**
  Sharpen exactly how BPGS differs from GradNorm, dynamic task prioritization, PCGrad, CAGrad, and
  Sener–Koltun's Pareto-based approach. State the novelty claim at the size the evidence actually
  supports — a scale-robustness-focused refinement of uncertainty weighting, not a general
  multi-task optimization advance.
  **Resolves:** MR-3, MR-5, AqnD-20, AqnD-21, AqnD-23 (partial), MKod-1 (partial)
  **Status:** Open

- [ ] **WI-17. Add intuition and motivation prose throughout Section 3 (Method).**
  Explain *why* each design choice exists (the bounded chart, batch-conditioning, the split
  optimization) in plain language surrounding the formulas, not just the formulas themselves.
  **Resolves:** MR-1 (partial), MR-2
  **Status:** Open

- [ ] **WI-18. Fix the appendix/supplementary layout.**
  Separate figures and results tables from the NeurIPS checklist section (currently interleaved);
  use the unused space on page 9 for additional analysis or baseline results instead of leaving it
  blank.
  **Resolves:** AqnD-19, MKod-8
  **Status:** Open

---

### Tier 5 — Final gate (do last, after everything above)

- [ ] **WI-19. Final consistency pass: verify the abstract/intro claims match what's actually demonstrated.**
  After all fixes above are in, re-read the abstract and introduction specifically for overreach —
  confirm the stated scope of motivation, novelty, and significance doesn't exceed what the
  (now-corrected) evidence supports. This is the AC's central, cross-cutting complaint and deserves
  a deliberate dedicated check, not just an assumption that the accumulated fixes handled it.
  **Resolves:** MR-6, MR-7, MR-8, MR-9 (partial), MR-10, Mxe9-1, Mxe9-2, AqnD-16 (partial)
  **Status:** Open

---

## Section 2 — Full Atomic Issue Log (traceability appendix — reference only)

### Meta Review (AC zptV)
- [ ] MR-1 — Section 3 presented mainly as formulas, insufficient intuition → WI-2, WI-17
- [ ] MR-2 — Design choices not sufficiently justified → WI-17
- [ ] MR-3 — Relationship to existing techniques not explained clearly → WI-16
- [ ] MR-4 — Choice in Eq. (4) not explained → WI-6
- [ ] MR-5 — Positioning relative to prior work limited → WI-16
- [ ] MR-6 — Empirical evaluation narrow → WI-19
- [ ] MR-7 — Results modest → WI-19
- [ ] MR-8 — Problem motivation not established strongly enough → WI-19
- [ ] MR-9 — Novelty not established strongly enough → WI-2, WI-19
- [ ] MR-10 — Significance not established strongly enough → WI-16, WI-19

### Reviewer Mxe9
- [ ] Mxe9-1 — Scope narrower than framing suggests → WI-19
- [ ] Mxe9-2 — Not shown superior for general MTL optimization → WI-19
- [ ] Mxe9-3 — Mixed-stress shows limits in noisy/conflict regimes → WI-14
- [ ] Mxe9-4 — Kendall/PCGrad beat BPGS in noisy/conflict regimes → WI-14
- [ ] Mxe9-5 — Comparison set incomplete → WI-9
- [ ] Mxe9-6 — Missing Nash-MTL, IMTL-G, FAMO → WI-9
- [ ] Mxe9-7 — Limited evaluation beyond NYUv2 → WI-15
- [ ] Mxe9-8 — Only two additional real-data benchmarks → WI-15
- [ ] Mxe9-9 — Only three seeds → WI-7
- [ ] Mxe9-10 — Statistical evidence insufficient for fine-grained ranking → WI-7
- [ ] Mxe9-11 — No runtime/overhead analysis → WI-10
- [ ] Mxe9-12 — Practical cost of calibration/split-optimization unclear → WI-10
- [ ] Mxe9-Q1 — Sensitivity to first-batch calibration? → WI-13
- [ ] Mxe9-Q2 — Would a different first batch change trajectories? → WI-13
- [ ] Mxe9-Q3 — Evaluated against Nash-MTL/IMTL-G/FAMO? → WI-9
- [ ] Mxe9-Q4 — Runtime/memory overhead vs. Kendall? → WI-10
- [ ] Mxe9-Q5 — Can BPGS combine with PCGrad/CAGrad? → WI-14
- [ ] Mxe9-Q6 — Sensitivity to batch size? → WI-12

### Reviewer AqnD
- [ ] AqnD-1 — Undocumented 100× gradient scale on θ → WI-4
- [ ] AqnD-2 — Equations don't fully describe actual optimizer → WI-4
- [ ] AqnD-3 — Eqs. (5)–(10) wouldn't reproduce Table 2 → WI-4
- [ ] AqnD-4 — No analysis of θ saturation → WI-5
- [ ] AqnD-5 — s bounded proven, θ learnability at boundary not addressed → WI-5
- [ ] AqnD-6 — Gradient factor can collapse at saturation → WI-5
- [ ] AqnD-7 — "Matches classical homoscedastic weighting" claim misleading → WI-3
- [ ] AqnD-8 — Same algebraic form ≠ same fixed-point structure → WI-3
- [ ] AqnD-9 — Kendall's optimum reachable, BPGS's isn't outside bound → WI-3
- [ ] AqnD-10 — NYUv2 hyperparameter mismatch (120/8 vs 80/4) → WI-4
- [ ] AqnD-11 — Selection metric mismatch (val/total_loss vs val/miou) → WI-4
- [ ] AqnD-12 — Gradient clipping mismatch → WI-4
- [ ] AqnD-13 — Mismatches undercut the reproducibility-under-scale-mismatch claim → WI-4
- [ ] AqnD-14 — Narrow experimental scope overall → WI-15
- [ ] AqnD-15 — Only three seeds → WI-7
- [ ] AqnD-16 — Robustness claim rests mainly on synthetic diagnostics; Table 4 admits not best on RF1 → WI-2, WI-8, WI-19
- [ ] AqnD-17 — Eq. (10) omits stop-gradient on batch statistics → WI-4
- [ ] AqnD-18 — Paper/code disagree in other non-trivial places → WI-4
- [ ] AqnD-19 — Supplementary material poorly laid out → WI-18
- [ ] AqnD-20 — BPGS is another option, not a paradigm shift → WI-16
- [ ] AqnD-21 — No single benchmark shows clear dominance → WI-16
- [ ] AqnD-22 — Lacks comparison to recent SOTA (most recent ref. from 2021) → WI-9
- [ ] AqnD-23 — Characterized as engineering refinement, not novel concept → WI-3, WI-16
- [ ] AqnD-C1 — Boundedness of s ≠ learnability of θ → WI-5
- [ ] AqnD-C2 — Limitations section omits the saturation issue → WI-5
- [ ] AqnD-F1 — Anonymity violation in released repo → WI-1

### Reviewer MKod
- [ ] MKod-1 — Largely a constrained reparameterization of Kendall + normalization → WI-3, WI-16
- [ ] MKod-2 — Deeper properties (invariance, convergence) not analyzed → WI-2, WI-5
- [ ] MKod-3 — Batch-size sensitivity not analyzed → WI-12
- [ ] MKod-4 — Stop-gradient role not ablated independently → WI-11
- [ ] MKod-5 — Missing CAGrad, Nash-MTL, Auto-Lambda comparisons → WI-9
- [ ] MKod-6 — Only one full-scale dense-prediction benchmark → WI-15
- [ ] MKod-7 — No computational overhead analysis → WI-10
- [ ] MKod-8 — Presentation: figures wedged into checklist, unused page-9 space → WI-18

### Technical Analysis (independent findings from direct PDF review — not from an official reviewer)
- [ ] TA-1 — Table 1's rescaling invariance is an algebraic identity of the construction, not an emergent empirical finding → WI-2
- [ ] TA-2 — Unknown whether bounded/batch-aware chart adds value beyond plain L1-normalization — needs a controlled ablation → WI-3
- [ ] TA-3 — Table 5 gaps are all within ~1 combined standard deviation at 3 seeds — current framing overstates significance → WI-7
- [ ] TA-4 — Abstract's RF1 framing obscures that BPGS is last of 6 methods on RMSE and MAE → WI-8
- [ ] TA-5 — τ_T (Eq. 4) has no stated derivation for its specific functional form → WI-6
- [ ] TA-6 — No empirical check exists for whether θ_i/z_i approach the saturation boundary in any reported run → WI-5
