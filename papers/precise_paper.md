# Evaluating and Recommending Online Covariance Estimators, with a Schur-Complement Connection

**Peter Cotton** · *Draft* · microprediction/precise

## Abstract

We treat the choice of an online (streaming) covariance estimator as a first-class problem with
three parts. First, we assemble a registry of incremental covariance/correlation estimators behind a
single `partial_fit` contract, and add a *Schur-style* estimator that damps the cross-block coupling
of the running covariance. Second, we study how a covariance estimate should be *assessed*, and show
— both by a statistical-power experiment and by appeal to random matrix theory — that the held-out
Gaussian likelihood, while most powerful when the precision is trustworthy (Neyman–Pearson), is
*demonstrably worse than chance* at ranking estimators in high dimensions with an unidentifiable
spectral tail; inversion-free and *block (Schur) pseudo-likelihood* judges recover the lost power.
This is the same instability that afflicts the minimum-variance portfolio, and the Schur-complement
control that unifies hierarchical and optimization-based allocation (Cotton 2024) is the shared
regularization knob. Third, we build a recommender that maps observable sample properties to an
estimator, and lay out an out-of-sample validation protocol — leave-one-ensemble-out across
generative families plus a real-data holdout — designed to be robust to the strong dependence of all
conclusions on the covariance-generating ensemble.

## 1. Introduction

Covariance estimation underlies portfolio construction, risk, Gaussian models, and ensembling of
forecasts. In streaming settings one wants *online* estimators that update in O(1)–O(d³) per
observation without storing a window. There are many such estimators — empirical, exponentially
weighted, shrinkage (Ledoit–Wolf, OAS), robust (Huber, Tyler), factor, dynamic-conditional-
correlation — and, as we show, none dominates: the best choice depends on the regime (dimension
relative to sample, spectral shape, tail heaviness, stationarity). This motivates three questions:
*which estimators*, *how to judge them*, and *how to choose among them* — the structure of the
`precise` package and of this paper.

## 2. A registry of online covariance estimators

Every estimator implements `partial_fit(y)` and exposes `covariance_`, `correlation_`, `precision_`,
`location_` (the sklearn convention, which `sklearn.covariance` offers only in batch form). The
registry (`all_estimators()`) currently holds 14 truly-online estimators across families: empirical
and exponentially weighted; linear and Oracle shrinkage; fixed-intensity and constant-correlation
shrinkage; partial-moment (semi-)covariance; robust Huber and Tyler M-estimators; a Riemannian
(geodesic) update; dynamic conditional correlation; an online low-rank+diagonal factor model
(O(d·k)/step); and the **Schur** estimator of §4. A keyed adapter layer (`keyed`) lifts any of them
to a river-style estimator over a *dynamic universe* of named variables that enter and leave.

## 3. How should a covariance estimate be assessed?

We pose assessment as a *statistical power* question: given two estimates whose true quality ordering
we know (because in simulation we know Σ, via exact KL divergence), which finite-sample judge most
reliably reproduces that ordering? We compare a panel of assessors — held-out log-likelihood,
Frobenius, Stein/entropy loss, random k-dimensional projection scores, minimum-variance realized
variance, Mahalanobis calibration, and block pseudo-likelihood (§4) — over Monte-Carlo trials.

**Findings (reproducible: `research/metric_power.py`).**
- *Well-specified, low dimension:* the log-likelihood (log score) is most powerful, Stein essentially
  tied — as Neyman–Pearson predicts.
- *Random projections:* scoring data projected onto random k-subspaces *jointly* recovers
  cross-direction information lost by marginal (k=1) projections; power rises with k toward the full
  likelihood.
- *High dimension with a noisy tail:* the full likelihood — dominated by Σ̂⁻¹ and log det, i.e. the
  smallest, least-identifiable eigenvalues (Marčenko–Pastur / spiked regime) — **collapses to
  chance**. Power versus k or block size becomes non-monotonic, peaking at moderate complexity;
  inversion-free judges (Frobenius, variogram) and block pseudo-likelihoods retain power.

**Caveat — generation sensitivity.** These rankings are *not* ensemble-invariant. A near-identity
LKJ draw or a low-dimensional problem keeps the likelihood optimal; a spiked/Marčenko–Pastur or
factor ensemble produces the failure. Any honest benchmark must sweep the generative ensemble; we
delegate generation to the sibling `randomcov` library and report per-ensemble. See
`papers/evaluation_and_generation_review.md` for the full literature.

## 4. Schur-style methods

The full Gaussian likelihood factorizes, via Schur complements, into a sum of *block-conditional*
log-likelihoods. Dropping (or regularizing by a coupling parameter γ) the cross-block conditioning
yields a **block pseudo-likelihood** that inverts only small matrices. As an *assessor* it is cheap
(feasible at p≈500), robust where the full likelihood fails, a proper composite likelihood, and
tunable (block size is the robustness↔power knob; the full block recovers the likelihood). As an
*estimator*, `SchurCovariance` damps the cross-block coupling of the running covariance (γ=0
block-diagonal, γ=1 full), improving conditioning in high dimensions.

This is the **same trade-off as portfolio theory.** The minimum-variance portfolio `w ∝ Σ̂⁻¹1` fails
in high dimensions for the identical reason — it trusts the raw inverse of an ill-conditioned matrix
(de Prado 2015/2016; Antonov, Lipton & de Prado 2024). Schur complementary allocation (Cotton 2024)
controls exactly how much of that coupling to trust, interpolating hierarchical risk parity (γ=0) and
minimum variance (γ=1). The block pseudo-likelihood is the *evaluation* analogue of that allocation
principle: do not invert the full ill-conditioned covariance to *judge* an estimate, any more than to
*allocate* with it. We verify both the γ-regularized and block-factorized likelihood recover power in
the high-dimensional regime.

## 5. Recommendation from matrix properties

Because no estimator dominates, we recommend one from *observable* sample features —
`p`, `n`, `p/n`, effective rank, sphericity, condition number, off-diagonal mass, excess kurtosis —
none of which require the unknown Σ (`covariance_features`). `suggest(X)` returns a ranked estimator
list. The current ruleset is a transparent frozen heuristic (shrinkage/factor when `p/n` is large or
ill-conditioned, robust under heavy tails, empirical otherwise), to be replaced by a recommender
trained out-of-sample. The bake-off (`research/bakeoff.py`) already exhibits the regime-dependence
that makes recommendation worthwhile: empirical wins clean stationary data, factor wins high-`p/n`,
DCC wins regime change, Huber wins gross-outlier contamination.

## 6. Out-of-sample validation (protocol)

The contribution is real only if the recommender beats the best *single* fixed estimator (a strong
baseline, e.g. nonlinear shrinkage) out of sample, and closes most of the gap to the per-problem
oracle. The protocol, designed against the generation-sensitivity caveat:
1. **Leave-one-ensemble-out:** train the recommender on a subset of generative families
   (LKJ, Wishart, factor, spiked, Toeplitz, HQS) and test on a held-out family, so it cannot memorize
   ensemble labels.
2. **Real-data holdout:** equity-return windows — the decisive test, since every synthetic ensemble
   is suspect.
3. **Scoring** under a high-dimensional-robust assessor (block pseudo-likelihood or GMV out-of-sample
   variance), *not* the full likelihood, per §3. Report recommender vs best-fixed vs oracle.

*(This is the next experimental milestone; the harness lives in `research/`.)*

## 7. Related work

Decision-theoretic matrix losses (James & Stein 1961; Stein loss); random matrix theory and the
oracle rotationally-invariant estimator (Bun, Bouchaud & Potters 2017); financial out-of-sample and
shrinkage criteria (Ledoit & Wolf 2004; Engle, Ledoit & Wolf 2019); proxy-consistent forecast losses
of Bregman form (Patton 2011; Laurent, Rombouts & Violante 2013); forecast-comparison testing
(Diebold–Mariano 1995; Hansen, Lunde & Nason 2011); proper scoring rules (Gneiting & Raftery 2007);
high-dimensional covariance testing power (Ledoit & Wolf 2002; Chen, Zhang & Zhong 2010; Cai & Ma
2013); and covariance generation (Lewandowski, Kurowicka & Joe 2009; Hirschberger, Qi & Steuer 2007;
spiked models, Johnstone 2001). Full details and citations in
`papers/evaluation_and_generation_review.md`.

## References

See `papers/covariance_evaluation.md` and `papers/evaluation_and_generation_review.md` for the
complete reference lists. Key: López de Prado (2015/2016); Antonov, Lipton & López de Prado (2024);
Cotton (2024, arXiv:2411.05807); Bun, Bouchaud & Potters (2017); Ledoit & Wolf (2002, 2004);
Laurent, Rombouts & Violante (2013); Hansen, Lunde & Nason (2011); Gneiting & Raftery (2007).
