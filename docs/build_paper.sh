#!/usr/bin/env bash
# Regenerate a paper's WEB edition from its LaTeX source — single source of truth, so the
# online version cannot drift from the PDF. Requires pandoc (with citeproc).
#
#   ./docs/build_paper.sh
#
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"     # docs/
root="$(dirname "$here")"

mkdir -p "$here/papers/schur-likelihood"
pandoc "$root/papers/schur_likelihood_paper.tex" \
  --from=latex \
  --katex \
  --citeproc --bibliography="$root/papers/refs.bib" \
  --shift-heading-level-by=1 \
  --template="$here/_paper_template.html" \
  --metadata title="Schur Covariance Evaluation" \
  --metadata subtitle="A Principled Pseudo-Likelihood in High Dimensions" \
  -o "$here/papers/schur-likelihood/index.html"
echo "wrote docs/papers/schur-likelihood/index.html (generated from papers/schur_likelihood_paper.tex)"
