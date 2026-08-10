# 05 — Appendix Restructure (WI-18 resolution + new content placement)

Resolves AqnD-19, MKod-8, WI-18. Current state (measured from compiled PDF): appendix content and
the NeurIPS checklist are interleaved on pages 9–10; figures from appendices B/C/D float into the
checklist region.

## 1. Target appendix structure

```
\appendix
\input{appendix/A_reproducibility_details}      (extended)
\input{appendix/B_additional_stress_results}    (+ normalization ablation)
\input{appendix/C_ablation_and_nyuv2_figures}   (+ Nash-MTL note)
\input{appendix/D_real_data_figures}            (unchanged)
\input{appendix/E_sensitivity_analyses}         (NEW)
\input{appendix/F_computational_overhead}       (NEW)
\input{appendix/G_bounded_chart_behavior}       (NEW: saturation)
\clearpage
\input{./checklist.tex}                         (alone on its own pages)
```

In `main.tex`:
```latex
\appendix
\input{appendix/A_reproducibility_details}
\input{appendix/B_additional_stress_results}
\input{appendix/C_ablation_and_nyuv2_figures}
\input{appendix/D_real_data_figures}
\input{appendix/E_sensitivity_analyses}
\input{appendix/F_computational_overhead}
\input{appendix/G_bounded_chart_behavior}
\clearpage
\input{./checklist.tex}
```

## 2. Per-appendix changes

### A — Reproducibility details (extend)
Keep all current paragraphs. Add:

1. **Optimizer fidelity note** (leads the section, answers AqnD-1/2/3/13 directly):
   > The released implementation matches the equations in §3 as follows: batch statistics
   > μ(L) and σ̄(L) are detached from the computation graph; the uncertainty update uses a
   > gradient scale g_θ = 100.0 on the θ-parameters, constant across all code paths
   > (`configs/method/bpgs.yaml`, `configs/empirical/bpgs/default.yaml`, and the baseline
   > registry); network training uses the detached normalized weights α_i. Gradient clipping is
   > 10.0 for all BPGS configurations and 1.0 for the Kendall ablation baseline (matching each
   > method's own configuration).
2. **Nash-MTL protocol**: 120 epochs, batch 8, AdamW lr 5e-4, wd 1e-4, linear warmup 100 steps,
   cosine decay to 1e-6, mixed precision, grad_clip 1.0; per-step Nash fixed-point solve on the
   gradient Gram matrix (G^T G)α = c/α; seeds 42/43/44.
3. **Controlled study configs** (bulleted, one line each):
   - Stop-gradient ablation: 50% subset, 60 epochs, canonical vs coupled variant, seeds 42/43/44.
   - Batch-size study: 50% subset, bs ∈ {4, 8, 16}, seeds 42/43/44.
   - First-batch study: 50% subset, loader seeds 1001/2001/3001, model seed 42.
   - Overhead study: 50% subset, 60 epochs, BPGS vs Kendall, seeds 42/43/44, single GPU;
     per-epoch wall-clock and peak CUDA memory logged.
   - Normalization ablation: pure-rescaling grid ×1/×10/×100/×1000, BPGS vs Kendall vs
     Kendall+L1, 3 seeds (seed set per decision 09).
4. **NYUv2 selection-metric note** (already present; keep): final benchmark runs use
   `val/miou` (max); ablation and controlled studies use dataset default `val/total_loss` (min).

### B — Additional stress results (extend)
- Add: normalization ablation table (`\input{data/norm_ablation/tables/norm_ablation_table}`)
  with one sentence of commentary.
- Optional: normalization ablation figure (F-norm) if space allows after the other figures.
- Keep all existing tables/figures.

### C — Ablation and NYUv2 figures (extend)
- Add one-sentence note on Nash-MTL per-step weight variance (from WI-9: α moves between
  near-uniform, near-one-hot, and equal-split configurations across batches; consistent across
  seeds). No figure needed (space).
- Keep all existing figures.

### D — Real-data figures (unchanged)

### E — Sensitivity analyses (NEW)
```
\section{Sensitivity Analyses}
\input{data/stop_gradient/tables/stop_gradient_table}
\input{data/batch_size/tables/batch_size_table}
\input{data/first_batch/tables/first_batch_table}
\begin{figure*}[t] ... stop_gradient_theta_max.pdf ... \end{figure*}
\begin{figure*}[t] ... batch_size_theta_max.pdf ... \end{figure*}
\begin{figure*}[t] ... first_batch_theta_max.pdf ... \end{figure*}
```
Order: stop-gradient (design ablation), batch size, first-batch calibration. Figures show
θ_max vs epoch with mean ± SD shading.

### F — Computational overhead (NEW)
```
\section{Computational Overhead}
\input{data/overhead/tables/overhead_table}
```
Plus one paragraph: hardware (single GPU, type), what was measured, and the interpretation
(+0.15% time / +0.87% memory; 3 extra parameters vs 18.9M shared).

### G — Bounded-chart behavior (NEW: saturation analysis)
```
\section{Bounded-Chart Behavior and Saturation}
\input{data/saturation/tables/saturation_table}
```
Plus one paragraph: reconstruction method (z_i = (s_i − μ)/σ̄ from logged
`batch_mu`, `batch_sigma`, `log_var_i`, `theta_i`), the derivative-factor computation, and the
conclusion (no boundary contact; worst point at epoch 0; all trajectories move inward).

### Checklist
- Preceded by `\clearpage` so it starts on a fresh page and never interleaves with figures.
- Content unchanged.

## 3. Figure float discipline (prevents recurrence)

The interleaving happened because `figure*` floats from the appendices drift forward into the
checklist. Mitigations:
1. `\clearpage` before the checklist (required).
2. Keep `figure*` captions self-contained (they already are).
3. If floats still cross the boundary, add `\usepackage{placeins}` and `\FloatBarrier` before
   the checklist (last resort; note in `07_page_budget` if needed).

## 4. Page-9 unused space (MKod-8)

The current page-9 whitespace was called out by MKod. With the restructure, that space is
naturally consumed by the new appendix E/F/G content. Do **not** add filler; verify visually
after build that no large blank stretches remain at appendix boundaries.

## 5. Verification checklist for this item

- [ ] Checklist starts on a fresh page, no figure/table above it.
- [ ] All appendix sections render in order A → G.
- [ ] Every new table/figure label resolves (no `??`).
- [ ] pdftotext page scan: "NeurIPS Paper Checklist" is the last marker, preceded only by
      appendix G content on the previous page.
- [ ] No overfull `\hbox` warnings introduced by the new tables (check build log).
