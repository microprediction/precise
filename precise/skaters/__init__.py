"""Compatibility shim for the removed functional 'skater' API.

Importing anything under ``precise.skaters`` raises a clear, actionable error: the functional skater
API was removed in precise 1.0 in favour of sklearn-style estimator classes. Kept only so that old
``from precise.skaters... import ...`` code fails helpfully, not with a bare ModuleNotFoundError.
"""

raise ImportError(
    "The functional 'skater' API (precise.skaters.*) was removed in precise 1.0. "
    "Use the sklearn-style estimator classes instead, e.g.\n"
    "    from precise import EwaCovariance\n"
    "    est = EwaCovariance(r=0.05)\n"
    "    est.partial_fit(y)            # then est.covariance_ / est.correlation_\n"
    "See MIGRATING.md: https://github.com/microprediction/precise/blob/main/MIGRATING.md "
    "(portfolio/allocation code now lives in https://github.com/microprediction/schur)."
)
