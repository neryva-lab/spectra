"""Kendall uncertainty-weighting with L1-normalized weights."""

from typing import Dict, List, Optional, Sequence, Tuple, Union

import torch
import torch.nn as nn

from spectra.baselines.kendall import KendallWeighter


class KendallNormWeighter(KendallWeighter):
    """Kendall-style uncertainty weighting with L1-normalized task weights.

    Same as KendallWeighter, but the precision weights are normalized to sum to 1
    before being applied to the task losses. This isolates the effect of L1
    normalization from the other components of BPGS (bounded chart, batch-awareness,
    split optimization).
    """

    def _loss_tensor(self, losses: Union[torch.Tensor, Sequence[torch.Tensor]]) -> torch.Tensor:
        if torch.is_tensor(losses):
            return losses
        return torch.stack(list(losses))

    def normalized_weights(self) -> torch.Tensor:
        """Return the L1-normalized precision weights used on the network loss."""
        precision = torch.exp(-self.log_vars)
        denom = precision.sum().clamp_min(torch.finfo(precision.dtype).eps)
        return precision / denom

    def network_loss(self, losses: Union[torch.Tensor, Sequence[torch.Tensor]]) -> torch.Tensor:
        """Loss term used to update the shared network parameters."""
        loss_tensor = self._loss_tensor(losses)
        weights = self.normalized_weights().detach()
        return (0.5 * weights * loss_tensor).sum()

    def uncertainty_loss(self, losses: Union[torch.Tensor, Sequence[torch.Tensor]]) -> torch.Tensor:
        """Standard Kendall uncertainty objective used to update log-variances."""
        loss_tensor = self._loss_tensor(losses).detach()
        precision = torch.exp(-self.log_vars)
        return (0.5 * (precision * loss_tensor + self.log_vars)).sum()

    def forward(
        self,
        losses: torch.Tensor,
        shared_params: Optional[List[nn.Parameter]] = None,
        sync_ddp: bool = True,
        raw_losses: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        total = self.network_loss(losses) + self.uncertainty_loss(losses)
        weights = self.normalized_weights().detach()

        metrics: Dict[str, float] = {}
        for i in range(self.num_tasks):
            metrics[f"kendall_norm/log_var_{i}"] = self.log_vars[i].item()
            metrics[f"kendall_norm/weight_{i}"] = weights[i].item()
        return total, metrics
