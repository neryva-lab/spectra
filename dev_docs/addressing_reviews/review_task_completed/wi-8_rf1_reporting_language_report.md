# WI-8 RF1 Reporting Language Report

Date: 2026-07-24

## Scope

WI-8 corrected the RF1 wording in the paper so the abstract and main text match the table-level
results already reported in Section 5.4.

The underlying RF1 numbers were already correct. The issue was the framing: the abstract implied
near parity with the leading baseline on RF1 RMSE and MAE, while the reported table shows that
BPGS is not the top method on those metrics.

## Files Updated

- `working/paper/sections/00_abstract.tex`
- `working/paper/sections/01_introduction.tex`
- `working/paper/sections/04_results.tex`
- `dev_docs/addressing_reviews/review_ledger.md`

## What Changed

- Rewrote the abstract RF1 sentence to say BPGS is competitive on RF1 without claiming closeness
  to the leading baseline on RMSE or MAE.
- Rewrote the introduction contribution bullet to state that BPGS is competitive on RF1 but not
  best on RMSE or MAE.
- Tightened the RF1 results paragraph so it explicitly says:
  - BPGS is not the top method on RF1
  - PCGrad has the best RMSE and MAE
  - UWSO has the best mean $R^2$
- Marked WI-8 complete in the review ledger and updated the progress snapshot.

## Verification

- Searched the paper source for the old RF1 overclaim phrasing and replaced it.
- Confirmed the remaining RF1 language now consistently uses the narrower claim of
  competitiveness rather than near-dominance.
- Checked that the results section and abstract now agree on the scope of the RF1 claim.

## Completion Note

WI-8 is now resolved as a wording and framing fix only. No experiment reruns were needed because the
paper already contained the correct RF1 results; only the presentation of those results required
correction.
