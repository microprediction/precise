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
