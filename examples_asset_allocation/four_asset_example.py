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

cov = np.array([[ 1.09948514, -1.02926114,  0.22402055,  0.10727343],
       [-1.02926114,  2.54302628,  1.05338531, -0.12481515],
       [ 0.22402055,  1.05338531,  1.79162765, -0.78962956],
       [ 0.10727343, -0.12481515, -0.78962956,  0.86316527]])


def weaker_port(cov, b=0.976):
    dcov = np.diag(np.diag(cov))
    off_diag_cov = cov - dcov
    weak_cov = 0.9 * off_diag_cov + dcov
    return unit_port(weak_cov)


if __name__=='__main__':
    ports = LONG_PORT
    anchor_cov = np.eye(40)
    moments = port_kurtosis(ports=ports, cov=anchor_cov, n_draws=50, n_true=50, metric='mean')
    pprint(moments)






