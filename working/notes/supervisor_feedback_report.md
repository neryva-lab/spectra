# Final Supervisor Report: Experiment Design And Paper Direction

**Project:** SPECTRA / BPGS study  
**Date:** 2026-05-04  
**Audience:** Student researcher  
**Purpose:** Final guidance on what experiments to run, which datasets to use, and how to turn the completed implementation into a coherent paper

## 1. Where You Are Now

You have already done the hard implementation work. The BPGS method is now locked in its final form in:

[spectra/core/bpgs.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/spectra/core/bpgs.py:1)

That means the next phase is no longer method invention. The next phase is **experiment design**.

From now on, your job is not to keep trying random experiments. Your job is to build a clean body of evidence around one clear research claim.

## 2. The Final Research Claim

The paper should be built around this claim:

> BPGS is a bounded, batch-aware uncertainty-weighting method that is especially useful under heterogeneous loss-scale stress, where it provides more robust and stable task balancing while remaining competitive in broader multi-task regimes.

This is the best possible decision for your paper direction because it matches:

- the locked implementation
- the synthetic stress-test strengths already visible in the repository
- a realistic and defensible contribution

Do **not** frame the paper as:

- “BPGS is best everywhere”
- “BPGS is the universal state-of-the-art solution”
- “BPGS wins every benchmark”

That is not the right paper for this project.

## 3. What Types Of Experiments You Need

You need three experiment families:

1. **Ablation study**
2. **Synthetic stress tests**
3. **Real-data supporting tests**

These three experiment families do different jobs. Do not mix them.

### 3.1 Ablation study

Purpose:

- justify why the final BPGS design is the locked one

Question:

- why is `batch_aware + auto_calibrate` the final version instead of nearby alternatives?

This is the experiment that protects your paper from the reviewer question:

> “How do we know this final BPGS version was not selected arbitrarily?”

### 3.2 Synthetic stress tests

Purpose:

- provide the **main evidence** for your paper

Question:

- does BPGS remain stable and competitive when task scales become badly mismatched or when the regime becomes heterogeneous?

This is where your paper is strongest. These experiments are not secondary. These are the center of the study.

### 3.3 Real-data supporting tests

Purpose:

- show that the method is not only a synthetic artifact

Question:

- does BPGS remain reasonable and competitive on real tasks?

These experiments support the claim. They do not define the claim.

## 4. The Best Experimental Program For This Project

I am making the decision here on your behalf:

### Core paper evidence

These should definitely be in the paper:

- one ablation study
- one pure loss-scale stress study
- one mixed heterogeneous stress study

### Supporting paper evidence

These should be included if run carefully:

- one real-data classification benchmark
- one real-data regression benchmark

### High-cost optional evidence

These should only be included if data and compute are ready:

- final full NYUv2 comparison

That is the correct hierarchy.

## 5. Dataset Decision

Based on the current project structure on **2026-05-04**, the locally available prepared datasets are:

- `yeast`
- `rf1`
- `qm9`

As of this review, there is **no prepared `datasets/nyuv2` directory** in the local workspace, even though NYUv2 appears in the study plan. That means NYUv2 should not be allowed to block progress unless you already have the dataset elsewhere and can restore it immediately.

So the correct dataset decision is:

### Use these now

- synthetic generated benchmarks for the main claim
- `yeast` for real-data classification support
- `rf1` for real-data regression support

### Use with caution

- `qm9` only as optional extra evidence, not as a main paper pillar

### Use only if the data is truly available

- `nyuv2` for ablation and final vision-style benchmark

This is the best decision because it keeps the paper moving with the assets you already have.

## 6. The Recommended Final Experiment Plan

Below is the plan I recommend you follow exactly.

## Experiment 1: BPGS Ablation

### Goal

Show why the locked BPGS configuration is the final one.

### Recommended dataset

**Primary choice:** NYUv2 subset  
Reason:

- it is the closest to the original design motivation
- it is suitable for showing multi-task behavior
- it makes the ablation easier to interpret

**If NYUv2 is not currently available:** do not pause the project indefinitely. Either restore it immediately or adapt the ablation to the most suitable existing multi-task setting already available in your framework.

### Recommended variants

Use the ablation structure already implied in:

[studies/bpgs_objective/definitions.py](/C:/Users/Hellx/Documents/Programming/python/Project/iron/bc/SPECTRA/studies/bpgs_objective/definitions.py:58)

Compare:

- `bpgs_canonical`
- `bpgs_stateless_fixed`
- `bpgs_stateless_auto`
- `bpgs_batch_aware_fixed`
- `kendall`

### What this experiment should prove

- batch-awareness matters
- auto-calibration matters
- the canonical combination is not arbitrary
- BPGS is not just Kendall with a cosmetic change

### Recommended protocol

- 3 seeds minimum
- same subset across methods
- same epoch budget
- same early stopping rule
- same optimization settings

### Metrics to report

- primary task performance summary
- worst-task performance
- variance across seeds
- weight behavior if available
- runtime only as a secondary note

### Output for the paper

One compact ablation table with a short conclusion:

> “The batch-aware and auto-calibrated form was selected as the final BPGS configuration because it gave the best balance of robustness and task performance.”

## Experiment 2: Pure Loss-Scale Stress Test

### Goal

Test the strongest hypothesis of the paper:

- BPGS should be robust when task loss scales become extremely mismatched

### Recommended dataset

Synthetic empirical benchmark

This is already the correct choice. You do not need a real dataset for this claim, because the point is controlled stress, not realism.

### Recommended study

Use the existing structure around:

- `02_synthetic_scale_stress`
- `06_pure_loss_rescaling`

In practice, the cleaner paper-facing version is likely the pure loss-rescaling study because it directly isolates scale stress.

### Recommended methods

- BPGS
- UWSO
- Kendall

This is the right comparison because all three are weighting-style methods, and the claim is specifically about uncertainty and scale handling.

### Recommended scale settings

- `x1`
- `x10`
- `x100`
- `x1000`

### What this experiment should prove

- BPGS degrades more gracefully as scale mismatch becomes extreme
- BPGS protects worst-task performance better than simpler baselines
- bounded, batch-aware uncertainty has value under stress

### Metrics to report

- macro score
- worst-task score
- best-task score
- seed variance
- gradient norm or stability-related quantities if already logged
- weight entropy if already logged

### Output for the paper

This should be one of the main figures:

- scale multiplier on the x-axis
- performance on the y-axis
- one curve per method

This is a paper-defining figure.

## Experiment 3: Heterogeneous Mixed-Stress Test

### Goal

Show that BPGS is not only good in artificial scale inflation, but also remains competitive when the regime is more mixed and realistic.

### Recommended dataset

Synthetic heterogeneous benchmark

Again, this is the correct choice. The purpose here is controlled regime variation, not real-world realism.

### Recommended study

Use the existing study:

`07_heterogeneous_mixed_stress`

### Recommended regimes

- clean
- conflict
- noisy

### Recommended methods

- BPGS
- Kendall
- PCGrad
- UWSO

This is the right comparison set because:

- Kendall tests uncertainty-based weighting
- UWSO tests direct reactive weighting
- PCGrad tests a gradient-conflict solution

### What this experiment should prove

- BPGS remains competitive outside the pure scale-stress setting
- BPGS does not collapse under heterogeneous conditions
- BPGS is a robustness-oriented method, not a one-scenario trick

### Metrics to report

- macro score
- worst-task score
- variance across seeds
- evidence of collapse or failure if any
- weight or gradient behavior if available

### Output for the paper

One table and one figure are enough.

The key message should be:

> “BPGS is not always the absolute top performer, but it remains competitive across heterogeneous regimes while preserving controlled behavior.”

That is the right message.

## Experiment 4: Real-Data Classification Support

### Goal

Show that BPGS behaves reasonably on a real dataset outside synthetic stress tests.

### Recommended dataset

`yeast`

Reason:

- already locally available
- classification setting
- low enough cost to run properly
- useful as a supporting benchmark

### Recommended methods

- Static
- UWSO
- BPGS

If Kendall is easy to include consistently, you may add it. But do not delay the experiment just to expand the baseline list unless the integration is already ready.

### Recommended protocol

The current single-seed form is not enough for paper-quality support.

Use:

- 3 seeds minimum
- same early stopping rule
- same epoch budget
- identical data split

### What this experiment should prove

- BPGS is not obviously brittle on real classification data
- BPGS is competitive even when the setting is not synthetic

### Output for the paper

One small supporting table is enough. Do not overemphasize it.

## Experiment 5: Real-Data Regression Support

### Goal

Show that the method also behaves reasonably in a real regression setting.

### Recommended dataset

`rf1`

Reason:

- already locally available
- gives you a real regression example
- complements `yeast` well

### Recommended methods

- Static
- UWSO
- BPGS

Same note as above: only expand the baseline list if it is easy and consistent.

### Recommended protocol

- 3 seeds minimum
- same budget across methods
- same early stopping rule

### What this experiment should prove

- BPGS can operate sensibly outside classification
- the method is not tied to only one task type

### Output for the paper

Again, one small supporting table is enough.

## 7. What To Do With QM9

My recommendation is:

- keep QM9 as optional
- do not make it a core requirement for the paper

Reason:

- it is not necessary for the central claim
- your paper already has enough structure with synthetic stress + one classification dataset + one regression dataset
- adding too many datasets can weaken focus if the story is not tight

If you use QM9, present it only as additional supporting evidence.

## 8. What To Do With NYUv2

My recommendation is:

- use NYUv2 only if the dataset is genuinely available and runnable without derailing the schedule

Best role for NYUv2:

- ablation dataset
- optional final multi-task vision benchmark

Worst role for NYUv2:

- blocking the whole paper while you wait on data or long compute

If NYUv2 is ready, it is a good dataset. If it is not ready, do not let it stall the entire study.

## 9. Recommended Baseline Strategy

Do not use the same baseline set blindly for every experiment.

### For ablation

- BPGS variants
- Kendall

### For scale-stress

- BPGS
- UWSO
- Kendall

### For heterogeneous stress

- BPGS
- UWSO
- Kendall
- PCGrad

### For real-data support

- Static
- UWSO
- BPGS

This is the most practical and defensible baseline design. It keeps each experiment focused on the right scientific question.

## 10. Recommended Seed Policy

You must use a consistent seed policy.

### Core studies

Use:

- 3 seeds minimum

These include:

- ablation
- pure loss-scale stress
- heterogeneous mixed-stress
- final real-data support tables

### Exploratory runs

Use:

- 1 seed only for quick debugging or scouting

But do not turn single-seed results into paper conclusions.

## 11. What The Final Paper Should Contain

If you follow my guidance, the final paper should contain:

### Section 1: Problem and motivation

- instability of task weighting under heterogeneous scale
- why bounded uncertainty might help

### Section 2: Method

- the locked BPGS definition from `spectra/core/bpgs.py`

### Section 3: Ablation

- why the final BPGS version is the right one

### Section 4: Main result

- pure loss-scale stress test

### Section 5: Broader robustness result

- heterogeneous mixed-stress benchmark

### Section 6: Supporting real-data evidence

- Yeast
- RF1

### Section 7: Discussion

- where BPGS is strongest
- where BPGS is only competitive
- what kinds of regimes it is designed for

This is enough. You do not need a giant benchmark zoo.

## 12. What You Must Avoid

Avoid these mistakes from now on:

- do not run expensive experiments without knowing what question they answer
- do not collect many datasets just to look comprehensive
- do not treat supporting studies as main studies
- do not overclaim from single-seed results
- do not write the conclusion before the ablation is finished

The paper becomes stronger when it is narrower but clearer.

## 13. Final Ordered Plan

I recommend the following exact order:

1. Finalize the ablation study around the locked BPGS method.
2. Finalize the pure loss-scale stress study.
3. Finalize the heterogeneous mixed-stress study.
4. Upgrade `yeast` from pilot to proper 3-seed support study.
5. Upgrade `rf1` from pilot to proper 3-seed support study.
6. Use QM9 only if time and clarity remain.
7. Use NYUv2 only if the dataset is already available and does not delay the project.
8. Write the paper around the synthetic robustness story, with real-data support added carefully.

## 14. Final Supervisor Verdict

Your implementation work is already strong enough. The correct next decision is **not** to keep expanding the method. The correct next decision is to run a disciplined experiment program.

If you follow the plan above, your study will become coherent:

- ablation proves why the final BPGS version is the locked one
- synthetic stress tests prove the main claim
- real-data tests show the method is reasonable beyond synthetic settings

That is the right paper.

If you ignore this structure and keep mixing exploratory experiments with final claims, the project will remain technically impressive but scientifically weak.
