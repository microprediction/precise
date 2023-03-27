from precise.skaters.portfoliostatic.unitport import unit_port
import numpy as np
from precise.skatervaluation.portfoliocomparisonutil.portcomparison import port_kurtosis

# A small example intended to illustrate why cov weakening can sometimes serve
# one well out of sample


cov = np.array([[ 1.09948514, -1.02926114,  0.22402055,  0.10727343],
       [-1.02926114,  2.54302628,  1.05338531, -0.12481515],
       [ 0.22402055,  1.05338531,  1.79162765, -0.78962956],
       [ 0.10727343, -0.12481515, -0.78962956,  0.86316527]])


if __name__=='__main__':
    w = unit_port(cov=cov)
    print(w)
    ports = [ unit_port ]
    moments = port_kurtosis(ports=ports, seed_cov=cov, max_time=60 * 60, n_true=50,
                            n_anchor=50, n_observed=50, metric='mean')







