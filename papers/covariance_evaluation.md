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
