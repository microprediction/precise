#!/usr/bin/env python3
"""Preprocess a paper's LaTeX for the web edition (used by build_paper.sh).

Numbered equation environments work in the PDF but not in KaTeX: a \\label inside
math renders as a literal red "\\labeleq:..." and \\eqref becomes a dead [eq:...]
stub. This script reproduces LaTeX's numbering instead: each \\begin{equation}
increments a counter; a \\label{eq:X} inside it becomes a KaTeX \\tag{n} and the
mapping X -> n resolves every \\eqref{eq:X} in the prose to (n). Equation
environments are then converted to \\[ \\] display math, which KaTeX renders.

Usage: _webtex.py input.tex output.tex
"""
import re
import sys


def main(src_path: str, out_path: str) -> None:
    tex = open(src_path).read()

    numbers: dict[str, int] = {}
    counter = 0

    def process_equation(m: re.Match) -> str:
        nonlocal counter
        counter += 1
        body = m.group(1)

        def label_to_tag(lm: re.Match) -> str:
            numbers[lm.group(1)] = counter
            return rf"\tag{{{counter}}}"

        body = re.sub(r"\\label\{(eq:[^}]*)\}", label_to_tag, body)
        return rf"\[{body}\]"

    tex = re.sub(r"\\begin\{equation\}(.*?)\\end\{equation\}", process_equation,
                 tex, flags=re.DOTALL)

    def resolve_eqref(m: re.Match) -> str:
        key = m.group(1)
        if key not in numbers:
            raise SystemExit(f"_webtex.py: \\eqref{{{key}}} has no matching labeled equation")
        return f"({numbers[key]})"

    tex = re.sub(r"\\eqref\{(eq:[^}]*)\}", resolve_eqref, tex)

    open(out_path, "w").write(tex)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
