"""Registry of covariance-estimate assessors — the evaluation analogue of ``all_estimators()``."""

from __future__ import annotations

from precise.assessment.assessors import (
    BlockPseudoLikelihood,
    FrobeniusToTruth,
    GMVVariance,
    LogLikelihood,
    SchurLikelihood,
    SteinLoss,
    VariogramScore,
)
from precise.assessment.base import Assessor


def all_assessors() -> list[Assessor]:
    """Return instances of the registered assessors (default parameters)."""
    return [
        LogLikelihood(),
        BlockPseudoLikelihood(),
        SchurLikelihood(),
        SteinLoss(),
        FrobeniusToTruth(),
        GMVVariance(),
        VariogramScore(),
    ]


def assessor_from_name(name: str) -> Assessor:
    for a in all_assessors():
        if a.name == name:
            return a
    raise KeyError(f"Unknown assessor {name!r}. Known: {[a.name for a in all_assessors()]}")
