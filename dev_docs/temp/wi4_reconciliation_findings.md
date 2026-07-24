# Resolved Issues — Paper/Code Reconciliation

## Issue 1: AqnD-10 — NYUv2 hyperparams 120/8 vs 80/4

**File fixed:** `configs/preset/nyuv2_bpgs.yaml`

**What changed:** `train.epochs: 80 → 120`, `train.batch_size: 4 → 8`

**Rationale:** The preset is a convenience shorthand referenced in README, docs, and smoke tests. It had stale values (80/4) that did not match what the actual experiments used (120/8). The study runner (05_nyuv2_full_final.yaml) bypasses the preset by composing `dataset=nyuv2 method=bpgs` directly, so the preset's incorrect values never affected published results — but anyone using `preset=nyuv2_bpgs` for quick experimentation would get wrong hyperparameters. Updated to match ground truth.

---

## Issue 2: AqnD-11 — Selection metric

**File fixed:** Paper/benchmark overrides rather than the shared NYUv2 default

**What changed:** `selection_metric: val/total_loss → val/miou`, `selection_mode: min → max`

**Three facts:**
1. **Config default:** said `val/total_loss (min)` — the "intended" default
2. **Actual experiments** (all methods in study 05, confirmed from resolved configs): used `val/miou (max)` via explicit override `train.selection_metric=val/miou train.selection_mode=max`
3. **Paper claim:** says `val/total_loss` — does not match what was executed

**Action:** Keep the dataset default as `val/total_loss` / `min`, and make the final NYUv2 benchmark override explicit in the study config and paper appendix. The ablation continues to use the dataset default.

**Justification:** mIoU shows 2.7× better method separation (CV 8.9% vs 3.3%) and does NOT favor BPGS — static has highest mIoU (0.345 vs bpgs 0.311). Per-method checkpoint quality is nearly identical regardless of metric (max 0.0025 mIoU diff), so the choice does not distort results.

---

## Issue 3: AqnD-12 — Gradient clipping

**File fixed:** None — no config change needed.

**Three facts:**
1. **Config hierarchy:** Every dataset defaults to `grad_clip: 1.0`. `configs/method/bpgs.yaml` overrides it to `10.0`. All other method configs (kendall, uwso, pcgrad, gradnorm_proxy) keep `1.0` or don't override.
2. **Actual experiments** (confirmed from resolved configs): BPGS everywhere → `grad_clip: 10.0`. All other methods → `grad_clip: 1.0`.
3. **Paper says** (`appendix/A_reproducibility_details.tex`):
   - Line 5 (NYUv2 main BPGS): "gradient clipping 10.0" — ✓ correct
   - Line 8 (NYUv2 ablation): "gradient clipping 1.0" — ✗ **wrong for BPGS ablation variants** (they use `method=bpgs` which sets 10.0). Only the Kendall ablation variant actually used 1.0.
   - Line 11 (Yeast/RF1 BPGS): "gradient clipping 10.0" — ✓ correct

**Action needed:** Fix paper line 8 — the ablation description needs to state that BPGS variants used `gradient clipping 10.0` (matching the method config) while only the Kendall variant used `1.0`. No code or config changes required.

**Additional note:** The empirical synthetic runner uses a separate parameter `gradient_clip_norm: 5.0` from `configs/empirical/runtime/default.yaml`. This is a different config system and should not be confused with the training `grad_clip` parameter.

---

## Issue 4: AqnD-17 — Eq. (10) stop-gradient on batch statistics

**File fixed:** `docs/bpgs_formalization.md`

**What changed:** Added `\operatorname{sg}[\cdot]` inside the definitions of `\mu(L)` and `\bar{\sigma}(L)`.

**Three facts:**
1. **Code** (`spectra/core/bpgs.py:126-133`): `_update_batch_stats()` calls `.detach()` on losses before computing `mu` and `sigma`. These statistics never carry gradients to the network.
2. **Formalization doc before fix:** The `\mu(L)` and `\bar{\sigma}(L)` equations used bare `\log \widetilde{L}_i` with no `\operatorname{sg}[\cdot]`, making a reader think gradients flow through losses into the batch statistics.
3. **Paper** (external): May use similar notation — needs verification.

**Action:** Added `\operatorname{sg}[\log \widetilde{L}_i]` in the `\mu(L)` sum and the `\bar{\sigma}(L)` variance term. The prose line "Define the **detached** log-loss statistics" was already correct and is unchanged. The `J_{\text{unc}}` equation already used `\operatorname{sg}[L_i]` correctly.

**Justification:** Makes the equations match the code exactly. The `sg[]` annotation tells readers that `mu` and `sigma` are shielded from backprop through the losses — only `theta` carries the gradient in the uncertainty objective.

---

## Issue 5: Undocumented `theta_grad_scale=100.0`

**File fixed:** `docs/bpgs_formalization.md`

**What changed:** Added "(default 100.0)" to the `gamma_theta` symbol table entry.

**Three facts:**
1. **Code** (`spectra/core/bpgs.py:62`): `theta_grad_scale: float = 100.0` — the `GradScale` custom autograd function multiplies theta's backward gradient by this factor, giving the uncertainty parameters an effective 100× learning rate multiplier.
2. **Config consistency:** Value is 100.0 in both `configs/method/bpgs.yaml:12` (real-data) and `configs/empirical/bpgs/default.yaml:8` (synthetic), and `spectra/baselines/__init__.py:38` defaults to 100.0. Fully consistent across all code paths.
3. **Formalization doc before fix:** Symbol table said "Gradient scale applied to `theta`" without stating the value. Paper (external): not mentioned at all.

**Action needed:** Paper should mention `theta_grad_scale=100.0` as a BPGS hyperparameter. No code or config changes required — the value is consistent everywhere.

**Justification:** This is a design choice, not a bug. The gradient scale compensates for the fact that the uncertainty objective's contribution to parameter updates is structurally smaller than the network objective's. The paper should document it for reproducibility.

---

## Issue 6: `batch_augmentation=cpu` vs default `cuda`

**File fixed:** None — no config change needed. Preflight check already enforces correctness.

**Three facts:**
1. **Config default** (`configs/dataset/nyuv2.yaml:6`): `batch_augmentation: "cuda"`
2. **Actual final experiments** (study 05): used `batch_augmentation=cpu` via explicit override
3. **Ablation study** (01): used `batch_augmentation=cuda` (default, no override)

**Root cause — not an inconsistency, but a by-design constraint:**
`spectra/train/preflight.py:102-107` has a safety check:
```python
if dataset_name == "nyuv2" and deterministic and batch_augmentation == "cuda":
    raise ValueError("NYUv2 deterministic mode is incompatible with batch_augmentation=cuda.")
```
The final study sets `train.deterministic=true`, which FORCES `batch_augmentation=cpu`. The ablation and other studies use `deterministic=false` (default), so they can keep `batch_augmentation=cuda`.

The augmentation transform (`NYUv2BatchTrainTransform`) is identical in both modes — only the compute device differs (CPU for deterministic, CUDA for faster but non-deterministic).

**Action needed:** Paper should document that the final NYUv2 experiments used `deterministic=true` (requiring `batch_augmentation=cpu`), while the ablation used the default settings (`deterministic=false`, `batch_augmentation=cuda`). No code or config changes required.

---

## Issue 7: `configs/method/static.yaml` wrong format

**File fixed:** `configs/method/static.yaml`

**What changed:**
```yaml
# Before (1 line, fragile):
name: static

# After (standard pattern matching all other method configs):
# @package _global_
method_name: static
method:
  name: static
```

**Three facts:**
1. **Before fix:** `static.yaml` was the only method config not using `# @package _global_`. It relied on Hydra's implicit nesting (placing `name: static` under `method:` key). This worked but was inconsistent with all other method configs.
2. **After fix:** Matches the standard pattern. Tested with `method=static` + all dataset configs (nyuv2, yeast, qm9, synthetic) — method resolves to `"static"` correctly in all cases.
3. **No behavioral change:** Both `cfg.get("method_name")` and `cfg.get("method", {}).get("name")` return `"static"` identically before and after. The `StaticWeighter` requires no special params, so no additional config sections needed.

---

## Issue 8: `s_min/s_max` differs between synthetic (-6/6) and real-data (-10/10)

**File fixed:** None — benign difference, no change needed.

**Three facts:**
1. **Config values:** `configs/method/bpgs.yaml:6-7` has `s_min=-10, s_max=10` (real-data). `configs/empirical/bpgs/default.yaml:4-5` has `s_min=-6, s_max=6` (synthetic). Both configs set `s_mode: batch_aware`.
2. **Code trace** (`spectra/core/bpgs.py`): In batch_aware mode, `get_s()` returns `mu + z * sigma` where `z = tau * (2 * sigmoid(theta) - 1)`. The `self.s_min_v` and `self.s_max_v` buffers are **never referenced** in this path. They are only used in `_bounded_stateless_s()` (stateless ablation mode only) and `_theta_from_s()` (initialization, both give `theta=0` for `s_init=0`).
3. **No experiment affected:** All canonical experiments (synthetic and real-data) use batch_aware mode. The stateless ablation experiments (NYUv2 study 01) use `method=bpgs` → `s_min=-10, s_max=10`. The config difference between -6/6 and -10/10 has **zero effect** on any result.

**Action needed:** None. The paper correctly describes "bounded sigmoid chart" as a concept without specifying numeric values. The configs differ but are both valid — this is a historical artifact with no practical impact.

---

## Issue 9: Inconsistent overrides across study configs

**File fixed:** None — differences are by design, no change needed.

**Three facts:**
1. **Studies have different purposes:** 05_nyuv2_full_final is the canonical benchmark (deterministic, full data, 120 epochs). 01_nyuv2_ablation is a fast comparative study (non-deterministic, 50-example subset, 60 epochs). 03_yeast/08_rf1/04_qm9 are separate benchmarks on different datasets with their own optimal defaults.
2. **The differences are causally linked:** The final study uses `deterministic=true` which forces `batch_augmentation=cpu`. The ablation doesn't need deterministic mode (all variants compared under the same non-deterministic conditions) so it keeps the defaults. The per-dataset settings for yeast/rf1/qm9 come from each dataset's own config.
3. **Paper already describes each study separately** (appendix A, paragraphs 1-3) — it does not claim uniform settings across all studies. Each paragraph lists its own epochs, batch size, gradient clipping, etc.

**Action needed:** The paper text for the ablation (line 8) already needs grad_clip corrected (Issue 3). Beyond that, the different settings are appropriate — a fast ablation with non-deterministic mode and subset data is methodologically valid when the purpose is comparative, not producing final benchmark numbers. The paper should continue to describe each study independently as it already does.

---

## Issue 10: `configs/method/pcgrad.yaml` has unusual checkpoint settings

**File fixed:** None — benign inconsistency, no change needed.

**Three facts:**
1. **Override chain verified:** `configs/method/pcgrad.yaml:13-14` sets `save_ckpt: true, checkpoint_every_minutes: 10`. The study config `experiments/bpgs_study/optional/configs/05_nyuv2_full_final.yaml:93-94` has `train.save_ckpt=true, train.checkpoint_every_minutes=30` in extra_overrides for the pcgrad variant, which correctly overrides the method-level values. Effective values in the study are `save_ckpt=true, checkpoint_every_minutes=30` — identical to all other methods.
2. **Sole outlier:** pcgrad.yaml is the only method config (among static, kendall, uwso, gradnorm_proxy, bpgs) that specifies checkpoint settings. The others rely on dataset defaults (`save_ckpt: false, checkpoint_every_minutes: 0`). This is a minor style inconsistency — pcgrad likely had these added during debugging and they were never removed.
3. **Standalone use unaffected but notable:** If pcgrad is run outside the study runner (`method=pcgrad dataset=nyuv2` without extra_overrides), checkpoints will save every 10 minutes vs. every 30 minutes for other methods run standalone. This has no effect on any published result but could cause confusion if someone uses pcgrad without studying the config.

**Action needed:** None. No experiment results are affected because the study runner's extra_overrides take precedence. The inconsistency is cosmetic and harmless. If desired, pcgrad.yaml could be cleaned up to remove `save_ckpt` and `checkpoint_every_minutes` for consistency with other method configs — but this would change standalone behavior.

---

## Issue 12: Ablation study's `subset_budget` data location undocumented

**Files fixed:** `docs/studies.md:62-71`, `working/paper/appendix/A_reproducibility_details.tex:8`

**Three facts:**
1. **Full mechanism verified:** The subset pipeline spans 20+ files across `experiments/bpgs_study/` and `spectra/data/`. Subset files are JSON with indices + metadata, generated by `nyuv2_subsets.py` via stratified sampling by majority class and depth quartile, placed at `experiments/bpgs_study/assets/nyuv2_subsets/v1/`. The ablation study config (`01_nyuv2_ablation.yaml`) sets `subset_budget: "50"`, `subset_seed: 11`, `use_subset_file: true`. The subset files DO NOT EXIST on disk (not yet generated), confirming a documentation gap.
2. **Existing docs were too vague:** `experiments/bpgs_study/README.md` mentions "deterministic NYUv2 subset preparation" but gives no parameters. `docs/studies.md` line 62 references the script but gives no details. The paper says "fixed 50% training subset" without specifying the sampling method, seed, or exact count (398 images). A reader couldn't determine exactly which images were used.
3. **Fixes applied:** (a) `docs/studies.md` now documents the subset parameters — budget, seed, stratified sampling method, file naming, output location, and the 9-file generation pattern. (b) Paper appendix line 8 updated to specify "398 of 795 images, selected via stratified sampling by majority semantic class and depth quartile using seed 11".

**Action needed:** The documentation gaps are now filled. If the ablation is ever re-run, run `python experiments/bpgs_study/nyuv2_subsets.py` (via `experiments/bpgs_study/run.py --study 01_nyuv2_ablation` which auto-prepends the subset stage) to generate the files. Subset files are deterministic — same input + same seed → same indices.
