"""Online analytical nonlinear shrinkage of the covariance spectrum.

The zoo already shrinks *linearly* towards a target:
:class:`~precise.ledoitwolf.LedoitWolfCovariance` and :class:`~precise.oas.OASCovariance` pull
every eigenvalue towards a common scaled identity, which (with an identity target) leaves the
sample eigenvectors untouched. What was missing is a **nonlinear** map: one that moves each
eigenvalue by a different amount — pushing the overstated large ones down and the understated
small ones up — while still keeping the sample eigenvectors.

The rule is the analytical nonlinear shrinkage of Ledoit & Wolf (2020), *Analytical Nonlinear
Shrinkage of Large-Dimensional Covariance Matrices*, Annals of Statistics 48(5) 3043-3065.
Equation numbers in the code refer to that paper. It is fully analytical: a kernel estimate of the
sample spectral density and its Hilbert transform, no numerical optimization and nothing learned.

**Why this is online.** The shrinkage map reads only the *eigenvalues of the running covariance*
and the *observation count* — never the observations themselves. So the accumulation stays a plain
Welford update (O(p^2) per step, no window, no growth with stream length) and the spectral work
happens lazily in ``_state_to_cov``, the same seam where ``LedoitWolfCovariance`` computes its
shrinkage intensity. Reading ``covariance_`` costs O(p^3) for the eigendecomposition — the price
``precision_`` and ``GeodesicEwaCovariance`` already pay — and the result is memoized per state so
that reading ``covariance_``, ``correlation_`` and ``precision_`` in turn decomposes once, not
three times.

**Why the sample is expanding rather than exponentially weighted.** The asymptotics behind the map
assume equally weighted observations, so over an expanding sample this estimator reproduces its
batch counterpart exactly. Substituting an "effective sample size" for exponentially decaying
weights is an approximation — a scalar moment match that does not encode the whole weight
distribution — and the weighted theory that would do it properly (Oriol, arXiv:2410.14420) is a
separate construction. The exponentially weighted variant is therefore developed under
``research/``, not shipped here.
"""

from __future__ import annotations

import numpy as np

from precise._state import emp_init, emp_update, ewa_init, ewa_update
from precise.base import BaseOnlineCovariance

_SQRT5 = float(np.sqrt(5.0))

# Below this many observations the kernel bandwidth h = n^(-1/3) is too wide for the p > n
# branch (which needs sqrt(5)*h < 1), and the density estimate is not informative anyway.
_MIN_OBS = 12

# Eigenvalues below this fraction of the largest are treated as null. See the tolerance comment in
# `nonlinear_shrinkage_spectrum`: the kernel divides by the eigenvalue, so "small enough to ignore"
# is set by that inversion, not by the precision of the representation.
_NULL_EIGENVALUE_RATIO = float(np.sqrt(np.finfo(float).eps))

# Bounds on shrunk-trace over raw-trace before the map is rejected as having failed. Wide, because
# genuine shrinkage does move the trace; the failure being caught moves it by a factor of 1e-9.
_TRACE_TOLERANCE = (0.5, 2.0)


def nonlinear_shrinkage_spectrum(lam: np.ndarray, n: int) -> np.ndarray | None:
    """Map sample eigenvalues to nonlinearly shrunk ones. ``lam`` ascending, ``n`` observations.

    Returns ``None`` when the analytical map is not usable (too few observations for the kernel
    bandwidth), leaving the caller to fall back to the unshrunk spectrum. The map is
    scale-equivariant: scaling ``lam`` by c scales the result by c.

    Only the ``k`` eigenvalues above the numerical-rank tolerance carry spectral density; the
    other ``p - k`` are null. Ledoit-Wolf assume the nulls are exactly the ``p - n`` forced by
    having fewer observations than variables, but data can be rank-deficient for its own reasons
    (a duplicated series, a hedged pair), so ``k`` is measured rather than assumed. Null
    eigenvalues must be *excluded* from the density estimate, not merely floored: at 1e-15 they
    contribute ~1e30 to the Hilbert transform of every other eigenvalue and collapse the whole
    spectrum to zero.
    """
    lam = np.asarray(lam, dtype=float)
    p = lam.size
    n = int(n)
    if n < _MIN_OBS or p == 0 or lam[-1] <= 0:
        return None
    h = n ** (-1.0 / 3.0)  # kernel bandwidth exponent, eq. (4.9)

    # Machine epsilon is the wrong scale here, and using it shipped a silent failure. The kernel
    # divides by the eigenvalue twice -- `H = h * lam` sets the bandwidth, and both `x` and
    # `hf / H` are scaled by it -- so an eigenvalue far below the bulk does not merely contribute
    # little, it contributes ~1/lam to the Hilbert transform of *every* other eigenvalue and drives
    # the whole shrunk spectrum to zero. A relative eigenvalue of 1e-15 is excluded by an
    # epsilon-scaled tolerance, but one of 1e-10 survives it and collapses the estimate.
    #
    # That band is reachable from ordinary data rather than from contrived spectra: one series
    # quoted in basis points among percents is a variance ratio of 1e-8, and a hedged pair is
    # smaller still. Measured, a p=10 stream with one column scaled by 1e-4 returned a covariance
    # with 1e-9 of the correct trace.
    #
    # sqrt(eps) is the conventional floor for a quantity a method inverts, and it sits an order of
    # magnitude clear of the band where the kernel estimate degrades. Directions below it carry no
    # variance worth estimating and stay null, exactly as the p > n nulls do.
    tol = lam[-1] * max(p * np.finfo(float).eps, _NULL_EIGENVALUE_RATIO)
    k = min(int(np.count_nonzero(lam > tol)), n)
    if k < 1:
        return None
    lam_top = lam[p - k :]

    L = np.tile(lam_top[:, None], (1, k))
    H = h * L.T
    x = (L - L.T) / H

    # Epanechnikov kernel estimate of the sample spectral density, eq. (4.9).
    ftilde = (3.0 / 4.0 / _SQRT5) * np.mean(np.maximum(1.0 - x**2 / 5.0, 0.0) / H, axis=1)

    # Its Hilbert transform, eq. (4.7); the integrand is finite at |x| = sqrt(5) by continuity.
    with np.errstate(divide="ignore", invalid="ignore"):
        hf = (-3.0 / 10.0 / np.pi) * x + (3.0 / 4.0 / _SQRT5 / np.pi) * (1.0 - x**2 / 5.0) * np.log(
            np.abs((_SQRT5 - x) / (_SQRT5 + x))
        )
    at_edge = np.abs(np.abs(x) - _SQRT5) < 1e-12
    hf[at_edge] = (-3.0 / 10.0 / np.pi) * x[at_edge]
    hftilde = np.mean(hf / H, axis=1)

    if k >= p or n >= p:
        # Every direction the data actually spans is informative: shrink within that subspace,
        # eq. (4.3) with the aspect ratio of the observed rank. Genuinely null directions carry
        # no variance to estimate, so they stay null rather than being handed an invented one.
        q = k / n
        dtilde = lam_top / (
            (np.pi * q * lam_top * ftilde) ** 2 + (1.0 - q - np.pi * q * lam_top * hftilde) ** 2
        )
        return dtilde if k == p else np.concatenate([np.zeros(p - k), dtilde])

    # Fewer observations than variables: the p - k nulls are a sampling artifact rather than a
    # property of the data, and they share one positive value. Eqs. (C.4), (C.5), (C.8), with
    # Ledoit-Wolf's p - n null count generalized to the observed p - k.
    if _SQRT5 * h >= 1.0:
        return None
    hftilde0 = (
        (1.0 / np.pi)
        * (
            3.0 / 10.0 / h**2
            + 3.0
            / 4.0
            / _SQRT5
            / h
            * (1.0 - 1.0 / 5.0 / h**2)
            * np.log((1.0 + _SQRT5 * h) / (1.0 - _SQRT5 * h))
        )
        * np.mean(1.0 / lam_top)
    )
    dtilde0 = 1.0 / (np.pi * (p - k) / k * hftilde0)
    dtilde1 = lam_top / (np.pi**2 * lam_top**2 * (ftilde**2 + hftilde**2))
    return np.concatenate([np.full(p - k, dtilde0), dtilde1])


class _LazySpectrumCovariance(BaseOnlineCovariance):
    """Shared plumbing: shrink the spectrum lazily on read, and memoize the result per state.

    Subclasses accumulate however they like and report ``(covariance, sample size)`` through
    :meth:`_spectrum_inputs`; the eigendecomposition happens here, once per state, so that reading
    ``covariance_``, ``correlation_`` and ``precision_`` in turn does not decompose three times.
    """

    def __init__(self) -> None:
        super().__init__()
        self._cleaned_for: dict | None = None
        self._cleaned: np.ndarray | None = None

    def _spectrum_inputs(self, state: dict) -> tuple[np.ndarray, int]:
        raise NotImplementedError

    def _state_to_cov(self, state: dict) -> np.ndarray:
        # Every update returns a fresh state dict, so identity is a sound memo key.
        if state is self._cleaned_for and self._cleaned is not None:
            return self._cleaned
        cov, n = self._spectrum_inputs(state)
        cleaned = _shrink(cov, n)
        self._cleaned_for, self._cleaned = state, cleaned
        return cleaned

    def set_state(self, state: dict | None) -> _LazySpectrumCovariance:
        self._cleaned_for = self._cleaned = None
        super().set_state(state)
        return self


class NonlinearShrinkageCovariance(_LazySpectrumCovariance):
    """Online covariance with analytically nonlinearly shrunk eigenvalues (Ledoit-Wolf 2020).

    Keeps the sample eigenvectors and remaps the eigenvalues individually. Unlike the linear
    shrinkers it needs no target and no intensity parameter — the map is determined by the observed
    spectrum and the sample size — and it stays finite and invertible when ``p > n``, where the
    sample covariance is singular.

    The sample expands over the whole stream, so ``q = p/n`` falls towards zero and the shrinkage
    correctly fades: on a genuinely stationary stream this converges on
    :class:`~precise.empirical.EmpiricalCovariance`, which is the right answer there and the wrong
    one under drift. :class:`WindowedNonlinearShrinkageCovariance` is the forgetting counterpart.

    :param diff:  If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, diff: bool = False):
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        return emp_init(n_dim)

    def _update_state(self, state: dict, x: np.ndarray) -> dict:
        return emp_update(state, x)

    def _spectrum_inputs(self, state: dict) -> tuple[np.ndarray, int]:
        return np.asarray(state["cov"], dtype=float), int(state["n_samples"]) - 1


class WindowedNonlinearShrinkageCovariance(_LazySpectrumCovariance):
    """Nonlinear shrinkage over a rolling window of the last ``window`` observations.

    The forgetting counterpart to :class:`NonlinearShrinkageCovariance`, and the reason it is a
    window rather than an exponential decay: the Ledoit-Wolf asymptotics describe an *equally
    weighted* sample of size ``n``, and a rolling window is exactly that, with ``n = window``.
    Nothing about the map is approximated. Substituting an "effective sample size" for
    exponentially decaying weights would be a different matter -- the whole weight distribution
    enters the limiting spectrum, not just its second moment, so a moment match there is an
    approximation wearing an equivalence's clothes. The weighted theory that does it properly is
    Oriol, arXiv:2410.14420.

    The pairing is the point. A short window is what tracks drift, but on its own it is too noisy
    and ill-conditioned to use; the shrinkage is what makes a short window affordable, and
    ``q = p/window`` becomes an explicit dial rather than a quantity drifting towards zero. Against
    that, if the covariance really is stationary then a window is pure variance for no bias
    reduction and the expanding estimator strictly dominates.

    ``research/forgetting.py`` scores both. Measured there: under drift the window wins by a wide
    margin (roughly 3-4x lower error than the expanding estimator when factor structure rotates or
    dies), on static spectra it loses by 3-5x, and cleaning the window's spectrum beats leaving it
    raw at *every* window length -- by 20x at W=60 -- so a cleaned short window outperforms a raw
    window four times longer. Which regime your data is in is the empirical question; the default
    below is one trading year.

    One caveat that squared error cannot show, measured in ``research/turnover.py``: the boundary is
    hard, so a shock is paid for twice -- once on arrival and again exactly ``window`` periods later
    when it drops out and the estimate jumps back for no reason. Minimum-variance turnover spikes
    over 12x at that offset, where an exponentially weighted estimator of matched effective memory
    shows nothing. Under Gaussian draws the window's average turnover is still the lower of the two,
    but the echo is charged per shock: at t(4) innovations the window is already the churnier, and
    at t(3) it is 15% churnier with worse realized risk. If you trade on the estimate and your
    returns have tails, weigh that against the accuracy.

    :param window:  Number of most recent observations to estimate from.
    :param diff:    If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, window: int = 250, diff: bool = False):
        self.window = window
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        w = max(int(self.window), 2)
        return {
            "n_dim": int(n_dim),
            "n_samples": 0,
            "window": w,
            "fill": 0,  # observations currently in the buffer
            "pos": 0,  # next slot to write
            "buf": np.zeros((w, n_dim)),
            "s1": np.zeros(n_dim),  # running sum over the window
            "s2": np.zeros((n_dim, n_dim)),  # running sum of outer products over the window
        }

    def _update_state(self, state: dict, x: np.ndarray) -> dict:
        w, fill, pos = int(state["window"]), int(state["fill"]), int(state["pos"])
        buf = state["buf"]
        s1, s2 = state["s1"], state["s2"]

        if fill == w:  # evict the observation leaving the window
            old = buf[pos]
            s1 = s1 - old
            s2 = s2 - np.outer(old, old)
        else:
            fill += 1
        buf[pos] = x  # in place: the buffer is bounded, and the state dict below is still fresh
        s1 = s1 + x
        s2 = s2 + np.outer(x, x)
        pos = (pos + 1) % w

        n_samples = int(state["n_samples"]) + 1
        if n_samples % w == 0:
            # Add-and-drop accumulates cancellation error over a long stream. Recomputing from the
            # buffer costs O(window * p^2) but happens once per window, so it is O(p^2) amortized --
            # the same order as the update it corrects.
            live = buf[:fill]
            s1, s2 = live.sum(axis=0), live.T @ live

        return {
            "n_dim": state["n_dim"],
            "n_samples": n_samples,
            "window": w,
            "fill": fill,
            "pos": pos,
            "buf": buf,
            "s1": s1,
            "s2": s2,
        }

    def _state_to_mean(self, state: dict) -> np.ndarray:
        return np.asarray(state["s1"], dtype=float) / max(int(state["fill"]), 1)

    def _spectrum_inputs(self, state: dict) -> tuple[np.ndarray, int]:
        fill = max(int(state["fill"]), 1)
        mean = np.asarray(state["s1"], dtype=float) / fill
        cov = np.asarray(state["s2"], dtype=float) / fill - np.outer(mean, mean)
        return cov, fill - 1


def effective_sample_size(r: float) -> float:
    """Effective sample size of an exponentially weighted mean with decay ``r``.

    For normalized geometric weights ``w_k = r(1-r)^k`` the usual moment-based measure is
    ``(sum w)^2 / sum w^2 = (2-r)/r``. Note what this is not: matching one moment of the weight
    distribution does not make the exponentially weighted covariance behave like an equally
    weighted sample of that size. The whole weight distribution enters the limiting spectrum.
    """
    return (2.0 - r) / r


class EwaNonlinearShrinkageCovariance(_LazySpectrumCovariance):
    """Nonlinear spectrum shrinkage over an exponentially weighted sample.

    The second forgetting variant, and the approximate one. Ledoit-Wolf's asymptotics describe an
    *equally weighted* sample of size ``n``, which is what
    :class:`WindowedNonlinearShrinkageCovariance` supplies exactly. Here the map is instead applied
    to an exponentially weighted covariance at ``n = (2-r)/r``, its effective sample size, and that
    substitution is a moment match rather than an equivalence: the shape of the weight distribution
    enters the limiting spectrum, not only its second moment. Oriol (arXiv:2410.14420) derives the
    weighted formulas properly, and a future estimator built on them would supersede this one.

    It ships anyway, because exactness is not the only axis. A window has a hard boundary, so an
    observation enters the estimate on arrival and leaves it exactly ``W`` steps later, and a shock
    is therefore paid for twice: the second rebalance prompted by nothing happening. Exponential
    decay has no such discontinuity. In ``research/turnover.py``, with effective memory matched so
    the comparison measures the boundary rather than the memory, both react identically to a shock
    on arrival and only the window rebalances again a window later, spiking over 12x. Aggregate
    turnover follows the tail weight: under Gaussian draws the window is the cheaper of the two, at
    t(4) innovations they cross, and at t(3) the window is 15% churnier with worse realized risk.

    So: prefer the window when accuracy against the truth is what matters and the data is
    well-behaved, and prefer this when the estimate is traded and returns have tails.

    :param r:     Weight of the most recent observation (decay rate), in (0, 1].
    :param diff:  If ``True``, estimate the covariance of first differences of the stream.
    """

    def __init__(self, r: float = 0.05, diff: bool = False):
        self.r = r
        self.diff = diff
        super().__init__()

    def _init_state(self, n_dim: int) -> dict:
        return ewa_init(n_dim, self.r)

    def _update_state(self, state: dict, x: np.ndarray) -> dict:
        return ewa_update(state, x)

    def _spectrum_inputs(self, state: dict) -> tuple[np.ndarray, int]:
        # Early in the stream the accumulator has seen fewer observations than the decay's
        # asymptotic effective sample, and during burn-in it is a plain empirical average, so the
        # honest sample size is the smaller of the two.
        n_eff = min(float(state["n_samples"]), effective_sample_size(float(state["r"])))
        return np.asarray(state["cov"], dtype=float), int(n_eff) - 1


def _shrink(cov: np.ndarray, n: int) -> np.ndarray:
    """Nonlinearly shrink the spectrum of ``cov``, seen over ``n`` (mean-adjusted) observations."""
    lam, evecs = np.linalg.eigh((cov + cov.T) / 2.0)
    order = np.argsort(lam)
    lam, evecs = lam[order], evecs[:, order]
    dtilde = nonlinear_shrinkage_spectrum(lam, n)
    if dtilde is None or not np.all(np.isfinite(dtilde)) or np.any(dtilde < 0):
        return cov

    # Trace check, because the failure this catches is finite, non-negative and therefore passes
    # every test above. Shrinkage redistributes eigenvalues -- pulling the top down and lifting the
    # bulk -- but it does not change the total by an order of magnitude; Ledoit-Wolf's map is
    # asymptotically trace-preserving. A shrunk spectrum summing to a thousandth of the raw one is
    # not a shrinkage estimate, it is the kernel having divided by something it should have
    # excluded, and returning the unshrunk covariance is strictly better than returning that.
    raw, shrunk = float(np.sum(lam)), float(np.sum(dtilde))
    if raw > 0 and not (_TRACE_TOLERANCE[0] * raw <= shrunk <= _TRACE_TOLERANCE[1] * raw):
        return cov
    return (evecs * dtilde) @ evecs.T
