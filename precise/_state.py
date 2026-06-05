"""Pure state-update functions — the incremental compute engine.

Each function takes a plain state ``dict`` and one observation ``x`` and returns a
new state dict. These are the hooks the estimator classes wrap: the object-oriented
``partial_fit`` API on the outside, pure functional updates on the inside (which keeps
the state transparently serializable via ``BaseOnlineCovariance.get_state``).

State dict keys (a superset; method-specific keys added as needed):
    n_dim       number of variables
    n_samples   observations seen so far
    mean        running mean vector (the estimator's ``location_``)
    cov         running population covariance matrix (the estimator's ``covariance_``)
"""

from __future__ import annotations

import math

import numpy as np


def emp_init(n_dim: int) -> dict:
    """Initialize empirical (Welford) covariance tracking."""
    return {
        "n_dim": int(n_dim),
        "n_samples": 0,
        "mean": np.zeros(n_dim),
        "cov": np.zeros((n_dim, n_dim)),
    }


def emp_update(s: dict, x: np.ndarray) -> dict:
    """One Welford step maintaining the population covariance (divide by n).

    Matches ``numpy.cov(..., bias=True)`` and sklearn's empirical-covariance (MLE)
    convention. Returns a fresh state dict; the input is not mutated.
    """
    count = s["n_samples"] + 1
    delta_prev = x - s["mean"]
    mean = s["mean"] + delta_prev / count
    weighted_delta = (x - mean) / count
    cov = s["cov"] * (count - 1) / count + np.outer(delta_prev, weighted_delta)
    return {"n_dim": s["n_dim"], "n_samples": count, "mean": mean, "cov": cov}


def ewa_burn_n(r: float) -> int:
    """Number of burn-in observations before switching from empirical to exponential.

    Roughly ``1/r`` (clamped), so the recency-weighted estimate starts from a sane
    empirical covariance rather than a degenerate one.
    """
    return int(min(250, max(5, math.ceil(1.0 / r))))


def ewa_init(n_dim: int, r: float) -> dict:
    s = emp_init(n_dim)
    s["r"] = float(r)
    s["n_burn"] = ewa_burn_n(r)
    return s


def ewa_update(s: dict, x: np.ndarray) -> dict:
    """Exponentially weighted covariance update (RiskMetrics-style).

    During the burn-in window the plain empirical update is used; thereafter both the
    mean and covariance decay with rate ``r``.
    """
    if s["n_samples"] < s["n_burn"]:
        out = emp_update(s, x)
        out["r"] = s["r"]
        out["n_burn"] = s["n_burn"]
        return out
    r = s["r"]
    delta = x - s["mean"]
    mean = (1 - r) * s["mean"] + r * x
    cov = (1 - r) * s["cov"] + r * np.outer(delta, delta)
    return {
        "n_dim": s["n_dim"],
        "n_samples": s["n_samples"] + 1,
        "mean": mean,
        "cov": cov,
        "r": r,
        "n_burn": s["n_burn"],
    }
