"""Learning the spectral correction online, from the next observation.

The shipped :class:`~precise.nonlinear_shrinkage.NonlinearShrinkageCovariance` cleans the spectrum
analytically, over an expanding sample. Its asymptotics assume equally weighted, identically
distributed observations -- exactly the assumption real dependence violates, since it drifts. This
module asks whether the correction can instead be *learned from the stream itself*, with bounded
state and no pretrained network.

**The construction.** Suppose that immediately before observing ``x_t`` we hold a basis ``U`` built
entirely from past data. Project the new observation, ``z = U' x_t``. Because ``u_i`` is measurable
with respect to the past,

    E[ z_i^2 | past ] = u_i' Sigma_t u_i,

which is precisely the variance we want to assign to that empirical eigenvector. Every observation
therefore supplies a noisy but unbiased training label for *every* cleaned eigenvalue at once.

**Why that is the right objective.** In the basis ``U`` the instantaneous squared error decomposes
exactly:

    || U diag(d) U' - x x' ||_F^2  =  sum_i (d_i - z_i^2)^2  +  sum_{i != j} z_i^2 z_j^2,

and the second term does not involve ``d``. So learning to predict the squared projections
minimizes the same instantaneous objective as learning the covariance matrix within the chosen
basis. No held-out window is needed: the identity is conditional, requiring neither Gaussianity nor
stationarity. (Learning a *useful* map from such noisy labels still needs regularity over time --
that is the open question, not the identity.)

This is a sequential adaptation of the held-out projection idea behind cross-validated covariance
cleaning (Bartz 2016; Lamrani, Bongiorno & Potters 2025), where the split is made by partitioning a
sample. In a stream the arrow of time supplies the split for free, and it captures the central
restriction of Manolakis, Bongiorno & Mantegna (2026): learn the mode strengths, keep the empirical
directions.

**Cost.** Projecting is O(p^2), and between basis refreshes the eigenvalues need no
eigendecomposition at all -- for a fixed basis the exponentially weighted Rayleigh quotient obeys
the same recursion as the covariance, ``lambda_i <- (1-r) lambda_i + r z_i^2``, which is O(p) given
the projections we already compute. Refreshing the basis every ``K`` observations therefore costs
O(p^2 + p^3/K) amortized. Stale eigenvectors are the price, and they bound how fast the estimator
can follow an abrupt rotation.

**The open question** is not whether spectral cleaning can be online -- it plainly can -- but how to
share and forget calibration information as the spectrum changes. Calibrating against rank position
remembers a useful spectral shape but keeps imposing it after that shape is gone; calibrating
against the observed eigenvalue is more robust to that but gives up some of the gain elsewhere. The
scenarios below are built to separate those failures.

    python research/spectral_calibration.py
"""

from __future__ import annotations

import numpy as np

from precise import (
    EwaCovariance,
    LedoitWolfCovariance,
    NonlinearShrinkageCovariance,
    OASCovariance,
)

# --------------------------------------------------------------------------- the online calibrator


class _KernelMap:
    """Nadaraya-Watson map with exponential forgetting, over a fixed grid of feature centers.

    Kernel-weighted running averages rather than a fitted network: the prediction is a ratio of
    two nonnegative accumulators, so it is positive by construction (the labels are squares), it
    pools directions with identical features automatically -- preserving the symmetry that equal
    eigenvalues must receive equal treatment -- and it forgets at a controlled rate.
    """

    def __init__(self, centers: np.ndarray, bandwidth, rho: float):
        self.centers = np.atleast_2d(centers)
        # Per-axis bandwidth: the feature axes are on different scales, and one shared width lets
        # the wider axis smear away entirely -- which silently collapses a 2-d map into a 1-d one.
        self.bandwidth = np.broadcast_to(
            np.asarray(bandwidth, dtype=float), (self.centers.shape[1],)
        ).copy()
        self.rho = float(rho)
        self.num = np.zeros(len(self.centers))
        self.den = np.zeros(len(self.centers))

    def _weights(self, feats: np.ndarray) -> np.ndarray:
        delta = (np.atleast_2d(feats)[:, None, :] - self.centers[None, :, :]) / self.bandwidth
        w = np.exp(-0.5 * (delta**2).sum(axis=2))
        return w / np.maximum(w.sum(axis=1, keepdims=True), 1e-300)

    def learn(self, feats: np.ndarray, y: np.ndarray) -> None:
        w = self._weights(feats)
        self.num = (1 - self.rho) * self.num + self.rho * (w.T @ y)
        self.den = (1 - self.rho) * self.den + self.rho * w.sum(axis=0)

    def predict(self, feats: np.ndarray, fallback: np.ndarray) -> np.ndarray:
        w = self._weights(feats)
        num, den = w @ self.num, w @ self.den
        seen = den > 1e-8
        out = np.where(seen, num / np.where(seen, den, 1.0), fallback)
        return np.maximum(out, 1e-12)


class CalibratedSpectrumCovariance:
    """Exponentially weighted covariance whose eigenvalues are recalibrated from the stream.

    :param r:        EW decay of the covariance accumulator.
    :param refresh:  Recompute the eigenvector basis every this many observations.
    :param mode:     Which features the calibration map is indexed by --
                     ``"rank"`` (spectral position only), ``"eigenvalue"`` (observed normalized
                     eigenvalue only), or ``"shared"`` (eigenvalue plus global spectral shape).
    :param rho:      Forgetting rate of the calibration map itself.
    """

    def __init__(self, r=0.02, refresh=10, mode="shared", rho=0.02, n_bins=16, n_shape=5):
        self.r, self.refresh, self.mode, self.rho = r, refresh, mode, rho
        self.n_bins, self.n_shape = n_bins, n_shape
        self._mean = self._cov = self._basis = self._lam = None
        self._n = 0
        self._map = self._build_map()

    def _build_map(self) -> _KernelMap:
        # Features are scale-free by construction: log eigenvalue ratios and a rank position.
        grid = np.linspace(-2.5, 2.5, self.n_bins) if self.mode != "rank" else np.linspace(
            0.0, 1.0, self.n_bins
        )
        width = (grid[1] - grid[0]) * 1.5
        if self.mode == "shared":
            # Dispersion of the log spectrum. The grid covers the range this statistic actually
            # occupies within one stream (~0.3-1.1); spanning [0, 1.5] instead makes every bin
            # wider than the variation being resolved, and the axis quietly does nothing.
            shape = np.linspace(0.25, 1.15, self.n_shape)
            centers = np.array([[g, s] for s in shape for g in grid])
            return _KernelMap(centers, [width, (shape[1] - shape[0]) * 0.75], rho=self.rho)
        return _KernelMap(grid[:, None], width, rho=self.rho)

    def _features(self) -> np.ndarray:
        lam = np.maximum(self._lam, 1e-12)
        p = lam.size
        if self.mode == "rank":
            return (np.argsort(np.argsort(lam)) / max(p - 1, 1))[:, None]
        g = np.log(lam / lam.mean())
        if self.mode == "eigenvalue":
            return g[:, None]
        return np.column_stack([g, np.full(p, g.std())])  # local level + global shape

    def partial_fit(self, x) -> CalibratedSpectrumCovariance:
        x = np.asarray(x, dtype=float).ravel()
        p = x.size
        if self._cov is None:
            self._mean, self._cov = np.zeros(p), np.zeros((p, p))

        dev = x - self._mean
        self._n += 1
        w = 1.0 / self._n if self._n <= max(int(1 / self.r), 5) else self.r  # burn in empirically

        if self._basis is not None:
            # The basis predates x, so the squared projections are honest out-of-sample labels.
            z2 = (self._basis.T @ dev) ** 2
            scale = max(self._lam.mean(), 1e-12)
            self._map.learn(self._features(), z2 / scale)
            # Fixed basis => the Rayleigh quotient obeys the covariance's own recursion, at O(p)
            # instead of an eigendecomposition. It must use the *same* weight to stay consistent.
            self._lam = (1 - w) * self._lam + w * z2

        self._mean = self._mean + w * dev
        self._cov = (1 - w) * self._cov + w * np.outer(dev, dev)

        if self._basis is None or self._n % self.refresh == 0:
            lam, evecs = np.linalg.eigh((self._cov + self._cov.T) / 2.0)
            self._basis, self._lam = evecs, np.maximum(lam, 0.0)
        return self

    @property
    def covariance_(self) -> np.ndarray:
        if self._basis is None:
            return np.zeros_like(self._cov) if self._cov is not None else np.zeros((0, 0))
        scale = max(self._lam.mean(), 1e-12)
        d = self._map.predict(self._features(), fallback=self._lam / scale) * scale
        return (self._basis * d) @ self._basis.T


# ------------------------------------------------------------------------------------- scenarios


def _random_basis(p, rng):
    return np.linalg.qr(rng.standard_normal((p, p)))[0]


def _factor_cov(p, rng, k=3, load=1.2):
    B = _random_basis(p, rng)[:, :k] * load
    return B @ B.T + np.diag(0.3 + 0.4 * rng.random(p))


def scenarios(p, n, rng):
    """Each returns a function t -> true covariance at time t."""
    iso = np.eye(p)

    basis = _random_basis(p, rng)
    spread = basis @ np.diag(np.exp(np.linspace(-1.5, 1.5, p))) @ basis.T

    before, after = _factor_cov(p, rng), _factor_cov(p, rng)
    diag_only = np.diag(0.3 + 0.4 * rng.random(p))
    switch = n // 2

    period = max(n // 6, 1)
    return {
        "isotropic": lambda t: iso,
        "broad spectrum": lambda t: spread,
        "factor rotation": lambda t: before if t < switch else after,
        "factors vanish": lambda t: before if t < switch else diag_only,
        # The one scenario where a spectral shape *recurs*: a map indexed by shape can recall the
        # calibration it already learned, where one indexed by rank cannot and one indexed only by
        # the eigenvalue must relearn it each time.
        "regimes alternate": lambda t: before if (t // period) % 2 == 0 else diag_only,
    }


# ----------------------------------------------------------------------------------- the bake-off


def _estimators(r, refresh, rho):
    return {
        "Raw EW": lambda: EwaCovariance(r=r),
        "LedoitWolf": lambda: LedoitWolfCovariance(r=r),
        "OAS": lambda: OASCovariance(r=r),
        "NonlinearShrinkage": NonlinearShrinkageCovariance,
        "rank calib": lambda: CalibratedSpectrumCovariance(r, refresh, "rank", rho),
        "eigenvalue calib": lambda: CalibratedSpectrumCovariance(r, refresh, "eigenvalue", rho),
        "shared calib": lambda: CalibratedSpectrumCovariance(r, refresh, "shared", rho),
    }


def run(p=32, n=6000, seeds=8, r=0.02, refresh=10, rho=0.02, burn=1000, every=50):
    """Mean squared Frobenius error, relative to the squared norm of the truth. Lower is better."""
    names = list(_estimators(r, refresh, rho))
    totals = {s: {nm: [] for nm in names} for s in scenarios(p, n, np.random.default_rng(0))}

    for seed in range(seeds):
        rng = np.random.default_rng(1000 + seed)
        for scenario, cov_at in scenarios(p, n, rng).items():
            ests = {nm: make() for nm, make in _estimators(r, refresh, rho).items()}
            errs = {nm: [] for nm in names}
            chol_cache: dict[int, np.ndarray] = {}
            for t in range(n):
                C = cov_at(t)
                key = id(C)
                if key not in chol_cache:
                    chol_cache[key] = np.linalg.cholesky(C)
                x = chol_cache[key] @ rng.standard_normal(p)
                for est in ests.values():
                    est.partial_fit(x)
                if t >= burn and t % every == 0:
                    denom = np.sum(C**2)
                    for nm, est in ests.items():
                        errs[nm].append(np.sum((est.covariance_ - C) ** 2) / denom)
            for nm in names:
                totals[scenario][nm].append(float(np.mean(errs[nm])))

    return {s: {nm: float(np.mean(v)) for nm, v in cells.items()} for s, cells in totals.items()}


def report(results) -> str:
    names = list(next(iter(results.values())))
    width = max(len(s) for s in results) + 2
    head = "scenario".ljust(width) + "".join(nm.rjust(20) for nm in names)
    lines = [head, "-" * len(head)]
    for scenario, cells in results.items():
        best = min(cells.values())
        row = scenario.ljust(width)
        for nm in names:
            mark = "*" if cells[nm] == best else " "
            row += f"{cells[nm]:>19.4f}{mark}"
        lines.append(row)
    lines.append("")
    lines.append("Mean squared Frobenius error / squared norm of the truth;"
                 " * = best. Lower is better.")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report(run()))
