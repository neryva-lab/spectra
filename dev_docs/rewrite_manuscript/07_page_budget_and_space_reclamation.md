# 07 — Page Budget & Space Reclamation

NeurIPS 2026 limit: **9 pages of main content** (figures included). References, acknowledgments,
appendices, checklist are unlimited.

## 1. Provisional baseline usage (compiled `build/main.pdf`, 21 pages total)

The compiled PDF/build auxiliary files predate the final source reconciliation in places (notably
the auxiliary table entry still says the scale-stress table has 3 seeds although the source table
has 10). Therefore these measurements are planning estimates only; Phase 0 must rebuild and
remeasure before any prose is cut to the page budget.

- Pages 1–7: main text.
- Page 8: tail of Discussion + **References start** → main body is ≈ **7.4 pages**.
- Page 9+: appendices + checklist (interleaved — see `05_appendix_restructure.md`).

**Headroom: ≈ 1.6 pages before the 9-page limit.**

## 2. Estimated additions (from 02/03/04)

| Addition | Est. lines | Est. pages |
|---|---|---|
| τ_T derivation (§3.2) | 12 | 0.13 |
| grad-scale note (§3.3) | 4 | 0.04 |
| fixed-point rewording (§3.3, net of removed sentence) | +3 | 0.04 |
| saturation paragraph (§3.4) | 10 | 0.11 |
| §3.5 Invariance: subsection + Prop 1 + proof + remarks | 22 | 0.25 |
| Experimental setup: controlled studies + Nash-MTL + protocol | 10 | 0.11 |
| §5.1: invariance ref sentence + normalization-ablation paragraph | 8 | 0.09 |
| §5.2: Nash-MTL sentence | 5 | 0.06 |
| §5.3: stop-gradient paragraph | 6 | 0.07 |
| §5.4: new subsection (2 paragraphs + headers) | 14 | 0.16 |
| §5.6: new subsection (3–4 sentences) | 5 | 0.06 |
| Related work: Nash-MTL/IMTL-G/FAMO sentence | 3 | 0.04 |
| Abstract + intro edits | +2 | 0.02 |
| §6: new limit items + mixed-stress paragraph, minus removed items | +12 | 0.14 |
| **Total** | **≈ 116** | **≈ 1.32** |

Projected main text: **≈ 8.7 pages** — inside the limit, but **too tight** (float placement of
tables/figures can push 1–2 lines over; a reviewer will notice a crammed last page). Target:
**≤ 8.4 pages** → reclaim **≈ 0.3 pages** (~25 lines).

## 3. Reclamation plan (executed during the prose edit, in this priority order)

All cuts are *tightening*, never content removal of claims:

| # | Cut | Est. savings |
|---|---|---|
| 1 | Compress the five WI-17 motivation paragraphs in §3 (problem setup, canonical chart, first-batch calibration, split optimization, batch-conditional boundedness — WI-17 added five blocks). Each currently runs 4–6 lines of plain-language restatement; keep the key sentence of each, merge the rest. | 10–12 lines (0.11–0.13 p) |
| 2 | Tighten §5.1 lead-in ("We organize the evaluation around four questions…") and the scale-stress paragraph by one clause each. | 4–5 lines (0.05 p) |
| 3 | Tighten §4.1 benchmark bullets (drop repeated "120 epochs / 3 seeds" phrasing where the protocol section already states it). | 4–5 lines (0.05 p) |
| 4 | Tighten §6 opening paragraph and societal-impact paragraph slightly. | 3–4 lines (0.04 p) |
| 5 | Trim intro paragraph 2 (PCGrad sentence) if needed. | 2 lines (0.02 p) |

Total ≈ 0.25–0.30 p → projected **8.4–8.5 pages**.

## 4. Fallback cuts (use only if the build still exceeds 9 pages or page 9 is overfull)

Apply in order, only as needed — each is a real sacrifice, so decide deliberately:

| Fallback | Cost | Save |
|---|---|---|
| F1. Move `tab:stress_rescaling` (pure rescaling, 3-seed) to Appendix B; keep its numbers in prose in §5.1 | Loses an inline table; rescaling evidence already carried by Figure 1 + Proposition 1 | ~0.12 p (plus float-freed space) |
| F2. Shrink Figure 1 (`stress_robustness_summary`) from `\textwidth` to `0.85\textwidth` | Cosmetic | ~0.05–0.10 p |
| F3. Merge §5.4 and §5.6 into one subsection "Sensitivity and overhead" | Loses one subsection header; acceptable | ~0.05 p |
| F4. Drop the optional F-norm figure (already optional) | Nothing (appendix only) | n/a |
| F5. Move `tab:ablation` (NYUv2 ablation) to Appendix C with prose summary in §5.3 | Ablation table is core evidence; last resort | ~0.15 p |

**Do not** cut: Proposition 1 (the paper's formal core), the Kendall+L1 paragraph (novelty
evidence), the Nash-MTL row, the saturation paragraph, or the mixed-stress discussion.

## 5. Float management to protect the limit

- New tables live in appendices (E/F/G) by design — only one new row enters a main table
  (Nash-MTL).
- Keep `[t]`/`[h]` placement hints; after the first full build, inspect where floats land and
  adjust placement hints before cutting prose.
- If the main text lands at exactly 9.0 pages with an overfull page 9, apply F1 before F2/F3.

## 6. Verification gate

After the final build:
1. `pdftotext -f 1 -l 9 build/main.pdf` → page 9 must contain main-text content and
   **not** spill; References must start on page 9 **at the earliest** (i.e., main text ≤ 9 pages
   inclusive).
   Exact check: find the page on which "References" first appears → that page number ≤ 9 means
   main text (incl. floats) fits; references may begin there.
2. `build/main.log`: no `Overfull \hbox` > 20pt in the main-text region; no
   `LaTeX Warning: Float too large` (resize the offending float if present).
3. Visual scan of page 8–9 for awkward gaps (this was an MKod complaint; don't reintroduce it).
