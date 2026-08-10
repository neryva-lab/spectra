# 03 — Technical Content Drafts (LaTeX-ready)

Full drafts for the new formal and technical content. These are written to be dropped into the
manuscript with minimal editing; each block states its insertion point. All numbers are
cross-checked against `dev_docs/addressing_reviews/review_task_completed/*` reports and the
experiment outputs (see `04_tables_figures_specs.md` for source files).

---

## 1. τ_T derivation — insert in §3.2 (Canonical BPGS chart), right after Eq. (4)

```latex
The constant $\tau_T$ in Eq.~\eqref{eq:tau} is not arbitrary. For a fixed batch, the
standardized log-loss coordinates
\begin{equation}
\hat z_i \;=\; \frac{\log \widetilde L_i - \mu(L)}{\bar\varsigma(L)}
\end{equation}
satisfy $\sum_{i=1}^{T}\hat z_i = 0$ and $\frac{1}{T}\sum_{i=1}^{T}\hat z_i^2 = 1$
by construction, whenever the numerical clamps are inactive. These two constraints bound every
coordinate: if one coordinate has magnitude $M$, the remaining $T-1$ coordinates must sum to $-M$,
and their sum of squares is minimized when they are equal, giving
$\sum_i \hat z_i^2 \ge M^2 + (T-1)\left(\frac{M}{T-1}\right)^2 = M^2 \frac{T}{T-1}$.
Together with $\sum_i \hat z_i^2 = T$ this yields $M \le \sqrt{T-1}$, and the bound is tight
(achieved when one coordinate is at the bound and the others are equal). The radius
$\tau_T = \sqrt{T-1} + 0.1$ therefore covers every coordinate that can arise from a
population-standardized batch-loss vector; the $+0.1$ term is a small numerical margin that keeps
the inverse-sigmoid calibration away from the exact boundary, where the map becomes numerically
fragile.
```

**Verification notes:**
- Uses the population standard deviation convention (matches code: `std(unbiased=False)`).
- The bound argument is Cauchy–Schwarz/AM-style minimization, stated self-contained.
- Do **not** claim the +0.1 term is derived; it is a safety margin (WI-6 instruction).

---

## 2. theta_grad_scale documentation — insert in §3.3 (Split optimization objectives), after Eq. (10)

```latex
In the implemented method, the uncertainty objective is optimized with a fixed gradient scale
$g_\theta = 100$ on the $\theta$-update, used identically across all experiments and code paths.
This compensates for the fact that the uncertainty objective produces gradients that are smaller
in magnitude than those of the network objective. The scale does not change the weighting rule
itself: Proposition~\ref{prop:invariance} holds for any positive $g_\theta$. All optimizer
settings, including $g_\theta$, the gradient-clipping values, and the validation selection rule
per experiment, are listed in Appendix~\ref{app:reproducibility}.
```

**Why it exists (rationale sentence, optional):** the uncertainty objective is a sum of
per-task scalar terms while the network objective aggregates full-batch gradients through a
deep network; without compensation the θ update would be orders of magnitude slower than the
network update, and the calibration would effectively freeze.

**Restoration note (verified 2026-08-11):** the compiled PDF already carries grad-scale
sentences in the §3.3 prose ("an explicit scale $g_\theta=100$ on the update") and §4.3
("the uncertainty objective (Eq.~10) includes a gradient scale $g_\theta = 100$ on the
uncertainty update, and the network objective does not see it"); the working tex has lost
both. Restore them merged with this block (one mention per section — no third mention).

---

## 3. Reworded Eq. (10) comment — replaces the current sentence in §3.3

**State check (2026-08-11):** the current paper no longer contains the old sentence below —
the split-interpretation and fixed-point paragraphs are already present (in the compiled PDF
and the working file). Treat this block as the reference wording to verify against; apply it
only if an older sentence survives. The remaining mandatory action is retargeting the
fixed-point paragraph's closing reference from the undefined `sec:ablation_sg` to
`\ref{sec:norm_ablation}` (see 02 §3.3b).

Replace:
> This matches the scalar uncertainty objective used by classical homoscedastic uncertainty
> weighting \cite{kendall2018}, but changes the chart from the learnable coordinate $\theta_i$ to
> the task log-variance $s_i$.

With:
```latex
Eq.~\eqref{eq:unc} has the same algebraic form as the scalar uncertainty objective of classical
homoscedastic uncertainty weighting \cite{kendall2018}, but it is not the same optimization
problem. Kendall's log-variance is unconstrained, so its optimum is reachable at any loss scale;
BPGS confines $s_i$ to a batch-conditional interval (Section~\ref{sec:boundedness}), so its fixed
point --- when it exists --- lies inside that interval by construction. The fixed-point structures
therefore differ even though the objective forms coincide, and Section~\ref{sec:norm_ablation}
shows empirically that this distinction matters.
```

---

## 4. Saturation paragraph — append to §3.4 (Batch-conditional boundedness)

```latex
Boundedness of $s_i$ does not by itself guarantee that $\theta_i$ remains learnable near the
boundary: the sigmoid derivative $\sigma(\theta_i)(1-\sigma(\theta_i))$ vanishes as
$z_i \to \pm\tau_T$, so a task whose log-loss sat outside the bounded interval for a long time
would receive a vanishingly small gradient and would be difficult to recover. We therefore
checked the logged training trajectories on all three datasets (Appendix~\ref{app:chart_behavior}).
The maximum observed coordinate is $|z_i|/\tau_T = 0.93$ (NYUv2, epoch 0, seed 43, task 2), with
lower maxima on Yeast ($0.70$) and RF1 ($0.89$); every trajectory moves inward from its
initialization, reaching final-epoch ratios of $\le 0.84$ (NYUv2), $\le 0.69$ (Yeast), and
$\le 0.89$ (RF1). At the worst observed point the derivative factor is
$\sigma(\theta)(1-\sigma(\theta)) \approx 0.033$ --- about 13\% of its peak value $0.25$ --- and
it rises to $\approx 0.074$ (about 30\% of peak) by the final epochs. Saturation is therefore a
theoretical risk that did not materialize in any logged run; we discuss the residual risk in
Section~\ref{sec:limitations}.
```

**Cross-check (wi-5, response AqnD #4):** ratios 0.9327 / 0.7017 / 0.8937; final-epoch caps
0.84 / 0.69 / 0.89; derivative factor at worst point ≈ 0.033 (13%), final ≈ 0.074 (30%).
All consistent.

---

## 5. Proposition 1: Uniform rescaling invariance — NEW §3.5 (after §3.4)

```latex
\subsection{Uniform rescaling invariance}
\label{sec:invariance}
The batch-aware construction is designed so that the normalized weights are insensitive to the
absolute scale of the losses. This is a formal property, not an empirical accident.

\begin{proposition}[Uniform rescaling invariance]
\label{prop:invariance}
Let all task losses be rescaled by a common positive factor, $L'_i = c L_i$ for $c > 0$, and
assume the numerical clamps $\varepsilon_{\log}$ and $\varepsilon_{\mathrm{std}}$ are inactive on
both $L$ and $L'$. Then the normalized BPGS weights are unchanged:
\[
\alpha_i(\theta_i; L') = \alpha_i(\theta_i; L) \qquad \text{for all } i.
\]
If first-batch auto-calibration is used, the initialized coordinates $\theta_i$ are also
unchanged under the same rescaling of the calibration batch.
\end{proposition}

\begin{proof}
With the clamps inactive, $\log \widetilde L'_i = \log c + \log \widetilde L_i$, so
$\mu(L') = \mu(L) + \log c$. The centered deviations are unchanged by this additive shift, so
$\bar\varsigma(L') = \bar\varsigma(L)$. The latent coordinate $z_i(\theta_i)$ depends only on
$\theta_i$, hence is unchanged. The log-variance therefore shifts uniformly,
$s_i(\theta_i; L') = s_i(\theta_i; L) + \log c$, the raw precision rescales as
$\omega_i(L') = e^{-s_i(L')} = \omega_i(L)/c$, and the common factor $1/c$ cancels in the
L1-normalization, giving $\alpha_i(L') = \alpha_i(L)$. For the auto-calibration path, the
standardized coordinates $(\log \widetilde L_i - \mu(L))/\bar\varsigma(L)$ are invariant under
the additive shift, so the initial $\theta_i$ values computed from the first batch are unchanged.
\end{proof}

Two scope remarks are important. First, the invariant quantity is the \emph{normalized} weight
vector; the raw precisions scale by $1/c$, which is exactly the mechanism that makes the
normalized weights invariant. Second, the property is algebraic and holds per batch; it does not
claim that the optimizer trajectory, learning-rate effects, or downstream metrics are invariant
(Table~\ref{tab:stress_rescaling} confirms that the invariance propagates to the final predictions
in the pure-rescaling study).
```

**Placement/format notes:**
- Requires `\newtheorem{proposition}{Proposition}` (add to preamble). Numbering decision is
  resolved in 09 D4: standalone proposition counter (Option A); the shared equation counter
  (`[equation]`) is the fallback.
- If a `proposition` environment is undesirable, format as **Proposition 1** (bold run-in)
  followed by a proof paragraph — but a numbered environment is cleaner and reads more formal.
- Keep the proof compact (the above is ~120 words of math prose).

---

## 6. Normalization-ablation paragraph — insert in §5.1 (Results)

```latex
A natural alternative hypothesis is that BPGS inherits its robustness from L1-normalizing the
weights rather than from the bounded chart or the split optimization. We tested this directly by
adding an L1-normalized Kendall variant to the pure-rescaling grid
(Appendix~\ref{app:norm_ablation}). Kendall+L1 improves over plain Kendall at the largest factor
(0.689 vs.\ 0.658 at $\times1000$) but still degrades by $-0.105$ from $\times1$ to $\times1000$,
whereas BPGS degrades by only $-0.004$. L1-normalization therefore contributes, but it does not
reproduce BPGS behavior; combined with the stop-gradient ablation of
Section~\ref{sec:ablation_sg}, this shows that both the bounded chart and the split optimization
do work beyond normalization.
```

---

## 7. Stop-gradient paragraph — insert in §5.3 (Results, ablation subsection)

```latex
A separate ablation isolates the split-optimization stop-gradient while holding the bounded,
batch-aware chart and the initialization rule fixed (Appendix~\ref{app:sensitivity},
Table~\ref{tab:stop_gradient}). Removing the stop-gradient leaves most validation metrics
comparable, but it changes the learned uncertainty dynamics qualitatively: $\theta_{\max}$ grows
by $+28\%$ over training (3.11 $\to$ 3.99) instead of decaying and settling
(3.08 $\to$ 2.44), its seed-to-seed standard deviation increases by $14\times$
(0.192 vs.\ 0.014), and segmentation mIoU drops by $4.3\%$ (0.198 $\to$ 0.190). The
stop-gradient is therefore an active design component of the method, not an implementation
detail.
```

---

## 8. Sensitivity subsection — NEW §5.4 (Results)

```latex
\subsection{Sensitivity to batch statistics and calibration}
Because the canonical chart conditions on current-batch log-loss statistics, we measured
sensitivity to batch size and to the auto-calibration batch
(Appendix~\ref{app:sensitivity}).

\paragraph{Batch size.}
Canonical BPGS was trained at batch sizes 4, 8, and 16 (3 seeds each, NYUv2 50\% subset).
Across batch sizes, every validation metric has a coefficient of variation below 3.5\%, with most
below 1.2\% (Table~\ref{tab:batch_size}); $\theta_{\max}$ shifts only modestly, from 2.40
(bs = 4) to 2.59 (bs = 16), consistent with larger batches giving more stable gradient estimates
(Figure~\ref{fig:batch_size_theta}). No retuning was needed across the $4\times$ range.

\paragraph{First-batch calibration.}
Varying only the loader seed (1001/2001/3001) with fixed model seed leaves all validation
metrics with CV below 2\% (most below 0.6\%) and makes the $\theta_{\max}$ trajectories converge
within 0.3\% of each other (Table~\ref{tab:first_batch}, Figure~\ref{fig:first_batch_theta}).
The auto-calibration step is robust to which batch arrives first.
```

---

## 9. Overhead subsection — NEW §5.6 (Results)

```latex
\subsection{Computational overhead}
The added cost of BPGS relative to Kendall is negligible. Measured on the NYUv2 50\% subset
(3 seeds, 60 epochs, single GPU), the per-epoch wall-clock time increases by $+0.15\%$
(40.979 s vs.\ 40.916 s) and peak GPU memory by $+0.87\%$ (3368 MB vs.\ 3339 MB)
(Appendix~\ref{app:overhead}, Table~\ref{tab:overhead}). BPGS adds only $T = 3$ scalar
parameters to the 18.9M-parameter network. The batch-statistics computation and the separate
uncertainty pass therefore do not present a practical efficiency concern.
```

---

## 10. Discussion rewrite — §6 (full structure, from 02_section_by_section_rewrite_plan.md)

Key paragraphs requiring careful wording:

**Mixed-stress explanation (new item 3):**
```latex
In the heterogeneous mixed-stress study, BPGS trails Kendall and PCGrad in the noisy and conflict
regimes (macro score 0.641 vs.\ 0.659, and 0.652 vs.\ 0.664). This is consistent with what BPGS
does: it stabilizes scalar task weights against scale imbalance but does not modify gradient
directions, so when the dominant difficulty is gradient conflict or noise, methods that act on
the gradients themselves (Kendall through its unconstrained parameterization, PCGrad through
projection) have a structural advantage. Combining BPGS with a conflict-aware method --- BPGS for
the weighting, PCGrad or CAGrad for the gradient --- is a natural direction, but we did not test
such combinations and make no claim about them.
```

**Saturation risk (new item 4):**
```latex
Boundedness does not by itself guarantee learnability at the boundary: if a task's log-loss lay
outside the bounded interval for a sustained period, the sigmoid gradient factor would decay and
recovery would be difficult. In all logged main-paper runs the coordinate remains strictly inside
the boundary (the largest observed $|z_i|/\tau_T$ is 0.93 at the initialization epoch, and the
final-epoch caps are $\le 0.84$ on NYUv2, $\le 0.69$ on Yeast, and $\le 0.89$ on RF1), but this
is an empirical margin rather than a guarantee.
```

**Future work (merged into items 1, 3, 7):** Cityscapes / second dense benchmark; BPGS +
conflict-aware combination; CAGrad / IMTL-G / FAMO / Auto-Lambda baselines.
