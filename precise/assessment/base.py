"""The assessor contract: how to judge the quality of a covariance estimate.

An :class:`Assessor` scores a covariance matrix (the ``covariance_`` of a fitted estimator) — higher
is better, by convention. Two capability flags say what an assessor needs:

* ``needs_data`` — it scores against a held-out sample ``X_test`` (usable on real data, no truth);
* ``needs_truth`` — it scores against the known true covariance (synthetic benchmarks only).

This mirrors the estimator side: a registry (:func:`precise.assessment.all_assessors`) of uniform
objects, so the research bake-offs and the recommender can iterate over judges the way they iterate
over estimators. The motivating finding (see ``research/metric_power.py`` and
``papers/covariance_evaluation.md``) is that the right judge is regime-dependent — the full
likelihood is most powerful when the precision is trustworthy but fails in high dimensions, where
inversion-free / block judges win.
"""

from __future__ import annotations

import numpy as np


class Assessor:
    """Base class for covariance-estimate quality judges (higher score == better)."""

    needs_data: bool = True
    needs_truth: bool = False

    def score(
        self,
        cov: np.ndarray,
        *,
        X_test: np.ndarray | None = None,
        true_cov: np.ndarray | None = None,
    ) -> float:
        raise NotImplementedError

    def usable(self, *, have_data: bool, have_truth: bool) -> bool:
        """Whether this assessor can run given what is available."""
        return (have_data or not self.needs_data) and (have_truth or not self.needs_truth)

    @property
    def name(self) -> str:
        return type(self).__name__

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
