"""Nash-MTL gradient aggregation engine.

Computes per-task gradients, solves the Nash bargaining problem
for task weights a, then backpropagates the weighted sum.
Mirrors the structure of PCGradEngine.
"""

from typing import Any

import numpy as np
import torch
import torch.distributed as dist
import pytorch_lightning as pl

from spectra.engine.optimizers.base import OptimizationEngine


class NashMTLEngine(OptimizationEngine):
    """Solves (G^T G) a = 1 / a for the Nash bargaining solution.

    Uses fixed-point iteration (no external solver dependencies), with
    optional state reuse and max-norm clipping to match the published
    algorithm more closely.
    """

    def __init__(
        self,
        max_iter: int = 50,
        tol: float = 1e-8,
        max_norm: float = 1.0,
        update_weights_every: int = 1,
    ):
        super().__init__()
        if max_iter <= 0:
            raise ValueError(f"max_iter must be positive; got {max_iter}.")
        if tol <= 0:
            raise ValueError(f"tol must be positive; got {tol}.")
        if max_norm < 0:
            raise ValueError(f"max_norm must be non-negative; got {max_norm}.")
        if update_weights_every <= 0:
            raise ValueError(f"update_weights_every must be positive; got {update_weights_every}.")
        self.max_iter = max_iter
        self.tol = tol
        self.max_norm = max_norm
        self.update_weights_every = update_weights_every
        self._prvs_alpha = None
        self._step = 0

    def setup(self, module: pl.LightningModule) -> None:
        module.automatic_optimization = False

    def _solve_nash(self, gtg: torch.Tensor) -> np.ndarray:
        K = gtg.shape[0]
        gtg_np = gtg.cpu().numpy()

        if self._prvs_alpha is not None:
            alpha = self._prvs_alpha.copy()
        else:
            alpha = np.ones(K, dtype=np.float64) / K

        for _ in range(self.max_iter):
            v = gtg_np @ alpha
            v = np.maximum(v, 1e-12)
            alpha_new = 1.0 / v
            alpha_new = alpha_new / alpha_new.sum()

            if not np.isfinite(alpha_new).all():
                alpha_new = np.ones(K, dtype=np.float64) / K

            if np.linalg.norm(alpha_new - alpha) < self.tol:
                alpha = alpha_new
                break
            alpha = alpha_new

        if not np.isfinite(alpha).all():
            alpha = np.ones(K, dtype=np.float64) / K

        self._prvs_alpha = alpha.astype(np.float64).copy()
        return alpha.astype(np.float32)

    def reset(self) -> None:
        self._prvs_alpha = None
        self._step = 0

    def backward_and_step(
        self,
        module: pl.LightningModule,
        batch_idx: int,
        losses: Any,
        total_loss: torch.Tensor,
        optimizers: Any,
        lr_schedulers: Any,
    ) -> torch.Tensor:
        opt = optimizers if not isinstance(optimizers, list) else optimizers[0]
        sch = None
        if lr_schedulers:
            sch = lr_schedulers if not isinstance(lr_schedulers, list) else lr_schedulers[0]

        opt.zero_grad()

        scaler = getattr(module.trainer.precision_plugin, "scaler", None)
        raw_opt = opt.optimizer if hasattr(opt, "optimizer") else opt

        shared_params = list(module.backbone.parameters())
        weighted_task_loss_list = list(losses.values())
        K = len(weighted_task_loss_list)

        update_weights = (self._prvs_alpha is None) or (self._step % self.update_weights_every == 0)

        # 1. Per-task backbone gradients
        task_grads = []
        for task_loss in weighted_task_loss_list:
            loss_scaled = scaler.scale(task_loss) if scaler is not None else task_loss
            grads = torch.autograd.grad(
                loss_scaled, shared_params,
                retain_graph=True, allow_unused=True,
            )
            grads = [g if g is not None else torch.zeros_like(p) for g, p in zip(grads, shared_params)]
            task_grads.append(grads)

        # 2. Flatten and stack into G, compute GTG
        flat_grads = [torch.cat([g.reshape(-1) for g in tg]) for tg in task_grads]
        G = torch.stack(flat_grads)
        GTG = G @ G.T

        if module.trainer.world_size > 1 and dist.is_initialized():
            dist.all_reduce(GTG, op=dist.ReduceOp.SUM)
            GTG = GTG / dist.get_world_size()

        # 3. Normalize GTG for numerical stability
        norm_factor = torch.norm(GTG).detach() + 1e-8
        GTG_normalized = GTG / norm_factor

        # 4. Solve for Nash weights, or reuse the cached ones.
        if update_weights:
            alpha = self._solve_nash(GTG_normalized.detach())
        else:
            alpha = self._prvs_alpha.copy()
        self._step += 1
        alpha_tensor = torch.from_numpy(alpha).to(G.device, dtype=G.dtype)

        if not torch.isfinite(alpha_tensor).all():
            alpha_tensor = torch.full_like(alpha_tensor, 1.0 / K)
            alpha = alpha_tensor.detach().cpu().numpy()

        if self.max_norm > 0:
            combined_grad = torch.mv(G.T, alpha_tensor)
            combined_norm = torch.linalg.norm(combined_grad)
            if torch.isfinite(combined_norm) and combined_norm > self.max_norm:
                alpha_tensor = alpha_tensor * (self.max_norm / (combined_norm + 1e-12))
                alpha = alpha_tensor.detach().cpu().numpy()

        # 5. Backbone gradients: combine task gradients with Nash weights.
        combined_flat_grad = torch.mv(G.T, alpha_tensor)
        offset = 0
        for param in shared_params:
            numel = param.numel()
            grad_slice = combined_flat_grad[offset: offset + numel].reshape(param.shape).to(param.dtype)
            if param.grad is None:
                param.grad = grad_slice.clone()
            else:
                param.grad.copy_(grad_slice)
            offset += numel

        # 6. Head gradients: each head receives its own task loss gradient.
        for i, task_name in enumerate(module.task_names):
            head = module.heads.get(task_name) if hasattr(module, "heads") else None
            if head is None:
                continue
            head_params = list(head.parameters())
            if not head_params:
                continue
            loss_scaled = scaler.scale(weighted_task_loss_list[i]) if scaler is not None else weighted_task_loss_list[i]
            is_last_head = (i == len(module.task_names) - 1)
            head_grads = torch.autograd.grad(
                loss_scaled,
                head_params,
                retain_graph=not is_last_head,
                allow_unused=True,
            )
            for param, grad in zip(head_params, head_grads):
                if grad is not None:
                    grad = grad.to(param.dtype)
                    if param.grad is None:
                        param.grad = grad.clone()
                    else:
                        param.grad.copy_(grad)

        # 7. Unscale if AMP
        if scaler is not None:
            scaler.unscale_(raw_opt)

        # 8. DDP sync: the Nash weights are synchronized above through GTG.
        #    Shared/head grads are assigned manually, so all-reduce must happen
        #    through the wrapped optimizer/strategy in the caller if needed.

        # 9. Gradient clipping
        if module.cfg.train.get("grad_clip", 0) > 0:
            module.clip_gradients(opt, gradient_clip_val=module.cfg.train.grad_clip)

        # 10. Optimizer + scheduler step
        if scaler is not None:
            old_scale = scaler.get_scale()
            scaler.step(raw_opt)
            scaler.update()
            if sch is not None and scaler.get_scale() >= old_scale:
                sch.step()
        else:
            opt.step()
            if sch is not None:
                sch.step()

        # 11. Logging
        for i, a in enumerate(alpha):
            module.log(f"nash_mtl/alpha_{i}", a, on_step=True, on_epoch=False, prog_bar=False)
        if sch is not None:
            module.log("lr", sch.get_last_lr()[0], on_step=True, on_epoch=False, prog_bar=False)

        return sum(weighted_task_loss_list).detach()
