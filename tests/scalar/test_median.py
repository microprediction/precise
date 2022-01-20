import numpy as np
import random
from precise.skaters.scalarutil.runningmedian import med


def test_running_median():
    xs = np.random.randn(random.choice([1, 5, 10, 1000]))
    s = {}
    for x in xs:
        s = med(s=s, x=x)
    assert s['median'] == np.median(xs)