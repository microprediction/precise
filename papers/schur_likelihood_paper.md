# Schur Covariance Evaluation
### A Principled Pseudo-Likelihood in High Dimensions

**Peter Cotton** · *Draft* · microprediction/precise

## Abstract

We introduce the **Schur pseudo-likelihood**, a one-parameter family `ℓ_γ`, `γ ∈ [0,1]`, that
deforms the Gaussian likelihood by damping the cross-block coupling carried by its Schur complements.
The endpoints are familiar — `γ=1` is the exact joint likelihood, `γ=0` is block composite
(pseudo-)likelihood — and the interior is the new object: a continuous **coupling-strength** dial that
the composite-likelihood, Vecchia, and Gaussian-Markov-random-field literatures do not have, because
those methods regularize the *conditioning structure* (which variables to condition on) at full
strength, an axis orthogonal to `γ`. The contribution is deliberately narrow and, we think, clean:
not a new estimator but a *pseudo-likelihood with a single interpretable knob* that (i) recovers the
power and conditioning the full likelihood loses in high dimensions, where it becomes — we show —
worse than chance at ranking estimators; (ii) admits an exact characterization of what `γ` does, via a
worked model we verify numerically: it recovers the true predictive law for every `γ` but maps to an
inflated covariance that leaves the positive-definite cone below a coupling-dependent threshold —
pinning down precisely why `ℓ_γ` is a device for *scoring* or *transforming* a covariance rather than
for estimating one by free maximization; and (iii) is **broadly applicable** — wherever a Gaussian
block likelihood is used (spatial statistics, graphical models, longitudinal data, any
composite-likelihood setting), and even, via the identical algebra, in portfolio allocation, where the
same `γ` interpolates hierarchical risk parity and minimum-variance optimization. We show in
simulation that an interior `γ` strictly dominates both endpoints when the coupling is partially
reliable, that a geodesic (affine-invariant) damping is stable where the linear one is not, and that
the high-dimensional inversion catastrophe the construction avoids is borne out on real equity returns.

## 1. The high-dimensional failure of the likelihood

For a zero-mean Gaussian the per-sample log-likelihood is `ℓ(Σ̂; x) = −½(log det Σ̂ + xᵀΣ̂⁻¹x)`,
equivalently the **covariance-likelihood** form in the sample covariance `S`,
`ℓ(Σ̂; S) = −½(log det Σ̂ + tr(Σ̂⁻¹S))` — proportional to the Wishart log-likelihood of `S` given `Σ̂`
and, up to constants, the negative Stein/entropy loss. Both terms are governed by the *smallest*
eigenvalues of `Σ̂`: `log det = Σ log λᵢ → −∞` and `Σ̂⁻¹` blows up as `λ_min → 0`. When `p/n → c > 0`
(the Marčenko–Pastur / spiked regime) those eigenvalues collapse toward zero and are unidentifiable,
so the likelihood stakes its verdict on noise. Empirically (`research/metric_power.py`) the held-out
likelihood drops to **≈0.45** — *below chance* — at correctly ordering two estimates of *known*
relative quality, while inversion-free judges hold ≈0.85. This is the evaluation-side image of
Markowitz "error maximization" in `w ∝ Σ̂⁻¹1`: the same `Σ̂⁻¹`, the same fragility. The remedy is to
stop trusting the raw inverse — the question is how, with one interpretable knob.

## 2. The exact Schur factorization of the Gaussian likelihood

Partition the `p` variables into `K` ordered blocks `x = (x_1, …, x_K)`. The joint density factorizes
*exactly* into block conditionals, `p(x) = ∏_k p(x_k | x_{<k})`, and for a Gaussian each is itself
Gaussian with

- conditional covariance = **Schur complement** `S_k = Σ_kk − Σ_{k,<k} Σ_{<k,<k}⁻¹ Σ_{<k,k}`,
- conditional mean `μ_{k|<k} = μ_k + Σ_{k,<k} Σ_{<k,<k}⁻¹ (x_{<k} − μ_{<k})`.

Hence `log det Σ = Σ_k log det S_k` and the quadratic form splits blockwise — the block-LDLᵀ /
block-Cholesky factorization, the engine of Vecchia, GMRF, and nested-dissection elimination. **No
approximation has been made yet**: only a re-expression of the same likelihood as a sum of
block-conditional terms, each inverting only the conditioning block `Σ_{<k,<k}`.

## 3. The Schur pseudo-likelihood

We introduce a single **coupling-strength** parameter `γ ∈ [0,1]` that damps the Schur complement and
the conditional regression in lockstep:

```
S_k(γ)      = Σ_kk − γ · Σ_{k,<k} Σ_{<k,<k}⁻¹ Σ_{<k,k}   =  (1−γ) Σ_kk + γ S_k
μ_{k|<k}(γ) = μ_k + γ · Σ_{k,<k} Σ_{<k,<k}⁻¹ (x_{<k} − μ_{<k})

ℓ_γ(Σ; x)   = Σ_k  log N( x_k ; μ_{k|<k}(γ), S_k(γ) ).
```

| `γ` | `ℓ_γ` is | character |
|---|---|---|
| `1` | the **exact joint Gaussian likelihood** | most powerful, fragile (inverts all of `Σ`) |
| `(0,1)` | a **tunable bridge** that *changes the block covariances* | inverts only conditioning blocks; better-conditioned |
| `0` | the **block composite likelihood** | robust; product of block marginals |

**What kind of object is `ℓ_γ`?** At `γ=1` it is the joint log-density; at `γ=0` it is a product of
block marginals — a composite likelihood in the sense of Besag/Lindsay/Varin–Reid–Firth: a sum of
proper component log-densities that does not itself integrate to one. For `γ∈(0,1)` each term
`log N(x_k; μ(γ), S_k(γ))` is still a *genuine* Gaussian log-density (a strictly proper local score
whenever `S_k(γ) ≻ 0`), but the damped conditionals are mutually inconsistent — they are not the
conditionals of any single joint Gaussian — so `ℓ_γ` is a **pseudo-likelihood**, not a normalized
joint. This is the composite-likelihood bargain: trade the joint-density property for tractable,
well-conditioned components, and `γ` controls how much of the cross-block information the marginals
discard is dialed back in.

**Three uses, only two of them well-behaved.** (a) *Score* a fixed estimate `Σ̂` by `ℓ_γ(Σ̂; S_test)`.
(b) *Transform* a given `Σ̂` by replacing each conditional covariance with `S_k(γ) = (1−γ)Σ̂_kk + γ Ŝ_k`
— a structured (block-conditional) **shrinkage** of the coupling toward block-diagonal with intensity
`1−γ`, the basis-dependent counterpart of spectral shrinkage (§5); always PSD for `γ∈[0,1]` and the
operation `SchurCovariance` and Schur allocation perform. (c) *Estimate* `Σ` by maximizing
`ℓ_γ(Σ; S)` — which §4 shows is **degenerate** for `γ<1`. The clean reading is that `ℓ_γ` is a
scoring/transform device, not a free estimation objective.

## 4. What `γ` does, exactly: a worked model

To see precisely what damping does — and why estimation by free maximization fails while scoring and
transformation do not — take the smallest non-trivial case and solve it in closed form. Let
`x₁ ~ N(0, a)`, `x₂ = b⋆ x₁ + ε`, `ε ~ N(0, s⋆)`, two scalar blocks, so the true conditional law of
`x₂` given `x₁` has regression `b⋆` and Schur complement (conditional variance) `s⋆`. For a candidate
`Σ = (A, C, D)` the damped conditional has effective coefficient `β = γC/A` and variance
`S(γ) = D − γC²/A`. Maximizing the population (expected) `ℓ_γ` over `(A, C, D)` gives (verified
numerically in `research/schur_likelihood_theory.py`):

> **Proposition (two-block Gaussian).** For every `γ ∈ (0,1]` the maximizer recovers the *true
> predictive law* — `β = b⋆` and `S(γ) = s⋆` — but the *implied covariance* is **inflated**:
> `Â = a`, `Ĉ = Σ₁₂⋆ / γ`, `D̂ = Σ₂₂⋆ + b⋆²a (1/γ − 1)`. This `Σ̂` is positive-definite iff
> `γ² (1 − ρ²) > (1 − γ) ρ²`, where `ρ² = b⋆²a / (b⋆²a + s⋆)` is the block coupling (the conditional
> `R²`). Below the threshold `γ_min(ρ²)` the free maximizer leaves the PSD cone.

The numerics (`a=1, b⋆=0.8, s⋆=0.5`, so `ρ²=0.561`) show `β=0.800` and `S(γ)=0.500` for every `γ`
while `Ĉ` runs `0.80 → 8.0` as `γ:1→0.1`, and the maximizer is PSD only above `γ_min = 0.660`.

**The general case** (verified in `research/schur_likelihood_theory.py` by an exact closed-form
expected `ℓ_γ` and independent local search):

> **Proposition (general blocks).** For an arbitrary ordered partition the population `ℓ_γ` maximizer
> recovers *every block's true conditional law* — effective regression `G_k(γ) = B_k⋆`, damped
> conditional covariance `S_k(γ) = S_k⋆` — for every `γ ∈ (0,1]`, and the implied joint covariance is
> inflated *sequentially*: block `k`'s cross-block coupling scales by `1/γ` through the (already
> inflated) conditioning covariance `Σ̂_{<k,<k}`. For **two vector blocks** the PSD condition is
> exactly `γ² (1 − ρ²_max) > (1 − γ) ρ²_max`, where **`ρ²_max` is the largest squared canonical
> correlation between the blocks** — the scalar `ρ²` generalized to the dominant coupling mode. For
> `K` blocks the inflation, and hence the PSD threshold, **compound along the chain**.

The verification confirms each clause: the recovered `(G_k(γ), S_k(γ))` equal the truth at every `γ`;
the local search finds nothing above the closed form (max-gap `0`); and for a random vector two-block
problem with `ρ²_max=0.115` the predicted threshold `γ_min=0.302` matches the exact PSD boundary (SPD
at `γ=0.32`, not at `γ=0.28`). Three consequences, now established beyond the scalar case:

1. **Damping is undone by rescaling.** `ℓ_γ` "knows" the true conditional distribution at any `γ`; it
   simply expresses it through a coefficient scaled by `1/γ`. So *fitting* `Σ` to maximize `ℓ_γ`
   overcompensates — the implied joint inflates and, for strong enough coupling relative to `γ`,
   ceases to be a covariance at all. **`ℓ_γ` is degenerate as a free estimation objective for `γ<1`**;
   this is exactly why the sane uses are to *score* a covariance or to *transform* one (shrink the
   coupling, §3b) — operations that hold `Σ̂` fixed rather than letting it absorb the damping.

2. **`ℓ_γ` is a bias–variance dial on the scoring rule.** Because the expected score is maximized at
   the *inflated* `Σ̂(γ)`, not at `Σ⋆`, `ℓ_γ` is for `γ<1` **not strictly proper** for `Σ`: it carries
   a (mild, for `γ` near 1) bias toward inflation. Its advantage is variance: the full likelihood
   (`γ=1`) is properly centered but, through `Σ̂⁻¹` and `log det`, has exploding variance in high
   dimensions; damping trades a little properness for a large reduction in score variance. The
   empirically optimal evaluation `γ` (§8) is the one whose bias²+variance for *ranking* is smallest.

3. **The usable range shrinks with coupling.** `γ_min(ρ²)` increases from `0` (weak coupling, any `γ`
   safe) to `1` (strong coupling, only the full likelihood stays PSD). This is the same near-singular
   Schur-complement regime in which linear damping destabilizes and geodesic damping does not (§7) —
   two faces of one fact: strong coupling is where naïve interpolation of the conditioning is most
   dangerous.

## 5. Schur damping is a structured shrinkage (and is complementary to spectral shrinkage)

The transform use (§3b) shrinks each conditional covariance from its full Schur complement `Ŝ_k`
toward the unconditional block `Σ̂_kk` with intensity `1−γ`. Since `Ŝ_k ⪯ Σ̂_kk`, this *raises* the
conditional covariance, lifting the small eigenvalues of every block-sized inverse `ℓ_γ` performs — a
James–Stein-style shrinkage applied *blockwise to the conditioning*. It is therefore **orthogonal and
complementary to spectral shrinkage**: Ledoit–Wolf and the rotationally-invariant estimators (Bun,
Bouchaud & Potters 2017) regularize the *eigenvalues* (basis-free); Schur damping regularizes the
*cross-block coupling* (basis-dependent). Both improve conditioning, along different geometry, and can
be composed: `γ` is to the block-conditional factorization what shrinkage intensity is to the spectrum.

## 6. The unifying role: one knob across many constructions

The same `ℓ_γ` places a scattered set of objects on **two axes of the same block factorization**:

- **Axis A — conditioning structure (sparsity):** for each block, *which / how many* earlier blocks
  it conditions on. Full (dense) ↔ none (block-diagonal). The axis Vecchia, GMRF, banding/tapering and
  nested dissection regularize along.
- **Axis B — coupling strength `γ`:** *how strongly* the chosen conditioning is trusted (§3). Full
  (`γ=1`) ↔ none (`γ=0`). The axis introduced here.

```
                         γ = 1 (full trust)        γ ∈ (0,1)                 γ = 0 (no trust)
  full conditioning   exact Gaussian likelihood   ┌────────────────────┐    block composite
  (dense)             = MVO  w ∝ Σ⁻¹1             │   SCHUR PSEUDO-LIK  │    likelihood
                                                   │     (this work)    │    = HRP-style allocation
  sparse conditioning block-Vecchia / GMRF        │  Schur + sparsity  │           (block-marginal,
  (Vecchia/GMRF)      likelihood (exact conds.)   └────────────────────┘            same column)
  nested dissection   = Schur-complement elimination of the (sparse) blocks
```

- **Vecchia / GMRF / nested dissection** (Vecchia 1988; Katzfuss–Guinness 2021; Pan et al. 2024;
  Rue–Held 2005; George 1973) use the *exact* conditioning (`γ=1`) and regularize by **sparsity**. The
  Schur pseudo-likelihood adds the orthogonal **strength** axis; the two compose.
- **Composite / pseudo-likelihood** (Besag 1975; Lindsay 1988; Varin–Reid–Firth 2011) is the `γ=0`
  column; `ℓ_γ` is its one-parameter deformation back toward the joint likelihood.
- **Portfolio allocation, the same algebra transported:** minimum-variance (`w ∝ Σ̂⁻¹1`) is the `γ=1`
  full-conditioning corner, hierarchical risk parity (López de Prado 2015/2016) the `γ=0` corner, and
  **Schur complementary allocation** (Cotton 2024) damps *the same Schur complement with the same `γ`*
  between them. The Schur pseudo-likelihood is its evaluation/estimation mirror — identity, not
  analogy; Antonov–Lipton–de Prado (2024) on HRP stability explains the interior dominance.

One sentence: **`γ` is one knob that, at its endpoints, recovers the joint likelihood, composite
likelihood, block-Vecchia/GMRF likelihoods, MVO and HRP — and in its interior is the common bridge
all of these lack.**

## 7. Broad applicability

The construction needs only three ingredients — a Gaussian (or Gaussian-pseudo) likelihood, a block
partition, and the conditional/Schur factorization of §2 — so the coupling-strength knob is **generic
to Gaussian-block models**, not specific to covariance estimation or finance:

- **Spatial statistics / Gaussian processes.** Vecchia and GMRF likelihoods already condition each
  location on a neighborhood; `γ` adds a robustness dial on *how strongly* those neighbor relations are
  trusted — orthogonal to, and composable with, the existing choice of neighborhood size/ordering.
- **Gaussian graphical models / precision estimation.** With blocks as cliques or neighborhoods, `γ`
  damps the conditional-dependence strength, a continuous relaxation between the full penalized
  likelihood and node-/block-wise pseudo-likelihood (Besag; Meinshausen–Bühlmann).
- **Longitudinal / panel / state-space models.** With blocks as time slices, `γ` interpolates between
  treating slices independently (`γ=0`) and the full temporal joint (`γ=1`) — a tempering of the
  temporal coupling.
- **General composite likelihood.** Anywhere composite likelihood is used for tractability (Varin–
  Reid–Firth's survey spans genetics, networks, multivariate survival, image analysis), `γ` is a
  generic dial from the composite (`γ=0`) toward the full (`γ=1`) likelihood, with §4's caveat that it
  is to be used for scoring/tempering, not free estimation.
- **High-dimensional model scoring.** As a *score*, `ℓ_γ` is a high-dimension-robust, nearly-proper
  alternative to the log score for any of the above — the use we test directly here.

What we prove is the two-block characterization (§4) and demonstrate the covariance-evaluation case
(§8); the wider applicability is a claim about the *mechanism* (damping a conditional factorization
shared by all these models), flagged as such, not a measured result in each domain.

## 8. Geometry, and results

**Linear vs geodesic damping.** Damping interpolates each conditional covariance between `Σ_kk` and
`S_k`. Linear damping is `S_k(γ) = (1−γ)Σ_kk + γS_k`; **geodesic** damping moves along the
affine-invariant SPD geodesic `Σ_BD #_γ Σ = Σ_BD^{1/2}(Σ_BD^{−1/2} Σ Σ_BD^{−1/2})^{γ} Σ_BD^{1/2}` (the
Fisher–Rao geodesic, reusing the `GeodesicEwaCovariance` step), lifting small eigenvalues
*multiplicatively*. They agree to first order and at the endpoints but differ near a singular Schur
complement.

Results (reproducible; rankings are ensemble-dependent — see
`papers/evaluation_and_generation_review.md`):

- **`γ` traces a regime-dependent optimum** (`research/metric_power.py`). Power climbs to `γ=1` when
  the coupling is reliable (Neyman–Pearson); falls toward `γ=0` in the high-dimensional noisy regime;
  and at *partial* reliability an **interior `γ` strictly dominates both endpoints** (≈0.84 vs ≈0.43)
  — the bias–variance optimum of §4(2), and the likelihood analogue of Schur allocation beating both
  HRP and MVO.
- **Geodesic stability.** Near a singular Schur complement (strong coupling — the `γ < γ_min` danger
  zone of §4(3)) linear damping dips (≈0.64) while geodesic damping holds full power.
- **The motivating failure, economically** (Ken French 100 portfolios, rolling minimum-variance OOS
  volatility, `p=100`, `n=60`; `research/oos_equity.py`). Not a test of `ℓ_γ` as an equity estimator —
  we are explicit about that — but a confirmation of the catastrophe it avoids: inverting/unregularized
  estimators blow up (annualized vol 9.6 empirical, 6.8 Huber, 1.3×10⁶ Tyler) while well-conditioned
  shrinkage stays at 0.141 (vs 0.129 oracle, 0.228 equal-weight). In high dimensions the reward is for
  *conditioning* — for not trusting the raw inverse, which is what `γ<1` does.

## 9. Limitations and open problems

- **Efficiency theorem.** §4 now covers vector and `K`-block partitions (predictive-law recovery,
  canonical-correlation PSD threshold, compounding inflation, all verified). What remains is a
  Godambe-information (composite-likelihood efficiency) statement for `ℓ_γ` relative to the full
  likelihood under a spiked/Marčenko–Pastur model, and a closed-form characterization of the
  *compounded* `K`-block PSD threshold (we have the two-block `ρ²_max` form and numerical evidence of
  compounding, not yet a chain formula).
- **Optimal `γ`.** The evaluation/tempering optimum `γ*(p, n, spectrum, blocks)` is characterized only
  empirically; a plug-in rule from the effective rank / coupling `ρ²` is open. (We are wary of a
  *trained* selector after the sibling recommender failed to generalize across novel generative
  families — `research/oos.py`.)
- **Block ordering and choice**, and composition with the Axis-A sparsity choice (the "Schur +
  sparsity" cell), remain to be studied; like Vecchia, `ℓ_γ` depends on the partition/ordering.
- **Scaling.** Recursive block inversion gives `O(p·b²)`; a Russell-scale (`p≈2000`) real-data study,
  where the separation should be largest, is set up to run.
- **Falsification.** The thesis predicts the interior-`γ` dominance should *vanish* when the coupling
  is fully reliable (LKJ, large `η`, low dimension → `γ*→1`) or pure noise (hard Marčenko–Pastur bulk
  → `γ*→0`); an interior optimum in a known-fully-reliable regime would contradict it.

## Acknowledgements

The original Schur complementary theory (Cotton 2024), of which the Schur pseudo-likelihood is the
evaluation/estimation mirror, was developed with the support of Intech Investments.

## References

López de Prado (2015/2016); Antonov, Lipton & López de Prado (2024, SSRN 4748151);
Cotton (2024, arXiv:2411.05807); Besag (1975); Lindsay (1988); Varin, Reid & Firth (2011);
Vecchia (1988); Katzfuss & Guinness (2021); Pan, Abdulah, Genton & Sun et al. (2024);
Rue & Held (2005); George (1973); Meinshausen & Bühlmann (2006);
Ledoit & Wolf (2004, 2012); Bun, Bouchaud & Potters (2017); James & Stein (1961);
Gneiting & Raftery (2007); Scheuerer & Hamill (2015).
Full annotated lists in `papers/evaluation_and_generation_review.md` and
`papers/covariance_evaluation.md`.
