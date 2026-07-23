"""Kendall uncertainty-weighting with L1-normalized weights (Ablation).

This is the critical ablation requested by the reviewer: standard Kendall
uncertainty weighting (Kendall et al. 2018) but with task weights
L1-normalized before application.  No bounded chart, no batch statistics,
no auto-calibration — just the normalization step that BPGS also uses
(Eq. 8 in the paper).

If this baseline recovers most of BPGS's rescaling-invariance, then the
bounded/batch-aware machinery is not earning its keep on the strongest
result and the paper's core contribution is undermined.
"""

from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn

from spectra.baselines.base import BaseWeighter


class NormalizedKendallWeighter(BaseWeighter):
    """Kendall uncertainty weighting with L1-normalized precision weights.

    Identical to ``KendallWeighter`` except that the raw precision weights
    ``0.5 * exp(-log_var_i)`` are L1-normalized to sum to 1 before being
    applied to the per-task losses.  The regularisation term
    ``0.5 * log_var_i`` is kept unchanged.

    This isolates the effect of normalization from the rest of BPGS's
    machinery (bounded chart, batch-aware statistics, auto-calibration).
    """

    def __init__(self, num_tasks: int, **kwargs):
        super().__init__(num_tasks)
        # Learnable log-variance per task, identical init to KendallWeighter
        self.log_vars = nn.Parameter(torch.zeros(num_tasks))

    def forward(
        self,
        losses: torch.Tensor,
        shared_params: Optional[List[nn.Parameter]] = None,
        sync_ddp: bool = True,
        raw_losses: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        # Raw precision weights (same as Kendall)
        precision = 0.5 * torch.exp(-self.log_vars)

        # ---- The ONLY difference from KendallWeighter ----
        # L1-normalize so weights sum to 1, mirroring BPGS Eq. (8).
        normalized_weights = precision / precision.sum()

        # Weighted loss + regularisation (unchanged from Kendall)
        weighted = normalized_weights * losses
        reg = 0.5 * self.log_vars
        total = (weighted + reg).sum()

        # Telemetry
        metrics: Dict[str, float] = {}
        for i in range(self.num_tasks):
            metrics[f"normalized_kendall/log_var_{i}"] = self.log_vars[i].item()
            metrics[f"normalized_kendall/raw_weight_{i}"] = precision[i].item()
            metrics[f"normalized_kendall/weight_{i}"] = normalized_weights[i].item()
        return total, metrics
