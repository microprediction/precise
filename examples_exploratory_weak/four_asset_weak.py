from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef, weaken_cov
from precise.skaters.locationutil.vectorfunctions import normalize
from precise.skaters.portfoliostatic.weakport import weak_long_port
from precise.skaters.portfoliostatic.unitport import unit_port
from precise.skaters.portfoliostatic.weakportfactory import _weak_from_cov
from precise.skaters.portfolioutil.portfunctions import portfolio_variance
import numpy as np
from pprint import pprint
from momentum.functions import var_init, var_update, kurtosis_init, kurtosis_update
from pprint import pprint
from precise.skaters.portfolioutil.portcomparison import port_kurtosis
from precise.skaters.portfoliostatic.allstaticport import LONG_PORT
from functools import partial, update_wrapper

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
    moments = port_kurtosis(ports=ports, cov=cov, n_draws=5000, n_true=50, n_anchor=50, n_observed=50,
                            metric='mean')







