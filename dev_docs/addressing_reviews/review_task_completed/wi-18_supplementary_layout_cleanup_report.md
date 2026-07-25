# WI-18 Supplementary Layout Cleanup Report

Date: 2026-07-24

## Scope

WI-18 is a presentation-only cleanup item. It does not change the paper's claims, experiments, or
technical content. The goal is to make the appendix and NeurIPS checklist read as a cleaner
supplementary package, with a layout that is easier to follow and easier to cite later if a final
revision needs presentation polish.

This report is self-contained. It records the current layout, the issue it creates, and the most
practical cleanup path for a later revision.

## Files Reviewed

- `working/paper/main.tex`
- `working/paper/appendix/A_reproducibility_details.tex`
- `working/paper/appendix/B_additional_stress_results.tex`
- `working/paper/appendix/C_ablation_and_nyuv2_figures.tex`
- `working/paper/appendix/D_real_data_figures.tex`
- `working/paper/checklist.tex`
- `working/paper/build/main.pdf`

## What I Verified

I inspected both the LaTeX source and the compiled PDF. The appendix is currently structured as:

1. Reproducibility details
2. Additional stress results
3. Ablation and NYUv2 figures
4. Real-data training curves
5. NeurIPS checklist

In the compiled PDF, the appendix begins on page 8. Page 9 then carries the tail of the
reproducibility appendix, the stress tables, the appendix section headings for B/C/D, and the start
of the checklist. Page 10 continues with the heterogeneous stress figure and the beginning of the
checklist questions.

So the current issue is not a missing result. It is that the supplementary material and the
submission checklist are visually interleaved in a way that makes the appendix feel less tidy than
it should.

## Layout Observation

The current source order in `main.tex` is:

```tex
\appendix
\input{appendix/A_reproducibility_details}
\input{appendix/B_additional_stress_results}
\input{appendix/C_ablation_and_nyuv2_figures}
\input{appendix/D_real_data_figures}
\input{./checklist.tex}
```

That order is structurally valid, but it is not the cleanest presentation for a paper that wants a
polished appendix. The checklist is a meta-document, not substantive supplementary evidence, so it
reads better when it is clearly separated from the research appendices.

## Why This Matters

The review concern is presentation-only, but it still matters for three reasons:

1. The appendix currently mixes substantive supporting material with the submission checklist.
2. A reviewer scanning the PDF can miss where the real appendix ends and the checklist begins.
3. If any extra space is used later, it should support substantive material rather than being
   absorbed by awkward float placement or section spillover.

## Recommended Cleanup Plan

If this item is revisited later, the cleanest revision would be:

1. Keep the substantive appendix sections together in one appendix block.
2. Move the NeurIPS checklist to its own clearly separated end section, ideally after a page break.
3. If there is spare space after the substantive appendix content, use it for a compact, relevant
   supplemental item such as a short compute note, an extra baseline summary, or a small
   reproducibility table.
4. Avoid padding the layout with filler just to occupy space.

The key principle is separation of concerns: the appendix should read as supporting scientific
material, and the checklist should read as administrative compliance material.

## Self-Contained Rebuttal/Revision Summary

If you need to describe WI-18 later without reopening the LaTeX source, the safe summary is:

> The paper's appendix content is already present, but the supplementary material and the NeurIPS
> checklist are laid out too close together. A final presentation cleanup should separate the
> checklist from the substantive appendices with a clearer page break and, if needed, repurpose any
> remaining space for a compact supplemental item rather than leaving the flow visually awkward.

## Current Status

No paper text was changed for WI-18 in this pass. This report is a reference note for a later
presentation cleanup, not an implementation record.
