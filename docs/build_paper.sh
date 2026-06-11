#!/usr/bin/env bash
# Regenerate each paper's WEB edition from its LaTeX source — single source of truth, so the
# online version cannot drift from the PDF. Requires pandoc (with citeproc).
#
#   ./docs/build_paper.sh
#
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"     # docs/
root="$(dirname "$here")"

# build_one <tex-basename> <out-slug> <title> <subtitle>
# The PDF lives next to the .tex in papers/ and is linked from the web header.
# The source keeps numbered equation environments (for the arXiv/PDF edition); for the
# web we strip them to unnumbered \[ \] display math, which KaTeX renders cleanly. The
# prose refers to equations descriptively, so no cross-references break in the process.
build_one() {
  local tex="$1" slug="$2" title="$3" subtitle="$4"
  local pdfurl="https://github.com/microprediction/precise/blob/main/papers/${tex}.pdf"
  local websrc; websrc="$(mktemp)"
  sed -e 's/\\begin{equation}/\\[/g' -e 's/\\end{equation}/\\]/g' "$root/papers/${tex}.tex" > "$websrc"
  mkdir -p "$here/papers/$slug"
  pandoc "$websrc" \
    --from=latex \
    --katex \
    --citeproc --bibliography="$root/papers/refs.bib" \
    --shift-heading-level-by=1 \
    --template="$here/_paper_template.html" \
    --metadata title="$title" \
    --metadata subtitle="$subtitle" \
    --metadata pdfurl="$pdfurl" \
    -o "$here/papers/$slug/index.html"
  rm -f "$websrc"
  echo "wrote docs/papers/$slug/index.html (generated from papers/${tex}.tex)"
}

build_one schur_likelihood_paper schur-likelihood \
  "Schur Covariance Evaluation" \
  "A Principled Pseudo-Likelihood in High Dimensions"

build_one two_sides_of_schur_damping two-sides-of-schur-damping \
  "Two Sides of Schur Damping" \
  "High-Dimensional Pseudo-Likelihoods and Portfolio Allocation"
