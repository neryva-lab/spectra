
You’re right to stop and reassess. At this point, more brute-force NYUv2 runs are likely to buy you **very little information per GPU hour**.

What your log says is simple:

- training is slow because each epoch is already expensive: `99` train steps plus `82` validation steps
- validation alone costs about `70` seconds here
- `120` epochs is already a serious run on free Colab
- the curve near epoch 118 is improving, but only **marginally**

A jump from `mIoU 0.300` to `0.304` at epoch 118 does not justify assuming a major qualitative result is hiding at epoch 200. The realistic expectation is:
- a bit more gain,
- mostly for the already-strong methods,
- and probably still a very small gap between `BPGS` and `UWSO`.

So yes: **do not pretend compute will rescue the paper**.

**What you should assume now**

Given the evidence so far, the most realistic expectation is:

- `BPGS` and `UWSO` will remain close on NYUv2
- extra epochs may slightly improve both
- multiple seeds may reorder a tiny gap
- the final story will probably **not** be “BPGS decisively wins NYUv2”

That is the intelligent prior.

**So what should you do instead**

Use compute only where it changes a decision.

Good uses of compute:
- short pilot runs on subsets
- mechanism/ablation experiments
- stress tests for scale mismatch
- 3-seed runs only for the final shortlisted comparisons

Bad uses of compute:
- extending every full NYUv2 run to 200+ epochs just to see
- running all methods on all datasets at full budget before you know the claim
- repeating expensive comparisons when the likely conclusion is already “close tie”

**Practical decision rule**

Adopt this:

1. If an experiment will only tell you whether the gap is `tiny` or `slightly less tiny`, do not run it.
2. If an experiment can change the paper claim, run it.
3. If an experiment can reveal where BPGS is uniquely strong, prioritize it.

That means your next experiments should be:
- subset NYUv2 for fast ablations
- controlled scale-mismatch benchmark
- one or two cross-dataset regime checks
- then one final full-budget comparison only for the most relevant methods

**Supervisor-level conclusion**

The realistic paper is not:
- “after enough epochs BPGS becomes the best”

The realistic paper is more likely:
- “BPGS is a bounded split uncertainty-weighting method that is consistently competitive and appears more stable in heterogeneous regimes”

That is a much smarter target, and much cheaper to validate.

If you want, I can now help you design a **compute-budgeted experiment matrix**: exactly which runs are worth doing, which ones to cut, and what evidence each run is supposed to produce.
**What BPGS Is Actually Trying To Do**

You are right: we need to work backward from the method, not forward from leaderboard hopes.

From the active implementation, BPGS is **not** a universal “beat every baseline” optimizer. Its heart is much narrower:

- it learns a **latent uncertainty coordinate per task** instead of using raw inverse loss directly [spectra/core/bpgs.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/core/bpgs.py:73)
- that coordinate is forced through a **bounded chart** so task uncertainty cannot drift arbitrarily [spectra/core/bpgs.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/core/bpgs.py:118)
- the chart is **batch-adaptive**, because log-variance is centered and scaled by the current batch log-loss mean/std [spectra/core/bpgs.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/core/bpgs.py:109)
- the network does **not** optimize the same object as the uncertainty variables; it uses a detached softmax of precision-like weights for the model update, then a separate Kendall-style objective for the uncertainty update [spectra/engine/optimizers/bpgs.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/engine/optimizers/bpgs.py:45)

That means BPGS is philosophically a **stability-biased, bounded, split uncertainty-weighting method**.

UWSO, by contrast, is much simpler:
- take detached raw losses,
- invert them,
- softmax them,
- train [spectra/baselines/uwso.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/baselines/uwso.py:29)

So the clean contrast is:

- `UWSO`: “weight tasks directly from current losses”
- `BPGS`: “learn a bounded latent precision field whose effect on the network is smoothed and decoupled from its own update rule”

That is the real story.

**What That Implies Scientifically**

If that is the method, then BPGS should be expected to help most when:
- task losses have very different scales,
- raw inverse-loss weighting is too reactive,
- unconstrained uncertainty variables become unstable,
- you want smoother cross-task tradeoffs rather than hard winner-take-most behavior.

It should be expected to help less, or even lose, when:
- simple direct weighting already works well,
- tasks are naturally compatible,
- gradient conflict dominates loss-scale issues,
- the best method is really a gradient-surgery method like PCGrad rather than a weighting method.

So your observation across datasets is not a contradiction. It is exactly what should happen in real MTL:
- `PCGrad` can win where gradient conflict is the main problem.
- `UWSO` can win where instant loss-based reweighting is enough.
- `BPGS` should win where **boundedness + learned uncertainty + smoothing** matter.

That is why “no universal winner” is not bad news. It means you need the right claim.

**The Right Research Question**

Not:
- “Is BPGS state of the art everywhere?”

Instead:
- “Under what conditions does bounded split uncertainty-weighting help?”
- “When is learned bounded uncertainty preferable to direct inverse-loss softmax?”
- “Is BPGS more stable than UWSO/Kendall under scale mismatch or noisy task imbalance?”
- “Does BPGS trade some peak aggressiveness for better robustness?”

That is a publishable direction if the evidence is clean.

**Important Clarity Problem In The Repo**

You need to fix the method definition before doing more science.

There is a mismatch:
- the header comment in [spectra/core/bpgs.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/core/bpgs.py:11) says “no auto-calibration”
- but the code clearly does one-shot auto-calibration in `uncertainty_loss()` [spectra/core/bpgs.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/core/bpgs.py:168)
- the `z2` math docs treat auto-calibration as part of the active implementation [docs/math_definition/z2/03_bpgs_claims_and_proofs.md](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/docs/math_definition/z2/03_bpgs_claims_and_proofs.md:13)

Until that is internally consistent, your paper story is vulnerable. Lock one definition.

Note: the mismatch described above has since been resolved by locking [spectra/core/bpgs.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/core/bpgs.py:1) as the canonical `batch_aware + auto_calibrate` implementation. Treat the older inconsistency note as historical context only.

**Should You Use A Subset Of NYUv2?**

Yes, for research iteration. No, not as your only final evidence.

Use a two-tier protocol:

- `Tier 1: pilot`
  - subset of NYUv2
  - fast runs
  - many ablations
  - many seeds if cheap
  - answer mechanism questions

- `Tier 2: final`
  - full NYUv2
  - only shortlisted methods
  - fixed fair budget
  - 3 seeds minimum
  - final tables

This is better than spending all compute on long unclear full-data runs.

Also, because your 120-epoch runs are still improving, you should not guess what happens at 130 or 200. Define a fair budget:
- fixed epochs for all methods, or
- fixed wall-clock time for all methods, or
- early stopping with the same rule for all methods.

Do not let one method have more opportunity than another.

**What BPGS Might Be Better At**

Here are the most promising directions, ordered by research value.

1. **Loss-scale robustness**
   BPGS is explicitly built around log-loss statistics and bounded latent coordinates. This is the strongest natural hypothesis.

2. **Weight stability over training**
   UWSO reacts directly to inverse losses. BPGS should produce smoother, less erratic task weighting.

3. **Protection against pathological uncertainty drift**
   Kendall is unconstrained. BPGS is bounded. That gives you a principled comparison.

4. **Graceful behavior under mixed task types**
   Segmentation + depth + normals is exactly the kind of setup where bounded uncertainty might matter.

5. **Initialization sensitivity**
   Auto-calibration may reduce cold-start inertia versus plain learned uncertainty.

Less promising as a main story:
- universal best benchmark performance
- superiority over gradient-conflict methods on all datasets
- pure convergence theory of the full neural network

Your own docs already mark those as unsafe claims [docs/math_definition/z2/03_bpgs_claims_and_proofs.md](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/docs/math_definition/z2/03_bpgs_claims_and_proofs.md:34).

**The Experiments You Should Design**

Do these in order.

**A. Mechanism study**
Use a small NYUv2 subset.

Compare:
- `kendall`
- `uwso`
- `bpgs`

Measure:
- task weights over time
- variance of task weights
- log-var trajectories
- whether one task collapses or dominates
- gradient norm per task if you can log it

Goal:
- show what BPGS is doing, not just whether it wins.

**B. Scale-mismatch stress test**
This is probably your strongest paper direction.

Take a benchmark and artificially rescale one task loss:
- `x1`
- `x10`
- `x100`
- `x1000`

Compare:
- final metrics
- stability across seeds
- weight entropy
- collapse rate
- performance drop relative to the unscaled case

Hypothesis:
- `UWSO` is more reactive
- `Kendall` can drift
- `BPGS` should be more controlled

**C. Bounded-vs-unbounded ablation**
This is essential.

Compare:
- full `BPGS`
- `BPGS` without auto-calibration
- `BPGS` with fixed temperature
- `BPGS` with adaptive temperature
- unbounded version approximating Kendall-like free log-vars

This tells you which component matters.

**D. Full NYUv2 final comparison**
Only after A-C are understood.

Methods:
- `static`
- `kendall`
- `uwso`
- `bpgs`
- optionally `pcgrad`

Use:
- same epoch budget or same wall-clock budget
- same checkpoint selection rule
- 3 seeds

Report from one checkpoint rule only, not per-metric best epochs.

**E. Cross-dataset generalization**
Do not try every dataset.
Pick datasets that test different failure modes.

Good split:
- `NYUv2`: mixed dense prediction
- `Yeast` or `River flow` if it exposes imbalance/heterogeneity
- `QM9`: many regression heads where PCGrad seems stronger

Then the story is not “BPGS wins all.”
It is:
- “BPGS helps specifically in regime X, while method Y helps in regime Z.”

That is more believable.

**The Questions You Should Force The Research To Answer**

These are the supervisor-level questions you should write down and answer explicitly.

1. What exact optimization pathology is BPGS targeting?
2. Is that pathology scale mismatch, uncertainty drift, or weight volatility?
3. Which baseline already solves most of that pathology?
4. Why is direct inverse-loss softmax not enough?
5. Why does boundedness matter empirically, not just aesthetically?
6. What does the split update buy you compared with one-shot weighting?
7. Is auto-calibration core to the method or just a useful heuristic?
8. Does BPGS improve final performance, or mainly stability?
9. Does BPGS help more in early training, late training, or both?
10. On which dataset characteristics does BPGS fail?
11. Is the effect preserved across seeds?
12. Is the gain large enough to justify a new method, or should this be a workshop/technical report paper instead?

If you cannot answer 1-6 with evidence, the paper is not ready.

**The Paper Direction I Would Recommend**

The strongest honest framing right now is:

“BPGS is a bounded, batch-adaptive, split uncertainty-weighting method for multi-task learning. Its main value is not universal superiority, but more stable behavior under heterogeneous task scales and uncertainty dynamics.”

That is much better than claiming SOTA.

**Practical Next Step**

You should now freeze a research program like this:

1. Clean up the BPGS definition so code and docs agree.
2. Run subset-based mechanism experiments on `kendall`, `uwso`, `bpgs`.
3. Run a scale-mismatch stress test.
4. Use full NYUv2 only for the final comparison after the mechanism is understood.
5. Treat other datasets as regime tests, not as a place to demand universal wins.

If you want, the next thing I can do is turn this into a concrete experimental protocol:
- exact tables,
- exact ablations,
- exact subset/full schedule,
- and the manuscript claim structure matched to those experiments.





Implemented the paper-track workflow in code.

Main changes:
- BPGS is now treated as the single active paper method, with the header/comments cleaned up and the active options exposed in config: `auto_calibrate`, `theta_grad_scale`, and fixed/adaptive temperature support in [spectra/core/bpgs.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/core/bpgs.py:1), [spectra/baselines/__init__.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/baselines/__init__.py:1), and [configs/method/bpgs.yaml](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/configs/method/bpgs.yaml:1).
- NYUv2 now supports explicit paper subset files on train only, while validation stays full. That wiring is in [spectra/data/nyuv2/dataset.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/data/nyuv2/dataset.py:137) and [spectra/data/datamodule.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/data/datamodule.py:199).
- Added a deterministic NYUv2 subset generator at [scripts/data/nyuv2_paper_subsets.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/scripts/data/nyuv2_paper_subsets.py:1). It writes fixed `25/50/75` train subsets for seeds `11/22/33` under `data/paper_splits/nyuv2/v1/`.
- Added post-fit run summaries with selection metric, selected checkpoint, stopped epoch, and elapsed time in [spectra/train/runner.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/train/runner.py:1) and [spectra/train/artifacts.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/train/artifacts.py:1).
- Added named preset execution in [scripts/execution/paper_runner.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/scripts/execution/paper_runner.py:1) for:
  - `nyuv2_pilot_25`
  - `nyuv2_pilot_50`
  - `nyuv2_full_final`
  - `synthetic_scale_stress`
  - `yeast_regime_check`
  - `qm9_regime_check`
- Added publication aggregation in [scripts/execution/aggregate_paper_results.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/scripts/execution/aggregate_paper_results.py:1), producing `tidy_runs.csv`, `summary.csv`, and `summary.json`.
- Excluded `bpgs_alb` from the old NYUv2 publication pipeline shortlist in [scripts/execution/reproduction_pipeline.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/scripts/execution/reproduction_pipeline.py:25).

Verification:
- `py_compile` passed on all modified Python files.
- `paper_runner.py --dry-run` works and prints the full preset command plan.
- `aggregate_paper_results.py --help` works and a no-data aggregation run completed.
- `nyuv2_paper_subsets.py --help` works.

Not run:
- I did not execute actual NYUv2 subset generation because this workspace currently does not contain the NYUv2 LMDB files.
- I did not run the heavy paper presets themselves.

Use:
```bash
python scripts/execution/paper_runner.py --preset nyuv2_pilot_50 --dry-run
python scripts/data/nyuv2_paper_subsets.py
python scripts/execution/paper_runner.py --preset nyuv2_full_final
python scripts/execution/aggregate_paper_results.py --preset nyuv2_full_final
```


# SPECTRA Final Paper Experiment Design

## Summary
Optimize the paper for a **low-compute, top-tier-defensible submission** with a narrow, honest claim:

**Claim to support:**  
BPGS is a **bounded, batch-adaptive, split uncertainty-weighting method** whose value is **robust, consistently competitive behavior under heterogeneous task scales and uncertainty dynamics**, not universal SOTA performance.

**Paper strategy:**  
Do **not** pursue a universal “wins every dataset” story. Use:
- one **main benchmark**: standard NYUv2 MTL (`795 train / 654 eval`)
- one **mechanism benchmark**: subset NYUv2 for ablations and fast sweeps
- one **controlled stress benchmark**: synthetic loss-scale mismatch
- two **cross-regime checks**: `Yeast` and `QM9`
- a **narrow final seeded comparison** only on shortlisted methods

This plan is chosen because full multi-dataset, full-seed, full-budget coverage is not realistic under free/low-cost Colab and is unlikely to change the conclusion.

## Implementation Changes
### 1. Lock the paper-truth definition of BPGS
- Treat the active implementation in [spectra/core/bpgs.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/core/bpgs.py:41) and [spectra/engine/optimizers/bpgs.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/engine/optimizers/bpgs.py:19) as the only paper method.
- Remove all manuscript-facing language implying universal superiority or “SOTA”.
- Resolve the inconsistency between the BPGS file header and the active code path regarding auto-calibration before any writing or plotting.
- Treat `bpgs_alb` as archived and exclude it from the primary paper benchmark set.

### 2. Fix the model-selection protocol
- For **all final reported experiments**, select a checkpoint using **one rule only** and report all metrics from that checkpoint.
- Use `val/total_loss` as the **primary checkpoint selection rule** for final tables, not per-metric best epochs.
- Keep `val/miou` checkpoints only for diagnostics and qualitative inspection.
- Keep the current early-stopping rule for pilot runs, but for final benchmark comparisons use the **same epoch cap and same early-stop settings** across all compared methods.
- Final paper tables must never mix:
  - different epoch budgets,
  - incomplete runs,
  - or best-mIoU/best-abs_rel/best-angle from different epochs.

### 3. Add a paper-safe NYUv2 subset protocol
Create a new subset-generation path rather than relying on the current plain random `subset_pct` behavior in [spectra/data/nyuv2/dataset.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/data/nyuv2/dataset.py:187).

Required behavior:
- Keep the `654` eval split untouched.
- Subset **train only** from the standard `795`-image NYUv2 MTL split.
- Generate three fixed public subset budgets:
  - `25%` = 199 images
  - `50%` = 398 images
  - `75%` = 596 images
- Generate three subset seeds:
  - `11`, `22`, `33`
- Persist exact train indices to versioned JSON files under a new paper-splits location.
- Add metadata per subset:
  - source dataset version/hash
  - subset size
  - subset seed
  - index list
  - basic label/depth coverage summary
- All pilot and ablation experiments must consume these explicit split files, not ad hoc random sampling.

Chosen default:
- Because the standard 795-image NYUv2 MTL split is already sparse and not raw-video-scale, use **fixed stratified image-level subsets** rather than inventing a new scene-level partition unless scene IDs are already present in the manifest.
- If scene/sequence identifiers are available in the index metadata, prefer **group-aware stratified sampling** and keep each group entirely in or out of a subset.

### 4. Add experiment presets for paper runs
Add named paper presets instead of manual command composition.

Required presets:
- `nyuv2_pilot_25`
- `nyuv2_pilot_50`
- `nyuv2_full_final`
- `synthetic_scale_stress`
- `yeast_regime_check`
- `qm9_regime_check`

Each preset must freeze:
- dataset
- subset file or full split
- epoch cap
- checkpoint rule
- early-stop settings
- compared methods
- seeds

### 5. Add result aggregation for publication tables
Create one non-mutating-compatible reporting path that aggregates each run’s:
- config
- metadata
- final selected checkpoint metrics
- wall-clock runtime
- epoch stopped
- seed
- subset identifier

Required outputs:
- one tidy CSV per experiment family
- one summary CSV for tables
- one JSON summary for plotting

Computed summary fields:
- `miou`
- `abs_rel`
- `mean_angle_deg`
- `delta_m` where applicable
- runtime
- stopped_epoch
- selected_checkpoint
- subset_budget
- subset_seed
- training_seed

## Final Experiment Matrix
### A. Main benchmark: NYUv2 full, final evidence
Purpose:
- support the main empirical statement
- compare BPGS only against the baselines that matter

Methods:
- `static`
- `kendall`
- `uwso`
- `bpgs`

Seeds:
- `42`, `43`, `44`

Budget:
- `train.epochs = 120`
- early stopping enabled with one common setting
- same batch size and augmentation for all methods

Selection rule:
- report all metrics from the checkpoint selected by **lowest `val/total_loss`**

Primary table:
- `mIoU`
- `AbsRel`
- `Mean Angle`
- `Δm`
- runtime
- stopped epoch
- mean ± std across seeds

Interpretation rule:
- If BPGS is only tied or narrowly ahead of UWSO, the paper text must say “competitive / slightly better in the reported setting,” not “superior.”

### B. NYUv2 pilot ablation study
Purpose:
- identify which BPGS components matter
- avoid wasting full-budget compute on dead directions

Dataset:
- fixed `50%` subset first
- use `25%` only if turnaround is still too slow

Variants:
- full `bpgs`
- `bpgs` without auto-calibration
- `bpgs` with fixed temperature
- `bpgs` with adaptive temperature
- unbounded/Kendall-style uncertainty comparison

Seeds:
- `42`, `43`, `44`

Budget:
- `train.epochs = 60`

Decision rule:
- A component stays in the final method only if it shows either:
  - better mean performance, or
  - lower variance, or
  - visibly better stability behavior

### C. Controlled synthetic stress benchmark
Purpose:
- test the mechanism BPGS is actually meant to address

Methods:
- `kendall`
- `uwso`
- `bpgs`

Conditions:
- loss-scale multiplier on one task:
  - `1x`
  - `10x`
  - `100x`
  - `1000x`

Seeds:
- `42`, `43`, `44`

Budget:
- short fixed epoch budget sufficient for convergence on synthetic

Required outputs:
- final task metrics
- failure/collapse count
- weight entropy or weight spread
- uncertainty trajectory summary
- variance across seeds

This experiment is mandatory. If BPGS does not show clearer robustness here, the paper’s main story weakens substantially.

### D. Cross-regime checks
Purpose:
- show BPGS is not a one-benchmark accident
- avoid pretending it is universally best

Datasets:
- `Yeast`
- `QM9`

Methods:
- `uwso`
- `bpgs`
- winner-specific reference baseline
  - `static` on Yeast if needed
  - `pcgrad` on QM9 because it appears strong there

Seeds:
- single seed for scouting
- 3 seeds only on the final narrowed comparison if BPGS looks meaningfully competitive

Budget:
- use existing full split
- standard epoch cap already configured for the dataset

Interpretation rule:
- These experiments are for **regime characterization**, not universal dominance.
- Expected acceptable outcome:
  - BPGS is close to the winner on some datasets,
  - loses on others,
  - but remains consistently competitive or more stable.

## Test Plan
### Reproducibility checks
- Verify every paper run writes:
  - resolved config
  - metadata
  - selected subset ID
  - selected checkpoint path
- Verify rerunning the same preset with the same seed reproduces the same subset and same metadata.
- Verify no experiment table pulls metrics from different epochs of the same run.

### Subset protocol checks
- Confirm subset files contain the exact intended counts: `199`, `398`, `596`.
- Confirm the eval split is unchanged.
- Confirm subset generation is deterministic for a given subset seed.
- Confirm coverage summaries do not show pathological omission of dominant semantic classes or near-empty valid-depth coverage.

### Reporting checks
- Verify final NYUv2 tables aggregate `mean ± std` over seeds.
- Verify runtime and stopped epoch are captured.
- Verify `pcgrad` is never included in a final table with incomplete runs.

### Claim-safety checks
- Verify no final figure, table, or caption says:
  - “state of the art”
  - “universally better”
  - “guaranteed superior”
- Verify the paper only claims what is supported by:
  - boundedness/split-update theory from the math docs
  - full-seed empirical evidence from the final tables

## Assumptions and Defaults
- Optimize for **low compute**: free Colab or similarly constrained single-GPU access.
- Use the **standard 795/654 NYUv2 MTL benchmark**, not the 50k-frame depth-completion regime.
- Treat `BPGS vs UWSO` as the main head-to-head.
- Treat `PCGrad` as a regime-specific competitor, not a universal final baseline.
- Use `3` training seeds as the maximum final seed count for expensive runs.
- Use subset pilots to make decisions; do not extend every full NYUv2 run beyond `120` epochs unless a final shortlisted run is clearly undertrained and that undertraining changes a paper decision.
- If final evidence shows BPGS is merely near-best rather than best, the publication target should still be pursued with a **robustness/stability framing**, not abandoned.
