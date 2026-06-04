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


if __name__ == "__main__":
    report()
