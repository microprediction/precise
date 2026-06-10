"""precise — online (incremental) covariance & correlation estimation.

The online complement to ``sklearn.covariance`` (whose estimators are batch-only and lack
``partial_fit``). Two cooperating layers:

* a positional, sklearn-style core (fixed dimension, fast) — :class:`EmpiricalCovariance` et al.;
* keyed, river-style adapters — :func:`keyed` → :class:`FixedUniverse` / :class:`DynamicUniverse` —
  that decorate any positional estimator to consume name-keyed dicts and track a universe whose
  variables enter and leave over time (a real need in finance).

    from precise import EwaCovariance
    est = EwaCovariance(r=0.05)
    for y in stream:
        est.partial_fit(y)
    est.covariance_   # also .correlation_, .precision_, .location_
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from precise.adaptive import AdaptiveEwaCovariance
from precise.assessment import all_assessors, assessor_from_name
from precise.base import BaseOnlineCovariance
from precise.conditional import ConditionalCovariance, from_skater
from precise.dcc import DCCCovariance
from precise.diagonal import DiagonalCovariance
from precise.empirical import EmpiricalCovariance
from precise.ewa import EwaCovariance
from precise.factor import FactorCovariance
from precise.geodesic import GeodesicEwaCovariance
from precise.huber import HuberCovariance
from precise.keyed import DynamicUniverse, FixedUniverse, keyed
from precise.ledoitwolf import LedoitWolfCovariance
from precise.oas import OASCovariance
from precise.partialmoments import PartialMomentsCovariance
from precise.recommend import covariance_features, suggest
from precise.registry import all_estimators, estimator_from_name, estimator_names
from precise.schur_ledoit_wolf import SchurLedoitWolfCovariance
from precise.schurcov import SchurCovariance
from precise.shrunk import ShrunkCovariance
from precise.tyler import TylerCovariance

try:
    __version__ = version("precise")
except PackageNotFoundError:  # running from a source checkout without install
    __version__ = "0.0.0+source"

__all__ = [
    "BaseOnlineCovariance",
    "EmpiricalCovariance",
    "DiagonalCovariance",
    "EwaCovariance",
    "AdaptiveEwaCovariance",
    "LedoitWolfCovariance",
    "OASCovariance",
    "ShrunkCovariance",
    "SchurCovariance",
    "SchurLedoitWolfCovariance",
    "PartialMomentsCovariance",
    "HuberCovariance",
    "TylerCovariance",
    "GeodesicEwaCovariance",
    "DCCCovariance",
    "FactorCovariance",
    "ConditionalCovariance",
    "from_skater",
    "keyed",
    "FixedUniverse",
    "DynamicUniverse",
    "all_estimators",
    "estimator_from_name",
    "estimator_names",
    "all_assessors",
    "assessor_from_name",
    "suggest",
    "covariance_features",
    "__version__",
]
