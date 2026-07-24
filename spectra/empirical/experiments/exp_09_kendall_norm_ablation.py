"""
exp_09_kendall_norm_ablation: Kendall + L1-normalization vs BPGS on scale-stress grid.

Runs the rescaling family with bpgs, kendall, and kendall_norm to determine
whether L1-normalization alone explains BPGS's scale robustness.
"""

from __future__ import annotations

import logging
from typing import Dict

from omegaconf import DictConfig

from spectra.empirical.experiments.common import run_single_experiment


def run(cfg: DictConfig, run_context: object, logger: logging.Logger) -> Dict[str, object]:
    return run_single_experiment(cfg, run_context, logger)
