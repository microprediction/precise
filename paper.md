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
    orcid: 0000-0000-0000-0000
    affiliation: 1
affiliations:
  - name: Microprediction, Inc.
    index: 1
date: 12 September 2026
bibliography: paper.bib
---

# Summary

`precise` estimates covariance, correlation and precision matrices from a stream. Each estimator
exposes `partial_fit`, consumes one observation at a time in a constant amount of work, and keeps
its entire state in a plain dictionary that can be checkpointed mid-stream. Twenty estimators share
one interface, from a Welford sample covariance through exponentially weighted and robust
M-estimators to linear and nonlinear spectral shrinkage. The package depends on `numpy` alone.

Two further layers sit on that core. An assessment layer scores a candidate matrix out of sample,
including a Schur pseudo-likelihood [@cotton2026schur] intended for the high-dimensional regime
where the plain Gaussian likelihood ranks estimates below chance. A recommender maps observable
features of a data window to an estimator choice, trained offline and shipped as a frozen
`numpy`-only decision tree. Adapters consume name-keyed dictionaries rather than fixed-length
vectors, so a universe whose members enter and leave over time — the ordinary situation in finance —
needs no special handling from the caller.

# Statement of need

Covariance estimation in Python is well served for batch data and poorly served for streams.
`scikit-learn`'s `sklearn.covariance` module [@scikit-learn] is the reference implementation of
Ledoit–Wolf shrinkage [@ledoit2004], the Oracle Approximating Shrinkage of @chen2010, graphical
lasso and robust alternatives; at the time of writing it offers eight estimators and **none of them
implements `partial_fit`**. Each must see the whole sample at once. A practitioner with a running
data feed is left to re-fit over a sliding window, which costs work proportional to the window at
every step, or to write the recursions themselves.

The gap is sharpest for nonlinear shrinkage. Moving each sample eigenvalue by its own amount while
retaining the sample eigenvectors [@ledoitpeche2011; @ledoitwolf2020] materially outperforms the
linear shrinkage that pulls every eigenvalue toward a common target, and it is precisely what makes
a short estimation window usable in high dimensions. The streaming implementations available
elsewhere are linear. We are not aware of a published streaming implementation of nonlinear
shrinkage, and `precise` provides three: over an expanding sample, over a rolling window, and over
an exponentially weighted sample.

Those three exist because they are not interchangeable, and the difference is measurable rather
than a matter of taste. The expanding-sample estimator reproduces its batch counterpart and cannot
forget. The rolling window keeps the asymptotics exact, since equal weights inside a window of
length $W$ are exactly the sample the theory describes, and on drifting synthetic covariances it
attains three to four times lower squared error than the expanding estimator.

The window also has a hard boundary, so a shock enters the estimate on arrival and leaves it exactly
$W$ steps later, producing a second rebalance prompted by nothing. The exponentially weighted variant
has no such discontinuity, but substitutes an effective sample size for the weight distribution,
which is a moment match rather than an equivalence [@oriol2024]. Under Gaussian innovations the
window is the cheaper of the two in turnover; under $t(3)$ innovations it is fifteen per cent
churnier with worse realized risk. Both ship, and the documentation states which to prefer and why.

The package is also a vehicle for comparison. Because no estimator wins everywhere, `precise`
carries a registry that lets a bake-off iterate over every estimator uniformly, a conformance suite
that holds all of them to one contract, and out-of-sample studies under `research/` that report what
the recommender does and does not buy — including that choosing per-problem is close to, and
sometimes worse than, fixing one good estimator, except in the regime where the number of variables
approaches the number of observations. Reporting that honestly seems more useful than asserting the
recommender works.

# Quality control

Two hundred and ninety-three tests run in continuous integration on Python 3.9 through 3.13. A
single parametrized conformance test holds every registered estimator to the shared contract:
symmetry, positive semidefiniteness, unit-diagonal correlation, agreement between `fit` and repeated
`partial_fit`, and state round-tripping. Targeted tests pin the properties that make individual
estimators correct rather than merely well formed — that nonlinear shrinkage vanishes as the sample
grows, that it stays invertible when variables outnumber observations, that a dominant market mode
survives rather than being shrunk into the bulk.

# Acknowledgements

The Schur complement machinery grew out of discussions on portfolio construction; the
`randomcov` package supplies optional generative ensembles for the bake-offs.

# References
