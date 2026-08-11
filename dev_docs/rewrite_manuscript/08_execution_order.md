# 08 — Execution Order & Verification Gates

Implementation is staged so that **data and scripts come first** (every table/figures regenerated
from sources), **then prose**, then **appendices**, with a **build + audit** at each gate.
Each phase is independently verifiable; do not skip gates.

> Pre-requisite: the resolved D1 normalization-ablation rerun (or its explicitly documented
> fallback) and the remaining implementation choices in `09_open_decisions.md`. Phase 1 must
> use the actual artifact paths recorded in `04_tables_figures_specs.md`.

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
   **Gate 1:** all 7 new/updated tables + 3 figures exist at their target paths and pass the
   acceptance check.

## Phase 2 — References (0.3 h)

1. Add the 4 bib entries (`06_references_update.md`); verify page numbers via web if unsure.
2. Insert the related-work sentence (draft in `06` §3).
3. **Gate 2:** `bibtex` clean (no undefined-citation warnings); every new `\cite` resolves.

## Phase 3 — Method section (`sections/02_method.tex`)

**Current-state audit note:** the working file already has the correct subsection order,
split-objective lead-in, and `\operatorname{sg}[\alpha_i]`. Verify the file before acting on the
historical Step 0 description below; do not purge or replace correct content.

**Step 0 — verify the file, do not restore (see 02 §3 Step 0):** verified 2026-08-11 — the
working file is clean and structurally correct (right §3.3/§3.4 order, split-objective
lead-in, `\operatorname{sg}[\alpha_i]` in Eq. 9, no scratch, no undefined references). No
purge and no restore-from-PDF is needed; the compiled PDF matches the Method section and is
stale only on the empirical sections (3-seed Table 5/§5.1 vs 10-seed source). All Method work
below is **new** content: grad-scale sentences (§3.3 prose + §4.3; value verified
`theta_grad_scale=100.0` in code/config), fixed-point paragraph (§3.3, draft in 03 §3), the
sg[·] action on μ(L)/σ̄(L) in Eq. 10, τ_T derivation, saturation paragraph, Proposition 1.

Apply in file order (drafts in `03_technical_content_drafts.md`):
1. τ_T derivation after Eq. (4); add `\operatorname{sg}` to μ/σ̄ where they enter Eq. (10).
2. Grad-scale note in §3.3 (new sentence — see note in 03 §2).
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

---

## Phase 11 — Post-rewrite review (2026-08-11, DONE)

Full review of the completed manuscript against the raw runs. Everything below was verified
against the compiled PDF (`build/main.pdf`, 26 pages: 9 main + 1 references + 10 appendix +
6 checklist) and the raw artifacts; the build was then re-run clean.

### Blocking issues found and fixed (build was silently truncated before the fix)

1. **`main.tex`: `\usepackage{amsthm}` missing.** `\begin{proof}` in §2.4 raised
   "Environment proof undefined"; `\end{proof}` consumed `\end{document}`, so everything after
   the proof (results, discussion, all appendices, checklist) was silently missing from the
   PDF while `build.ps1` still reported success (it only checks PDF existence). Fix applied;
   rebuild clean.
2. **Table 5 (`scale_stress_scale_table.tex`): ×10 bold on Kendall** (0.607) while BPGS
   (0.616) is highest — bold moved to BPGS; also verified the raw 10-seed means
   (BPGS 0.6159 > Kendall 0.6071) and that the printed stds equal numpy ddof=0 aggregation
   (e.g. ×1000 BPGS 0.0340 → 0.032).
3. **Caption debris `(02)/(06)/(07)`** (internal spec markers) removed from the three stress
   table captions; captions normalized. The generator
   `analysis/studies/stress/table.py` still emits these markers and hardcodes
   "over 3 seeds" — must be fixed so regeneration does not reintroduce them (scale table is
   now "over 10 seeds").

### Verified correct (no action needed)

- All §5.1–§5.6 prose numbers match the tables and the raw runs (rescaling 3-seed table;
  scale-stress 10-seed table; degradation 27.0/32.3/28.5%; gap 0.043 / 1.07 combined SD;
  NYUv2 0.223/0.790/1.891/0.078/Δ_M ≈ −0.038; ablation; sensitivity; Yeast 0.436/0.616/0.773;
  RF1 −0.429/30.158/23.548; overhead 40.979/40.916, 3368/3339 MB, +0.15%/+0.87%;
  saturation 0.93/0.84/0.69/0.89/0.033/0.074; heterogeneous worst-task clean 0.301, UWSO 0).
- Every `\ref`/`\eqref` resolves (no undefined refs in the log); bibtex clean; all 15 cited
  keys present in `references.bib`; no URLs in the paper; anonymization clean
  (no `Neryva`, no `github`, no personal strings in the PDF text layer).
- Submission-mode formatting is active and correct: anonymous title block, line numbers in
  the margin, "Submitted to NeurIPS 2026. Do not distribute." — these come from the official
  `neurips_2026.sty` and are expected.
- Checklist: all 16 items answered honestly; no `\answerTODO` left; section references correct.
- Layout: main text exactly 9 pages; references page 10; appendices 11–19; checklist 20–26.
- Data provenance: 10-seed scale-stress runs exist (seeds 42–51 under
  `experiment_results/02_synthetic_scale_stress/{x1,x10,x100,x1000}/`); norm-ablation runs
  exist (`experiment_results/exp_09_kendall_norm_ablation/20260724_*`); D1 fallback fully
  labeled (see 09); D8 paper-side complete (see 09).
- `02_method.tex` (169 lines): τ_T derivation, sg[·] in μ/σ̄, split objectives with
  `\operatorname{sg}[\alpha_i]`, fixed-point paragraph, saturation paragraph, Proposition 1
  + proof — all present and clean (the mid-edit debris the review caught earlier is gone).

### Remaining items (all optional except #1/#2)

1. **Harden `build.ps1`**: fail when `main.log` contains a LaTeX error (`^!` or
   "LaTeX Error"). Today the build "succeeded" on a truncated PDF.
2. **Fix the table generator** (`analysis/studies/stress/table.py`): drop the `(02)/(06)/(07)`
   markers and make the seed-count string a parameter ("over 10 seeds" for scale).
3. **Create the missing study packages** (Phase 1 item 2, not yet done): `studies/
   norm_ablation/`, `studies/sensitivity/`, `studies/saturation/` generator code so every
   paper table is regenerable from raw runs.
4. **θ_max figures** (04 §8): not referenced by the paper — either generate and add to
   Appendix E, or declare dropped. Paper is self-consistent as-is.
5. **`.gitignore`**: add `working/paper/build/` (build artifacts are currently tracked).
6. **Anonymized archive** for submission (09 D8): fresh orphan branch/new repo; excludes the
   real URL in `docs/getting_started.md`.
7. Cosmetic (optional): the anonymous title block shows the template's placeholder lines
   ("Affiliation / Address / email") — standard template behavior; leave as-is unless the
   venue guidance says otherwise.
