"""Post-publish smoke test: exercise the precise wheel installed from PyPI.

Run as ``python .github/smoke.py`` so that ``sys.path[0]`` is ``.github/`` (which has no ``precise``
package) — i.e. ``import precise`` resolves to the *installed* wheel, never the source tree. The
assertion below makes that guarantee explicit.
"""

import os

import numpy as np

import precise

ws = os.environ.get("GITHUB_WORKSPACE", "")
assert not precise.__file__.startswith(os.path.join(ws, "precise")), (
    f"imported the source tree, not the installed wheel: {precise.__file__}"
)
print("version:", precise.__version__, "| from", precise.__file__)

names = precise.estimator_names()
assert len(names) >= 10, names

rng = np.random.default_rng(0)
est = precise.EwaCovariance(r=0.05)
for _ in range(50):
    est.partial_fit(rng.standard_normal(4))
cov = est.covariance_
assert cov.shape == (4, 4)
assert np.all(np.linalg.eigvalsh(cov) > 0), "covariance_ is not positive definite"

top = precise.suggest(rng.standard_normal((80, 5)), top=2)
assert len(top) == 2

print(f"smoke OK: {precise.__version__} | {len(names)} estimators | suggest -> "
      f"{[c.__name__ for c in top]}")
