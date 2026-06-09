# On the statistical power of covariance evaluation — and a Schur-style pseudo-likelihood

Research notes (reproducible via `python research/metric_power.py`). The question: when we benchmark
online covariance estimators, *which scoring rule is the best judge* — the one that most reliably
ranks a genuinely-better estimate above a worse one from finite test data? We know the truth Σ in
these experiments, so the "true" ordering is the exact KL divergence to Σ; a judge is scored by how
often it reproduces that ordering (its statistical power), using only a held-out sample.

## Findings

1. **Well-specified, low dimension → held-out log-likelihood wins.** It is the most powerful judge
   (Neyman–Pearson), with Stein loss essentially tied. Frobenius is data-hungry; naive (marginal,
   k=1) random projections are weakest.

2. **Random k-D projections: power rises with k.** Scoring data projected onto random k-subspaces
   *jointly* recovers the cross-direction information that marginal projections discard; holding the
   direction budget fixed, power climbs monotonically toward the full likelihood as k → p.

3. **In high dimensions the full likelihood fails.** With an unidentifiable noisy small-eigenvalue
   tail (the p ≈ n regime), the Gaussian likelihood — dominated by Σ̂⁻¹ and log det, i.e. the
   smallest, least-estimable eigenvalues — drops to *chance* at ranking estimates. Power vs k
   becomes non-monotonic, peaking at moderate k; `k = p` (the full likelihood) falls back to chance.
   Inversion-free judges (Frobenius, moderate-k projections) retain power.

4. **Same trade-off as portfolio theory; Schur is the shared knob.** The min-variance portfolio
   (`w ∝ Σ̂⁻¹1`) fails for the identical reason — it trusts the raw inverse of an ill-conditioned
   covariance. Schur complementary allocation's γ (coupling-trust) knob, which interpolates HRP
   (γ=0) and min-variance (γ=1), is exactly the regularization both need. A γ-regularized likelihood
   judge recovers power, peaking at moderate γ, mirroring the k-curve.

5. **A useful Schur-style pseudo-likelihood for evaluation.** The full likelihood factorizes through
   Schur complements into block conditionals; dropping the cross-block conditioning gives a
   **block (composite) pseudo-likelihood** — a sum of Gaussian log-likelihoods on small blocks,
   inverting only b×b matrices. It is the evaluation analogue of the HRP/Schur allocation principle:

   | regime | full likelihood | block pseudo-likelihood (b≈10) |
   |---|---|---|
   | high-dim, noisy tail | 0.50 (chance) | **0.85** (recovers) |
   | clean, low-dim | 0.98 (optimal) | 0.84 (retains most) |

   So it is cheap (feasible at p≈500), robust where the full likelihood collapses, a proper
   composite likelihood (not ad hoc), and tunable — block size is the robustness↔power knob, with
   block = p recovering the full likelihood.

   (Seriation — aligning blocks to clusters — gave no clean gain for *scoring*: covariance-quality
   information is distributed across pairs, not localized, so block placement is second-order. Its
   payoff is on the *allocation* side, a different objective.)

## References

- López de Prado, M. (2015). *Building Diversified Portfolios that Outperform Out-of-Sample.*
  SSRN working paper 2708678 (the original HRP paper). [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678)
- López de Prado, M. (2016). *Building Diversified Portfolios that Outperform Out-of-Sample.*
  Journal of Portfolio Management 42(4), 59–69 (published version). [link](https://jpm.pm-research.com/content/42/4/59.short)
- Antonov, A., Lipton, A., & López de Prado, M. (2024). *Overcoming Markowitz's Instability with the
  Help of the Hierarchical Risk Parity (HRP): Theoretical Evidence.* SSRN 4748151. Analytical
  out-of-sample variance results for HRP. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4748151)
- Cotton, P. (2024). *Schur Complementary Allocation: A Unification of Hierarchical Risk Parity and
  Minimum Variance Portfolios.* arXiv:2411.05807. [link](https://arxiv.org/abs/2411.05807)

<!-- DRAFT addition for papers/covariance_evaluation.md. Append after the "Findings" list.
     Numbers tagged [prelim] refresh when the full grids complete. -->

## Large-scale corroboration with the shipped assessors (precise-lab)

The findings above were re-tested at scale with the *shipped* `precise` assessors over a
144-combination grid (4 generators × p ∈ {8…256} × n/p ∈ {½…16} × 200 reps), plus a
Neyman–Pearson **judge-power** experiment and real data (Fama–French ff100/ff49, crypto, Polymarket).
Reproducible from `precise-lab` (`lab.run_experiment`, `lab.judge_power`, `lab.assess_assessors`).

**The best judge depends on the gold — "match the judge to the objective."** A judge's power is the
probability that, from a single *finite* test sample, it orders a random pair of estimates the way the
truth does (0.5 = chance). At c = p/n ≈ 1, n_test = 2p, pooled over generators [prelim]:

| judge | gold = KL | gold = Frobenius | gold = GMV variance |
|---|---|---|---|
| LogLikelihood | **0.985** | 0.700 | 0.697 |
| SteinLoss | **0.985** | 0.700 | 0.698 |
| SchurLikelihood | 0.740 | **0.771** | 0.712 |
| GMVVariance | 0.693 | 0.691 | **0.949** |
| VariogramScore | 0.598 | 0.730 | 0.575 |
| BlockPseudoLikelihood | 0.761 | 0.724 | 0.689 |

This *sharpens* findings #1 and #3. The held-out log-likelihood is the most powerful judge **only for
the KL/density gold** — which is the same tail-dominated functional, so the agreement is partly
built-in (with a large test set it reproduces the KL ordering at Spearman ≈ 1.0 even at c ≈ 1; the
collapse is a *finite-test*, *practical-gold* phenomenon). Against the practically relevant golds —
matrix recovery (Frobenius) and realized portfolio variance (GMV) — the inversion-heavy likelihood
sheds power toward chance, while:

- **GMVVariance** is the most powerful judge of the **allocation** gold (0.95) but weak elsewhere — a
  *rank-1 probe* (it only sees the `w ∝ Σ̂⁻¹1` direction), a failure mode distinct from
  inverse-fragility;
- **SchurLikelihood** is the best judge of **matrix recovery** and is never the worst on any gold —
  the **robust default judge**, the evaluation-side counterpart of γ regularizing allocation.

So there is no gold-free "best scoring rule": the right judge is the assessor aligned with what you
ultimately care about, and the Schur pseudo-likelihood is the safest choice when that is unknown or
when you care about the matrix itself.

**Two distinct power-limiting axes.** (i) *Inverse-fragility* — log-likelihood/Stein collapse on
top-spectrum golds in high dimension because their score is dominated by the unidentifiable
small-eigenvalue tail; the Schur damping repairs this. (ii) *Probe rank* — GMV is a rank-1 probe and
is therefore a weak *recovery* judge at every dimension, regardless of conditioning. These are
orthogonal; only the first is a Schur-γ matter.

**Estimator landscape (context).** Ranking estimators by realized GMV variance, the empirical
covariance wins for n/p ≳ 4 and shrinkage/Schur win for n/p ≤ 1, the crossover tilting upward with p
— textbook random-matrix behaviour, with `SchurCovariance(γ=½)` taking the moderate-/high-dimension
low-sample cells [prelim]. `TylerCovariance` and `GeodesicEwaCovariance(r≥0.05)` are numerically
unstable under single-row streaming (≈99% non-PD on crypto), recorded rather than hidden.

**Real data.** The same rolling-window evaluation on Fama–French ff100/ff49 and on crypto / Polymarket
panels (no known truth, so likelihood / GMV / variogram only) reproduces the regime ordering on the
n/p axis recreated by sweeping universe size and window length. [prelim — full real-data tables pending]
