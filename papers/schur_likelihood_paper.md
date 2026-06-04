# Schur Covariance Evaluation
### A Principled Pseudo-Likelihood in High Dimensions

**Peter Cotton** · *Draft* · microprediction/precise

## Abstract

The Gaussian log-likelihood is the natural objective for estimating and for evaluating a covariance
matrix, but in high dimensions it is dominated by the smallest eigenvalues of the estimate — exactly
the part of the spectrum that cannot be identified when the dimension is comparable to the sample
size — so it becomes both numerically fragile and, as we show, *worse than chance* at ranking
estimators. We introduce the **Schur likelihood**, a one-parameter family of pseudo-likelihoods that
damps the cross-block coupling of the Gaussian likelihood through its Schur complement, with a
coupling-strength parameter `γ ∈ [0,1]` interpolating the full likelihood (`γ=1`) and the
block-diagonal likelihood (`γ=0`). Its value is less a new estimator than a **unifying lens**: the
exact block factorization it damps is the same Schur-complement conditioning identity that underlies
the Vecchia approximation, Gaussian-Markov-random-field likelihoods, and nested-dissection
elimination; `γ` is an axis *orthogonal* to the sparsity axis those methods regularize along; `γ=0`
is composite (pseudo-) likelihood and `γ=1` is the joint likelihood; the same `γ` damping of the same
Schur complement is exactly Schur complementary portfolio allocation, which interpolates hierarchical
risk parity (`γ=0`) and minimum-variance optimization (`γ=1`); and the damping is a *structured*
(block-conditional) shrinkage, complementary to the *spectral* shrinkage of Ledoit–Wolf and the
rotationally-invariant estimators. We show in simulation that an interior `γ` recovers the power and
the conditioning the full likelihood loses in high dimensions — strictly dominating both endpoints
when the coupling is partially reliable — that a geodesic (affine-invariant) damping is stable where
linear damping is not, and that the high-dimensional inversion catastrophe the construction is built
to avoid is borne out economically on real equity returns. We are careful about what `ℓ_γ` is: for
`γ<1` it is a composite/pseudo-likelihood (a sum of proper block scores, not a joint density), and as
an *estimation* objective its bias is its regularization — it is not, and is not claimed to be, a
consistent MLE or a competitor to nonlinear shrinkage as a point estimator.

## 1. The high-dimensional failure of the likelihood

For a zero-mean Gaussian the per-sample log-likelihood is `ℓ(Σ̂; x) = −½(log det Σ̂ + xᵀΣ̂⁻¹x)`,
equivalently the **covariance-likelihood** form in the sufficient statistic `S` (the sample
covariance), `ℓ(Σ̂; S) = −½(log det Σ̂ + tr(Σ̂⁻¹S))` — proportional to the Wishart log-likelihood of
`S` given `Σ̂`, and, up to constants, the negative Stein/entropy loss against `S`. Both terms are
governed by the *smallest* eigenvalues of `Σ̂`: `log det = Σ log λᵢ → −∞` and `Σ̂⁻¹` blows up as
`λ_min → 0`. When `p/n → c > 0` (the Marčenko–Pastur / spiked regime) those eigenvalues collapse
toward zero and are statistically unidentifiable, so the likelihood stakes its verdict on noise.

Empirically (`research/metric_power.py`) the held-out likelihood drops to **≈0.45** — *below chance* —
at correctly ordering two estimates of *known* relative quality, while inversion-free judges
(Frobenius, variogram) and block scores hold ≈0.85. This is the evaluation-side image of Markowitz
"error maximization" in `w ∝ Σ̂⁻¹1`: the same `Σ̂⁻¹`, the same small eigenvalues, the same fragility.
The remedy in both settings is to stop trusting the raw inverse — the question is *how*, and with what
single, interpretable knob.

## 2. The exact Schur factorization of the Gaussian likelihood

Partition the `p` variables into `K` ordered blocks `x = (x_1, …, x_K)`. The joint density factorizes
*exactly* into a product of block conditionals,

```
p(x) = ∏_k p(x_k | x_{<k}),
```

and for a Gaussian each conditional is itself Gaussian with

- conditional covariance = **Schur complement** `S_k = Σ_kk − Σ_{k,<k} Σ_{<k,<k}⁻¹ Σ_{<k,k}`,
- conditional mean `μ_{k|<k} = μ_k + Σ_{k,<k} Σ_{<k,<k}⁻¹ (x_{<k} − μ_{<k})`.

Hence `log det Σ = Σ_k log det S_k` and the quadratic form splits blockwise: this is exactly the
block-LDLᵀ / block-Cholesky factorization, and it is the engine of the Vecchia approximation, of GMRF
likelihoods, and of nested-dissection elimination. **No approximation has been made yet** — only a
re-expression of the same likelihood as a sum of block-conditional terms, each of which inverts only
the conditioning block `Σ_{<k,<k}`.

## 3. The Schur likelihood: damping the conditioning

We introduce a single **coupling-strength** parameter `γ ∈ [0,1]` that damps the Schur complement and
the conditional regression in lockstep:

```
S_k(γ)      = Σ_kk − γ · Σ_{k,<k} Σ_{<k,<k}⁻¹ Σ_{<k,k}
μ_{k|<k}(γ) = μ_k + γ · Σ_{k,<k} Σ_{<k,<k}⁻¹ (x_{<k} − μ_{<k})

ℓ_γ(Σ; x)   = Σ_k  log N( x_k ; μ_{k|<k}(γ), S_k(γ) ).
```

The endpoints are the two familiar objects, and the interior is the new one:

| `γ` | `ℓ_γ` is | character |
|---|---|---|
| `1` | the **exact full Gaussian likelihood** | most powerful, fragile (inverts the whole `Σ`) |
| `(0,1)` | a **tunable bridge** that *changes the block covariances* | inverts only conditioning blocks; better-conditioned, because damping lifts the small eigenvalues |
| `0` | the **block-diagonal likelihood** | robust; this endpoint is block-marginal **composite likelihood** |

**What kind of object is `ℓ_γ`? (an honest accounting).** At `γ=1` it is the joint log-density. At
`γ=0` it is a product of block *marginals* — a composite likelihood in the sense of Besag/Lindsay/
Varin–Reid–Firth: a sum of proper component log-densities that does not itself integrate to one. For
`γ∈(0,1)` each term `log N(x_k; μ(γ), S(γ))` is still a *genuine* Gaussian log-density (a strictly
proper local score, since `S_k(γ) ≻ 0` whenever the damping keeps it positive definite), but the
damped conditionals are mutually inconsistent — they are not the conditionals of any single joint
Gaussian — so `ℓ_γ` is a **pseudo-likelihood**, not a normalized joint density. This is exactly the
composite-likelihood bargain: we trade the joint-density property for tractable, well-conditioned
component scores. The consequences are:

- *As an evaluation score* (plug in a fixed estimate `Σ̂`, score held-out `S_test`), `ℓ_γ` is a valid
  sum of proper block scores; its quality is the *power* with which it ranks estimators, which we
  measure empirically (§7).
- *As an estimation objective* (`max_Σ ℓ_γ(Σ; S)`), the maximizer for `γ<1` is **not** `Σ_true` even
  in the well-specified limit — the damping biases it. That bias *is* the regularization: `ℓ_γ` is a
  regularized objective, a structured shrinkage (§5), not a consistent MLE. We make no claim that it
  competes with nonlinear shrinkage as a point estimator; the online `SchurCovariance` applies the
  same damping to a recency-weighted covariance purely to improve conditioning.

## 4. The unifying role

The contribution is best seen as placing a scattered set of constructions on **two axes of the same
block factorization** (§2):

- **Axis A — conditioning structure (sparsity):** for each block, *which / how many* earlier blocks
  it conditions on. Full conditioning (every earlier block) ↔ no conditioning (block-diagonal). This
  is the axis Vecchia, GMRF, banding/tapering and nested dissection regularize along.
- **Axis B — coupling strength `γ`:** *how strongly* the chosen conditioning is trusted, via the
  damping of §3. Full trust (`γ=1`) ↔ no trust (`γ=0`). This is the axis introduced here.

These axes are **orthogonal**, and naming both at once organizes the landscape:

```
                         γ = 1 (full trust)        γ ∈ (0,1)                 γ = 0 (no trust)
  full conditioning   exact Gaussian likelihood   ┌────────────────────┐    block-diagonal /
  (dense)             = MVO  w ∝ Σ⁻¹1             │   SCHUR LIKELIHOOD  │    composite likelihood
                                                   │     (this work)    │    = HRP-style allocation
  sparse conditioning block-Vecchia / GMRF        │  Schur + sparsity  │           (same column,
  (Vecchia/GMRF)      likelihood (exact conds.)   └────────────────────┘            block-marginal)
  nested dissection   = Schur-complement elimination of the (sparse) blocks
```

Reading the map:

1. **Vecchia / GMRF / nested dissection (Axis A only).** Vecchia (1988), its general framework
   (Katzfuss & Guinness 2021), block Vecchia (Pan et al. 2024), GMRFs (Rue & Held 2005) and
   nested-dissection elimination (George 1973) all use the *exact* Schur-complement conditioning of
   §2 (`γ=1`) and regularize by **choosing a sparse conditioning set** — which / how many variables
   each block sees. They do not damp the strength of a chosen conditioning. The Schur likelihood adds
   that orthogonal damping; the two compose (the "Schur + sparsity" cell). To our knowledge a
   *continuous strength-damping* of the Schur complement, as opposed to structural sparsity or
   tapering, is not used in that literature — that is the specific delta.

2. **Composite / pseudo-likelihood (the `γ=0` column).** The block-marginal likelihood (Besag 1975;
   Lindsay 1988; Varin, Reid & Firth 2011) is exactly `ℓ_0`. The Schur likelihood is the
   one-parameter deformation of composite likelihood that *re-introduces* the cross-block information
   the marginals discard — but only at strength `γ`, keeping the conditioning numerically benign.

3. **Portfolio allocation (the same two axes, transported).** Minimum-variance optimization
   (`w ∝ Σ̂⁻¹1`) is the `γ=1`, full-conditioning corner; hierarchical risk parity (López de Prado
   2015/2016) lives at the block-diagonal / `γ=0` corner; **Schur complementary allocation**
   (Cotton 2024, arXiv:2411.05807) interpolates them by damping *the same Schur complement with the
   same `γ`*. The Schur likelihood is therefore the **evaluation/estimation mirror of Schur
   allocation** — not an analogy but the identical algebraic object used for a different purpose. The
   Antonov–Lipton–de Prado (2024) analysis of why HRP is more stable than MVO is, read through this
   map, an explanation of why an interior `γ` beats the `γ=1` endpoint.

4. **Spectral shrinkage is complementary, not the same (a second unification).** Ledoit–Wolf linear
   and nonlinear shrinkage and the rotationally-invariant estimators (Bun, Bouchaud & Potters 2017)
   regularize the **spectrum** — they keep the sample eigenvectors and lift the small eigenvalues, a
   *rotationally-invariant* (basis-free) operation. Schur damping regularizes the **cross-block
   coupling** — a *block-structured*, basis-dependent operation. Both improve conditioning by lifting
   small eigenvalues, but along different geometry: spectral shrinkage is global and isotropic in the
   eigenbasis; Schur damping is local and conditional in the variable blocks. They are orthogonal
   regularizers and can be applied together; `γ` is to the block-conditional factorization what the
   shrinkage intensity is to the spectrum.

The single sentence: **`γ` is one knob that, held at its endpoints, recovers the full likelihood,
composite likelihood, block-Vecchia/GMRF likelihoods, MVO and HRP; held in its interior, it is the
common bridge all of these lack.**

## 5. Schur damping is a structured shrinkage

It is worth making the shrinkage reading of §4(4) explicit, because it is what makes an interior `γ`
work. Writing the full covariance as `Σ` and its block-diagonal as `Σ_BD`, the `γ=0` and `γ=1`
endpoints score against `Σ_BD` and `Σ` respectively, and the linear damping of §3 evaluates the
block conditionals of

```
Σ(γ)  with   S_k(γ) = (1−γ) Σ_kk + γ S_k          (block-conditional convex combination),
```

i.e. each conditional covariance is shrunk from its full Schur complement `S_k` toward the
unconditional block `Σ_kk` with intensity `1−γ`. Because `S_k ⪯ Σ_kk` (conditioning reduces
variance), the damping *raises* the conditional covariance toward `Σ_kk`, which lifts its small
eigenvalues and improves the conditioning of every block-sized inverse `ℓ_γ` actually performs. This
is a James–Stein-style shrinkage applied *blockwise to the conditioning*, with `1−γ` the intensity —
the structured counterpart of the eigenvalue shrinkage in §4(4).

## 6. The interpolation can be linear or geodesic

Damping interpolates each block's conditional covariance between the block-diagonal endpoint `Σ_kk`
and the full Schur complement `S_k`. **Linear** damping (§5, `S_k(γ) = (1−γ)Σ_kk + γS_k`) is simplest.
**Geodesic** damping moves along the **affine-invariant SPD geodesic** between the block-diagonal and
full covariances,

```
Σ_BD #_γ Σ  =  Σ_BD^{1/2} ( Σ_BD^{-1/2} Σ Σ_BD^{-1/2} )^{γ} Σ_BD^{1/2},
```

the natural interpolation under the Fisher–Rao / affine-invariant metric on the positive-definite
cone (the same geodesic step used by the `GeodesicEwaCovariance` estimator, credited to `randomcov`).
It lifts the small eigenvalues *multiplicatively* rather than additively. The two agree to first order
in `γ` and at both endpoints, but differ where the Schur complement is near-singular — precisely the
strong-coupling regime where the choice matters (§7).

## 7. Results

All reproducible from `research/metric_power.py` (synthetic power) and `research/oos_equity.py`
(real data). Rankings are ensemble-dependent (see `papers/evaluation_and_generation_review.md`); we
report the regimes and the mechanism, not an ensemble-invariant claim.

- **`γ` traces a regime-dependent optimum.** Power climbs monotonically to `γ=1` when the coupling is
  reliable (low dimension / clean spectrum), recovering the full likelihood as Neyman–Pearson
  predicts; it falls monotonically toward `γ=0` in the high-dimensional noisy regime, where the
  coupling is pure error; and — the key result — when the coupling is *partially* reliable, an
  **interior `γ` strictly dominates both endpoints** (power ≈0.84 vs ≈0.43 at either end). This is the
  likelihood analogue of Schur allocation beating both HRP and MVO, and it is exactly what a bridge
  between a fragile-but-informative endpoint and a robust-but-blind endpoint should do.

- **Geodesic stability.** When the Schur complement is near-singular (strong coupling), linear
  damping shows a power dip (≈0.64) while geodesic damping stays at full power — making geodesic the
  safer default in the regime where the two differ, consistent with its multiplicative eigenvalue
  lift (§6).

- **Economic corroboration of the motivating failure** (Ken French 100 portfolios, daily, rolling
  minimum-variance out-of-sample volatility, `p=100`, `n=60`, so `p/n≈1.7`; `research/oos_equity.py`).
  This is *not* a test of `ℓ_γ` as an equity estimator — we are explicit about that — but it confirms
  the high-dimensional inversion catastrophe the whole construction is built to avoid: the
  unregularized/inverting estimators blow up by orders of magnitude (annualized vol 9.6 empirical,
  6.8 Huber, 1.3×10⁶ Tyler), while well-conditioned shrinkage stays at 0.141 (vs 0.129 per-window
  oracle, 0.228 equal-weight). The economic moral matches the likelihood moral exactly: in high
  dimensions the reward is for *conditioning*, i.e. for not trusting the raw inverse — which is what
  `γ<1` does in the likelihood.

## 8. Limitations and open problems

- **No consistency / efficiency theorem yet.** For `γ<1`, `ℓ_γ` is a regularized pseudo-likelihood;
  the natural theory is a composite-likelihood **efficiency** statement for `ℓ_γ` relative to the
  full likelihood under a spiked / Marčenko–Pastur model, and a bias–variance characterization of
  the maximizer. We have empirical power curves, not a Godambe-information bound.
- **Optimal `γ`.** The regime-dependent optimum `γ*(p, n, spectrum, block structure)` is
  characterized only empirically. A plug-in rule (e.g. from the effective rank / `p/n`) is open, and
  is the right home for a *trained* selector — though our leave-one-family-out experiments on the
  sibling recommender (`research/oos.py`) are a caution that such selectors generalize across
  *samples* far better than across wholly novel generative families.
- **Block ordering and choice.** Like Vecchia, `ℓ_γ` depends on the partition and (for sparse
  conditioning) the ordering; a permutation-averaged or seriation-informed variant is open, as is the
  composition with the Axis-A sparsity choice (the "Schur + sparsity" cell).
- **Scaling.** Recursive block inversion gives `O(p·b²)` for block size `b`; a Russell-scale
  (`p≈2000`) real-data study, where the high-dimensional separation should be largest, is the
  natural stress test and is set up to run.
- **Falsification.** The thesis predicts the interior-`γ` dominance should *vanish* whenever the
  coupling is either fully reliable (LKJ with large `η`, low dimension → `γ*→1`) or pure noise
  (hard Marčenko–Pastur bulk → `γ*→0`); finding an interior optimum in a regime where the coupling is
  known to be fully reliable would contradict it.

## 9. Relation to existing constructions (precise deltas)

- **Composite / pseudo-likelihood** (Besag 1975; Lindsay 1988; Varin–Reid–Firth 2011): the
  block-marginal likelihood is exactly the `γ=0` endpoint; `ℓ_γ` is its one-parameter deformation
  toward the joint likelihood.
- **Vecchia / GMRF / nested dissection** (Vecchia 1988; Katzfuss–Guinness 2021; Pan et al. 2024;
  Rue–Held 2005; George 1973): same exact Schur-complement identity; `γ=1` with limited conditioning
  *is* a block-Vecchia / GMRF likelihood. They regularize by **sparsity** at full strength; the delta
  here is the **orthogonal coupling-strength axis `γ`**.
- **Schur complementary allocation** (Cotton 2024): the identical `γ` knob on the identical Schur
  complement, transported from portfolio risk to likelihood; Antonov–Lipton–de Prado (2024) on HRP
  stability explains the interior dominance.
- **Spectral shrinkage / RIE** (Ledoit–Wolf 2004, 2012/2020; Bun–Bouchaud–Potters 2017): a
  *complementary, orthogonal* regularizer — eigenvalue (rotationally-invariant) vs cross-block
  (structured) shrinkage; composable with `γ`.

## Acknowledgements

The original Schur complementary theory (Cotton 2024), of which the Schur likelihood is the
evaluation/estimation mirror, was developed with the support of Intech Investments.

## References

López de Prado (2015/2016); Antonov, Lipton & López de Prado (2024, SSRN 4748151);
Cotton (2024, arXiv:2411.05807); Besag (1975); Lindsay (1988); Varin, Reid & Firth (2011);
Vecchia (1988); Katzfuss & Guinness (2021); Pan, Abdulah, Genton & Sun et al. (2024);
Rue & Held (2005); George (1973); Ledoit & Wolf (2004, 2012); Bun, Bouchaud & Potters (2017);
James & Stein (1961); Gneiting & Raftery (2007); Scheuerer & Hamill (2015).
Full annotated lists in `papers/evaluation_and_generation_review.md` and
`papers/covariance_evaluation.md`.
