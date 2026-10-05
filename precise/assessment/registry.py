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
    """Return an instance, with default parameters, of the assessor called ``name``.

    :param name: The assessor's class name, as listed by ``[a.name for a in all_assessors()]``,
                 for example ``"SteinLoss"``.
    :raises KeyError: If no registered assessor has that name.

    Example::

        >>> from precise import assessor_from_name
        >>> assessor_from_name("SteinLoss").name
        'SteinLoss'
    """
    for a in all_assessors():
        if a.name == name:
            return a
    raise KeyError(f"Unknown assessor {name!r}. Known: {[a.name for a in all_assessors()]}")
