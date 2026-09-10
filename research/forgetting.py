"""Does forgetting pay? Expanding versus rolling-window nonlinear shrinkage.

`precise` ships two analytical nonlinear shrinkers that differ only in which sample they read:
:class:`~precise.nonlinear_shrinkage.NonlinearShrinkageCovariance` over the whole stream, and
:class:`~precise.nonlinear_shrinkage.WindowedNonlinearShrinkageCovariance` over the last ``W``
observations. The docstrings should not be the thing that decides between them, so this scores them.

Three questions, and the scenarios are built to separate them.

1. **Does a window pay under drift?** The expanding sample is the one the Ledoit-Wolf asymptotics
   describe, but ``q = p/n`` falls towards zero as the stream runs, the shrinkage correctly fades,
   and the estimator converges on the plain sample covariance -- which is the right answer if the
   covariance is stationary and the wrong one if it is not.

2. **Does the expanding sample win when there is no drift?** It should. A window is then pure
   variance for no bias reduction, and paying for adaptivity a static problem does not reward is a
   real cost, not a rounding error.

3. **Is the shrinkage what makes a short window usable?** A short window tracks drift but is noisy
   and ill-conditioned on its own. We score each window's covariance twice -- once cleaned, once
   raw -- so the claim is tested rather than assumed.

A fourth arm is included for contrast and not shipped: an exponentially weighted accumulator cleaned
with an "effective sample size" ``n_eff = (2-r)/r``. That substitution is an approximation rather
than an equivalence -- the whole weight distribution enters the limiting spectrum, not just its
second moment -- which is why the shipped forgetting variant is a window, where equal weights make
``n = W`` exact. See Oriol, arXiv:2410.14420, for the weighted theory done properly.

    python research/forgetting.py
"""

from __future__ import annotations

import numpy as np

from precise import (
    EmpiricalCovariance,
    EwaCovariance,
    LedoitWolfCovariance,
    NonlinearShrinkageCovariance,
    OASCovariance,
    WindowedNonlinearShrinkageCovariance,
)
from precise.nonlinear_shrinkage import _shrink

WINDOWS = (60, 125, 250, 500)


class _EwaNeffShrinkage:
    """Contrast arm: EW accumulator cleaned with an effective sample size. Not shipped."""

    def __init__(self, r: float = 0.02):
        self.r, self._est = r, EwaCovariance(r=r)

    def partial_fit(self, x):
        self._est.partial_fit(x)
        return self

    @property
    def covariance_(self) -> np.ndarray:
        return _shrink(self._est.covariance_, int((2 - self.r) / self.r) - 1)


def _orthonormal(p, rng):
    return np.linalg.qr(rng.standard_normal((p, p)))[0]


def _factor_cov(p, rng, k=3, load=1.2):
    B = _orthonormal(p, rng)[:, :k] * load
    return B @ B.T + np.diag(0.3 + 0.4 * rng.random(p))


def scenarios(p, n, rng):
    """Two static regimes and three drifting ones; t -> true covariance at time t."""
    basis = _orthonormal(p, rng)
    spread = basis @ np.diag(np.exp(np.linspace(-1.5, 1.5, p))) @ basis.T
    before, after = _factor_cov(p, rng), _factor_cov(p, rng)
    diag_only = np.diag(0.3 + 0.4 * rng.random(p))
    half, period = n // 2, max(n // 6, 1)
    identity = np.eye(p)
    return {
        "isotropic (static)": lambda t: identity,
        "broad spectrum (static)": lambda t: spread,
        "factor rotation": lambda t: before if t < half else after,
        "factors vanish": lambda t: before if t < half else diag_only,
        "regimes alternate": lambda t: before if (t // period) % 2 == 0 else diag_only,
    }


def _arms(r):
    arms = {
        "Empirical (exp)": EmpiricalCovariance(),
        "NLS (exp)": NonlinearShrinkageCovariance(),
        "LedoitWolf": LedoitWolfCovariance(r=r),
        "OAS": OASCovariance(r=r),
        "EWA-NLS n_eff": _EwaNeffShrinkage(r),
    }
    for w in WINDOWS:
        arms[f"NLS W={w}"] = WindowedNonlinearShrinkageCovariance(window=w)
    return arms


def run(p=32, n=6000, seeds=5, burn=1000, every=50, r=0.02):
    """Mean squared Frobenius error relative to the squared norm of the truth. Lower is better."""
    names = list(_arms(r)) + [f"raw window W={w}" for w in WINDOWS]
    totals = {s: {nm: [] for nm in names} for s in scenarios(p, n, np.random.default_rng(0))}

    for seed in range(seeds):
        rng = np.random.default_rng(500 + seed)
        for scenario, cov_at in scenarios(p, n, rng).items():
            arms, errs, chol = _arms(r), {nm: [] for nm in names}, {}
            for t in range(n):
                cov = cov_at(t)
                if id(cov) not in chol:
                    chol[id(cov)] = np.linalg.cholesky(cov)
                x = chol[id(cov)] @ rng.standard_normal(p)
                for arm in arms.values():
                    arm.partial_fit(x)
                if t >= burn and t % every == 0:
                    denom = np.sum(cov**2)
                    for nm, arm in arms.items():
                        errs[nm].append(np.sum((arm.covariance_ - cov) ** 2) / denom)
                    for w in WINDOWS:
                        # The same window with the spectral map switched off, to isolate its effect.
                        arm = arms[f"NLS W={w}"]
                        raw = arm._spectrum_inputs(arm._state)[0]
                        errs[f"raw window W={w}"].append(np.sum((raw - cov) ** 2) / denom)
            for nm in names:
                totals[scenario][nm].append(float(np.mean(errs[nm])))

    return {s: {nm: float(np.mean(v)) for nm, v in c.items()} for s, c in totals.items()}


def report(results) -> str:
    names = list(next(iter(results.values())))
    width = max(len(s) for s in results) + 2
    head = "scenario".ljust(width) + "".join(nm.rjust(17) for nm in names)
    lines = [head, "-" * len(head)]
    for scenario, cells in results.items():
        best = min(cells.values())
        row = scenario.ljust(width)
        for nm in names:
            row += f"{cells[nm]:>16.4f}" + ("*" if cells[nm] == best else " ")
        lines.append(row)
    lines += ["", "Mean squared Frobenius error / squared norm of the truth;"
                  " * = best. Lower is better."]
    return "\n".join(lines)


if __name__ == "__main__":
    print(report(run()))
