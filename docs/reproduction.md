# End-to-End Reproduction Guide

This docs would guide to reproduce the core results of the SPECTRA paper. Ensure you have installed the package and its dependencies as described in [Getting Started](getting_started.md).

## 1. Dataset Preparation

Before running the studies, you must materialize the required datasets locally. These steps only need to be run once.

```bash
# NYUv2 dense prediction
python scripts/data/nyuv2_generate.py

# Yeast multi-label classification
python scripts/data/yeast_generate.py

# RF1 multi-target regression
python scripts/data/rf1_generate.py

# QM9 molecular regression
python scripts/data/qm9_generate.py
```
*(Clinical data resolves automatically through its specific acquisition tier when executed.)*

## 2. Execute Training Studies

Execute the training-based studies to generate the necessary artifacts. 

```bash
# NYUv2 Ablation
python experiments/bpgs_study/run.py --study 01_nyuv2_ablation

# Yeast Regime Check
python experiments/bpgs_study/run.py --study 03_yeast_regime_check

# RF1 Regime Check
python experiments/bpgs_study/run.py --study 08_rf1_regime_check

# QM9 Regime Check (Optional)
python experiments/bpgs_study/run.py --study 04_qm9_regime_check

# NYUv2 Full Final (Optional)
python experiments/bpgs_study/run.py --study 05_nyuv2_full_final
```

*(Note: Add `--dry-run` to any command above to preview the execution plan without starting runs.)*

## 3. Execute Empirical Stress Tests

Run the controlled synthetic stress benchmarks.

```bash
# Synthetic Scale Stress
python experiments/bpgs_study/run.py --study 02_synthetic_scale_stress

# Pure Loss Rescaling
python experiments/bpgs_study/run.py --study 06_pure_loss_rescaling

# Heterogeneous Mixed Stress
python experiments/bpgs_study/run.py --study 07_heterogeneous_mixed_stress
```

## 4. Run Analysis and Asset Generation

Once all study runs are complete, run the analysis pipeline to process outputs into figures, tables, and statistics.

```bash
cd experiments/bpgs_analysis
python -m analysis.scripts.generate_all
```

The assembled final paper assets will be written to `experiments/bpgs_analysis/analysis/outputs/paper_final`.
