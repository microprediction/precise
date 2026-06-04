"""Toward a closed form for gamma* under a spiked model (the open item in section 10).

Section 5 located the high-dimensional advantage in ESTIMATE instability: the training-draw variance
of the score gap, driven by d W_gamma / d Sigma_hat, which at gamma=1 (W_1 = Sigma_hat^-1) scales
like 1/lambda_min^2 per entry -> 1/lambda_min^4 in the variance. This makes that quantitative:

  * Monte-Carlo training-draw SNR(gamma) in a spiked model, exhibiting the interior gamma* and how
    it moves with the sample size n and with the coupling reliability;
  * a delta-method (first-order) prediction of that SNR from the model spectrum and n alone -- no
    simulation -- using the Gaussian sampling covariance of S, Cov(S_ij,S_kl)=(Sig_ik Sig_jl +
    Sig_il Sig_jk)/n, propagated through the analytic gradient of the score gap;
  * the explicit gamma=1 variance blow-up vs the bounded gamma<1 variance.

We report honestly where the linearization holds and where it breaks: it predicts the VARIANCE
(the blow-up) well, but not gamma* -- the signal/shrinkage benefit is second-order in the sampling
noise, so first-order propagation misses it. The interior gamma* is a genuinely nonlinear effect.

    python research/schur_spiked.py
"""

from __future__ import annotations

import numpy as np

from research.schur_godambe import _spiked, schur_operator
from research.schur_likelihood_theory import _is_spd


def _estimates(S, alpha_a, alpha_b):
    """Two shrinkage estimates of the same sample cov S: A well-shrunk, B under-shrunk."""
    p = S.shape[0]
    target = (np.trace(S) / p) * np.eye(p)
    A = (1 - alpha_a) * S + alpha_a * target
    B = (1 - alpha_b) * S + alpha_b * target
    return 0.5 * (A + A.T), 0.5 * (B + B.T)


def _score_gap(S, sizes, gamma, Sig_t, alpha_a, alpha_b):
    """D(S) = E_test[ell_gamma(A) - ell_gamma(B)] = -1/2[Ld_A - Ld_B + tr((W_A - W_B) Sig_t)]."""
    A, B = _estimates(S, alpha_a, alpha_b)
    if not (_is_spd(A) and _is_spd(B)):
        return np.nan
    WA, LdA = schur_operator(A, sizes, gamma)
    WB, LdB = schur_operator(B, sizes, gamma)
    return -0.5 * ((LdA - LdB) + np.trace((WA - WB) @ Sig_t))


def snr_montecarlo(p, n, sizes, gamma, alpha_a, alpha_b, Sig_t, n_draws=600, seed=0):
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_draws):
        X = rng.multivariate_normal(np.zeros(p), Sig_t, size=n)
        S = np.cov(X, rowvar=False, bias=True)
        d = _score_gap(S, sizes, gamma, Sig_t, alpha_a, alpha_b)
        if not np.isnan(d):
            vals.append(d)
    v = np.array(vals)
    return v.mean(), v.std(), (v.mean() / v.std() if v.std() > 0 else np.inf)


def _grad_score_gap(S, sizes, gamma, Sig_t, alpha_a, alpha_b, h=1e-5):
    """Gradient of D w.r.t. the (symmetric) sample covariance S, by central differences."""
    p = S.shape[0]
    G = np.zeros((p, p))
    for i in range(p):
        for j in range(i, p):
            E = np.zeros((p, p))
            E[i, j] = E[j, i] = 1.0
            dp = _score_gap(S + h * E, sizes, gamma, Sig_t, alpha_a, alpha_b)
            dm = _score_gap(S - h * E, sizes, gamma, Sig_t, alpha_a, alpha_b)
            G[i, j] = G[j, i] = (dp - dm) / (2 * h)
    return G


def _cov_quadform(G, Sig, n):
    """Var of <G, S> for S ~ Gaussian sample cov: sum_{ij,kl} G_ij Cov(S_ij,S_kl) G_kl,
    Cov(S_ij,S_kl) = (Sig_ik Sig_jl + Sig_il Sig_jk)/n. Closed form: (2/n) tr((G Sig)^2)."""
    M = G @ Sig
    return (2.0 / n) * np.trace(M @ M)


def snr_delta(p, n, sizes, gamma, alpha_a, alpha_b, Sig_t):
    """Delta-method SNR: mean ~ D(Sig_t), variance ~ (2/n) tr((grad D . Sig_t)^2)."""
    mean = _score_gap(Sig_t, sizes, gamma, Sig_t, alpha_a, alpha_b)
    G = _grad_score_gap(Sig_t, sizes, gamma, Sig_t, alpha_a, alpha_b)
    var = _cov_quadform(G, Sig_t, n)
    return mean, np.sqrt(var), (mean / np.sqrt(var) if var > 0 else np.inf)


def variance_blowup(p=24, seed=1):
    """Show the gamma=1 variance scaling like 1/lambda_min^4 as the truth conditioning worsens,
    vs bounded gamma<1. Uses the delta-method variance term (2/n) tr((grad D . Sig)^2)."""
    sizes = [4] * (p // 4)
    print(f"{'lambda_min':>11}{'cond':>8}" + "".join(f"  Var(g={g:.1f})" for g in (1.0, 0.7, 0.3)))
    print("-" * 56)
    for bulk in (0.5, 0.2, 0.08, 0.03):
        Sig_t, _, _ = _spiked(p, spike=12.0, bulk=bulk, seed=seed)
        lam = np.linalg.eigvalsh(Sig_t).min()
        cond = np.linalg.cond(Sig_t)
        row = ""
        for g in (1.0, 0.7, 0.3):
            G = _grad_score_gap(Sig_t, sizes, g, Sig_t, 0.5, 0.05)
            row += f"{_cov_quadform(G, Sig_t, 60):11.1f}"
        print(f"{lam:>11.3f}{cond:>8.0f}{row}")


def report():
    print("=== spiked model: training-draw SNR(gamma), Monte-Carlo vs delta-method ===\n")
    gammas = (1.0, 0.9, 0.7, 0.5, 0.3, 0.1)
    for p, n in ((24, 30), (40, 50)):
        sizes = [4] * (p // 4)
        Sig_t, _, _ = _spiked(p, spike=12.0, bulk=0.15, seed=p)
        print(f"p={p}, n={n}, spiked (bulk=0.15):")
        print(f"{'':12}" + "".join(f"  g={g:.2f}" for g in gammas) + f"{'argmax':>9}")
        mc = [snr_montecarlo(p, n, sizes, g, 0.5, 0.05, Sig_t, n_draws=500, seed=p)[2]
              for g in gammas]
        dl = [snr_delta(p, n, sizes, g, 0.5, 0.05, Sig_t)[2] for g in gammas]
        gm = gammas[int(np.argmax(mc))]
        gd = gammas[int(np.argmax([abs(x) for x in dl]))]
        print(f"{'monte-carlo':12}" + "".join(f"{x:8.2f}" for x in mc) + f"{gm:>9.2f}")
        print(f"{'delta-method':12}" + "".join(f"{x:8.2f}" for x in dl) + f"{gd:>9.2f}\n")

    print("=== gamma=1 variance blow-up with truth conditioning (delta-method Var) ===\n")
    variance_blowup()


if __name__ == "__main__":
    report()
