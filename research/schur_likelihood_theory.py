"""Numerical verification of the worked two-block model in the Schur-likelihood paper.

A scalar two-block Gaussian: x1 ~ N(0, a), x2 = b* x1 + eps, eps ~ N(0, s*). The exact
factorization conditions x2 on x1 with regression coefficient B = b* and Schur complement
(conditional variance) S = s*. The gamma-Schur likelihood damps the conditioning:

    effective coefficient  beta(gamma) = gamma * (C / A)
    damped conditional var S(gamma)    = D - gamma * C^2 / A        (A=Sig11, C=Sig12, D=Sig22)

This script confirms, by maximizing the *population* (large-n Monte-Carlo) gamma-Schur
log-likelihood over candidate covariances Sigma = (A, C, D):

  1. In *effective* (predictive) coordinates the maximizer is the truth for every gamma:
       beta = b*,  S(gamma) = s*.   (gamma-Schur "knows" the true conditional law.)
  2. In *Sigma* coordinates the maximizer is INFLATED:
       A_hat = a,  C_hat = Sig12* / gamma,  D_hat = Sig22* + b*^2 a (1/gamma - 1).
  3. That maximizer leaves the PSD cone (A_hat D_hat - C_hat^2 <= 0) exactly when
       gamma^2 (1 - rho^2) <= (1 - gamma) rho^2,     rho^2 = b*^2 a / (b*^2 a + s*)
     i.e. the usable gamma range shrinks as the block coupling rho^2 grows.

Conclusion (used in papers/schur_likelihood_paper.md): gamma-Schur for gamma<1 is an
improper scoring rule for Sigma (biased toward inflation) and is degenerate as a *free*
estimation objective. It must be used to SCORE a covariance or to TRANSFORM a given one
(shrink the coupling) -- which is what SchurCovariance and Schur allocation do.

    python research/schur_likelihood_theory.py
"""

from __future__ import annotations

import numpy as np


def schur_loglik_population(a, b_star, s_star, gamma, A, C, D):
    """Expected per-sample gamma-Schur log-lik (constants dropped) under the truth (a,b*,s*),
    evaluating candidate covariance (A, C, D). Closed-form expectation, no sampling needed."""
    beta = gamma * C / A
    Sg = D - gamma * C * C / A  # damped conditional variance
    if A <= 0 or Sg <= 0:
        return -np.inf
    # block-1 marginal term (x1): -1/2 (log A + E[x1^2]/A), E[x1^2] = a
    t1 = -0.5 * (np.log(A) + a / A)
    # block-2 conditional term: E[(x2 - beta x1)^2] = (b* - beta)^2 a + s*
    resid = (b_star - beta) ** 2 * a + s_star
    t2 = -0.5 * (np.log(Sg) + resid / Sg)
    return t1 + t2


def closed_form_maximizer(a, b_star, s_star, gamma):
    A = a
    C = b_star * a / gamma
    D = s_star + b_star**2 * a / gamma
    return A, C, D


def spd_threshold_holds(a, b_star, s_star, gamma):
    """True iff the closed-form maximizer is SPD (A D - C^2 > 0)."""
    e = b_star**2 * a
    return gamma**2 * s_star > (1.0 - gamma) * e  # equivalently gamma^2(1-rho^2) > (1-gamma)rho^2


def _numerical_argmax(a, b_star, s_star, gamma, seed=0):
    """Confirm the closed form by random local search over SPD candidates (numpy only)."""
    rng = np.random.default_rng(seed)
    A0, C0, D0 = closed_form_maximizer(a, b_star, s_star, gamma)
    best = (A0, C0, D0)
    best_val = schur_loglik_population(a, b_star, s_star, gamma, A0, C0, D0)
    scale = 0.5
    for _ in range(20000):
        A = A0 * np.exp(scale * rng.standard_normal())
        C = C0 + scale * abs(C0 + 1e-6) * rng.standard_normal()
        D = D0 * np.exp(scale * rng.standard_normal())
        if A * D - C * C <= 0:
            continue
        val = schur_loglik_population(a, b_star, s_star, gamma, A, C, D)
        if val > best_val:
            best_val, best = val, (A, C, D)
    return best, best_val


def report():
    a, b_star, s_star = 1.0, 0.8, 0.5
    e = b_star**2 * a
    rho2 = e / (e + s_star)
    sig12, sig22 = b_star * a, b_star**2 * a + s_star
    print(f"Truth: a={a}, b*={b_star}, s*={s_star}  ->  "
          f"Sigma=[[{a},{sig12}],[{sig12},{sig22}]],  block-R^2 rho^2={rho2:.3f}\n")

    print(f"{'gamma':>6}{'C_hat':>10}{'Sig12*/g':>10}{'D_hat':>10}"
          f"{'beta':>8}{'S(g)':>8}{'SPD?':>6}{'argmax ok':>10}")
    print("-" * 78)
    for gamma in (1.0, 0.9, 0.7, 0.5, 0.3, 0.2, 0.1):
        A, C, D = closed_form_maximizer(a, b_star, s_star, gamma)
        beta = gamma * C / A             # effective coefficient -> should equal b*
        Sg = D - gamma * C * C / A       # damped conditional var -> should equal s*
        spd = spd_threshold_holds(a, b_star, s_star, gamma)
        # numerical confirmation only where the maximizer is SPD (else search space is empty there)
        ok = "-"
        if spd:
            (An, Cn, Dn), _ = _numerical_argmax(a, b_star, s_star, gamma)
            ok = "yes" if (abs(An - A) < 0.05 and abs(Cn - C) < 0.1 and abs(Dn - D) < 0.1) else "NO"
        print(f"{gamma:>6.2f}{C:>10.3f}{sig12 / gamma:>10.3f}{D:>10.3f}"
              f"{beta:>8.3f}{Sg:>8.3f}{str(spd):>6}{ok:>10}")

    gstar = _solve_spd_threshold(rho2)
    print("-" * 78)
    print(f"\nPredicted PSD-exit threshold: gamma_min where gamma^2(1-rho^2)=(1-gamma)rho^2"
          f"  ->  gamma_min={gstar:.3f}")
    print("(Below gamma_min the free gamma-Schur maximizer leaves the PSD cone: gamma-Schur is")
    print(" degenerate as a free estimation objective; use it to score / transform, not to fit.)")


def _solve_spd_threshold(rho2):
    """Root of gamma^2 (1-rho^2) - (1-gamma) rho^2 = 0 in (0,1) (quadratic, positive root)."""
    A, B, C = (1.0 - rho2), rho2, -rho2  # A g^2 + B g + C = 0
    return (-B + np.sqrt(B * B - 4 * A * C)) / (2 * A)


# =====================================================================================
# General case: vector blocks and K-block chains.
#
# The exact (population) expected gamma-Schur log-likelihood of a candidate Sigma under a
# true Sigma, for an arbitrary ordered block partition, has a closed form (no sampling):
#   E[ell_gamma] = -1/2 sum_k [ log det S_k(gamma) + tr( S_k(gamma)^{-1} M_k ) ] + const,
# where for block k with conditioning index set "<k":
#   G_k(gamma) = gamma * Sig_cand[k,<k] Sig_cand[<k,<k]^{-1}     (effective regression)
#   S_k(gamma) = Sig_cand[k,k] - gamma * Sig_cand[k,<k] Sig_cand[<k,<k]^{-1} Sig_cand[<k,k]
#   M_k        = E_true[(x_k - G_k(gamma) x_<k)(.)^T]
#              = Sig_true[k,k] - G_k T[<k,k] - T[k,<k] G_k^T + G_k T[<k,<k] G_k^T   (T = Sig_true)
# This lets us verify the closed-form maximizer by independent local search.
# =====================================================================================


def _blocks(sizes):
    idx, start = [], 0
    for s in sizes:
        idx.append(list(range(start, start + s)))
        start += s
    return idx


def _sub(M, rows, cols):
    return M[np.ix_(rows, cols)]


def expected_schur_loglik(Sig_true, Sig_cand, sizes, gamma):
    """Exact population expected gamma-Schur log-lik (constants dropped)."""
    idx = _blocks(sizes)
    total, prev = 0.0, []
    for rows in idx:
        if not prev:  # block 1: marginal
            Sg = _sub(Sig_cand, rows, rows)
            Mk = _sub(Sig_true, rows, rows)
        else:
            cWW = _sub(Sig_cand, prev, prev)
            cKW = _sub(Sig_cand, rows, prev)
            Gk = gamma * cKW @ np.linalg.inv(cWW)            # effective regression
            Sg = _sub(Sig_cand, rows, rows) - gamma * cKW @ np.linalg.solve(cWW, cKW.T)
            tWW = _sub(Sig_true, prev, prev)
            tKW = _sub(Sig_true, rows, prev)
            tKK = _sub(Sig_true, rows, rows)
            Mk = tKK - Gk @ tKW.T - tKW @ Gk.T + Gk @ tWW @ Gk.T
        evals = np.linalg.eigvalsh(0.5 * (Sg + Sg.T))
        if evals.min() <= 0:
            return -np.inf
        total += -0.5 * (np.sum(np.log(evals)) + np.trace(np.linalg.solve(Sg, Mk)))
        prev = prev + rows
    return total


def closed_form_general(Sig_true, sizes, gamma):
    """Sequential inflated maximizer: per block, effective coef = true regression (recovers the
    true predictive law); implied covariance inflated through the inflated conditioning block."""
    idx = _blocks(sizes)
    p = sum(sizes)
    Sig = np.zeros((p, p))
    prev = []
    for rows in idx:
        if not prev:
            Sig[np.ix_(rows, rows)] = _sub(Sig_true, rows, rows)
        else:
            tWW = _sub(Sig_true, prev, prev)
            tKW = _sub(Sig_true, rows, prev)
            tKK = _sub(Sig_true, rows, rows)
            Bk = tKW @ np.linalg.inv(tWW)                    # true regression B_k*
            Sk = tKK - Bk @ tKW.T                            # true Schur complement S_k*
            cWW = _sub(Sig, prev, prev)                      # candidate (inflated) conditioning cov
            Gk = Bk / gamma                                  # G_k = B_k* / gamma
            cKW = Gk @ cWW
            cKK = Sk + gamma * Gk @ cWW @ Gk.T               # = Sk* + (1/gamma) Bk* cWW Bk*^T
            Sig[np.ix_(rows, prev)] = cKW
            Sig[np.ix_(prev, rows)] = cKW.T
            Sig[np.ix_(rows, rows)] = cKK
        prev = prev + rows
    return 0.5 * (Sig + Sig.T)


def canonical_corr2(Sig, p1):
    """Squared canonical correlations between block-1 (first p1) and block-2."""
    S11 = Sig[:p1, :p1]
    S22 = Sig[p1:, p1:]
    S12 = Sig[:p1, p1:]
    Mmat = np.linalg.solve(S11, S12) @ np.linalg.solve(S22, S12.T)
    return np.clip(np.sort(np.linalg.eigvalsh(0.5 * (Mmat + Mmat.T)))[::-1], 0, 1)


def _is_spd(M, tol=1e-9):
    return np.linalg.eigvalsh(0.5 * (M + M.T)).min() > tol


def _local_search_confirms(Sig_true, sizes, gamma, seed=0, iters=4000):
    """Confirm closed_form_general is a local max of expected_schur_loglik (SPD perturbations)."""
    rng = np.random.default_rng(seed)
    Sig0 = closed_form_general(Sig_true, sizes, gamma)
    if not _is_spd(Sig0):
        return None
    base = expected_schur_loglik(Sig_true, Sig0, sizes, gamma)
    p = Sig0.shape[0]
    best = base
    for _ in range(iters):
        E = 0.02 * rng.standard_normal((p, p))
        E = E + E.T
        cand = Sig0 + E
        if not _is_spd(cand):
            continue
        v = expected_schur_loglik(Sig_true, cand, sizes, gamma)
        if v > best:
            best = v
    return best - base  # <= ~0 (up to search tolerance) confirms Sig0 is the local max


def _random_spd(p, rng):
    A = rng.standard_normal((p, p))
    return A @ A.T + p * np.eye(p)


def report_general():
    print("\n================ GENERAL CASE: vector two-block ================\n")
    rng = np.random.default_rng(1)
    p1, p2 = 3, 2
    Sig_true = _random_spd(p1 + p2, rng)
    rho2 = canonical_corr2(Sig_true, p1)
    rho2_max = rho2[0]
    gmin = _solve_spd_threshold(rho2_max)
    print(f"true canonical corr^2 between blocks: {np.round(rho2, 3)}  -> rho2_max={rho2_max:.3f}")
    print(f"predicted PSD-exit threshold gamma_min(rho2_max) = {gmin:.3f}\n")
    print(f"{'gamma':>6}{'Sig SPD?':>10}{'pred SPD?':>11}{'recovers law':>14}{'max-gap':>10}")
    print("-" * 51)
    for gamma in (1.0, 0.9, 0.8, gmin + 0.02, gmin - 0.02, 0.5, 0.3):
        Sig = closed_form_general(Sig_true, [p1, p2], gamma)
        spd = _is_spd(Sig)
        pred = gamma**2 * (1 - rho2_max) > (1 - gamma) * rho2_max
        # recovers law: effective regression == true regression, damped cond cov == true Schur
        tWW, tKW = Sig_true[:p1, :p1], Sig_true[p1:, :p1]
        Bstar = tKW @ np.linalg.inv(tWW)
        Sstar = Sig_true[p1:, p1:] - Bstar @ tKW.T
        cWW, cKW = Sig[:p1, :p1], Sig[p1:, :p1]
        Geff = gamma * cKW @ np.linalg.inv(cWW)
        Sg = Sig[p1:, p1:] - gamma * cKW @ np.linalg.solve(cWW, cKW.T)
        recovers = np.allclose(Geff, Bstar, atol=1e-6) and np.allclose(Sg, Sstar, atol=1e-6)
        gap = _local_search_confirms(Sig_true, [p1, p2], gamma) if spd else None
        gaps = f"{gap:+.2e}" if gap is not None else "   (n/a)"
        print(f"{gamma:>6.2f}{str(spd):>10}{str(pred):>11}{str(recovers):>14}{gaps:>10}")

    print("\n================ GENERAL CASE: 3-block chain (scalar) ================\n")
    rng = np.random.default_rng(7)
    Sig_true3 = _random_spd(3, rng)
    print("recovery + inflation compounding through the conditioning covariance:\n")
    print(f"{'gamma':>6}{'Sig SPD?':>10}{'recovers all':>14}{'max-gap':>10}")
    print("-" * 40)
    for gamma in (1.0, 0.9, 0.8, 0.7, 0.6, 0.5):
        Sig = closed_form_general(Sig_true3, [1, 1, 1], gamma)
        spd = _is_spd(Sig)
        # check every block conditional recovers truth
        rec = True
        prev = []
        for rows in _blocks([1, 1, 1]):
            if prev:
                tWW = _sub(Sig_true3, prev, prev)
                tKW = _sub(Sig_true3, rows, prev)
                Bstar = tKW @ np.linalg.inv(tWW)
                Sstar = _sub(Sig_true3, rows, rows) - Bstar @ tKW.T
                cWW = _sub(Sig, prev, prev)
                cKW = _sub(Sig, rows, prev)
                Geff = gamma * cKW @ np.linalg.inv(cWW)
                Sg = _sub(Sig, rows, rows) - gamma * cKW @ np.linalg.solve(cWW, cKW.T)
                rec = (rec and np.allclose(Geff, Bstar, atol=1e-6)
                       and np.allclose(Sg, Sstar, atol=1e-6))
            prev = prev + rows
        gap = _local_search_confirms(Sig_true3, [1, 1, 1], gamma) if spd else None
        gaps = f"{gap:+.2e}" if gap is not None else "   (n/a)"
        print(f"{gamma:>6.2f}{str(spd):>10}{str(rec):>14}{gaps:>10}")


if __name__ == "__main__":
    report()
    report_general()
