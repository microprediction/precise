# Covariance estimator evaluation and generation — a literature review

Notes gathered while building the `research/metric_power.py` experiments. Two questions: (1) how is
the *quality* of a covariance estimate judged in the literature, and (2) how are synthetic
ground-truth covariances *generated* — because, as our experiments show, the conclusions about (1)
are sensitive to (2).

## Part 1 — Evaluation methodologies

### A. Statistical decision theory (matrix loss functions)
The classical framing: an estimator is judged by risk under a loss `L(Σ̂, Σ)`.
- **Quadratic / Frobenius loss** `‖Σ̂ − Σ‖²`. Simple, scale-dependent, never inverts — robust in high
  dimensions (matches our finding that Frobenius survives where the likelihood fails).
- **Stein / entropy loss** `tr(Σ̂Σ⁻¹) − log det(Σ̂Σ⁻¹) − p`. The natural loss for covariance; it is the
  KL divergence between the two Gaussians and the loss the MLE / likelihood implicitly targets.
  James & Stein (1961, *Estimation with quadratic loss*, 4th Berkeley Symp.) gave the minimax
  estimator under Stein loss; Stein (1975, 1977) orthogonally-invariant improvements; modern
  high-dimensional treatments e.g. Tsukuma & Konno; Tsukuma (arXiv:1506.00748). Because Stein loss
  inverts Σ̂, it inherits the high-dimensional fragility we observed.

### B. Random Matrix Theory and the *oracle* estimator
Bun, Bouchaud & Potters (2017, *Cleaning large correlation matrices: tools from RMT*, Physics
Reports 666:1–109; arXiv:1610.08104) evaluate estimators against the **oracle** Rotationally
Invariant Estimator, which keeps the sample eigenvectors and replaces eigenvalues to **minimize the
Frobenius error** (equivalently the KL divergence as `n→∞`). The Marčenko–Pastur law and the spiked
model describe exactly *why* the small eigenvalues are unidentifiable when `p/n → c > 0` — the
mechanism behind our high-dimensional likelihood failure. "Overlap" between estimated and true
eigenvectors is another RMT evaluation object.

### C. Financial out-of-sample criteria
- **Global-minimum-variance realized variance** — the dominant economic criterion. Ledoit & Wolf
  (2003 *Honey, I Shrunk the Sample Covariance Matrix*; 2004 *A well-conditioned estimator*, JMVA;
  2017/2020 nonlinear shrinkage) and Engle, Ledoit & Wolf (2019, JBES, *Large Dynamic Covariance
  Matrices*) rank estimators by the out-of-sample variance / Sharpe / turnover of the GMV portfolio.
- **PRIAL** (percentage relative improvement in average loss) — Ledoit–Wolf's normalized loss metric.
- **HRP out-of-sample variance** — López de Prado (2015/2016); analytical results in Antonov, Lipton
  & López de Prado (2024, SSRN 4748151). Our `min_variance` judge sits in this family — and it failed
  for the same reason the likelihood does (it inverts), which is the bridge to portfolio theory.

### D. Forecast-evaluation econometrics — *which loss gives the right ranking*
A distinct, methodologically crucial literature: when Σ is unobserved and replaced by a **noisy
proxy** (e.g. realized covariance), the loss function used to rank forecasts must be chosen so the
proxy-based ranking is *consistent* for the true one.
- Patton (2011, J. Econometrics) — univariate: MSE and QLIKE are robust to proxy noise; many popular
  losses are not.
- Laurent, Rombouts & Violante (2013, J. Econometrics 173(1):1–10) — multivariate: the consistent
  losses are exactly those of **Bregman form**. *This is the key caveat our experiments dodge*: we
  knew Σ exactly, so any loss ranks consistently; in practice with a realized-covariance proxy, loss
  choice itself biases the ranking.

### E. Forecast-comparison testing (significance, multiple models)
Turning "metric says A > B" into a statistical statement:
- Diebold & Mariano (1995) — equal predictive ability test.
- Hansen, Lunde & Nason (2011, Econometrica 79:453–497) — the **Model Confidence Set**: the set of
  models statistically indistinguishable from the best, for an arbitrary loss. The rigorous version
  of our informal "power to rank" framing.

### F. Proper scoring rules
Gneiting & Raftery (2007, JASA 102:359–378): a score is *strictly proper* if truth optimizes it.
- The **logarithmic score** is the held-out log-likelihood (our `loglik`) — strictly proper, but it
  needs the density, hence Σ̂⁻¹ and log det → high-dimensional fragility.
- The **energy score** (multivariate CRPS) and the **variogram score** (Scheuerer & Hamill 2015) are
  proper scores built from sample draws / pairwise differences and **do not invert Σ** — natural
  robust high-dimensional judges, kin to Frobenius and to our random-projection / block
  pseudo-likelihood scores.

### G. High-dimensional covariance hypothesis testing (where "power" is the formal object)
A different goal — testing a null `Σ = I` / `Σ₁ = Σ₂` / a structure — but the literature in which
*statistical power* is the precise quantity:
- Ledoit & Wolf (2002, Annals of Statistics) — John's (1971/72) sphericity test extended to `p/n → c`.
- Chen, Zhang & Zhong (2010, JASA) — U-statistic tests, no normality, `p ≫ n`.
- Cai & Ma (2013) — optimal (minimax) testing of high-dimensional covariances.
Our meta-experiment borrows the *power* concept (probability of correctly ranking) from here.

### H. Matrix norms and minimax rates of convergence
In the `p ≫ n` regime the *unscaled* Frobenius norm is misleading (error accumulates over `p²`
entries). The theory instead uses the **spectral / operator norm** `‖Σ̂ − Σ‖₂` (controls downstream
linear combinations and inversion), the **element-wise max norm** `‖Σ̂ − Σ‖_max` (support recovery),
and the **scaled Frobenius norm** `‖Σ̂ − Σ‖_F / √p`. Estimators are judged by whether they attain the
**minimax lower bound** over a structured class — e.g. `s·√(log p / n)` for `s`-sparse matrices —
proved with Le Cam's method and Assouad's lemma (Cai, Zhang & Zhou 2010; Cai, Liu & Zhou 2016). An
estimator matching the bound is "minimax-rate optimal." (Our metric-power study is empirical, not
minimax, but the spectral-norm caution is the same instinct as our high-dim likelihood warning.)

### I. Structural recovery (sparse precision / graphical models)
When the precision matrix `Ω = Σ⁻¹` is read as a *network* (an edge iff `ω_ij ≠ 0` ⇔ conditional
dependence), the evaluation target is the **support**, not a matrix distance. Estimates are judged as
binary classifiers of edges: **true/false positive rates**, **AUROC** across the regularization path,
and — crucial under extreme sparsity (genomics) — **AUPRC**, plus **graph edit distance**. This is a
distinct evaluation family from §A–H, tied to the conditional-independence objective.

## Part 2 — Covariance generation methods (and why the results depend on them)

- **LKJ / vine / onion** — Lewandowski, Kurowicka & Joe (2009, JMVA 100:1989–2001), building on Joe
  (2006) partial-correlation D-vines and the Ghosh–Henderson onion. Uniform over correlation
  matrices with a concentration parameter `η` (`η` large → near identity). `randomcov` implements
  `lkj`. The `η` knob strongly affects conclusions: near-identity draws are well-conditioned, so the
  likelihood never fails there.
- **Wishart / inverse-Wishart** — the conjugate ensembles; Wishart draws mimic sample-covariance
  fluctuations.
- **RMT ensembles: Marčenko–Pastur bulk + spiked models** — Johnstone (2001) spiked covariance;
  Baik, Ben Arous & Péché (2005, BBP transition); Bai & Yao. A few large eigenvalues (factors) over
  a near-degenerate bulk. **Our high-dimensional construction is essentially a spiked/factor model
  with a noisy bulk** — so our "likelihood fails" headline is a property of *this* ensemble.
- **Factor models / POET** — Fan, Liao & Mincheva (2013, JRSS-B): low-rank-plus-sparse, the realistic
  financial structure. Block pseudo-likelihood and `FactorCovariance` are matched to it.
- **Hirschberger, Qi & Steuer (2007, EJOR 177:1610–1625)** — generate covariances with specified
  diagonal/off-diagonal moment distributions, tuned to empirical market covariance, for benchmarking
  optimizers.
- **Structured families** — equicorrelation, Toeplitz/AR(1) (banded/local), block/group. We used these.

### Sensitivity — the methodological takeaway
The ranking of *evaluation* metrics is not ensemble-invariant:
- **LKJ with large `η`, or low dimension** → well-conditioned spectrum → the full likelihood is
  best (Neyman–Pearson), as we saw in the clean regime.
- **Spiked / Marčenko–Pastur with a hard bulk** (our high-dim regime) → small eigenvalues
  unidentifiable → the full likelihood collapses; inversion-free / block / projection judges win.
- **Factor (POET) structure** → block pseudo-likelihood is naturally favoured.
- **Toeplitz / AR** → banded (block-Markov) Schur factorization is the natural fit.

So any honest benchmark must **sweep the generative ensemble** (LKJ, Wishart, spiked/MP, factor,
Toeplitz, HQS) and report per-ensemble — which is precisely the role of `randomcov` and the
`research/bakeoff.py` scenario suite. A single ensemble can manufacture or hide any of these effects.

## Part 3 — Regularized estimators beyond the online registry (related work)

`precise` ships *online* estimators; the high-dimensional literature is dominated by *batch*
regularized estimators that impose structure. They are the natural related work (and candidate
future online variants):
- **Structural (ordered variables): banding / tapering.** When `σ_ij` decays with `|i−j|`
  (time/space), zero or down-weight far entries: Bickel & Levina (2008, banding); Cai, Zhang & Zhou
  (2010, minimax-optimal tapering); Xue & Zou (nonparanormal/rank-based). Spatial **covariance
  tapering** (Furrer, Genton & Nychka 2006; Kaufman, Schervish & Nychka 2008) multiplies a Matérn
  covariance by a compactly-supported correlation to get a sparse, O(n³)-avoiding system for Kriging.
- **Sparsity (no ordering): thresholding.** Set small sample entries to zero — universal, or
  **adaptive** thresholding scaled by each entry's variability (Cai & Liu 2011), which is
  minimax-optimal and heteroscedasticity-aware.
- **Factor structure: POET** (Fan, Liao & Mincheva 2013) — low-rank common factors via PCA plus
  adaptive thresholding of the idiosyncratic remainder (`Σ = BBᵀ + Σ_u`); the direct ancestor of our
  online `FactorCovariance`.
- **Sparse precision / Gaussian graphical models.** Neighborhood selection via node-wise Lasso
  (Meinshausen & Bühlmann 2006); the **Graphical Lasso** (Friedman, Hastie & Tibshirani 2008),
  ℓ₁-penalized Gaussian likelihood, symmetric and positive-definite; **CLIME** (Cai, Liu & Luo 2011),
  a likelihood-free ℓ₁ linear program robust to heavy tails with spectral/Frobenius optimality.

## Part 4 — Evaluation is tethered to the downstream task

The survey's structural conclusion is the same as ours: *the right estimator and the right metric
depend on the objective.* The true Σ is never observed in the field, so practitioners evaluate by
**downstream proxy**:
- **Finance** — global-minimum-variance out-of-sample variance, tracking error, information ratio,
  turnover (Ledoit-Wolf; Engle-Ledoit-Wolf); recent neural nonlinear-shrinkage learns the eigenvalue
  map directly against the portfolio-risk objective.
- **Genomics** — gene-regulatory-network recovery (GGMs), benchmarked on synthetic topologies
  (GeneNetWeaver) by AUPRC; differential co-expression contrasts two precision matrices.
- **Spatial / climatology** — tapered Kriging judged on predictive MSE at the truth's likelihood,
  with massive compute savings.
- **Classification** — LDA needs `Ω = Σ⁻¹`; high-dim variants (sparse discriminant, AdaLDA, ADAM for
  missing data) are judged on out-of-sample misclassification, often estimating the discriminant
  direction directly rather than Σ.

**This directly validates the recommendation thesis (§5 of the paper):** because no estimator is best
across objectives or regimes, *choosing* the estimator (and the assessor) from the problem's
properties — and proving the choice out of sample — is exactly the contribution. It also reinforces
the generation-sensitivity warning: an estimator tuned for one structural class (bandable, sparse,
factor) need not win in another.

## References (primary)
- James, W. & Stein, C. (1961). Estimation with quadratic loss. *4th Berkeley Symp.*
- Stein, C. (1975, 1977). Rietz lecture / unpublished — orthogonally invariant covariance estimation.
- Bun, J., Bouchaud, J.-P. & Potters, M. (2017). Cleaning large correlation matrices. *Physics Reports* 666:1–109. arXiv:1610.08104.
- Johnstone, I. (2001). On the distribution of the largest eigenvalue (spiked model). *Annals of Statistics*.
- Baik, Ben Arous & Péché (2005). Phase transition of the largest eigenvalue. *Annals of Probability*.
- Ledoit, O. & Wolf, M. (2004). A well-conditioned estimator for large-dimensional covariance matrices. *JMVA* 88:365–411.
- Engle, R., Ledoit, O. & Wolf, M. (2019). Large dynamic covariance matrices. *J. Business & Economic Statistics* 37:363–375.
- Patton, A. (2011). Volatility forecast comparison using imperfect volatility proxies. *J. Econometrics* 160:246–256.
- Laurent, S., Rombouts, J. & Violante, F. (2013). On loss functions and ranking forecasting performances of multivariate volatility models. *J. Econometrics* 173(1):1–10.
- Hansen, P., Lunde, A. & Nason, J. (2011). The Model Confidence Set. *Econometrica* 79:453–497.
- Gneiting, T. & Raftery, A. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA* 102:359–378.
- Scheuerer, M. & Hamill, T. (2015). Variogram-based proper scoring rules. *Monthly Weather Review* 143:1321–1334.
- Ledoit, O. & Wolf, M. (2002). Some hypothesis tests for the covariance matrix when the dimension is large. *Annals of Statistics* 30:1081–1102.
- Chen, S., Zhang, L. & Zhong, P. (2010). Tests for high-dimensional covariance matrices. *JASA* 105:810–819.
- Cai, T. & Ma, Z. (2013). Optimal hypothesis testing for high-dimensional covariance matrices. *Bernoulli* 19:2359–2388.
- Lewandowski, D., Kurowicka, D. & Joe, H. (2009). Generating random correlation matrices based on vines and extended onion method. *JMVA* 100:1989–2001.
- Joe, H. (2006). Generating random correlation matrices based on partial correlations. *JMVA* 97:2177–2189.
- Hirschberger, M., Qi, Y. & Steuer, R. (2007). Randomly generating portfolio-selection covariance matrices with specified distributional characteristics. *EJOR* 177:1610–1625.
- Fan, J., Liao, Y. & Mincheva, M. (2013). Large covariance estimation by thresholding principal orthogonal complements (POET). *JRSS-B* 75:603–680.
- Bickel, P. & Levina, E. (2008). Regularized estimation of large covariance matrices; and Covariance regularization by thresholding. *Annals of Statistics* 36.
- Cai, T., Zhang, C.-H. & Zhou, H. (2010). Optimal rates of convergence for covariance matrix estimation. *Annals of Statistics* 38:2118–2144.
- Cai, T. & Liu, W. (2011). Adaptive thresholding for sparse covariance matrix estimation. *JASA* 106:672–684.
- Cai, T., Liu, W. & Zhou, H. (2016). Estimating sparse precision matrix: optimal rates of convergence and adaptive estimation. *Annals of Statistics* 44:455–488.
- Ledoit, O. & Wolf, M. (2012). Nonlinear shrinkage estimation of large-dimensional covariance matrices. *Annals of Statistics* 40:1024–1060; and Optimal estimation under Stein's loss (2018/2021).
- Meinshausen, N. & Bühlmann, P. (2006). High-dimensional graphs and variable selection with the Lasso. *Annals of Statistics* 34:1436–1462.
- Friedman, J., Hastie, T. & Tibshirani, R. (2008). Sparse inverse covariance estimation with the graphical lasso. *Biostatistics* 9:432–441.
- Cai, T., Liu, W. & Luo, X. (2011). A constrained ℓ₁ minimization approach to sparse precision matrix estimation (CLIME). *JASA* 106:594–607.
- Furrer, R., Genton, M. & Nychka, D. (2006). Covariance tapering for interpolation of large spatial datasets. *J. Computational & Graphical Statistics* 15:502–523; Kaufman, Schervish & Nychka (2008), *JASA*.
- Xue, L. & Zou, H. (2012). Regularized rank-based estimation of high-dimensional nonparanormal graphical models. *Annals of Statistics*.
