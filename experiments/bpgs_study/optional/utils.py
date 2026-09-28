from __future__ import annotations

from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent / "configs"
CONFIG_FILES = (
    "04_qm9_regime_check.yaml",
    "05_nyuv2_full_final.yaml",
    "09_nyuv2_overhead.yaml",
    "10_nyuv2_first_batch.yaml",
    "11_nyuv2_batch_size.yaml",
    "12_nyuv2_stop_gradient.yaml",
)
