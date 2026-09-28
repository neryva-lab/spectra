"""
Hydra entrypoint for SPECTRA training experiments.

All orchestration is delegated to `spectra.train.runner`.
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

# --- Python 3.14 + Hydra compatibility patch ---
import argparse
def _patched_check_help(self, action):
    try:
        if action.help is not None and '%' not in action.help:
            pass
    except TypeError:
        pass  # Ignore LazyCompletionHelp TypeError in Python 3.14
argparse.ArgumentParser._check_help = _patched_check_help
# -----------------------------------------------

import hydra
from omegaconf import DictConfig
from hydra.core.hydra_config import HydraConfig

from spectra.train.runner import execute_training_mission

@hydra.main(config_path="../configs", config_name="config", version_base=None)
def main(cfg: DictConfig):
    output_dir = Path(HydraConfig.get().runtime.output_dir)
    execute_training_mission(cfg, output_dir)

if __name__ == "__main__":
    main()
