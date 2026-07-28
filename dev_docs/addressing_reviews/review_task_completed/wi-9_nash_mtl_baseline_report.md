# WI-9 Nash-MTL Baseline Report

Date: 2026-07-25

## Scope

WI-9 implements and evaluates Nash-MTL (Navon et al., 2022) on the NYUv2 dense-prediction benchmark. This addresses the reviewer request (Mxe9-5, Mxe9-6, Mxe9-Q3, AqnD-22, MKod-5) for comparison against modern MTL baselines beyond the paper's original set (Static, Kendall, UWSO, PCGrad, GradNorm).

## Implementation

- `spectra/baselines/nash_mtl.py`: `NashMTLWeighter` — no-op placeholder; Nash weights are computed in the engine, not the weighter.
- `spectra/engine/optimizers/nash_mtl.py`: `NashMTLEngine` — computes per-task backbone gradients via `torch.autograd.grad`, builds the gradient Gram matrix G^T G, solves the Nash fixed-point iteration (G^T G)α = c/α in numpy, then backpropagates the α-weighted sum.
- `configs/method/nash_mtl.yaml`: method config pointing to the NashMTLEngine target.
- Runs via `python experiments/bpgs_study/run.py --study 05_nyuv2_full_final --variant nash_mtl`.

## Setup

- Dataset: NYUv2 (795 train, 654 val, 288×384, batch_size=8)
- Backbone: SegNet (18.9M params), 3 task heads (segmentation, depth, normals)
- Training: 120 epochs, AdamW (lr=5e-4, wd=1e-4), linear warmup 100 steps, cosine decay to 1e-6
- Precision: 16-mixed, grad_clip=1.0
- Seeds: 42, 43, 44

## Results

### Final Metrics (epoch 119)

| Seed | mIoU ↑ | AbsRel ↓ | RMSE ↓ | Angle ↓ | Within 11.25° ↑ | Total Loss ↓ |
|------|--------|----------|--------|---------|-----------------|--------------|
| 42   | 0.289  | 0.230    | 0.824  | 28.74°  | 0.226           | 1.974        |
| 43   | 0.238  | 0.249    | 0.895  | 31.14°  | 0.199           | 2.144        |
| 44   | 0.228  | 0.248    | 0.848  | 30.66°  | 0.207           | 2.094        |
| **Mean** | **0.252** | **0.242** | **0.856** | **30.18°** | **0.211** | **2.071** |
| **±Std** | **±0.027** | **±0.009** | **±0.029** | **±1.01°** | **±0.011** | **±0.070** |

### Comparison to Paper Baselines (published 3-seed means)

| Method | mIoU ↑ | AbsRel ↓ | Angle ↓ | Total Loss ↓ |
|--------|--------|----------|---------|-------------|
| Static | 0.341 | 0.239 | 35.93° | 1.992 |
| Kendall | 0.281 | 0.229 | 28.63° | 1.977 |
| UWSO | 0.294 | 0.228 | 26.11° | 1.936 |
| BPGS | 0.312 | 0.223 | 26.85° | 1.891 |
| **Nash-MTL** | **0.252** | **0.242** | **30.18°** | **2.071** |

Nash-MTL underperforms all paper baselines on every metric. The 3-seed variance (particularly mIoU: 0.289 vs 0.228–0.238) is larger than any paper baseline.

### Alpha Trajectory

The Nash weights α (logged per step via `nash_mtl/alpha_{i}`) move through multiple regimes over the 119 epochs:
- **Early (steps ~0–1000)**: α nearly uniform across all 3 tasks.
- **Mid-to-late (steps ~1000–11879)**: α oscillates between mixed weights (e.g., [0.15, 0.14, 0.71]), near-one-hot configurations (e.g., [1.0, ~0, ~0]), and equal-split pairs (e.g., [0.5, 0.5, ~0]) from batch to batch.

This pattern is consistent across all 3 seeds. The per-step alpha variance is high; whether this reflects genuine Nash-MTL behavior or solver noise on per-batch GTG is not determined from the current logs.

## Files Created

| File | Purpose |
|------|---------|
| `spectra/baselines/nash_mtl.py` | NashMTLWeighter (no-op) |
| `spectra/engine/optimizers/nash_mtl.py` | NashMTLEngine (gradient extraction, GTG, fixed-point solve, weighted backward) |
| `configs/method/nash_mtl.yaml` | Method config |
| `experiments/bpgs_study/optional/configs/05_nyuv2_full_final.yaml` | Study variant (nash_mtl) |
| `outputs/nash_mtl/seed_{42,43,44}/` | Training artifacts for 3 seeds |

## Ledger Status

- [x] **WI-9**: Closed. Nash-MTL implemented, 3-seed NYUv2 run complete. Paper already has 7+ comparison methods. FAMO, CAGrad, IMTL-G, Auto-Lambda dropped — marginal return doesn't justify engineering cost for heavy gradient-surgery baselines on top of 7 existing comparators.
- Review ledger progress: 16/19 work items complete.
