"""
run_kendall_norm_grid.py

Single-shot runner for the WI-3 Kendall + L1-normalization ablation grid.
Runs exp_09_kendall_norm_ablation at ×1, ×10, ×100, ×1000 scale multipliers
in a single invocation. Total: 4 multipliers × 3 methods × 3 seeds = 36 runs.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from hydra import compose, initialize_config_dir
from spectra.empirical.experiments import EXPERIMENT_REGISTRY
from spectra.empirical.utils import validate_empirical_config, EmpiricalRunContext

SCALE_MULTIPLIERS = [1, 10, 100, 1000]
EXPERIMENT_NAME = "exp_09_kendall_norm_ablation"
CONFIG_DIR = str(Path(root_dir, "configs", "empirical").resolve())

for multiplier in SCALE_MULTIPLIERS:
    print(f"\n{'='*60}")
    print(f"Running scale multiplier = ×{multiplier}")
    print(f"{'='*60}")

    overrides = [
        f"experiment={EXPERIMENT_NAME}",
        "runtime.epochs=20",
        "runtime.device=auto",
        f"experiment.training_stress.loss_scale_multiplier={multiplier}",
    ]

    with initialize_config_dir(config_dir=CONFIG_DIR):
        cfg = compose(config_name="config", overrides=overrides)

    validate_empirical_config(cfg)
    run_context = EmpiricalRunContext.from_config(cfg).initialize()
    logger = run_context.setup_logging()
    run_context.save_latest_pointer()
    run_context.save_resolved_config(cfg)
    run_context.save_run_metadata(cfg)

    logger.info("Starting scale multiplier ×%d", multiplier)
    EXPERIMENT_REGISTRY[EXPERIMENT_NAME](cfg, run_context, logger)
    logger.info("Completed scale multiplier ×%d", multiplier)

print(f"\n{'='*60}")
print("Grid complete — all multipliers done.")
print(f"{'='*60}")
