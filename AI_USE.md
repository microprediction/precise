# Use of generative AI in precise

This file records how generative AI was used to write `precise`, and how the result is checked.
The figures come from the git history of `main` on 2026-10-05, before this file was added, and can
be recomputed with the commands at the end.

## What was used, and for what

- **Before June 2026** (the 0.x releases, December 2021 to October 2025): 958 commits, none of
  which records an AI co-author.
- **The 1.x rewrite and since** (from June 2026; 1.0.0 was released on 2026-06-05): 99 of the 103
  commits to `main` carry a `Co-Authored-By: Claude` trailer. The work was done with
  [Claude Code](https://claude.com/claude-code), Anthropic's coding assistant, using the models
  named in those trailers: Claude Opus 4.8 (81 commits), Claude Opus 5 (11), Claude Fable 5 (5)
  and Claude Opus 5.5 (2).
- **Share of the code:** about 97% of the lines now in `precise/` were last changed by one of those
  commits (`git blame`).

The assistant wrote most of the 1.x package code, the tests, the reproduction scripts in
`research/`, much of the documentation, and drafts of the papers in `papers/`, including the JOSS
paper. It was used for code generation, refactoring, test writing, debugging, auditing existing
code for errors, and drafting and editing prose.

The author, Peter Cotton, directed that work: he chose what the package should do and which
published methods to implement, set the design (the `partial_fit` contract, state as a plain
dictionary, lazy spectral work, numpy as the only dependency), and reviewed, edited and validated
the output before it was merged. He is responsible for the package and everything in this
repository.

`SKILL.md` and `.claude/skills/` are something else: instructions that help AI agents *use* precise
correctly. They are documentation for users' assistants, not a record of how the package was
written.

## How the output is checked

Code is not accepted because an assistant produced it, or because it looks right. It has to pass
checks that do not depend on the assistant's own view of what the code should do:

- **Tests** (`tests/`, run in CI on Python 3.9, 3.11, 3.12 and 3.13, and again with numpy alone):
  - a contract test run against every registered estimator: symmetry, positive semidefiniteness,
    unit-diagonal correlation, finite scores;
  - agreement between batch `fit` and repeated `partial_fit`, and exact restoration of state
    after a `get_state()` / `set_state()` round trip;
  - comparisons with independent references: `numpy.cov` on the same data, an explicit
    recomputation over a rolling window, the analytic Gaussian log-likelihood;
  - properties the theory requires, derived from the cited papers rather than from the code:
    nonlinear shrinkage vanishing as the sample grows, staying invertible when variables
    outnumber observations, estimates that do not depend on the units of the data.
- **Coverage:** CI fails if line coverage of `precise/` falls below 95%.
- **Lint and types:** `ruff` and `mypy` run in CI.
- **Reproduction scripts:** the numbers quoted in the papers come from scripts in `research/`, so
  they can be rerun rather than taken on trust.
- **Audits:** the code has been reviewed for silent numerical errors; findings are filed as GitHub
  issues and fixed with a test that would have caught them.

Several drafts were rejected or corrected when these checks failed. Some known defects are still
open; they are listed in the [issue tracker](https://github.com/microprediction/precise/issues).

Parts of the package implement new methods rather than published ones: the Schur estimators, the
Schur pseudo-likelihood assessor and the `suggest()` recommender. Those are marked experimental in
their documentation.

## Contributions

Contributions made with AI help are welcome on the same terms as any other; see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Recomputing the figures

```bash
git log main --no-merges --until=2026-06-01 --oneline | wc -l
git log main --no-merges --since=2026-06-01 --oneline | wc -l
git log main --no-merges --since=2026-06-01 --format='%(trailers:key=Co-Authored-By,valueonly)' \
  | grep -v '^$' | sort | uniq -c
```
