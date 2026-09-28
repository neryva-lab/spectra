"""Nash-MTL baseline: Multi-Task Learning as a Bargaining Game (Navon et al., ICML 2022)."""

from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn

from spectra.baselines.base import BaseWeighter


class NashMTLWeighter(BaseWeighter):
    """Nash-MTL weighting via Nash bargaining solution over per-task gradients.

    The forward() is a no-op (returns losses.sum()) because the actual
    Nash weight computation happens inside NashMTLEngine. This follows
    the same pattern as PCGradWeighter.
    """

    def __init__(self, num_tasks: int, **kwargs):
        super().__init__(num_tasks)

    def forward(
        self,
        losses: torch.Tensor,
        shared_params: Optional[List[nn.Parameter]] = None,
        sync_ddp: bool = True,
        raw_losses: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        return losses.sum(), {}
