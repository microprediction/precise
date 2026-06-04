"""Registry of online covariance estimators.

Mirrors the convention of ``sklearn.utils.all_estimators`` and the
``allcorrgens``/``allvargens`` registries in the sibling ``randomcov`` package, so the
conformance test and the ``research/`` bake-offs can iterate over every estimator uniformly.
"""

from __future__ import annotations

from precise.adaptive import AdaptiveEwaCovariance
from precise.base import BaseOnlineCovariance
from precise.dcc import DCCCovariance
from precise.diagonal import DiagonalCovariance
from precise.empirical import EmpiricalCovariance
from precise.ewa import EwaCovariance
from precise.factor import FactorCovariance
from precise.geodesic import GeodesicEwaCovariance
from precise.huber import HuberCovariance
from precise.ledoitwolf import LedoitWolfCovariance
from precise.oas import OASCovariance
from precise.partialmoments import PartialMomentsCovariance
from precise.shrunk import ShrunkCovariance
from precise.tyler import TylerCovariance

# The shipped positional estimators. Add new estimator classes here (one line each).
_REGISTRY: list[type[BaseOnlineCovariance]] = [
    EmpiricalCovariance,
    DiagonalCovariance,
    EwaCovariance,
    AdaptiveEwaCovariance,
    LedoitWolfCovariance,
    OASCovariance,
    ShrunkCovariance,
    PartialMomentsCovariance,
    HuberCovariance,
    TylerCovariance,
    GeodesicEwaCovariance,
    DCCCovariance,
    FactorCovariance,
]


def all_estimators() -> list[type[BaseOnlineCovariance]]:
    """Return the list of registered online covariance estimator classes."""
    return list(_REGISTRY)


def estimator_names() -> list[str]:
    return [cls.__name__ for cls in _REGISTRY]


def estimator_from_name(name: str) -> type[BaseOnlineCovariance]:
    """Look up an estimator class by name (raises KeyError if unknown)."""
    for cls in _REGISTRY:
        if cls.__name__ == name:
            return cls
    raise KeyError(f"Unknown estimator {name!r}. Known: {estimator_names()}")
