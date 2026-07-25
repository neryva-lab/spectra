"""
Multi-task learning weighter registry.
(Redirected to spectra.baselines to eliminate duplication).
"""

from spectra.baselines import (
    BaseWeighter,
    StaticWeighter,
    KendallWeighter,
    UWSOWeighter,
    PCGradWeighter,
    GradNormProxyWeighter,
    NashMTLWeighter,
    build_weighter,
    WEIGHTER_REGISTRY
)

__all__ = [
    "BaseWeighter", "StaticWeighter", "KendallWeighter",
    "UWSOWeighter", "PCGradWeighter", "GradNormProxyWeighter", "NashMTLWeighter",
    "WEIGHTER_REGISTRY", "build_weighter",
]
