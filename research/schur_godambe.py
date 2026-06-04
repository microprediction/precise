"""Discrimination efficiency of the Schur pseudo-likelihood, and the Godambe boundary.

This makes section 4(2) of the paper exact. The gamma-Schur score of a candidate covariance
is a quadratic form in the data,

    ell_gamma(Sig_hat; x) = -1/2 [ Ld_gamma(Sig_hat) + x^T W_gamma(Sig_hat) x ]  + const,

where W_gamma(Sig_hat) = sum_k T_k^T S_k(gamma)^{-1} T_k is the gamma-Schur operator
(T_k = [-gamma G_k, I, 0] selects block k minus its gamma-damped regression on earlier blocks)
and Ld_gamma = sum_k log det S_k(gamma). At gamma=1, W_1 = Sig_hat^{-1} exactly (block LDL^T).

For two candidates A, B and true Sigma_t, the per-test-sample score difference
d(x) = ell_gamma(A;x) - ell_gamma(B;x) has, under x ~ N(0, Sig_t) (Gaussian quadratic form):

    mu(gamma)    = -1/2 [ (Ld_A - Ld_B) + tr((W_A - W_B) Sig_t) ]
    sigma^2(g.)  =  1/2  tr( ((W_A - W_B) Sig_t)^2 )

so n_test samples rank A above B with probability ~ Phi( sqrt(n_test) * mu/sigma ). The per-sample
DISCRIMINATION SNR mu/sigma is the gamma-dependent efficiency. In the high-dimensional spiked regime
the gamma=1 SNR collapses (W_1 = Sig^{-1} amplifies noise-subspace differences by 1/lambda_min^2),
while an interior gamma maximizes it -- the bias-variance optimum.

Godambe note: the gamma-Schur estimating function U_gamma = grad ell_gamma is unbiased at the truth
only at the endpoints (gamma=1 full score; gamma=0 correct block marginals); the interior is a
misspecified/tempered score (section 4: its expected maximizer is inflated), so the right efficiency
object is the discrimination SNR above, not an estimation Godambe variance. We verify the boundary
numerically (score bias zero at the endpoints, nonzero interior).

    python research/schur_godambe.py
"""

from __future__ import annotations

import numpy as np

from research.metric_power import _project_pd
from research.schur_likelihood_theory import (
    _blocks,
    _is_spd,
    _sub,
    expected_schur_loglik,
)


def schur_operator(Sig, sizes, gamma):
    """W_gamma(Sig) and Ld_gamma(Sig) = sum_k log det S_k(gamma)."""
    idx = _blocks(sizes)
    p = sum(sizes)
    W = np.zeros((p, p))
    Ld = 0.0
    prev = []
    for rows in idx:
        T = np.zeros((len(rows), p))
        T[:, rows] = np.eye(len(rows))
        if prev:
            cWW = _sub(Sig, prev, prev)
            cKW = _sub(Sig, rows, prev)
            Gk = cKW @ np.linalg.inv(cWW)
            T[:, prev] = -gamma * Gk
            Sg = _sub(Sig, rows, rows) - gamma * cKW @ np.linalg.solve(cWW, cKW.T)
        else:
            Sg = _sub(Sig, rows, rows)
        Sg = 0.5 * (Sg + Sg.T)
        W += T.T @ np.linalg.solve(Sg, T)
        Ld += float(np.linalg.slogdet(Sg)[1])
        prev = prev + rows
    return 0.5 * (W + W.T), Ld


def snr(Sig_A, Sig_B, Sig_t, sizes, gamma):
    """Exact per-sample discrimination SNR mu/sigma for ranking A above B under truth Sig_t."""
    WA, LdA = schur_operator(Sig_A, sizes, gamma)
    WB, LdB = schur_operator(Sig_B, sizes, gamma)
    dW = WA - WB
    mu = -0.5 * ((LdA - LdB) + np.trace(dW @ Sig_t))
    M = dW @ Sig_t
    var = 0.5 * np.trace(M @ M)
    return mu / np.sqrt(var) if var > 0 else np.inf


def snr_montecarlo(Sig_A, Sig_B, Sig_t, sizes, gamma, n=400000, seed=0):
    """Monte-Carlo check of the closed-form SNR."""
    rng = np.random.default_rng(seed)
    X = rng.multivariate_normal(np.zeros(sum(sizes)), Sig_t, size=n)
    WA, LdA = schur_operator(Sig_A, sizes, gamma)
    WB, LdB = schur_operator(Sig_B, sizes, gamma)
    qa = np.einsum("ij,jk,ik->i", X, WA, X)
    qb = np.einsum("ij,jk,ik->i", X, WB, X)
    d = -0.5 * ((LdA - LdB) + (qa - qb))
    return float(d.mean() / d.std())


def _spiked(p, n_spikes=3, spike=12.0, bulk=0.4, seed=0):
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.standard_normal((p, p)))
    evals = np.concatenate([np.full(n_spikes, spike), np.full(p - n_spikes, bulk)])
    Sig = (Q * evals) @ Q.T
    return 0.5 * (Sig + Sig.T), Q, evals


def _noise_subspace_pair(p, eps_a, eps_b, seed=0):
    """Truth (spiked) plus two candidates differing by a perturbation in the small-eigenvalue
    (noise) subspace; A is uniformly closer to truth than B (eps_a < eps_b). WELL-CONDITIONED."""
    Sig_t, Q, evals = _spiked(p, seed=seed)
    rng = np.random.default_rng(seed + 1)
    k = 3
    V = Q[:, k:]  # noise-subspace eigenvectors
    G = rng.standard_normal((V.shape[1], V.shape[1]))
    G = 0.5 * (G + G.T)
    P = V @ G @ V.T
    P = P / np.linalg.norm(P)
    return Sig_t, Sig_t + eps_a * P, Sig_t + eps_b * P


def _kl(Sig_hat, Sig_t):
    """KL(N(0,Sig_t) || N(0,Sig_hat)) = 1/2 [tr(Sig_hat^-1 Sig_t) - p + logdet Sig_hat/Sig_t]."""
    p = Sig_t.shape[0]
    iH = np.linalg.inv(Sig_hat)
    return 0.5 * (np.trace(iH @ Sig_t) - p
                  + np.linalg.slogdet(Sig_hat)[1] - np.linalg.slogdet(Sig_t)[1])


def _finite_sample_pair(p, n_train, seed=0):
    """Truth (spiked) plus two ILL-CONDITIONED finite-sample estimates at high p/n: A well-shrunk
    (good), B under-shrunk (bad, near-singular -> B^-1 amplifies noise). Returns truth, A, B and
    their KL-to-truth so the intended ordering KL(A) < KL(B) can be checked."""
    Sig_t, _, _ = _spiked(p, seed=seed)
    rng = np.random.default_rng(seed + 5)
    X = rng.multivariate_normal(np.zeros(p), Sig_t, size=n_train)
    S = np.cov(X, rowvar=False, bias=True)
    target = (np.trace(S) / p) * np.eye(p)
    A = 0.5 * S + 0.5 * target           # well shrunk
    B = 0.93 * S + 0.07 * target         # under-shrunk, ill-conditioned
    A, B = 0.5 * (A + A.T), 0.5 * (B + B.T)
    return Sig_t, A, B, _kl(A, Sig_t), _kl(B, Sig_t)


def discrimination_power_over_draws(p, n_train, gammas, n_draws=300, seed=0):
    """The mechanism behind the high-dim collapse: variance over TRAINING draws, not test samples.

    A = well-shrunk estimator (good), B = lightly-ridged sample covariance (bad, ill-conditioned).
    For each fresh training draw we form A,B and the EXPECTED-over-test score gap
    D = E_test[ell_gamma(A) - ell_gamma(B)] = -1/2[Ld_A - Ld_B + tr((W_A - W_B) Sig_t)].
    A is the better estimator (lower mean KL), so a reliable judge yields D>0. The judge's power is
    Phi(mean_draws(D)/sd_draws(D)); at gamma=1, W=Sigma_hat^-1 is wildly variable across draws
    (~1/lambda_min^2 for the ill-conditioned B), inflating sd(D) and collapsing power; an interior
    gamma stabilizes W and recovers it, until the damping bias pulls mean(D) down."""
    rng = np.random.default_rng(seed)
    sizes = [4] * (p // 4)
    Sig_t, _, _ = _spiked(p, seed=seed)
    ridge = 0.02 * np.trace(Sig_t) / p
    Ds = {g: [] for g in gammas}
    klA, klB = [], []
    for _ in range(n_draws):
        X = rng.multivariate_normal(np.zeros(p), Sig_t, size=n_train)
        S = np.cov(X, rowvar=False, bias=True)
        target = (np.trace(S) / p) * np.eye(p)
        A = 0.5 * S + 0.5 * target
        B = S + ridge * np.eye(p)
        A, B = 0.5 * (A + A.T), 0.5 * (B + B.T)
        if not (_is_spd(A) and _is_spd(B)):
            continue
        klA.append(_kl(A, Sig_t))
        klB.append(_kl(B, Sig_t))
        for g in gammas:
            WA, LdA = schur_operator(A, sizes, g)
            WB, LdB = schur_operator(B, sizes, g)
            Ds[g].append(-0.5 * ((LdA - LdB) + np.trace((WA - WB) @ Sig_t)))
    out = {}
    for g in gammas:
        d = np.array(Ds[g])
        out[g] = {"mean": d.mean(), "sd": d.std(),
                  "snr": d.mean() / d.std() if d.std() > 0 else np.inf,
                  "power": float((d > 0).mean())}
    return out, np.mean(klA), np.mean(klB)


def structured_power_over_draws(p=120, g=6, rho=0.6, err_good=0.05, err_bad=0.20,
                                sig_cross=0.18, gammas=(1.0, 0.75, 0.5, 0.25, 0.0),
                                n_test=90, trials=250, seed=0):
    """Reproduce the interior-gamma optimum with the PRINCIPLED W_gamma operator (Schur-complement
    damping), mirroring research/metric_power.schur_power's regime: truth block-diagonal within g
    groups (the recoverable signal in the within-group correlation), both estimates carrying
    independent spurious noisy BETWEEN-group correlations (the unidentifiable part). Power is the
    fraction of trials the judge ranks the lower-within-error estimate above the worse one."""
    rng = np.random.default_rng(seed)
    gs = p // g
    sizes = [gs] * g  # blocks aligned to the true groups (canonical order, no shuffle)
    canon = np.repeat(np.arange(g), gs)
    cross = canon[:, None] != canon[None, :]

    def _within(re):
        c = np.zeros((p, p))
        for j in range(g):
            sl = slice(j * gs, (j + 1) * gs)
            c[sl, sl] = (1 - re) * np.eye(gs) + re * np.ones((gs, gs))
        return c

    def _make(err):
        re = rho + rng.choice([-1, 1]) * err
        c = _within(re)
        n = rng.standard_normal((p, p))
        n = (n + n.T) / 2
        c[cross] += sig_cross * n[cross]  # spurious noisy between-group correlations
        return _project_pd(c)

    correct = dict.fromkeys(gammas, 0)
    for _ in range(trials):
        good, bad = _make(err_good), _make(err_bad)  # good has smaller within-group error
        true_cov = _within(rho)
        X = rng.multivariate_normal(np.zeros(p), true_cov, size=n_test)
        for gm in gammas:
            Wg, Ldg = schur_operator(good, sizes, gm)
            Wb, Ldb = schur_operator(bad, sizes, gm)
            sg = -0.5 * (Ldg + np.einsum("ij,jk,ik->i", X, Wg, X).mean())
            sb = -0.5 * (Ldb + np.einsum("ij,jk,ik->i", X, Wb, X).mean())
            correct[gm] += sg > sb
    return {gm: correct[gm] / trials for gm in gammas}


def report():
    print("=== W_gamma identity check: W_1 == inv(Sigma_hat) ===")
    Sig_t, _, _ = _spiked(6, seed=2)
    W1, _ = schur_operator(Sig_t, [2, 2, 2], 1.0)
    err = np.max(np.abs(W1 - np.linalg.inv(Sig_t)))
    print(f"  max|W_1 - Sigma^-1| = {err:.2e}\n")

    print("=== closed-form SNR vs Monte-Carlo (p=6, two blocks) ===")
    St, A, B = _noise_subspace_pair(6, eps_a=0.05, eps_b=0.15, seed=3)
    for g in (1.0, 0.6, 0.3):
        if _is_spd(A) and _is_spd(B):
            print(f"  gamma={g:.1f}:  closed-form={snr(A, B, St, [3, 3], g):+.4f}"
                  f"   monte-carlo={snr_montecarlo(A, B, St, [3, 3], g):+.4f}")
    print()

    print("=== reliable regime (well-conditioned candidates): gamma=1 should win ===\n")
    gammas = [1.0, 0.9, 0.7, 0.5, 0.3, 0.1]
    print(f"{'p':>5}" + "".join(f"  g={g:.2f}" for g in gammas) + f"{'argmax':>9}")
    print("-" * 66)
    for p in (20, 40, 80):
        sizes = [4] * (p // 4)
        St, A, B = _noise_subspace_pair(p, eps_a=0.05, eps_b=0.15, seed=p)
        if not (_is_spd(A) and _is_spd(B)):
            continue
        snrs = [snr(A, B, St, sizes, g) for g in gammas]
        print(f"{p:>5}" + "".join(f"{s:8.3f}" for s in snrs)
              + f"{gammas[int(np.argmax(snrs))]:>9.2f}")

    print("\n=== high-dim ill-conditioned regime (finite-sample estimates at p/n~1) ===")
    print("    truth spiked; A well-shrunk, B under-shrunk (near-singular).")
    print("    gamma=1 score uses Sigma_hat^-1 -> noise-amplified -> SNR collapses.\n")
    print(f"{'p':>5}{'p/n':>6}{'KL(A)':>8}{'KL(B)':>8}{'ord':>5}"
          + "".join(f"  g={g:.2f}" for g in gammas) + f"{'argmax':>9}")
    print("-" * 92)
    for p, n_train in ((20, 24), (40, 48), (80, 96)):
        sizes = [4] * (p // 4)
        St, A, B, klA, klB = _finite_sample_pair(p, n_train, seed=p)
        if not (_is_spd(A) and _is_spd(B)):
            continue
        snrs = [snr(A, B, St, sizes, g) for g in gammas]
        order = "A<B" if klA < klB else "A>B"  # A<B means A is the better (closer) estimate
        print(f"{p:>5}{p / n_train:>6.2f}{klA:>8.2f}{klB:>8.2f}{order:>5}"
              + "".join(f"{s:8.3f}" for s in snrs)
              + f"{gammas[int(np.argmax(snrs))]:>9.2f}")

    print("\n=== the actual mechanism: power over TRAINING draws (A better than B) ===")
    print("    judge power = P(score gap D>0) over fresh training draws; SNR = mean(D)/sd(D)\n")
    gset = [1.0, 0.9, 0.7, 0.5, 0.3, 0.1]
    print(f"{'p':>5}{'p/n':>6}{'KL(A)':>8}{'KL(B)':>8}{'stat':>6}"
          + "".join(f"  g={g:.2f}" for g in gset))
    print("-" * 86)
    for p, n_train in ((20, 22), (40, 44), (80, 88)):
        out, kA, kB = discrimination_power_over_draws(p, n_train, gset, n_draws=300, seed=p)
        snr_row = "".join(f"{out[g]['snr']:8.3f}" for g in gset)
        pow_row = "".join(f"{out[g]['power']:8.2f}" for g in gset)
        print(f"{p:>5}{p / n_train:>6.2f}{kA:>8.2f}{kB:>8.2f}{'SNR':>6}{snr_row}")
        print(f"{'':>5}{'':>6}{'':>8}{'':>8}{'power':>6}{pow_row}")

    print("\n=== structured regime: interior gamma optimum, via principled W_gamma operator ===")
    print("    signal in within-group correlation; shared unidentifiable noise in between-group.\n")
    sp = structured_power_over_draws()
    print("    " + "  ".join(f"g={g:.2f}:{sp[g]:.3f}" for g in (1.0, 0.75, 0.5, 0.25, 0.0)))
    star = max(sp, key=sp.get)
    print(f"    -> peak at gamma={star:.2f} (power {sp[star]:.3f}); both endpoints near chance.")

    print("\n=== Godambe boundary: is the score unbiased at the truth? ===")
    print("    ||grad_Sigma E[ell_gamma]|| at Sigma=truth, by finite differences (0 => unbiased)\n")
    St, _, _ = _spiked(6, seed=2)
    sizes = [3, 3]
    p = 6
    print(f"{'gamma':>6}{'offdiag grad norm':>20}{'diag grad norm':>17}")
    print("-" * 43)
    for g in (1.0, 0.8, 0.5, 0.2, 0.0):
        h = 1e-5
        goff, gdiag = 0.0, 0.0
        for i in range(p):
            for j in range(i, p):
                E = np.zeros((p, p))
                E[i, j] = E[j, i] = 1.0
                d = (expected_schur_loglik(St, St + h * E, sizes, g)
                     - expected_schur_loglik(St, St - h * E, sizes, g)) / (2 * h)
                offblock = (i < 3) != (j < 3)
                if offblock:
                    goff += d * d
                else:
                    gdiag += d * d
        print(f"{g:>6.2f}{np.sqrt(goff):>20.4f}{np.sqrt(gdiag):>17.4f}")


if __name__ == "__main__":
    report()
