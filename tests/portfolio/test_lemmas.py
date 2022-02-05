import numpy as np
from precise.skaters.portfolioutil.unitlemmas import quirky_solve


def test_lemmas():
    A = np.cov(np.random.randn(500,10),rowvar=False)
    b = np.random.randn(10)
    x1 = np.linalg.solve(A,b)
    x2 = quirky_solve(A=A, b=b)
    assert np.allclose(x1,x2)