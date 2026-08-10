# 08 — Execution Order & Verification Gates

Implementation is staged so that **data and scripts come first** (every table/figures regenerated
from sources), **then prose**, then **appendices**, with a **build + audit** at each gate.
Each phase is independently verifiable; do not skip gates.

> Pre-requisite: user decision on the open items (`09_open_decisions.md`), especially D1
> (normalization-ablation seeds) which changes where Phase 1 reads data.

---

## Phase 0 — Baseline & backup (0.5 h)

1. Record baseline state: `git status` clean-ish, current `build/main.pdf` hash, page count (21).
2. Copy `working/paper/` → `dev_docs/temp/baseline_paper_backup/` (or git tag `pre-rewrite`).
3. Run `.\build.ps1` and confirm it still produces the current PDF (build tooling sanity check).
   **Gate 0:** build succeeds; baseline hash recorded.

## Phase 1 — Data pipeline (the long pole; no manuscript edits yet)

1. **Nash-MTL table row**
   - Add `nash_mtl` to `NYUV2_METHODS` (analysis/studies/nyuv2/constants.py or the common
     constants file).
   - Stage/copy Nash-MTL metrics CSVs so `discover_nyuv2_runs` finds them (extend
     `resolve_nyuv2_path` or copy into the standard layout — implementation detail, keep a note
     of which).
   - Regenerate `nyuv2_main_table.tex`; verify Nash-MTL row against acceptance numbers in
     `04_tables_figures_specs.md` §1 (esp. Δ_M ≈ −0.038 computed, not typed).
2. **New analysis study packages** (mirror existing study layout: `extract.py`, `table.py`,
   `figures.py`):
   - `studies/norm_ablation/` → `data/norm_ablation/tables/norm_ablation_table.tex`
     (source: `experiment_results/exp_09_kendall_norm_ablation/20260724_113615/`; or the rerun
     output if D1 = rerun).
   - `studies/sensitivity/` → stop-gradient, batch-size, first-batch tables + θ_max figures;
     overhead table (source roots: `experiment_results/12_nyuv2_stop_gradient`,
     `11_nyuv2_batch_size`, `10_nyuv2_first_batch`, `09_nyuv2_overhead`).
   - `studies/saturation/` → `data/saturation/tables/saturation_table.tex`
     (source: logged main runs listed in `04` §7).
   - Reuse the existing figure style helpers (`analysis/common/latex.py`, figure style module).
3. **Acceptance check:** every generated table cell matches the numbers in `04_tables_figures_specs.md`
   (rounded to the same precision). Any mismatch = investigate before proceeding.
   **Gate 1:** all 6 new/updated tables + 3 figures exist at their target paths and pass the
   acceptance check.

## Phase 2 — References (0.3 h)

1. Add the 4 bib entries (`06_references_update.md`); verify page numbers via web if unsure.
2. Insert the related-work sentence (draft in `06` §3).
3. **Gate 2:** `bibtex` clean (no undefined-citation warnings); every new `\cite` resolves.

## Phase 3 — Method section (`sections/02_method.tex`)

**Step 0 — restore the reviewer state of the file (before any additions; see 02 §3 Step 0):**
the working file diverged from the compiled PDF. Purge the draft notes (02_method.tex lines
~37, 56, 65–110: τ_1 edge-case note, J_net/J_all note, boundedness scratchpad), restore the
PDF's §3.3/§3.4 order (Split optimization objectives before Batch-conditional boundedness),
restore the lost `g_θ = 100` sentences (§3.3 prose and §4.3) and `\operatorname{sg}[\alpha_i]`
in the J_net equation, and retarget the fixed-point paragraph's undefined `sec:ablation_sg`
reference to `\ref{sec:norm_ablation}` (label added in §5.1(b)).

Apply in file order (drafts in `03_technical_content_drafts.md`):
1. τ_T derivation after Eq. (4); add `\operatorname{sg}` to μ/σ̄ where they enter Eq. (10).
2. Grad-scale note in §3.3 (restore the lost sentence first — see note in 03 §2).
3. Saturation paragraph at end of §3.4.
4. New §3.5 with Proposition 1 (add `\newtheorem{proposition}` to preamble; standalone
   counter per 09 D4).
5. Apply reclamation cuts #1 (motivation paragraphs) and #4 (discussion tightening deferred).
6. Build; confirm main text still ≤ 9 pages (page count via pdftotext).
   **Gate 3:** build clean; no undefined refs to new labels; page 9 not overflowed.

## Phase 4 — Experimental setup (`sections/03_experimental_setup.tex`)

1. Add controlled-studies block + normalization-ablation block (§4.1).
2. Add Nash-MTL to compared methods (§4.2).
3. Update reporting protocol (§4.3): new studies' seeds; optimizer-fidelity sentence.
4. Apply reclamation cut #3.
5. Build. **Gate 4:** clean build.

## Phase 5 — Results (`sections/04_results.tex`)

1. §5.1: invariance-reference sentence + normalization-ablation paragraph.
2. §5.2: Nash-MTL sentence (numbers as in the regenerated table).
3. §5.3: stop-gradient paragraph.
4. §5.4: new sensitivity subsection (draft 8 in `03`).
5. §5.6: new overhead subsection (draft 9 in `03`). (Keep §5.5 untouched.)
6. Apply reclamation cut #2.
7. Build; check page budget; apply fallbacks F1→F3 only if needed (see 07 §4).
   **Gate 5:** main text ≤ 9 pages; tables/figures all placed; no overfull boxes.

## Phase 6 — Discussion & Limitations (`sections/05_discussion_limitations.tex`)

1. Rewrite the limits list per `02` §6 and drafts 10 in `03`.
2. Keep societal-impact paragraph.
3. Build. **Gate 6:** clean build; limitation items all traceable to a reviewer issue.

## Phase 7 — Abstract & Introduction

1. Apply abstract draft (`02` §0) and intro bullet updates (`02` §1).
2. Apply reclamation cut #5 if needed.
3. **Gate 7:** abstract ≤ ~200 words; intro bullets ≤ 5; no claim exceeds the results tables.

## Phase 8 — Appendices (`appendix/*.tex` + `main.tex`)

1. Extend A (optimizer fidelity, Nash-MTL protocol, controlled-study configs).
2. Extend B (norm-ablation table + optional figure).
3. Extend C (Nash-MTL weight-variance note).
4. Create E, F, G per `05_appendix_restructure.md` (tables/figures from Phase 1).
5. Update `main.tex` appendix block + `\clearpage` before checklist.
6. Build; verify layout per `05` §5 checklist (incl. pdftotext scan for the checklist page).
   **Gate 8:** appendices A–G in order; checklist on its own page(s); no floats past it.

## Phase 9 — Final audit (the WI-19 gate, repeated for the new content)

1. **Claim audit:** read abstract + intro + results + discussion in one pass; each quantitative
   claim must appear in a table/figure with matching numbers; grep for banned phrasing
   (e.g., "superior", "dominates", "best on RF1", "paradigm").
2. **Number audit:** grep every number quoted in prose (0.777, 0.778, 0.780, 0.637, 0.223, 0.790,
   1.891, 0.616, −0.004, −0.105, 0.252, 0.038, 0.93, 0.84, 40.979, 3368…) against the table
   sources.
3. **Reference audit:** no undefined citations; no unused entries.
4. **Format audit:** 9-page main text; checklist included; anonymity (no author/affiliation
   strings anywhere in the PDF); line numbers on (submission mode, no `final`/`preprint` options).
5. **Anonymity audit:** search the compiled PDF text for `Neryva`, author names, and the real
   repo URL. The URL currently appears in **three** places — §4.3 of the main text
   (`03_experimental_setup.tex`), Appendix A, and `checklist.tex` — **all three** must be
   neutralized at submission time (see `09_open_decisions.md` D8).
6. Update `dev_docs/addressing_reviews/review_ledger.md`: close every `[ ]` box that this
   rewrite resolves; mark WI-14/WI-15 with their chosen status (09 §D2/D3).
   **Gate 9:** all audits pass; ledger reflects reality.

## Phase 10 — Hand-off

Produce a one-page change summary for the user: files changed, new data files, verification
results, remaining decisions. (Also serves as the future cover-letter skeleton.)
