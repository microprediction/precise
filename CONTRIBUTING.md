# Contributing to precise

Thanks for taking an interest. `precise` is a small, numpy-only library of online covariance
estimators, assessors and a recommender. Bug reports, questions, fixes and new estimators are all
welcome. This file says how to get help, how to report a problem, and how to change the code.

Everyone taking part is expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting support

- **Questions about using precise:** open a
  [GitHub issue](https://github.com/microprediction/precise/issues). Questions are welcome there;
  you do not need to have found a bug. The [documentation](https://precise.microprediction.org)
  and the README examples are the first place to look.
- **Who answers:** the maintainer, Peter Cotton, reads every issue. Support is best effort: there
  is no guaranteed response time, but bugs that give silently wrong results are treated as the top
  priority.
- **Private matters** (a conduct report, or a security problem you would rather not post
  publicly): email peter.cotton@microprediction.com.

## Governance

precise is maintained by one person, Peter Cotton, who reviews and merges pull requests and makes
releases. Decisions about scope and design are discussed in the open, on issues and pull requests,
before they are made. Anyone whose contributions are substantial and sustained can ask to become a
co-maintainer.

## Reporting a bug

Open an issue and include:

1. what you ran: a short, self-contained script, ideally with a fixed random seed;
2. what you expected, and what happened instead (the full traceback, or the numbers that are
   wrong);
3. versions: `python -c "import precise, numpy, sys; print(precise.__version__, numpy.__version__, sys.version)"`,
   and your operating system.

A result that is numerically wrong but raises no error is a bug, and the most important kind.
Please report it even if you are not sure.

## Proposing a change

- **Small fixes** (typos, documentation, an obvious bug): open a pull request directly.
- **New estimators, assessors or changes to the public API:** open an issue first, so the design
  can be agreed before you write the code. Say which paper or method the estimator implements, and
  how its output can be checked (a batch reference implementation, a known limit, an invariance).
  precise aims to ship established, citable methods; novel ones are marked experimental.
- Every pull request should:
  - target `main`, and keep to one topic;
  - add or update tests, so the change is exercised by `pytest`;
  - pass the checks below;
  - add a line under an "Unreleased" heading in [CHANGELOG.md](CHANGELOG.md) if users would
    notice the change.

### Adding an estimator

An estimator subclasses `BaseOnlineCovariance` (in `precise/base.py`) and implements
`_init_state(n_dim)` and `_update_state(state, x)`; expensive work belongs in `_state_to_cov`,
which runs only when `covariance_` is read. State must be a plain dict of arrays and scalars, so
that `get_state()` / `set_state()` work. Register the class in `precise/registry.py` and export it
from `precise/__init__.py`. The parametrized contract tests in `tests/test_estimators.py` then run
against it automatically.

## Development setup

You need Python 3.9 or later and git.

```bash
git clone https://github.com/microprediction/precise.git
cd precise
python -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

The `dev` extra installs pytest, pytest-cov, ruff and mypy, among other tools, plus pandas and
scikit-learn, which only the tests use (to compare against). The package itself needs only numpy.

Optionally, install the pre-commit hooks, which run ruff and some whitespace checks on each commit:

```bash
pip install pre-commit
pre-commit install
```

## Running the checks

CI runs all of these on every pull request; please run them before pushing.

```bash
pytest                              # the full test suite (a minute or two)
pytest --cov=precise                # the same, with a coverage report
ruff check precise tests research   # lint
mypy precise                        # type check
```

CI also:

- runs the tests on Python 3.9, 3.11, 3.12 and 3.13;
- runs them again with numpy as the only dependency, to keep the lean install working;
- fails if line coverage of `precise/` falls below 95%;
- checks the repository out on Windows, and fails if any tracked file name is one Windows cannot
  hold (`tests/test_repo_paths.py`);
- checks that the HTML versions of the papers under `docs/papers/` match their LaTeX sources. If
  you edit a `.tex` file in `papers/`, run `./docs/build_paper.sh` (it needs pandoc) and commit the
  result.

Code style is enforced by `ruff check` (line length 100; see `pyproject.toml`). `ruff format` is
applied to changed files by the pre-commit hook. Docstrings use the Sphinx `:param:` style.

The `research/` directory holds benchmark and reproduction scripts. It is not shipped in the
package, but it is linted, and several of its scripts are exercised by tests.
`research/legacy_skatervaluation/` is preserved pre-1.0 code and is not maintained.

## Releasing (maintainer)

1. Update `version` in `pyproject.toml` and move the "Unreleased" entries in `CHANGELOG.md` under
   the new version and date.
2. Merge to `main` and wait for CI to pass.
3. Create a GitHub release with tag `vX.Y.Z` matching the version.

Publishing the release runs `.github/workflows/publish.yml`. It refuses to publish if the tag and
the version differ, builds the sdist and wheel, test-installs the wheel, and uploads to PyPI by
trusted publishing. `install-smoke.yml` then installs the new release from PyPI on Linux, macOS
and Windows and exercises it.

## AI assistance

Much of the 1.x code was written with AI coding assistants under the maintainer's direction; see
[AI_USE.md](AI_USE.md). Contributions made with AI help are welcome on the same terms as any other:
you are responsible for the change, it must come with tests, and please say in the pull request
that you used an assistant.
