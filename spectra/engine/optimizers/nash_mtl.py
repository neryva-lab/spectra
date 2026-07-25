"""Nash-MTL gradient aggregation engine.

Computes per-task gradients, solves the Nash bargaining problem
for task weights a, then applies the weighted shared-gradient update.
"""

import logging
from typing import Any

import numpy as np
import torch
import torch.distributed as dist
import pytorch_lightning as pl

from spectra.engine.optimizers.base import OptimizationEngine

logger = logging.getLogger(__name__)


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
        debug: bool = False,
        debug_interval: int = 50,
        debug_max_steps: int = 10,
        debug_full_matrix: bool = False,
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
        if debug_interval <= 0:
            raise ValueError(f"debug_interval must be positive; got {debug_interval}.")
        if debug_max_steps < 0:
            raise ValueError(f"debug_max_steps must be non-negative; got {debug_max_steps}.")
        self.max_iter = max_iter
        self.tol = tol
        self.max_norm = max_norm
        self.update_weights_every = update_weights_every
        self.debug = debug
        self.debug_interval = debug_interval
        self.debug_max_steps = debug_max_steps
        self.debug_full_matrix = debug_full_matrix
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

    def _log_debug_stats(
        self,
        module: pl.LightningModule,
        gtg: torch.Tensor,
        raw_gtg: torch.Tensor,
        alpha: torch.Tensor,
        task_grads: list[list[torch.Tensor]],
        flat_grads: list[torch.Tensor],
        g_tensor: torch.Tensor,
        combined_grad: torch.Tensor,
        clip_factor: float,
    ) -> None:
        if not self.debug:
            return
        if self._step >= self.debug_max_steps:
            return
        if self._step % self.debug_interval != 0:
            return

        with torch.no_grad():
            gtg_cpu = gtg.detach().float().cpu()
            alpha_cpu = alpha.detach().float().cpu()
            row_sums = gtg_cpu.sum(dim=1)
            diag = torch.diag(gtg_cpu)
            off_diag = gtg_cpu - torch.diag_embed(diag)
            grad_norms = torch.tensor(
                [torch.cat([g.reshape(-1) for g in grads]).norm().item() for grads in task_grads],
                dtype=torch.float32,
            )
            task_finite = torch.tensor(
                [float(all(torch.isfinite(g).all().item() for g in grads)) for grads in task_grads],
                dtype=torch.float32,
            )
            flat_finite = torch.tensor(
                [float(torch.isfinite(g).all().item()) for g in flat_grads],
                dtype=torch.float32,
            )
            g_finite = float(torch.isfinite(g_tensor).all().item())
            raw_gtg_finite = float(torch.isfinite(raw_gtg).all().item())
            gtg_finite = float(torch.isfinite(gtg).all().item())
            logger.info(
                "[NashMTL debug] step=%s alpha=%s clip_factor=%.6f row_sums=%s diag=%s grad_norms=%s combined_norm=%.6f g_finite=%s raw_gtg_finite=%s gtg_finite=%s task_finite=%s flat_finite=%s",
                self._step,
                [float(x) for x in alpha_cpu.tolist()],
                clip_factor,
                [float(x) for x in row_sums.tolist()],
                [float(x) for x in diag.tolist()],
                [float(x) for x in grad_norms.tolist()],
                float(torch.linalg.norm(combined_grad).item()),
                g_finite,
                raw_gtg_finite,
                gtg_finite,
                [float(x) for x in task_finite.tolist()],
                [float(x) for x in flat_finite.tolist()],
            )

            module.log("nash_mtl/debug/row_sum_mean", row_sums.mean().item(), on_step=True, on_epoch=False, prog_bar=False)
            module.log("nash_mtl/debug/row_sum_std", row_sums.std(unbiased=False).item(), on_step=True, on_epoch=False, prog_bar=False)
            module.log("nash_mtl/debug/diag_mean", diag.mean().item(), on_step=True, on_epoch=False, prog_bar=False)
            module.log("nash_mtl/debug/diag_std", diag.std(unbiased=False).item(), on_step=True, on_epoch=False, prog_bar=False)
            module.log("nash_mtl/debug/grad_norm_mean", grad_norms.mean().item(), on_step=True, on_epoch=False, prog_bar=False)
            module.log("nash_mtl/debug/grad_norm_std", grad_norms.std(unbiased=False).item(), on_step=True, on_epoch=False, prog_bar=False)
            module.log("nash_mtl/debug/g_finite", g_finite, on_step=True, on_epoch=False, prog_bar=False)
            module.log("nash_mtl/debug/raw_gtg_finite", raw_gtg_finite, on_step=True, on_epoch=False, prog_bar=False)
            module.log("nash_mtl/debug/gtg_finite", gtg_finite, on_step=True, on_epoch=False, prog_bar=False)
            module.log("nash_mtl/debug/clip_factor", clip_factor, on_step=True, on_epoch=False, prog_bar=False)
            for i, value in enumerate(task_finite.tolist()):
                module.log(f"nash_mtl/debug/task_{i}_finite", value, on_step=True, on_epoch=False, prog_bar=False)
            for i, value in enumerate(flat_finite.tolist()):
                module.log(f"nash_mtl/debug/flat_{i}_finite", value, on_step=True, on_epoch=False, prog_bar=False)

            if self.debug_full_matrix:
                for i in range(gtg_cpu.shape[0]):
                    for j in range(gtg_cpu.shape[1]):
                        module.log(
                            f"nash_mtl/debug/gtg_{i}_{j}",
                            gtg_cpu[i, j].item(),
                            on_step=True,
                            on_epoch=False,
                            prog_bar=False,
                        )
                if gtg_cpu.shape[0] > 1:
                    row0 = gtg_cpu[0]
                    for i in range(1, gtg_cpu.shape[0]):
                        cos_like = torch.nn.functional.cosine_similarity(
                            row0.unsqueeze(0), gtg_cpu[i].unsqueeze(0), dim=1
                        ).item()
                        module.log(
                            f"nash_mtl/debug/gtg_row_cos_{i}",
                            cos_like,
                            on_step=True,
                            on_epoch=False,
                            prog_bar=False,
                        )

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
        flat_grads = [torch.cat([g.reshape(-1) for g in tg]).to(torch.float32) for tg in task_grads]
        flat_grads = [torch.nan_to_num(g, nan=0.0, posinf=0.0, neginf=0.0) for g in flat_grads]
        G = torch.stack(flat_grads)
        G = torch.nan_to_num(G, nan=0.0, posinf=0.0, neginf=0.0)
        G_cpu = G.detach().to(torch.float64).cpu()
        raw_GTG = G_cpu @ G_cpu.T
        raw_GTG = torch.nan_to_num(raw_GTG, nan=0.0, posinf=0.0, neginf=0.0)
        GTG = raw_GTG

        if module.trainer.world_size > 1 and dist.is_initialized():
            dist.all_reduce(GTG, op=dist.ReduceOp.SUM)
            GTG = GTG / dist.get_world_size()

        # 3. Normalize GTG for numerical stability
        norm_factor = torch.norm(GTG).detach() + 1e-8
        GTG_normalized = GTG / norm_factor

        # 4. Solve for Nash weights, or reuse the cached ones.
        if update_weights:
            alpha = self._solve_nash(GTG_normalized.detach().to(torch.float32))
        else:
            alpha = self._prvs_alpha.copy()
        self._step += 1
        alpha_tensor = torch.from_numpy(alpha).to(G.device, dtype=G.dtype)

        if not torch.isfinite(alpha_tensor).all():
            alpha_tensor = torch.full_like(alpha_tensor, 1.0 / K)
            alpha = alpha_tensor.detach().cpu().numpy()

        combined_flat_grad = torch.mv(G.T, alpha_tensor)
        clip_factor = 1.0
        if self.max_norm > 0:
            combined_norm = torch.linalg.norm(combined_flat_grad)
            if torch.isfinite(combined_norm) and combined_norm > self.max_norm:
                clip_factor = float((self.max_norm / (combined_norm + 1e-12)).item())
                combined_flat_grad = combined_flat_grad * clip_factor

        # 5. Backbone gradients: combine task gradients with Nash weights.
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
            if not hasattr(module, "heads") or task_name not in module.heads:
                continue
            head = module.heads[task_name]
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

        self._log_debug_stats(
            module=module,
            gtg=GTG_normalized,
            raw_gtg=raw_GTG,
            alpha=alpha_tensor,
            task_grads=task_grads,
            flat_grads=flat_grads,
            g_tensor=G,
            combined_grad=combined_flat_grad,
            clip_factor=clip_factor,
        )

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
