# Schur Covariance Evaluation
### A Principled Pseudo-Likelihood in High Dimensions

**Peter Cotton** · *Draft* · microprediction/precise

## Abstract

The Gaussian log-likelihood is the natural objective for estimating and for evaluating a covariance
matrix, but in high dimensions it is dominated by the smallest eigenvalues of the estimate — exactly
the part of the spectrum that cannot be identified when the dimension is comparable to the sample
size — so it becomes both numerically fragile and, as we show, *worse than chance* at ranking
estimators. We introduce the **Schur likelihood**: a one-parameter family that damps the cross-block
coupling of the Gaussian likelihood through its Schur complement, with a coupling-strength parameter
`γ` interpolating the full likelihood (`γ=1`) and the block-diagonal likelihood (`γ=0`). The family
shares the exact Schur-complement conditioning identity of the Vecchia and Gaussian-Markov-random-
field likelihoods — to which it adds an orthogonal coupling-*strength* axis — and it is the exact
likelihood counterpart of Schur complementary portfolio allocation, which interpolates hierarchical
risk parity and minimum variance by the same knob. We show, in simulation and on real equity
returns, that an interior `γ` recovers the power and the conditioning the full likelihood loses in
high dimensions, and that a geodesic (affine-invariant) damping is stable where linear damping is
not.

## 1. The high-dimensional failure of the likelihood

For a Gaussian, `ℓ(Σ̂; X) = −½(log det Σ̂ + xᵀΣ̂⁻¹x)` per sample, equivalently the
**covariance-likelihood** form in the sufficient statistic `S` (the sample covariance),
`ℓ(Σ̂; S) = −½(log det Σ̂ + tr(Σ̂⁻¹S))` (proportional to the Wishart log-likelihood of `S` given `Σ̂`,
and to Stein/entropy loss against `S`). Both terms are governed by the smallest eigenvalues of `Σ̂`:
`log det = Σ log λᵢ` and `Σ̂⁻¹` blow up as `λ_min → 0`. When `p/n → c > 0` (Marčenko–Pastur / spiked
regime) those eigenvalues collapse toward zero and are unidentifiable, so the likelihood stakes its
verdict on noise. Empirically (`research/metric_power.py`) the held-out likelihood drops to **~0.45**
(below chance) at ranking two estimates of known relative quality, while inversion-free judges hold
~0.85. This is the same instability as Markowitz "error maximization" in `w ∝ Σ̂⁻¹1`.

## 2. The Schur likelihood

Partition the variables into blocks. The Gaussian likelihood factorizes *exactly* through Schur
complements into block-conditional terms; we damp the conditioning by `γ`, replacing each block's
covariance by its `γ`-damped Schur complement `Σ_ii − γ Σ_{iC}Σ_{CC}⁻¹Σ_{Ci}` (and the conditional
mean by its `γ`-scaled regression). This defines a likelihood `ℓ_γ`:

- **`γ=1`** — the exact full likelihood (most powerful; fragile);
- **`γ=0`** — the block-diagonal likelihood (robust; the marginal *composite likelihood*);
- **`γ∈(0,1)`** — a tunable bridge that *changes the block covariances*, inverts only block-sized
  matrices, and is better conditioned than the full likelihood because damping lifts the small
  eigenvalues.

**Two uses, one object.** *Evaluation:* score an estimate by `ℓ_γ(Σ̂; S_test)`. *Estimation:*
maximize `ℓ_γ(Σ; S)` over `Σ` — a Schur/composite-likelihood MLE; the online estimator
`SchurCovariance` applies the same coupling damping to a recency-weighted covariance.

## 3. Relation to existing constructions (so the contribution is precise)

- **Composite / pseudo-likelihood** (Besag 1975; Lindsay 1988; Varin–Reid–Firth 2011): the
  block-marginal likelihood is exactly the `γ=0` endpoint.
- **Vecchia / GMRF** (Vecchia 1988; Katzfuss–Guinness 2021; block Vecchia, Pan et al. 2024; Rue–Held
  2005; nested dissection, George 1973): these use the *same exact Schur-complement conditioning
  identity*; `γ=1` with limited conditioning *is* a block-Vecchia/GMRF likelihood. They regularize by
  **sparsity** (which to condition on) at full strength; the Schur likelihood adds an **orthogonal
  coupling-strength axis `γ`**. To our knowledge a continuous strength-damping of the Schur
  complement (versus structural sparsity/tapering) is new here.
- **Schur complementary allocation** (Cotton 2024): the identical `γ` knob interpolates HRP (`γ=0`)
  and minimum-variance (`γ=1`); the Schur likelihood is its evaluation/estimation mirror. The
  Antonov–Lipton–de Prado (2024) analytics on HRP stability explain why the interior beats the
  `γ=1` endpoint.

## 4. The interpolation can be linear or geodesic

Damping interpolates each block covariance between the block-diagonal endpoint and the full Schur
complement. **Linear** damping (`Σ_ii − γ·BD⁻¹Bᵀ`) is simplest; **geodesic** damping moves along the
affine-invariant SPD geodesic between the two endpoints, lifting small eigenvalues *multiplicatively*.

## 5. Results

- **γ traces a regime-dependent optimum** (`research/metric_power.py`, `SchurLikelihood`): power
  climbs to `γ=1` when the coupling is reliable; falls toward `γ=0` in the high-dimensional noisy
  regime; and at *partial* reliability an **interior `γ` strictly dominates both endpoints**
  (0.84 vs 0.43/0.43) — the likelihood analogue of Schur allocation beating both HRP and minimum
  variance. The interior dominance is robust to the interpolation geometry.
- **Geodesic stability**: when the Schur complement is near-singular (strong coupling), linear
  damping has a power dip (≈0.64) while geodesic damping stays at full power — the safer default.
- **Real data** (Ken French 100 portfolios, daily, rolling minimum-variance OOS volatility,
  `p=100`, `n=60` so `p/n≈1.7`; `research/oos_equity.py`): the inverting/unregularized estimators
  blow up by orders of magnitude (annualized vol 9.6 empirical, 6.8 Huber, 1.3×10⁶ Tyler), while the
  recommender routes to shrinkage (0.141, rank 2/14, vs 0.129 oracle and 0.228 equal-weight) — the
  economic counterpart of the likelihood result: in high dimensions the value is reliably selecting
  the well-conditioned family and avoiding catastrophe with no hindsight.

## 6. Open directions

A composite-likelihood **efficiency** statement for `ℓ_γ` relative to the full likelihood under a
spiked/Marčenko–Pastur model; the optimal `γ(p, n, spectrum)`; recursive block inversion for
`O(p·b²)` scaling; and a Russell-scale (`p≈2000`) real-data study, where the high-dimensional
separation should be largest.

## References

López de Prado (2015/2016); Antonov, Lipton & López de Prado (2024); Cotton (2024, arXiv:2411.05807);
Besag (1975); Lindsay (1988); Varin, Reid & Firth (2011); Vecchia (1988); Katzfuss & Guinness (2021);
Pan et al. (2024); Rue & Held (2005); George (1973); Ledoit & Wolf (2004); Bun, Bouchaud & Potters
(2017). Full lists in `papers/evaluation_and_generation_review.md` and `papers/covariance_evaluation.md`.
