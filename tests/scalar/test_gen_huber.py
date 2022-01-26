
from precise.skaters.locationutil.hubermean import huber_mean
import numpy as np


def test_huber_mean():
    n_vars = 5
    n_samples = 50
    xs = np.random.randn(n_samples ,n_vars)
    a = 1.0
    b = 1.5
    x_median = np.median(xs ,axis=0)
    x_mean = np.mean(xs ,axis=0)
    mu = huber_mean(xs=xs)
    ratios = (mu-x_median)/(x_mean-x_median)
    return ratios


if __name__=='__main__':
    print(test_huber_mean())