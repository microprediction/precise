"""Which covariance *evaluation metric* has the most statistical power?

A meta-experiment. When we benchmark covariance estimators we score their estimates with some
metric on held-out data — log-likelihood, Frobenius error, Stein loss, a min-variance portfolio's
realized variance, random projections, ... Which of these is the best *judge*: the one that most
reliably ranks a genuinely-better estimate above a worse one, from the fewest test samples?

Design: we know the truth Σ, so we can build two estimates with a known quality ordering (smaller
exact KL divergence to Σ is better). Then, using only a finite test SAMPLE (no access to Σ), we ask
each metric to order the pair. Power = P(metric agrees with the true KL ordering), as a function of
the test-set size. Paired scoring (both estimates judged on the same test set) and a fresh random
estimate-pair + test set per trial make the estimate a clean Monte-Carlo power.

    python research/metric_power.py
"""

from __future__ import annotations

import numpy as np


# ----------------------------------------------------------------- truth & estimate pairs
def _spd_factor(p, rng, k=3):
    B = rng.standard_normal((p, k))
    return B @ B.T + np.diag(rng.uniform(0.3, 1.2, size=p))


def _project_pd(m, floor_ratio=1e-3):
    w, V = np.linalg.eigh((m + m.T) / 2)
    w = np.clip(w, floor_ratio * w.max(), None)
    return (V * w) @ V.T


def _perturb(cov, eps, rng):
    """A noisy, PD estimate-like matrix: Σ + eps * (scaled random symmetric noise)."""
    a = rng.standard_normal(cov.shape)
    e = (a + a.T) / 2
    e *= np.linalg.norm(cov) / np.linalg.norm(e)
    return _project_pd(cov + eps * e)


def _kl(true_cov, est_cov):
    """KL( N(0, true) || N(0, est) ) — exact; lower means the estimate is closer to the truth."""
    p = len(true_cov)
    prec = np.linalg.inv(est_cov)
    _, ld_est = np.linalg.slogdet(est_cov)
    _, ld_true = np.linalg.slogdet(true_cov)
    return 0.5 * (np.trace(prec @ true_cov) - p + ld_est - ld_true)


# ------------------------------------------------------- candidate metrics (higher == better)
def _loglik(cov, X):
    prec = np.linalg.inv(cov)
    _, logdet = np.linalg.slogdet(prec)
    quad = np.einsum("ij,jk,ik->i", X, prec, X)
    return float(np.mean(0.5 * logdet - 0.5 * quad))


def _frobenius(cov, X):
    S = np.cov(X, rowvar=False, bias=True)
    return -float(np.linalg.norm(cov - S))


def _stein(cov, X):
    S = np.cov(X, rowvar=False, bias=True)
    M = np.linalg.inv(cov) @ S
    _, logdet = np.linalg.slogdet(M)
    return -float(np.trace(M) - logdet - len(cov))


def _random_projection(cov, X, dirs):
    pv = np.einsum("rp,pq,rq->r", dirs, cov, dirs)  # predicted variance per direction
    proj = X @ dirs.T  # (n, R)
    # 1-D Gaussian log-likelihood of the projected data, averaged over directions and samples.
    ll = -0.5 * np.log(pv) - 0.5 * (proj**2) / pv
    return float(np.mean(ll))


def _min_variance(cov, X):
    ones = np.ones(len(cov))
    w = np.linalg.solve(cov, ones)
    w /= w.sum()
    return -float(np.mean((X @ w) ** 2))  # realized out-of-sample portfolio variance


def _mahalanobis_cal(cov, X):
    prec = np.linalg.inv(cov)
    maha2 = np.einsum("ij,jk,ik->i", X, prec, X)
    return -abs(float(np.mean(maha2)) - len(cov))


METRICS = {
    "loglik": lambda cov, X, dirs: _loglik(cov, X),
    "frobenius": lambda cov, X, dirs: _frobenius(cov, X),
    "stein": lambda cov, X, dirs: _stein(cov, X),
    "random_proj": lambda cov, X, dirs: _random_projection(cov, X, dirs),
    "min_variance": lambda cov, X, dirs: _min_variance(cov, X),
    "maha_calib": lambda cov, X, dirs: _mahalanobis_cal(cov, X),
}


# ----------------------------------------------------------------- power experiment
def run(p=15, eps_good=0.15, eps_bad=0.32, n_grid=(25, 50, 100, 200, 400), trials=400,
        n_dirs=50, min_gap=0.02, seed=0):
    """Return ``{metric: {n_test: power}}`` and the mean true KL gap actually tested."""
    rng = np.random.default_rng(seed)
    n_grid = list(n_grid)
    correct = {m: {n: 0 for n in n_grid} for m in METRICS}
    counted = {n: 0 for n in n_grid}
    gaps = []

    for _ in range(trials):
        true_cov = _spd_factor(p, rng)
        good = _perturb(true_cov, eps_good, rng)
        bad = _perturb(true_cov, eps_bad, rng)
        kl_good, kl_bad = _kl(true_cov, good), _kl(true_cov, bad)
        # Per-trial ground truth: the lower-KL matrix is genuinely better.
        a, b = (good, bad) if kl_good <= kl_bad else (bad, good)
        gap = abs(kl_good - kl_bad)
        if gap < min_gap:
            continue  # skip pairs that are essentially tied (nothing meaningful to detect)
        gaps.append(gap)
        dirs = rng.standard_normal((n_dirs, p))
        dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
        biggest_n = max(n_grid)
        pool = rng.multivariate_normal(np.zeros(p), true_cov, size=biggest_n)
        for n in n_grid:
            X = pool[:n]
            counted[n] += 1
            for name, fn in METRICS.items():
                if fn(a, X, dirs) > fn(b, X, dirs):  # metric ranks the truly-better one higher
                    correct[name][n] += 1

    power = {m: {n: correct[m][n] / counted[n] for n in n_grid} for m in METRICS}
    return power, float(np.mean(gaps)), n_grid


def report(power, mean_gap, n_grid) -> str:
    lines = [
        f"Statistical power of covariance evaluation metrics  (mean true KL gap = {mean_gap:.3f})",
        "Power = P(metric ranks the lower-KL estimate higher), by test-set size n:",
        "",
        f"{'metric':14}" + "".join(f"{('n=' + str(n)):>9}" for n in n_grid) + f"{'  mean':>8}",
        "-" * (14 + 9 * len(n_grid) + 8),
    ]
    order = sorted(power, key=lambda m: -np.mean(list(power[m].values())))
    for m in order:
        row = "".join(f"{power[m][n]:>9.3f}" for n in n_grid)
        lines.append(f"{m:14}{row}{np.mean(list(power[m].values())):>8.3f}")
    return "\n".join(lines)


# ------------------------------------------------- random k-dimensional projection scoring
def _random_subspaces(p, k, n_sub, rng):
    """A list of ``n_sub`` orthonormal (k, p) projection matrices."""
    subs = []
    for _ in range(n_sub):
        q, _ = np.linalg.qr(rng.standard_normal((p, k)))
        subs.append(q[:, :k].T)
    return subs


def _kproj_loglik(cov, X, subspaces):
    """Mean joint k-D Gaussian log-likelihood of X projected onto each random subspace."""
    total = 0.0
    for W in subspaces:
        Z = X @ W.T  # (n, k)
        C = W @ cov @ W.T  # (k, k) predicted covariance in the subspace
        prec = np.linalg.inv(C)
        _, logdet = np.linalg.slogdet(prec)
        quad = np.einsum("ij,jk,ik->i", Z, prec, Z)
        total += float(np.mean(0.5 * logdet - 0.5 * quad))
    return total / len(subspaces)


def projection_power(p=18, k_list=(1, 2, 3, 5, 10, None), total_dirs=60, eps_good=0.04,
                     eps_bad=0.055, n_test=40, trials=700, min_gap=0.005, seed=3):
    """Power of random k-D projection scoring vs the projection dimension k.

    The *total direction budget* is held ~constant (``n_sub = total_dirs // k``) so the comparison
    isolates the effect of scoring jointly in k dimensions versus marginally. ``k=None`` means the
    full dimension p (which is the full Gaussian log-likelihood, up to rotation).
    """
    rng = np.random.default_rng(seed)
    correct = {k: 0 for k in k_list}
    counted = 0
    gaps = []
    for _ in range(trials):
        true_cov = _spd_factor(p, rng)
        good, bad = _perturb(true_cov, eps_good, rng), _perturb(true_cov, eps_bad, rng)
        kl_good, kl_bad = _kl(true_cov, good), _kl(true_cov, bad)
        a, b = (good, bad) if kl_good <= kl_bad else (bad, good)
        gap = abs(kl_good - kl_bad)
        if gap < min_gap:
            continue
        gaps.append(gap)
        counted += 1
        X = rng.multivariate_normal(np.zeros(p), true_cov, size=n_test)
        for k in k_list:
            kk = p if k is None else k
            subs = _random_subspaces(p, kk, max(1, total_dirs // kk), rng)
            if _kproj_loglik(a, X, subs) > _kproj_loglik(b, X, subs):
                correct[k] += 1
    power = {k: correct[k] / counted for k in k_list}
    return power, float(np.mean(gaps))


def projection_report(power, mean_gap, p=18) -> str:
    lines = [
        f"Power of random k-D projection scoring vs k  (mean KL gap = {mean_gap:.3f})",
        "(total direction budget held ~constant; k=p is the full Gaussian log-likelihood)",
        "",
        f"{'k':>6}{'power':>10}",
        "-" * 16,
    ]
    for k in power:
        label = f"{('p=' + str(p)) if k is None else k}"
        lines.append(f"{label:>6}{power[k]:>10.3f}")
    return "\n".join(lines)


# ------------------------------------------------- high-dimensional cost of the full likelihood
def compute_scaling(ps=(50, 100, 200, 400), n_test=64, k=5, repeats=40, seed=0):
    """Per-evaluation cost of the full Gaussian log-likelihood vs k-D projection scoring.

    The full likelihood needs the precision and log-determinant of the dense p x p estimate
    (O(p^3)); k-D projection scoring needs only ``W Σ̂ Wᵀ`` and a k x k inverse. In high dimensions
    the full likelihood is also *statistically* fragile: it is dominated by the smallest eigenvalues
    of the estimate, which are exactly the least identifiable when the sample size is not >> p.
    """
    import time

    rng = np.random.default_rng(seed)
    rows = []
    for p in ps:
        cov = _spd_factor(p, rng)
        X = rng.multivariate_normal(np.zeros(p), cov, size=n_test)
        subs = _random_subspaces(p, k, max(1, 60 // k), rng)
        t = time.perf_counter()
        for _ in range(repeats):
            _loglik(cov, X)
        t_ll = (time.perf_counter() - t) / repeats * 1e3
        t = time.perf_counter()
        for _ in range(repeats):
            _kproj_loglik(cov, X, subs)
        t_pr = (time.perf_counter() - t) / repeats * 1e3
        rows.append((p, t_ll, t_pr))
    lines = [f"{'p':>6}{'loglik_ms':>12}{'proj_k' + str(k) + '_ms':>13}", "-" * 31]
    lines += [f"{p:>6}{a:>12.3f}{b:>13.3f}" for p, a, b in rows]
    return "\n".join(lines)


if __name__ == "__main__":
    pw, gap, grid = run()
    print(report(pw, gap, grid))
    print()
    ppw, pgap = projection_power()
    print(projection_report(ppw, pgap))
    print("\nPer-evaluation compute cost (full likelihood is O(p^3)):")
    print(compute_scaling())
