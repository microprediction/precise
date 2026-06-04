"""Registry of online covariance estimators.

Mirrors the convention of ``sklearn.utils.all_estimators`` and the
``allcorrgens``/``allvargens`` registries in the sibling ``randomcov`` package, so the
conformance test and the ``research/`` bake-offs can iterate over every estimator uniformly.
"""

from __future__ import annotations

from typing import List, Type

from precise.base import BaseOnlineCovariance
from precise.empirical import EmpiricalCovariance
from precise.ewa import EwaCovariance
from precise.geodesic import GeodesicEwaCovariance

# The shipped positional estimators. Add new estimator classes here (one line each).
_REGISTRY: List[Type[BaseOnlineCovariance]] = [
    EmpiricalCovariance,
    EwaCovariance,
    GeodesicEwaCovariance,
]


def all_estimators() -> List[Type[BaseOnlineCovariance]]:
    """Return the list of registered online covariance estimator classes."""
    return list(_REGISTRY)


def estimator_names() -> List[str]:
    return [cls.__name__ for cls in _REGISTRY]


def estimator_from_name(name: str) -> Type[BaseOnlineCovariance]:
    """Look up an estimator class by name (raises KeyError if unknown)."""
    for cls in _REGISTRY:
        if cls.__name__ == name:
            return cls
    raise KeyError(f"Unknown estimator {name!r}. Known: {estimator_names()}")
