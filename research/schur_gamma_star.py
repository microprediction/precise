"""A closed-form gamma* in the tractable two-block case (the simplified case that DOES solve).

The general gamma* resisted a closed form because, for a shrinkage *pair* of estimators, the
discriminating signal is second-order in the sampling noise (research/schur_spiked.py). But the
quantity gamma actually controls -- how much to trust the estimated cross-block coupling -- has a
first-order optimum: a Wiener / James-Stein shrinkage of the coupling.

Scalar two-block model: x1 ~ N(0,a); x2 = b x1 + eps, eps ~ N(0,s). The true conditional law of
x2|x1 has regression b and conditional variance s. From n samples the OLS estimate b_hat is unbiased
with Var(b_hat) = s / (a (n-2)). The gamma-Schur estimate uses the damped coupling gamma*b_hat.
The expected test predictive residual is

    R(gamma) = E (x2 - gamma b_hat x1)^2 = [ b^2 (1-gamma)^2 + gamma^2 Var(b_hat) ] a + s,

and the predictive log-likelihood is maximized by minimizing R (profiling out the conditional
variance). Minimizing R gives, with the block coupling rho^2 = b^2 a / (b^2 a + s) (the conditional
R^2):

    gamma* = b^2 / (b^2 + Var(b_hat)) = (n-2) rho^2 / ( (n-2) rho^2 + (1 - rho^2) ).

So gamma* is the RELIABILITY of the coupling: ->1 as n->inf or rho^2->1 (trust it: full likelihood),
->0 as rho^2->0 (ignore it: block-diagonal), interior when the coupling is partially reliable --
the paper's thesis, in closed form. This script verifies gamma* against the simulated argmin of R,
and confirms the monotonicities.

    python research/schur_gamma_star.py
"""

from __future__ import annotations

import numpy as np


def gamma_star(n, rho2):
    """Closed-form optimal coupling trust (scalar two-block)."""
    return (n - 2) * rho2 / ((n - 2) * rho2 + (1 - rho2))


def _ab_s_from(rho2, s=1.0):
    """Pick (a, b, s) realizing a given block coupling rho^2 (a=1; e = b^2 a = rho2/(1-rho2) s)."""
    e = rho2 / (1 - rho2) * s
    return 1.0, np.sqrt(e), s  # a, b, s


def residual_R(gamma, a, b, s, n, n_draws, rng):
    """Monte-Carlo expected test predictive residual E[(x2 - gamma b_hat x1)^2] over draws."""
    vals = np.empty(n_draws)
    for k in range(n_draws):
        x1 = rng.normal(0.0, np.sqrt(a), n)
        x2 = b * x1 + rng.normal(0.0, np.sqrt(s), n)
        b_hat = (x1 @ x2) / (x1 @ x1)
        vals[k] = (b - gamma * b_hat) ** 2 * a + s  # E over test x of (x2 - gamma b_hat x1)^2
    return vals.mean()


def empirical_gamma_star(rho2, n, n_draws=20000, seed=0):
    a, b, s = _ab_s_from(rho2)
    rng = np.random.default_rng(seed)
    # closed-form argmin of R is gamma* ; confirm by a fine grid of Monte-Carlo R(gamma)
    grid = np.linspace(0.0, 1.0, 51)
    Rs = [residual_R(g, a, b, s, n, n_draws, rng) for g in grid]
    return grid[int(np.argmin(Rs))]


def report():
    print("=== closed-form gamma* vs simulated argmin of the predictive residual ===\n")
    print(f"{'n':>5}{'rho^2':>8}{'gamma* (closed)':>18}{'gamma* (simulated)':>20}")
    print("-" * 51)
    for n in (5, 10, 30, 100):
        for rho2 in (0.1, 0.3, 0.6, 0.9):
            gc = gamma_star(n, rho2)
            ge = empirical_gamma_star(rho2, n, n_draws=15000, seed=n * 100 + int(100 * rho2))
            print(f"{n:>5}{rho2:>8.2f}{gc:>18.3f}{ge:>20.3f}")

    print("\n=== monotonicities (the paper's thesis, in closed form) ===\n")
    print("gamma* increases with sample size n (fix rho^2=0.4):")
    print("   " + "  ".join(f"n={n}:{gamma_star(n, 0.4):.3f}" for n in (3, 5, 10, 30, 100, 1000)))
    print("gamma* increases with coupling rho^2 (fix n=20):")
    print("   " + "  ".join(f"r={r}:{gamma_star(20, r):.3f}" for r in (0.05, 0.2, 0.5, 0.8, 0.99)))
    print("\n   limits:  rho^2->1 => gamma*->1 (full likelihood);"
          "  rho^2->0 => gamma*->0 (block-diagonal);")
    print("            n->inf  => gamma*->1.   Interior when the coupling is partially reliable.")


if __name__ == "__main__":
    report()
