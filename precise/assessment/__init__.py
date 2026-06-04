"""Covariance-estimate assessment: a registry of quality judges (higher score == better).

    from precise.assessment import all_assessors
    for assessor in all_assessors():
        if assessor.usable(have_data=True, have_truth=False):
            assessor.score(est.covariance_, X_test=holdout)

See ``papers/covariance_evaluation.md`` for which judge to trust in which regime.
"""

from __future__ import annotations

from precise.assessment.assessors import (
    BlockPseudoLikelihood,
    FrobeniusToTruth,
    GMVVariance,
    LogLikelihood,
    SteinLoss,
    VariogramScore,
)
from precise.assessment.base import Assessor
from precise.assessment.registry import all_assessors, assessor_from_name

__all__ = [
    "Assessor",
    "LogLikelihood",
    "BlockPseudoLikelihood",
    "SteinLoss",
    "FrobeniusToTruth",
    "GMVVariance",
    "VariogramScore",
    "all_assessors",
    "assessor_from_name",
]
