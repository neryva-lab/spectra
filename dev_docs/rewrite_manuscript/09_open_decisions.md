# 09 — Open Decisions (need user input before/during implementation)

Decisions are ordered by when they block work. Each has a recommendation with rationale.
Mark the chosen option and update the referencing files (`04_tables_figures_specs.md`,
`02_section_by_section_rewrite_plan.md`) accordingly.

---

## D1. Normalization-ablation seed set (RESOLVED; blocks Phase 1 until completed)

**Context.** The completed Kendall+L1 ablation (`experiment_results/exp_09_kendall_norm_ablation/`)
used seeds **{42, 123, 999}**, while the paper's rescaling table uses seeds **{42, 43, 44}**.
Consequently BPGS at ×1 reads 0.789 in the new table vs 0.777 in the existing rescaling table —
a visible, unexplained inconsistency if both tables appear in the paper.

| Option | Description | Cost | Verdict |
|---|---|---|---|
| **A (recommended)** | Rerun the normalization ablation with seeds 42/43/44 on the pure-rescaling grid (36 runs; the same synthetic task family that already ran 120 runs during the rebuttal) | ~hours–1 day of compute | **Best quality.** Tables consistent; no explanatory footnote needed; stronger paper |
| B | Keep the 42/123/999 run; add an explicit seed-set footnote to the table caption and phrase prose in relative terms (scale sensitivity Δ) only | free | Acceptable, but invites reviewer confusion |

**Decision: adopt Option A.** The synthetic experiments are cheap relative to the value of table
consistency; AqnD's original complaint was precisely about code/paper mismatches, and a
seed-set mismatch between two paper tables invites the same class of criticism.
The manuscript must not quote a newly regenerated normalization-ablation table until the
42/43/44 rerun has completed and passed the raw-output audit. If the rerun cannot be completed,
the fallback is not silent substitution: retain the existing {42,123,999} results, label the
seed set explicitly in every caption and table reference, and do not present the two tables as
directly seed-matched comparisons.

## D2. WI-14 — noisy/conflict regime + BPGS×PCGrad/CAGrad (BLOCKS Phase 6)

| Option | Description | Cost | Verdict |
|---|---|---|---|
| **A (recommended)** | Discussion-only: explain why BPGS trails in noisy/conflict regimes (scalar weights, no gradient surgery) and state combination as untested future work | free | Honest; matches what was promised in the rebuttal response |
| B | Run BPGS+PCGrad combination experiment (requires new training runs on the synthetic heterogeneous study + implementation work) | days–weeks; new code | Stronger evidence, but introduces a *new* untested code path and risks opening new review targets |

**Recommendation: A** for this revision. The response to Mxe9-Q5 already committed to the
discussion phrasing; combination experiments should not be rushed into the paper.

## D3. WI-15 — second dense-prediction benchmark (Cityscapes)

| Option | Description | Cost | Verdict |
|---|---|---|---|
| **A (recommended)** | State in Discussion as planned future work; do not promise results | free | Honest; the rebuttal already said "plan to add in the revision" — must be worded carefully ("planned, not yet completed") to avoid promising a result that is not in the paper |
| B | Actually run Cityscapes (needs dataset, baselines × 3 seeds, ~weeks) | weeks | Would substantially strengthen §5.2's generality claim — but only if completed; do not start unless the timeline allows |

**Recommendation: A** (this plan assumes A). If B becomes feasible mid-implementation, it is a
separate workstream and must not block the manuscript edits.

## D4. Proposition numbering style

- Option A: `\newtheorem{proposition}{Proposition}` — standalone numbering (Prop 1, 2, …).
- Option B: number with equations (Proposition 3.8-style).
- **Recommendation: A**, simpler cross-references (`Proposition~\ref{prop:invariance}`).
- Consistency note: the paper currently has no theorems; whichever is chosen, keep it uniform.

## D5. Optional F-norm figure (normalization ablation visualization)

- Include in Appendix B only if it renders clearly and the appendix doesn't bloat.
- **Recommendation:** include if trivial to generate (one matplotlib call reusing style
  helpers); skip otherwise. Table `tab:norm_ablation` is the authoritative artifact.

## D6. Auto-Lambda citation

- The paper attributes Δ_M to MTAN `liu2019mtan` (keep that attribution; do not move it to
  Auto-Lambda).
- MKod-5 explicitly named Auto-Lambda as a missing recent method, and the Discussion future-work
  item (02 §6 item 7) names it. A method named in prose must carry its citation.
- **Recommendation (revised):** keep `liu2022autolambda` in the bibliography and cite it once in
  the Discussion future-work sentence ("CAGrad, IMTL-G, FAMO, and Auto-Lambda are not yet
  evaluated and are future work \cite{liu2022autolambda}"). Cheap, answers MKod-5 fully, and the
  entry stays used (no uncited-entry warning).

## D7. Target venue (affects nothing in this plan, but worth deciding soon)

- The plan keeps NeurIPS 2026 formatting. If the next submission targets ICML 2027 or NeurIPS
  2027, formatting instructions will differ slightly (style file, checklist). Re-verify before
  submission; this does not change the content plan.

## D8. Anonymity at submission (MUST be handled before any upload)

- The identifying repo URL `https://github.com/neryva-lab/spectra` currently appears in
  **three** places, not one (verified by grep): `sections/03_experimental_setup.tex` §4.3
  (line 17, main text), `appendix/A_reproducibility_details.tex` (line 17), and
  `checklist.tex` (line 70). The reviewer (AqnD-F1) already flagged the "Neryva Lab" identity.
  At submission time:
  1. **All three** occurrences must be anonymized (per NeurIPS policy, an anonymized code link
     is allowed; a link to the real repo is an anonymity violation).
  2. WI-1 scrubbed the cited identity strings (author names in `spectra/__init__.py`,
     `setup.py`, `pyproject.toml`, `LICENSE`) but did not address git history. Remaining
     items: the real URL is still in current content at `docs/getting_started.md` (line 16)
     in addition to the three paper locations; and the git history is exposed (verified:
     `docs/getting_started.md` with the real URL is in the initial commit). Submit only an
     anonymized repository artifact (fresh orphan branch or new repository if necessary). Do
     not claim that WI-1 alone resolves this risk.
- **Action item for the user** (not part of the manuscript edits): prepare the anonymized
  repository + link before submission day. Phase 9 audit greps the compiled PDF text for the
  URL string to confirm zero hits.
