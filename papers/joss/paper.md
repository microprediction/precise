---
title: 'precise: online covariance, correlation and precision matrix estimation in Python'
tags:
  - Python
  - covariance estimation
  - streaming algorithms
  - shrinkage
  - portfolio construction
authors:
  - name: Peter Cotton
    orcid: 0000-0003-1832-2924
    affiliation: 1
affiliations:
  - name: Microprediction, LLC
    index: 1
date: 12 September 2026
bibliography: paper.bib
---

# Summary

`precise` estimates covariance, correlation and precision matrices from a stream. Each estimator
exposes `partial_fit`, consumes one observation at a time in a constant amount of work, and keeps
its entire state in a plain dictionary that can be checkpointed mid-stream and restored. Twenty
estimators share one interface, from a Welford sample covariance through exponentially weighted and
robust M-estimators to linear and nonlinear spectral shrinkage. The package depends on `numpy`
alone.

Two further layers sit on that core. An assessment layer scores a candidate matrix out of sample,
including a Schur pseudo-likelihood [@cotton2026schur] intended for the high-dimensional regime
where the plain Gaussian likelihood ranks estimates poorly. A recommender maps observable features
of a data window to an estimator choice, trained offline and shipped as a frozen `numpy`-only
decision tree. Adapters consume name-keyed dictionaries rather than fixed-length vectors, so a
universe whose members enter and leave over time — the ordinary situation in finance — needs no
special handling from the caller.

# Statement of need

Covariance is usually estimated once, from a batch. A practitioner whose data arrives continuously
wants the estimate updated per observation, at constant cost, with the option of checkpointing and
resuming. Doing that for a shrinkage estimator is not a matter of calling the batch routine more
often: the shrinkage intensity is itself a function of running statistics that must be maintained
incrementally, and the same is true of the spectral quantities behind nonlinear shrinkage.

The gap is sharpest for nonlinear shrinkage. Moving each sample eigenvalue by its own amount while
retaining the sample eigenvectors [@ledoitpeche2011; @ledoitwolf2020] materially outperforms linear
shrinkage, which pulls every eigenvalue toward a common target, and it is what makes a short
estimation window usable when variables are numerous relative to observations. We are not aware of
a streaming implementation of nonlinear shrinkage in another Python package. `precise` provides
three, differing in which sample the map reads: an expanding sample, a rolling window, and an
exponentially weighted sample.

Those three are not interchangeable, and the differences are measurable. The expanding-sample
estimator reproduces its batch counterpart and cannot forget. The rolling window uses the actual
window length and equal weights rather than an effective-sample-size approximation, and it tracks
drift: on the three drifting scenarios in `research/forgetting.py` it attains squared error lower
than the expanding estimator by factors of 3.75 (rotating factor directions), 4.27 (factor
structure disappearing) and 2.25 (alternating regimes).

The window also has a hard boundary, so a shock enters the estimate on arrival and leaves it
exactly $W$ steps later, producing a second rebalance prompted by nothing happening. The
exponentially weighted variant has no such discontinuity, but substitutes an effective sample size
for the weight distribution, which is a moment match rather than an equivalence [@oriol2024]. Under
Gaussian innovations the window is the cheaper of the two in portfolio turnover; under $t(3)$
innovations it is roughly fifteen per cent churnier with worse realized risk. Both ship, and the
documentation states which to prefer and why.

# State of the field

`scikit-learn`'s `sklearn.covariance` module [@scikit-learn] is the reference implementation for
much of this material, including Ledoit–Wolf shrinkage [@ledoit2004], the Oracle Approximating
Shrinkage of @chen2010, graphical lasso and robust alternatives. It offers eight estimators, none
of which implements `partial_fit`; each must see the whole sample at once.

`river` [@river] is the closest comparison, since online estimation is its purpose. Its
`covariance` module supplies `EmpiricalCovariance`, `EmpiricalPrecision` and an exponentially
weighted variant, all genuinely incremental. So Python is not without online covariance, and the
gap `precise` fills is narrower and more specific than absence: breadth of estimator under one
interface, a shared contract that makes them substitutable and comparable, and shrinkage —
particularly nonlinear shrinkage — in a streaming form.

`PyPortfolioOpt` [@martin2021] supplies Ledoit–Wolf and related estimators for portfolio
construction, batch only. The random-matrix line of work on spectral cleaning
[@bun2017] is well represented in the literature and in research code, but as batch procedures
over a fixed window.

# Software design

Every estimator implements two hooks, `_init_state(n_dim)` and `_update_state(state, x)`, and
inherits the public interface from a common base. State is a plain dictionary of arrays and
scalars, which is what makes `get_state`/`set_state` checkpointing transparent rather than a
pickling convention. The cost of that choice is that estimators cannot hold arbitrary objects; the
benefit is that a stream can be stopped, serialized and resumed in another process, which is the
situation the package exists for.

Expensive work is deferred to the read. Shrinkage intensities and spectral maps are computed in
`_state_to_cov` when `covariance_` is accessed, not on every update, so the per-observation cost
stays $O(p^2)$ and the $O(p^3)$ eigendecomposition is paid only when a matrix is actually wanted
and is memoized per state. This is what allows nonlinear shrinkage to be online at all: the map
reads only the eigenvalues of the running covariance and the observation count, never the
observations, so no window need be retained.

A registry exposes every estimator uniformly, which is what makes a single parametrized conformance
test possible and lets bake-offs iterate without enumeration. The trade-off accepted throughout is
numpy-only: no scikit-learn dependency, no compiled extensions, at the cost of reimplementing
recursions that exist elsewhere in batch form.

# Research impact statement

`precise` supports the covariance evaluation work in [@cotton2026schur], which introduces the Schur
pseudo-likelihood that the assessment layer implements, and the accompanying study of damping in
portfolio construction. The package is published on PyPI with documentation at
`precise.microprediction.org`, and the `research/` directory carries the reproduction scripts for
the comparisons quoted above so a reader can check them rather than take them.

The honest form of the impact claim is that the package is instrumentation. Its studies report what
the recommender does *not* buy as readily as what it does: choosing an estimator per problem is
close to, and sometimes worse than, fixing one good estimator, except where the number of variables
approaches the number of observations. That negative result is in the repository because a user
running the bake-off will find it anyway.

# Quality control

Two hundred and ninety-three tests run in continuous integration on Python 3.9, 3.11, 3.12 and
3.13. Three parametrized tests hold every registered estimator to the shared contract: `test_contract`
(symmetry, positive semidefiniteness, unit-diagonal correlation, finite scores),
`test_fit_equals_stream` (agreement between `fit` and repeated `partial_fit`), and
`test_state_roundtrip`. Targeted tests pin the properties that make individual estimators correct
rather than merely well formed — that nonlinear shrinkage vanishes as the sample grows, that it
stays invertible when variables outnumber observations, and that a dominant market mode survives
rather than being shrunk into the bulk.

# AI usage disclosure

Generative AI (Claude Code) was used substantially in this work: to draft the nonlinear shrinkage
estimators from the cited papers, the research scripts, the test suite and this paper. Every
quantitative claim here was produced by running the referenced script and is reproducible from the
repository. The implementations were checked against properties derived independently of the code —
asymptotic behaviour, invariances, agreement between streaming and batch paths — rather than
against the generating model's own expectations, and several drafts were corrected in review when
those checks failed. Responsibility for the content rests with the author.

# Acknowledgements

The Schur complement machinery grew out of discussions on portfolio construction; the `randomcov`
package supplies optional generative ensembles for the bake-offs.

# References
