#!/usr/bin/env bash
# Render a paper markdown to PDF with full unicode-math coverage.
# Requires: pandoc + lualatex (TeX Live), and the macOS fonts STIX Two Text /
# STIX Two Math / Andale Mono / Menlo (the fallback chain in _pdf_header.tex).
#
#   ./papers/build_pdf.sh papers/schur_likelihood_paper.md
#
set -euo pipefail
src="${1:-papers/schur_likelihood_paper.md}"
out="${src%.md}.pdf"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pandoc "$src" -o "$out" \
  --pdf-engine=lualatex \
  -H "$here/_pdf_header.tex" \
  -V geometry:margin=1in \
  -V fontsize=10pt \
  -V colorlinks=true
echo "wrote $out"
