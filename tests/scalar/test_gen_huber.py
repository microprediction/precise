
from precise.skaters.vectorutil.hubermean import parallel_bisection_root_finder, huber_deriv
import numpy as np


def test_root_finder():
    n_vars = 5
    n_samples = 500
    xs = np.random.randn(n_samples ,n_vars)
    a = 1.0
    b = 1.5
    x_median = np.median(xs ,axis=0)
    x_mean = np.mean(xs ,axis=0)
    lb = np.where( x_median < x_mean, x_median, x_mean )
    ub = np.where( x_median > x_mean, x_median, x_mean)
    xStar, fraction = parallel_bisection_root_finder(f=huber_deriv, lb=lb, ub=ub, a=a, b=b, xs=xs)
    print( (xStar, fraction))

if __name__=='__main__':
    test_root_finder()