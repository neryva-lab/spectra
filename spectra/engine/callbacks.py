"""
Gradient health monitoring callback.
"""

import logging
import time
from typing import Any, Dict

import torch
import torch.nn as nn
import pytorch_lightning as pl

logger = logging.getLogger("spectra.callbacks")


class GradientHealthCallback(pl.Callback):
    """
    Real-time gradient health monitoring for the shared backbone.

    Monitors:
        1. Backbone total gradient L2 norm (absolute signal strength)
        2. Per-group update-to-weight ratio (‖grad‖/‖param‖)
           Healthy range: ~0.001. <1e-4 = vanishing, >0.1 = exploding.
        3. Gradient spike detection (running-average-based): warns when current norm
           exceeds 5× the running average. This catches instability before NaN.

    Runs every `check_interval` optimizer steps. Zero overhead in between.

    Note: Uses on_before_optimizer_step (Lightning hook on Callback),
    which fires after backward() but before optimizer.step() — exactly
    when gradients are populated and can be read without side effects.
    """

    def __init__(self, check_interval: int = 50, spike_threshold: float = 5.0):
        """
        Args:
            check_interval: Log every N optimizer steps.
            spike_threshold: Log a warning when norm > spike_threshold × running average.
        """
        super().__init__()
        self.check_interval  = check_interval
        self.spike_threshold = spike_threshold
        self._grad_norm_avg: float = -1.0  # Uninitialized
        self._warned_this_epoch = set()   # Track conditions to prevent terminal spam

    def on_train_epoch_start(self, trainer: pl.Trainer, pl_module: pl.LightningModule) -> None:
        self._warned_this_epoch.clear()

    def _track_grad_health(self, trainer: pl.Trainer, pl_module: pl.LightningModule):
        # Skip Step 0 and respect interval to avoid initialization noise
        if trainer.global_step == 0 or trainer.global_step % self.check_interval != 0:
            return

        backbone = getattr(pl_module, "backbone", None)
        if backbone is None:
            return

        #  1. Backbone total gradient norm 
        squared_norms = []
        param_norms   = []
        for p in backbone.parameters():
            if p.grad is not None and p.requires_grad:
                gn = p.grad.data.norm(2).item()
                pn = p.data.norm(2).item()
                squared_norms.append(gn ** 2)
                if pn > 1e-8:
                    param_norms.append((gn, pn))

        if not squared_norms:
            return

        total_grad_norm = sum(squared_norms) ** 0.5
        # Set prog_bar=True for high-visibility telemetry
        pl_module.log("health/backbone_grad_norm", total_grad_norm, sync_dist=False, prog_bar=True)

        # 2. Mean update-to-weight ratio 
        if param_norms:
            ratios = [gn / pn for gn, pn in param_norms]
            mean_grad_weight_ratio = sum(ratios) / len(ratios)
            
            # Actual update scales with the learning rate!
            # Multi-parameter-group LR averaging
            # Safely extract mean LR across all param groups whether Automatic or Manual.
            current_lr = 1e-3
            try:
                optimizers = getattr(pl_module, "optimizers", lambda: None)()
                if optimizers is not None:
                    opts = optimizers if isinstance(optimizers, list) else [optimizers]
                    lrs = []
                    for opt in opts:
                        # Unwrap LightningOptimizer if necessary
                        opt_inner = opt.optimizer if hasattr(opt, "optimizer") else opt
                        if hasattr(opt_inner, "param_groups"):
                            for pg in opt_inner.param_groups:
                                if "lr" in pg:
                                    lrs.append(pg["lr"])
                    if lrs:
                        current_lr = sum(lrs) / len(lrs)
            except (RuntimeError, TypeError, AttributeError):
                pass # Silently fallback to 1e-3 if extraction fails

            true_update_ratio = mean_grad_weight_ratio * current_lr
            pl_module.log("health/update_weight_ratio", true_update_ratio, sync_dist=False, prog_bar=False)

            # Flag to W&B for EASY monitoring. Terminal warnings are RATE-LIMITED.
            if true_update_ratio < 1e-6:
                if "vanishing" not in self._warned_this_epoch:
                    pl_module.print(
                        f"[GradHealth] Step {trainer.global_step}: ratio {true_update_ratio:.2e} "
                        f"is very small — possible vanishing gradient. (Silencing further warnings this epoch)"
                    )
                    self._warned_this_epoch.add("vanishing")
            elif true_update_ratio > 0.1:
                if "exploding" not in self._warned_this_epoch:
                    pl_module.print(
                        f"[GradHealth] Step {trainer.global_step}: ratio {true_update_ratio:.2e} "
                        f"is large — possible exploding gradient. (Silencing further warnings this epoch)"
                    )
                    self._warned_this_epoch.add("exploding")

        # 3. Spike detection (running-average-based)
        if self._grad_norm_avg < 0:
            self._grad_norm_avg = total_grad_norm
        else:
            self._grad_norm_avg = 0.99 * self._grad_norm_avg + 0.01 * total_grad_norm

        spike_ratio = total_grad_norm / (self._grad_norm_avg + 1e-8)
        if spike_ratio > self.spike_threshold:
            if "spike" not in self._warned_this_epoch:
                pl_module.print(
                    f"[GradSpike] Step {trainer.global_step}: grad_norm={total_grad_norm:.4f} "
                    f"is {spike_ratio:.1f}x running_avg. Watch for instability. (Silencing per-step)"
                )
                self._warned_this_epoch.add("spike")
            pl_module.log("health/grad_spike_ratio", spike_ratio, sync_dist=False)

    def on_before_optimizer_step(
        self, trainer: pl.Trainer, pl_module: pl.LightningModule, optimizer: Any
    ):
        # Only use this hook for AUTOMATIC optimization
        if getattr(pl_module, "automatic_optimization", True):
            self._track_grad_health(trainer, pl_module)

    def on_train_batch_end(
        self, trainer: pl.Trainer, pl_module: pl.LightningModule, outputs: Any, batch: Any, batch_idx: int
    ):
        # Only use this hook for MANUAL optimization (PCGrad)
        if not getattr(pl_module, "automatic_optimization", True):
            self._track_grad_health(trainer, pl_module)

        # 4. Weighter-specific health (B-PGS theta saturation) 
        weighter = getattr(pl_module, "weighter", None)
        if weighter is not None and hasattr(weighter, "theta"):
            theta_abs_max = weighter.theta.data.abs().max().item()
            pl_module.log("health/bpgs_theta_max", theta_abs_max, sync_dist=False)
            if theta_abs_max > 10.0:
                logger.warning(
                    f"[GradHealth] B-PGS theta saturation: max|θ|={theta_abs_max:.2f}. "
                    f"Sigmoid is nearly flat here — B-PGS update is slowing."
                )


# Backward-compatible alias (train.py imports this name)
NTKGradExplosionTracker = GradientHealthCallback


class RuntimeOverheadCallback(pl.Callback):
    """Measure per-epoch wall-clock time and peak CUDA memory.

    This callback is intended for lightweight overhead studies where we
    want to compare methods like BPGS and Kendall under identical
    benchmark settings.
    """

    def __init__(self) -> None:
        super().__init__()
        self._epoch_start_time: float | None = None
        self._epoch_seconds: list[float] = []
        self._peak_cuda_mem_bytes: list[int] = []
        self._trainable_param_count: int | None = None
        self._total_param_count: int | None = None
        self._device: str | None = None

    def on_fit_start(self, trainer: pl.Trainer, pl_module: pl.LightningModule) -> None:
        self._trainable_param_count = sum(
            p.numel() for p in pl_module.parameters() if p.requires_grad
        )
        self._total_param_count = sum(p.numel() for p in pl_module.parameters())
        device = getattr(pl_module, "device", None)
        self._device = str(device) if device is not None else None

    def on_train_epoch_start(self, trainer: pl.Trainer, pl_module: pl.LightningModule) -> None:
        if torch.cuda.is_available() and getattr(pl_module, "device", None) is not None:
            device = pl_module.device
            if str(device).startswith("cuda"):
                torch.cuda.reset_peak_memory_stats(device)
                torch.cuda.synchronize(device)
        self._epoch_start_time = time.perf_counter()

    def on_train_epoch_end(self, trainer: pl.Trainer, pl_module: pl.LightningModule) -> None:
        if self._epoch_start_time is None:
            return

        if torch.cuda.is_available() and getattr(pl_module, "device", None) is not None:
            device = pl_module.device
            if str(device).startswith("cuda"):
                torch.cuda.synchronize(device)
                peak_bytes = int(torch.cuda.max_memory_allocated(device))
            else:
                peak_bytes = 0
        else:
            peak_bytes = 0

        elapsed = time.perf_counter() - self._epoch_start_time
        self._epoch_seconds.append(float(elapsed))
        self._peak_cuda_mem_bytes.append(peak_bytes)
        self._epoch_start_time = None

    def build_summary(self) -> Dict[str, Any]:
        """Return aggregated runtime-overhead statistics."""
        if self._epoch_seconds:
            epoch_arr = torch.tensor(self._epoch_seconds, dtype=torch.float64)
            mean_seconds = float(epoch_arr.mean().item())
            median_seconds = float(epoch_arr.median().item())
            std_seconds = float(epoch_arr.std(unbiased=False).item())
            max_seconds = float(epoch_arr.max().item())
            min_seconds = float(epoch_arr.min().item())
        else:
            mean_seconds = None
            median_seconds = None
            std_seconds = None
            max_seconds = None
            min_seconds = None

        if self._peak_cuda_mem_bytes:
            peak_bytes = max(self._peak_cuda_mem_bytes)
            peak_mb = float(peak_bytes / (1024 ** 2))
        else:
            peak_mb = None

        return {
            "epoch_seconds": list(self._epoch_seconds),
            "peak_cuda_mem_mb_per_epoch": [
                float(v / (1024 ** 2)) for v in self._peak_cuda_mem_bytes
            ],
            "mean_epoch_seconds": mean_seconds,
            "median_epoch_seconds": median_seconds,
            "std_epoch_seconds": std_seconds,
            "min_epoch_seconds": min_seconds,
            "max_epoch_seconds": max_seconds,
            "peak_cuda_mem_mb": peak_mb,
            "trainable_param_count": self._trainable_param_count,
            "total_param_count": self._total_param_count,
            "device": self._device,
            "num_epochs": len(self._epoch_seconds),
        }
