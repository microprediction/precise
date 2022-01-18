
from precise.scalar.generalizedhuber import parallel_root_finder, huber_deriv
import numpy as np


def test_root_finder():
    n_vars = 5
    n_samples = 500
    x = np.random.randn(n_samples ,n_vars)
    a = 1.0
    b = 1.5
    x_median = np.median(x ,axis=0)
    x_mean = np.mean(x ,axis=0)
    lb = np.where( x_median < x_mean, x_median, x_mean )
    ub = np.where( x_median > x_mean, x_median, x_mean)
    xStar = parallel_root_finder(f=huber_deriv, lb=lb ,ub=ub, a=a, b=b, x=x)
    print(xStar)