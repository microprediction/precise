"""What the Frobenius error cannot see: churn.

``research/forgetting.py`` scores estimators by squared error against the true covariance and
concludes that a rolling window beats an expanding sample wherever dependence drifts. That metric is
blind to how the estimate *moves*, and anyone trading on it pays for movement.

A rolling window has a hard boundary. An observation enters the estimate on arrival and leaves it
exactly ``W`` periods later, so a shock is paid for twice: once when it happens, and once when it
drops out and the estimate jumps back for no reason in the world. Exponential decay has no such
discontinuity -- an observation's influence fades smoothly and never leaves. That is the one axis on
which the effective-sample-size route rejected by
:class:`~precise.nonlinear_shrinkage.WindowedNonlinearShrinkageCovariance` can win, and rejecting it
on statistical exactness said nothing about it.

Two measurements.

``impulse_response`` injects one large observation into an otherwise stationary stream and reports
minimum-variance turnover around it, against a comparison whose effective memory is *matched*:
``(2-r)/r = W``, so ``r = 2/(W+1)``. Without matching, an exponentially weighted estimator with a
shorter memory simply reacts more, and the comparison measures the memory rather than the boundary.

``portfolio`` scores realized risk and turnover together over a regime change, so the accuracy win
and the churn cost can be read on the same page.

What they find: the echo is real and sharp -- at exactly ``W`` the window rebalances hard because
nothing happened -- and it roughly doubles what a shock costs. Whether that matters in aggregate
depends on how many shocks the stream holds, so ``portfolio`` also runs with multivariate-t
innovations. Under Gaussian draws the window's average turnover is *lower* than the matched
exponential decay; at ``t(4)`` it is higher; at ``t(3)`` it is 15% higher and its realized risk is
worse too. Equity returns are not Gaussian, so the squared-error table in ``forgetting.py`` is not
by itself a reason to prefer a window for anything that trades.

One reading caveat for the heavy-tailed table. ``LedoitWolfCovariance`` posts very low turnover
there, and it is not a virtue: fat-tailed observations inflate its running dispersion statistic
and saturate the shrinkage intensity, so it collapses towards a scaled identity. At ``t(3)`` it
retains under a tenth of the covariance structure that OAS retains, and its realized risk is the
worst in the table. It is static because it has stopped estimating, not because it is stable.

    python research/turnover.py
"""

from __future__ import annotations

import numpy as np

from precise import (
    EwaCovariance,
    LedoitWolfCovariance,
    NonlinearShrinkageCovariance,
    OASCovariance,
    WindowedNonlinearShrinkageCovariance,
)
from precise.nonlinear_shrinkage import _shrink


class EwaNonlinearShrinkage:
    """Contrast arm, not shipped: EW accumulator cleaned with an effective sample size.

    The substitution is an approximation -- the whole weight distribution enters the limiting
    spectrum, not just its second moment -- which is why the package ships a window instead. It is
    here because approximate and smooth may beat exact and jumpy once turnover is priced.
    """

    def __init__(self, r: float):
        self.r = r
        self.n_eff = int((2 - r) / r)
        self._est = EwaCovariance(r=r)

    def partial_fit(self, x):
        self._est.partial_fit(x)
        return self

    @property
    def covariance_(self) -> np.ndarray:
        return _shrink(self._est.covariance_, self.n_eff - 1)


def matched_decay(window: int) -> float:
    """The EW decay whose effective sample size equals ``window``: ``(2-r)/r = W``."""
    return 2.0 / (window + 1.0)


def mv_weights(cov: np.ndarray) -> np.ndarray:
    """Unconstrained minimum-variance weights, the standard sensitivity probe for an estimate."""
    p = cov.shape[0]
    try:
        w = np.linalg.solve(cov + 1e-10 * np.eye(p), np.ones(p))
    except np.linalg.LinAlgError:
        return np.ones(p) / p
    total = w.sum()
    return np.ones(p) / p if abs(total) < 1e-12 else w / total


def _factor_cov(p, rng, k=3, load=1.2):
    B = np.linalg.qr(rng.standard_normal((p, p)))[0][:, :k] * load
    return B @ B.T + np.diag(0.3 + 0.4 * rng.random(p))


def impulse_response(p=32, window=250, n=1400, shock_at=700, shock_size=8.0, seeds=6):
    """Turnover around a single large observation, window versus memory-matched EW decay."""
    r = matched_decay(window)
    names = [f"window W={window}", f"EW n_eff={int((2 - r) / r)}"]
    turnover = {nm: np.zeros(n) for nm in names}

    for seed in range(seeds):
        rng = np.random.default_rng(300 + seed)
        cov = _factor_cov(p, rng)
        chol = np.linalg.cholesky(cov)
        arms = {
            names[0]: WindowedNonlinearShrinkageCovariance(window=window),
            names[1]: EwaNonlinearShrinkage(r),
        }
        prev = dict.fromkeys(names)
        for t in range(n):
            x = chol @ rng.standard_normal(p)
            if t == shock_at:
                x = x * shock_size  # one large observation, then back to normal
            for arm in arms.values():
                arm.partial_fit(x)
            for nm, arm in arms.items():
                w = mv_weights(arm.covariance_)
                if prev[nm] is not None:
                    turnover[nm][t] = float(np.abs(w - prev[nm]).sum())
                prev[nm] = w

    out = {}
    for nm in names:
        path = turnover[nm] / seeds
        # Baseline from a quiet stretch before the shock, clamped so a small shock_at cannot
        # produce a negative start index and an empty (nan) slice.
        lo = max(shock_at // 2, shock_at - 300)
        base = float(np.median(path[lo : shock_at - 10]))
        out[nm] = {
            "baseline": base,
            "arrival": float(path[shock_at : shock_at + 3].sum() / base),
            "echo": float(path[shock_at + window - 2 : shock_at + window + 3].sum() / base),
            "path": path,
        }
    return out


def portfolio(p=32, n=4000, seeds=3, burn=800, window=250, bps=10.0, df=None):
    """Realized minimum-variance risk and turnover across a regime change, memory matched.

    ``df`` sets the degrees of freedom of a multivariate-t innovation; ``None`` is Gaussian. This
    matters for the boundary echo: the echo is charged per shock, so how much it costs in aggregate
    depends on how many shocks the stream contains, and equity returns are not Gaussian.
    """
    r = matched_decay(window)
    names = ["NLS expanding", "LedoitWolf", "OAS", "EW-NLS n_eff", f"NLS window W={window}"]
    acc = {nm: {"risk": [], "turnover": []} for nm in names}

    for seed in range(seeds):
        rng = np.random.default_rng(200 + seed)
        before, after = _factor_cov(p, rng), _factor_cov(p, rng)
        chol = {0: np.linalg.cholesky(before), 1: np.linalg.cholesky(after)}
        half = n // 2
        arms = {
            "NLS expanding": NonlinearShrinkageCovariance(),
            "LedoitWolf": LedoitWolfCovariance(r=r),
            "OAS": OASCovariance(r=r),
            "EW-NLS n_eff": EwaNonlinearShrinkage(r),
            f"NLS window W={window}": WindowedNonlinearShrinkageCovariance(window=window),
        }
        prev, risk, turn = dict.fromkeys(names), {nm: [] for nm in names}, {nm: [] for nm in names}
        for t in range(n):
            regime = 0 if t < half else 1
            truth = before if regime == 0 else after
            z = rng.standard_normal(p)
            if df is not None:  # multivariate t, scaled to keep the covariance unchanged
                z *= np.sqrt(df / rng.chisquare(df)) * np.sqrt((df - 2) / df)
            x = chol[regime] @ z
            for arm in arms.values():
                arm.partial_fit(x)
            if t >= burn:
                for nm, arm in arms.items():
                    w = mv_weights(arm.covariance_)
                    risk[nm].append(float(w @ truth @ w))
                    if prev[nm] is not None:
                        turn[nm].append(float(np.abs(w - prev[nm]).sum()))
                    prev[nm] = w
        for nm in names:
            acc[nm]["risk"].append(float(np.mean(risk[nm])))
            acc[nm]["turnover"].append(float(np.mean(turn[nm])))

    return {
        nm: {
            "ann_vol": float(np.sqrt(np.mean(v["risk"]) * 252)),
            "turnover": float(np.mean(v["turnover"])),
            "ann_cost": float(252 * (bps / 1e4) * np.mean(v["turnover"])),
        }
        for nm, v in acc.items()
    }


def report(impulse, port, window=250) -> str:
    lines = [f"Turnover around one 8x shock, relative to each estimator's own pre-shock median "
             f"(W={window}, memory matched):", ""]
    lines.append(f"{'estimator':<18}{'on arrival':>14}{'at the W boundary':>22}")
    for nm, v in impulse.items():
        lines.append(f"{nm:<18}{v['arrival']:>13.1f}x{v['echo']:>21.1f}x")
    lines += ["", "Minimum-variance portfolio across a regime change:", ""]
    lines.append(f"{'estimator':<20}{'ann. vol':>10}{'turnover':>11}{'ann. cost':>11}{'total':>10}")
    for nm, v in port.items():
        lines.append(f"{nm:<20}{v['ann_vol']:>10.4f}{v['turnover']:>11.4f}"
                     f"{v['ann_cost']:>11.4f}{v['ann_vol'] + v['ann_cost']:>10.4f}")
    return "\n".join(lines)


def tail_sweep(window=250, dfs=(None, 4, 3)):
    """Turnover and realized risk as the innovation tails fatten."""
    return {("gaussian" if df is None else f"t({df})"): portfolio(window=window, df=df)
            for df in dfs}


if __name__ == "__main__":
    w = 250
    print(report(impulse_response(window=w), portfolio(window=w), window=w))
    print("\n\nAs the tails fatten (turnover relative to the memory-matched EW decay):\n")
    sweep = tail_sweep(window=w)
    arms_ = list(next(iter(sweep.values())))
    print(f"{'innovations':<14}" + "".join(nm.rjust(22) for nm in arms_))
    for tag, res in sweep.items():
        base = res["EW-NLS n_eff"]["turnover"]
        print(f"{tag:<14}" + "".join(
            f"{res[nm]['turnover'] / base:>21.2f}x" for nm in arms_))
