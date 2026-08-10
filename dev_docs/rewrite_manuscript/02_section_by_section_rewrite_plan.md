# 02 — Section-by-Section Rewrite Plan

Reading-order edit instructions. Section numbers refer to the **revised** manuscript. For each
section: what stays, what changes, what is added (with pointers to draft content in
`03_technical_content_drafts.md` and numbers in `04_tables_figures_specs.md`).

Target section structure (revised):

```
1  Introduction
2  Related Work
3  Method
   3.1 Problem setup
   3.2 Canonical BPGS chart            (+ τ_T derivation)
   3.3 Split optimization objectives   (+ theta_grad_scale documentation, fixed-point note)
   3.4 Batch-conditional boundedness   (+ saturation paragraph)
   3.5 Uniform rescaling invariance    (NEW: Proposition 1 + proof)
4  Experimental Setup
   4.1 Benchmarks                      (+ new controlled studies)
   4.2 Compared methods and metrics    (+ Nash-MTL)
   4.3 Reporting protocol              (+ per-study seed reporting)
5  Results
   5.1 Robustness to loss-scale mismatch      (+ invariance ref, Kendall+L1 paragraph)
   5.2 Main NYUv2 benchmark                   (+ Nash-MTL row)
   5.3 Ablation on chart and initialization   (+ stop-gradient paragraph)
   5.4 Sensitivity to batch statistics and calibration  (NEW)
   5.5 Transfer to Yeast and RF1
   5.6 Computational overhead                 (NEW, short)
6  Discussion and Limitations         (rewrite)
```

---

## 0. Abstract (`sections/00_abstract.tex`)

**Keep:** the problem statement, BPGS definition, the rescaling numbers (0.777→0.778 vs 0.780→0.637),
NYUv2 depth numbers, Yeast micro-F1, the scoped RF1 sentence, the closing scope sentence.

**Change:**
1. Add the invariance property: *"The normalized BPGS task weights are provably invariant to
   uniform loss rescaling (Proposition 1), and we confirm this empirically."*
2. Add a compact non-triviality signal: *"an ablation shows that L1-normalizing Kendall's weights
   does not recover this robustness (−0.105 vs −0.004 scale sensitivity)."*
3. Add Nash-MTL to the NYUv2 sentence: *"...among the compared methods, including the recent
   Nash-MTL baseline."*
4. Optionally one clause on the sensitivity/overhead evidence if space allows (abstract has no
   hard word limit, but keep ≤ ~200 words).

**Draft** (target length ~190 words; final wording tuned during implementation):

> Multi-task learning often combines objectives with different numerical scales, which can
> destabilize uncertainty-based loss weighting. We propose Bounded Precision-Geometry Scaling
> (BPGS), a split uncertainty-weighting method that maps each task's latent uncertainty coordinate
> through a bounded sigmoid chart and, in its batch-aware form, expresses task log-variances in
> detached batch log-loss coordinates with first-batch calibration. The normalized BPGS weights are
> exactly invariant under uniform loss rescaling (Prop. 1); an ablation shows that L1-normalizing
> Kendall's weights does not recover this robustness, and that the split-optimization stop-gradient
> measurably stabilizes the learned uncertainty. Under pure post-hoc loss rescaling, BPGS keeps
> macro score nearly unchanged from ×1 to ×1000 (0.777 to 0.778), whereas Kendall-style uncertainty
> weighting drops from 0.780 to 0.637. On NYUv2, BPGS attains the best depth absolute relative
> error (0.223), the best depth RMSE (0.790), and the lowest total loss (1.891) among the compared
> methods, including the recent Nash-MTL baseline. Controlled diagnostics on NYUv2 show stability
> across batch sizes and first-batch choices, and overhead of +0.15% time and +0.87% memory
> relative to Kendall. On Yeast and RF1, BPGS remains competitive beyond synthetic stress settings,
> achieving the best Yeast micro-F1 (0.616) while remaining competitive, but not best, on RF1.
> These results support BPGS as a robust uncertainty-weighting method when loss-scale mismatch is
> a primary concern.

## 1. Introduction (`sections/01_introduction.tex`)

**Keep:** paragraphs 1–3 verbatim except small trims for space (see 07); the scoped question
sentence ("The question studied here is narrower…").

**Change the contribution list** (currently 4 bullets) → 5 bullets, tightened:

1. **Formulation** (keep, add "and its formal properties"): *We formulate BPGS as a bounded,
   batch-aware, split uncertainty-weighting method and prove that its normalized weights are
   exactly invariant to uniform loss rescaling.*
2. **Stress tests** (keep numbers; add one clause): *…whereas Kendall drops 0.780→0.637; a
   controlled ablation shows L1-normalization of Kendall's weights closes only part of this gap
   (−0.105 vs −0.004 scale sensitivity).*
3. **NYUv2** (keep numbers; add Nash-MTL): *…among the compared methods, including the recent
   Nash-MTL baseline; a NYUv2 ablation shows the batch-aware variants avoid the failure mode of the
   stateless auto-calibrated variant, and a stop-gradient ablation shows the split optimization
   does measurable work.*
4. **Controlled diagnostics** (new bullet, one line): *Ablations and sensitivity studies on
   NYUv2 confirm stability to batch size (4–16) and first-batch choice, and measure the
   computational overhead at +0.15% time / +0.87% memory.*
5. **Yeast/RF1** (keep, unchanged).

**Not allowed:** any sentence implying general-MTL superiority or promising Cityscapes.

## 2. Related Work (`sections/03_related_work.tex`)

**Keep:** the three paragraphs (uncertainty-weighting lineage; gradient-surgery/Pareto lineage;
scope statement). Small trims for space if needed.

**Add (in the Pareto paragraph, after Sener–Koltun):** one sentence on modern game-theoretic and
adaptive rules:

> More recent methods solve a per-step multi-objective subproblem, including Nash-MTL, which
> frames the update as a bargaining game over task gradients \cite{navon2022nash}, and other
> adaptive rules such as IMTL-G \cite{liu2021imtl} and FAMO \cite{liu2023famo}. These methods are
> not the closest conceptual predecessors to BPGS, but Nash-MTL provides a recent comparison point
> in our NYUv2 experiments.

Also add Auto-Lambda \cite{liu2022autolambda} either here or in the uncertainty-weighting
paragraph as the source of the Δ_M metric convention (Δ_M is attributed in setup to MTAN
\cite{liu2019mtan} already — optional; include the citation only if it is actually discussed).

**Do not:** claim CAGrad/IMTL-G/FAMO were evaluated.

**Fix an existing factual error:** the current last paragraph of `03_related_work.tex` says
"PCGrad and CAGrad are informative comparison baselines in our experiments" — CAGrad is
**not evaluated in any experiment** (verified against all benchmark descriptions in §4).
Reword to: *"PCGrad is a comparison baseline in our tabular experiments; CAGrad is closely
related to PCGrad but is not evaluated here."*

## 3. Method (`sections/02_method.tex`)

### Step 0 — verify the current reviewer state of the file before additions

**Current-state correction (2026-08-11 audit):** the working file already has the correct §3.3 →
§3.4 order, the split-objective lead-in, and `\operatorname{sg}[\alpha_i]` in $J_{\mathrm{net}}$.
Do not overwrite those sections with stale PDF text. Check for drafting debris, retain the
existing correct structure, and apply only the missing gradient-scale documentation,
detached-statistics notation, fixed-point-reference correction, saturation analysis, and new
invariance proposition described below.

Verified state 2026-08-11 (direct read of the working file + pdftotext of the compiled PDF):

1. **The working file is clean.** `sections/02_method.tex` (118 lines) has no drafting debris:
   the τ_1 note, the J_net/J_all note, and the boundedness scratchpad that existed earlier are
   gone. Nothing to purge.
2. **Structure is correct in both file and PDF.** §3.3 *Split optimization objectives* →
   §3.4 *Batch-conditional boundedness* (PDF order preserved); the split-objective lead-in
   ("BPGS uses separate objectives for the network parameters and the uncertainty
   coordinates…") is present; `\operatorname{sg}[\alpha_i]` is inside the J_net equation
   (Eq. 9); the "This matches the scalar uncertainty objective…" sentence is present. Do not
   re-edit these.
3. **No undefined reference exists.** Neither the PDF nor the working file contains
   `\ref{sec:ablation_sg}` or a "(see Section ??)" rendering. The earlier retarget
   instruction is obsolete.
4. **The compiled PDF is stale only in the empirical sections** (built 2026-05-07, before the
   WI-7 10-seed update): Table 5 and the §5.1 prose still carry the 3-seed caption/values
   ("Mean ± std over 3 seeds"; 0.529/0.495/0.486 at ×1000), while the current source has the
   10-seed values. The Method section in the PDF matches the working file; there is no hidden
   reviewer-visible text to restore.
5. **The g_θ = 100 documentation is NEW content** (present in neither the PDF nor the working
   file), sourced from the code, not the PDF: `theta_grad_scale: 100.0` in
   `configs/method/bpgs.yaml` (line 11), default `100.0` in `spectra/baselines/__init__.py`
   (line 40), applied as a 100× backward-gradient multiplier via `GradScale`
   (`spectra/core/bpgs.py`, per WI-4). Value verified; the wording below is a draft.

The correct boundedness claim (mathematically verified): with
$s_i \le s^{\max}_i$ and $s_j \ge s^{\min}_j$ for $j \neq i$, the normalized weight is at most
$\exp(-s^{\min}_i)/\left(\exp(-s^{\min}_i) + \sum_{j \neq i}\exp(-s^{\max}_j)\right)$.

### 3.1 Problem setup — **keep as-is** (minor trims OK).

### 3.2 Canonical BPGS chart — **add τ_T derivation** after Eq. (4)

Insert (draft in 03):

> **Choice of the latent radius.** The constant τ_T in Eq. (4) is not arbitrary. For a fixed batch,
> the standardized log-loss coordinates
> \begin{equation} \hat z_i = \frac{\log \widetilde L_i - \mu(L)}{\bar\varsigma(L)} \end{equation}
> satisfy \sum_i \hat z_i = 0 and \frac{1}{T}\sum_i \hat z_i^2 = 1 by construction. A
> Cauchy–Schwarz argument then gives the tight bound |\hat z_i| \le \sqrt{T-1}: setting one
> coordinate to magnitude M forces the remaining T−1 coordinates to sum to −M, whose sum of
> squares is minimized when they are equal, yielding M^2 \le T-1. The radius
> τ_T = \sqrt{T-1} + 0.1 therefore covers every coordinate that can actually arise from a
> standardized batch-loss vector; the +0.1 term is a small numerical margin that keeps the
> inverse-sigmoid calibration away from the exact boundary, where the map becomes numerically
> fragile.

Also: add the sg[·] notation to μ(L) and σ̄(L) where they enter the uncertainty objective
(Eq. 10) — **action, not verify-condition**: the AqnD response committed to "sg[] has been
added to the μ(L) and σ̄(L) definitions," but the current paper does not carry it (only the
prose "detached log-loss statistics" and `\operatorname{sg}[L_i]` in Eq. 10 exist).
`\operatorname{sg}[\alpha_i]` is already inside the J_net equation (Eq. 9) in both the
working file and the compiled PDF — no change needed there.

### 3.3 Split optimization objectives — **add two things**

**(a) theta_grad_scale documentation** (after the "matches the scalar uncertainty objective…"
sentence, which must be **reworded** — see (b)):

> In the implemented method the uncertainty objective is optimized with a gradient scale of
> g_θ = 100 on the θ update, constant across all experiments and code paths; this compensates for
> the smaller gradient magnitudes of the uncertainty objective relative to the network objective
> and does not affect the weighting rule itself (the invariance property of §3.5 holds for any
> positive g_θ). Full hyperparameter details are given in Appendix A.

**(b) Fixed-point paragraph — NEW content** (verified 2026-08-11: the paragraph exists in
neither the working file nor the compiled PDF; the old "This matches the scalar uncertainty
objective… but changes the chart" sentence is still present in the working file and should be
replaced). Add the paragraph below (draft in 03 §3), which supersedes that sentence; it
references `sec:norm_ablation` directly (no retarget needed — no undefined reference exists):

> Equation (10) has the same algebraic form as the scalar uncertainty objective of classical
> homoscedastic uncertainty weighting \cite{kendall2018}, but it is not the same optimization
> problem: Kendall's log-variance is unconstrained, so its optimum is reachable for any loss
> scale, whereas BPGS's log-variance s_i is confined to a batch-conditional interval, so its
> fixed point — when it exists — lies inside that interval by construction. The fixed-point
> structures therefore differ even though the objective forms coincide;
> Section~\ref{sec:norm_ablation} shows empirically that this distinction matters.

### 3.4 Batch-conditional boundedness — **add saturation paragraph** at the end

Insert (draft in 03) — acknowledges AqnD's learnability objection with quantified margins from
WI-5. Full numbers in appendix G table.

### 3.5 Uniform rescaling invariance — **NEW subsection**

Proposition 1 + proof (draft in 03), plus a framing sentence that connects it to the design
(batch-conditioning exists precisely so that this invariance holds) and a scope note (normalized
weights; clamps inactive; does not claim optimizer-level invariance). One sentence pointing to
Table 1 as empirical confirmation (reframes TA-1: the table becomes confirmation, not discovery).

## 4. Experimental Setup (`sections/03_experimental_setup.tex`)

### 4.1 Benchmarks — **add two blocks**

**(a) Controlled NYUv2 diagnostics** (after the existing ablation paragraph):

> Four further controlled studies use the same 50% training subset. (i) A stop-gradient
> ablation compares canonical BPGS against a variant with a coupled (non-detached) uncertainty
> gradient, 3 seeds × 60 epochs. (ii) A batch-size study trains canonical BPGS at batch sizes
> 4, 8, and 16 (3 seeds each, 60 epochs). (iii) A first-batch study varies only the loader seed
> (1001/2001/3001) with fixed model seed, 60 epochs. A computational-overhead study measures
> per-epoch wall-clock time and peak GPU memory of BPGS vs. Kendall on the same subset
> (3 seeds, 60 epochs, single GPU).

**(b) Normalization ablation** (after the synthetic studies paragraph):

> To test whether the robustness of BPGS reduces to L1-normalization of Kendall's weights, we run
> a normalization ablation on the pure loss-rescaling grid (×1/×10/×100/×1000) comparing BPGS,
> Kendall, and Kendall with L1-normalized weights, 3 seeds per setting. The final target seed set
> is 42/43/44; if the adopted rerun is unavailable, the existing 42/123/999 artifact must be
> labeled explicitly rather than silently presented as seed-matched to the main rescaling table.

### 4.2 Compared methods and metrics — **add Nash-MTL**

- Add to the NYUv2 main sentence: *The main NYUv2 benchmark compares BPGS against Static, Kendall,
  UWSO, and Nash-MTL \cite{navon2022nash} (120 epochs, same protocol; implementation details in
  Appendix A).*
- Add to the metrics list: Δ_M already there; no metric change.

### 4.3 Reporting protocol — **update seed reporting**

- Keep the 10-seed scale-stress sentence.
- **Add the gradient-scale sentence** (new; present in neither the PDF nor the working file;
  value verified in code/config: `theta_grad_scale=100.0`, see Step 0 item 5): *"Furthermore,
  the uncertainty weights are explicit functions of θ, so the uncertainty objective (Eq. 10)
  includes a gradient scale g_θ = 100 on the uncertainty update, and the network objective does
  not see it."*
- Add: *For the new controlled studies (stop-gradient, batch size, first-batch, overhead,
  normalization ablation), mean ± std over three seeds is reported as in the main tables; the
  synthetic normalization ablation uses the seed set noted in its table caption.*
- Keep the final-epoch extraction rule and the val/total_loss vs val/miou explanation (already
  present; add one sentence: *These choices are documented in Appendix A alongside the gradient
  scale g_θ = 100 and clipping values, so the equations in §3 correspond exactly to the released
  optimizer*).

## 5. Results (`sections/04_results.tex`)

### 5.1 Robustness to loss-scale mismatch — **add two insertions**

**(a) Invariance reference** (first paragraph, after the rescaling numbers):

> This near-invariance is not only an empirical finding: Proposition 1 shows the normalized BPGS
> weights are exactly invariant to uniform rescaling when the numerical safeguards are inactive,
> so the table should be read as confirming the algebraic property rather than as an isolated
> observation.

**(b) Normalization ablation paragraph** (new paragraph after the scale-stress paragraph):

> A natural alternative hypothesis is that the robustness of BPGS comes from L1-normalizing the
> weights rather than from the bounded chart or the split optimization. We tested this directly
> by adding an L1-normalized Kendall variant to the rescaling grid (Appendix Table X). Kendall+L1
> is better than plain Kendall at ×1000 (0.689 vs. 0.658) but still degrades by −0.105 from ×1 to
> ×1000, whereas BPGS degrades by −0.004. Normalization therefore contributes but does not
> reproduce BPGS behavior, and §5.3 shows the split optimization adds an independent stabilizing
> effect.

### 5.2 Main NYUv2 benchmark — **add Nash-MTL**

- Table: add Nash-MTL row (numbers in 04, `T-nyuv2`).
- Text (after the "Relative to the strongest competing values…" paragraph):

> Nash-MTL \cite{navon2022nash}, the most recent baseline, trails every other method on five of
> the six reported metrics and shows the largest seed variance (mIoU spans 0.228–0.289); its
> within-11.25° accuracy (0.211) is the only exception, edging Static (0.169). This is
> consistent with the batch-to-batch variation of its per-step game-theoretic weights observed
> in our runs (Appendix C), and with the view that per-step gradient-game solvers occupy a
> different operating point from scalar uncertainty weighting.
> (Checked against `tab:nyuv2_main` + the Nash-MTL row: "worse than every other method on
> every metric" would be FALSE — Within 11.25°: Nash-MTL 0.211 > Static 0.169.)

### 5.3 Ablation on chart and initialization — **add stop-gradient paragraph**

After the existing ablation analysis paragraph:

> A separate ablation isolates the split-optimization stop-gradient while holding the bounded,
> batch-aware chart fixed (Appendix Table X, Appendix Figure X). Removing the stop-gradient leaves
> most validation metrics comparable, but changes the learned uncertainty dynamics qualitatively:
> θ_max grows +28% over training (3.11 → 3.99) instead of decaying and settling (3.08 → 2.44),
> its seed-to-seed standard deviation increases 14× (0.192 vs. 0.014), and segmentation mIoU drops
> 4.3% (0.198 → 0.190). The stop-gradient is therefore an active design component, and the
> two-objective split is not an implementation detail.

### 5.4 Sensitivity to batch statistics and calibration — **NEW subsection** (short)

Two paragraphs (drafts in 03) covering:
- batch-size study: across-bs CV < 3.5% on all validation metrics (most < 1.2%); θ_max shifts
  modestly 2.40 (bs=4) → 2.59 (bs=16); no retuning across a 4× range (Appendix Table E1, Figure E1).
- first-batch study: CV < 2% across loader seeds (most < 0.6%); θ_max trajectories converge within
  0.3% of each other (Appendix Table E2, Figure E2).

One sentence ties both: the batch-conditional design does not create a meaningful dependency on
batch statistics within the tested ranges.

### 5.5 Transfer to Yeast and RF1 — **keep as-is** (already correct).

### 5.6 Computational overhead — **NEW subsection** (short, 3–4 sentences)

> The batch-statistics computation and the separate uncertainty pass add negligible cost.
> Measured on the NYUv2 50% subset (3 seeds, 60 epochs, single GPU), per-epoch wall-clock time
> increases by +0.15% (40.979 s vs. 40.916 s for Kendall) and peak GPU memory by +0.87%
> (3368 MB vs. 3339 MB); BPGS adds only T = 3 scalar parameters to the 18.9M-parameter network
> (Appendix Table F1).

## 6. Discussion and Limitations (`sections/05_discussion_limitations.tex`) — **rewrite**

**Structure (keep the opening paragraph, then rewrite the limits list):**

1. **Opening paragraph** — keep, add one sentence: *The invariance Proposition 1 and the
   normalization/stop-gradient ablations together place the contribution as a principled fix to a
   specific failure mode of uncertainty weighting, not a general optimizer.*
2. **Limits list (numbered):**
   1. *Benchmark coverage.* One dense-prediction benchmark, two tabular problems, synthetic
      studies. A second dense-prediction benchmark (e.g., Cityscapes) is planned future work;
      results are not yet available. (WI-15, honest)
   2. *Statistical strength.* Most headline results use three seeds; the synthetic scale-stress
      uses ten. We do not claim fine-grained ranking significance; gaps are reported as means ± SD.
   3. *Mixed-stress regimes.* In the noisy and conflict regimes BPGS trails Kendall and PCGrad
      (macro score 0.641 vs. 0.659, 0.652 vs. 0.664). BPGS stabilizes scalar weights but does not
      modify gradients; methods that act on gradient directions have a structural advantage when
      the problem is conflict-dominated. Combining BPGS with conflict-aware methods (e.g., PCGrad,
      CAGrad) is a natural future direction that we did not yet test. (WI-14 resolution)
   4. *Saturation risk.* Boundedness does not by itself guarantee learnability at the boundary;
      if a task's log-loss lay outside the bounded interval for long enough, the sigmoid gradient
      factor would decay and recovery would be difficult. Across all logged main-paper runs the
       coordinate stays inside the boundary (max |z_i|/τ_T = 0.93 at the initialization epoch;
       final-epoch caps: ≤ 0.84 on NYUv2, ≤ 0.69 on Yeast, ≤ 0.89 on RF1), but this is an
       empirical margin, not a guarantee. (AqnD-C1/C2)
   5. *Batch-statistics dependence.* Behavior is verified for batch sizes 4–16 and for the tested
      noise regimes; behavior outside these ranges is untested.
   6. *No convergence guarantees.* The formal results are the batch-conditional boundedness and
      the uniform-rescaling invariance; we do not claim global convergence properties for the
      split objective.
   7. *Baseline coverage.* Nash-MTL is evaluated; CAGrad, IMTL-G, FAMO, and Auto-Lambda are not
      yet evaluated and are future work. Their absence bounds the comparison set, and we do not
      interpret the current results as showing superiority over them.
3. **Societal impact paragraph** — keep as-is.

**Remove from the old limitations:** the "no dedicated runtime study" item (now measured, §5.6)
and the generic batch-size item (now studied, §5.4) — replaced by items 4/5 above.

---

## Appendices (details in 05_appendix_restructure.md)

- **A Reproducibility details** — add: g_θ=100 with rationale; Nash-MTL protocol (120 epochs,
  lr 5e-4, wd 1e-4, warmup 100, cosine to 1e-6, grad_clip 1.0, mixed precision, batch 8);
  the four new controlled studies' exact configs; the explicit reconciliation sentence; keep
  existing content.
- **B Additional stress results** — add: normalization ablation table (T-norm); keep existing.
- **C Ablation and NYUv2 figures** — add: stop-gradient θ_max figure (F-sg); Nash-MTL alpha
  variance note (optional, one sentence); keep existing.
- **D Real-data figures** — unchanged.
- **E Sensitivity analyses** — NEW: batch-size table + θ_max figure; first-batch table + θ_max
  figure.
- **F Computational overhead** — NEW: runtime/memory table.
- **G Bounded-chart behavior** — NEW: saturation table (|z_i|/τ_T ratios, derivative factors).
- **Checklist** — after `\clearpage`, unchanged content.

---

## Label checklist (add these to the manuscript; Phase 9 greps for undefined refs)

- `eq:tau` — the τ_T equation (Eq. 4) — required by draft 03 §1's `\eqref{eq:tau}`
- `eq:unc` — the J_unc equation (Eq. 10) — required by draft 03 §3
- `sec:invariance` — §3.5 (Proposition 1 subsection)
- `sec:boundedness` — §3.4 (batch-conditional boundedness) — required by draft 03 §3
- `sec:norm_ablation` — §5.1(b) normalization-ablation paragraph — required by the retargeted
  fixed-point reference and draft 03 §3
- `sec:ablation_sg` — §5.3 stop-gradient paragraph — required by draft 03 §6
- `sec:limitations` — §6 Discussion — required by draft 03 §4
- `prop:invariance` — Proposition 1 (draft 03 §5)
- `app:reproducibility`, `app:norm_ablation`, `app:weight_variance`, `app:sensitivity`,
  `app:overhead`, `app:chart_behavior` — appendix labels (05 §2)
- `tab:norm_ablation`, `tab:stop_gradient`, `tab:batch_size`, `tab:first_batch`,
  `tab:overhead`, `tab:saturation` — new tables (04)
- `fig:stop_gradient_theta`, `fig:batch_size_theta`, `fig:first_batch_theta` — new figures (04 §8)
