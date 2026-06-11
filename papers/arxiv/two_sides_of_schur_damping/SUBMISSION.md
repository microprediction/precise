# arXiv submission — Two Sides of Schur Damping

## What to upload
Upload **`two_sides_of_schur_damping_arxiv.tar.gz`** on the arXiv "Add Files" step.
It contains exactly the two files arXiv needs at top level:

- `two_sides_of_schur_damping.tex` — source (`article`, `pdflatex`)
- `two_sides_of_schur_damping.bbl` — pre-built bibliography (arXiv does **not** run BibTeX)

`refs.bib` is kept in this folder for future editing but is **deliberately excluded**
from the tarball — including it can make arXiv attempt a BibTeX run; the `.bbl` is authoritative.

Build verified with TeX Live 2025: compiles cleanly from `.tex` + `.bbl` alone
(no `.bib`), 5 pages, 0 undefined references/citations, all 11 citations resolved.

## Form metadata

**Title:**
Two Sides of Schur Damping: High-Dimensional Pseudo-Likelihoods and Portfolio Allocation

**Authors:** Peter Cotton

**Abstract** (plain text — paste into the arXiv abstract box):

Two communities that rarely cite each other -- spatial statisticians fitting
high-dimensional weather fields, and quantitative investors building portfolios --
have independently arrived at the same mathematical object: a Schur complement, damped
by one interpretable parameter. In spatial modeling the Schur complement is the
conditional covariance that makes a Gaussian (Vecchia) pseudo-likelihood estimable at
scale, and recent work regularizes it by shrinking toward a base model. In allocation
it is the residual risk of a bet net of its hedge, and the same parameter interpolates
hierarchical risk parity and the minimum-variance portfolio. We show these are one
operation -- reliability shrinkage of a conditional Gaussian -- so that the damping a
weather model needs to remain estimable when stations outnumber observations is, term
for term, the damping a portfolio needs to remain stable when assets outnumber returns.
The optimal amount is a closed-form reliability, a James--Stein shrinkage that is
simultaneously a Ledoit--Wolf intensity. The shrinkage machinery is classical, but the
identity appears to be new: to our knowledge neither literature has noted that the
conditional shrinkage a spatial model fits and the diversification--variance tilt a
portfolio chooses are one and the same quantity. We make the correspondence precise,
note that the two literatures have each supplied what the other lacks, and report a
small experiment on the one genuinely open choice -- how to set the damping --
suggesting the spatial community's fitted intensity is, if anything, the better recipe.

## Categories
- **Primary:** `q-fin.PM` (Portfolio Management) — the allocation reading and HRP↔min-variance interpolation
- **Cross-list:** `stat.ME` (Methodology) — the identity + closed-form reliability shrinkage
- **Cross-list (optional):** `stat.CO` (Computation) — the O(p·m²) streaming estimator

## Notes
- MSC/ACM: optional, can leave blank.
- License: default arXiv non-exclusive is fine; choose CC BY 4.0 if you want reuse.
- Comments field suggestion: "5 pages. Code: https://github.com/microprediction/precise"
