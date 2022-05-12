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




def weaker_port(cov, b=0.976):
    dcov = np.diag(np.diag(cov))
    off_diag_cov = cov - dcov
    weak_cov = b * off_diag_cov + dcov
    return unit_port(weak_cov)


if __name__=='__main__':
    # Make some weak ports
    bs = np.linspace(0.0,1.0,21)
    ports = []
    for b in bs:
        port = partial(weaker_port, b=b)
        setattr(port, '__name__', 'weak_'+str(b))
        ports.append(port)

    # Test them out of sample
    n_dim = 10
    anchor_cov = np.eye(n_dim)
    moments = port_kurtosis(ports=ports, cov=anchor_cov, n_draws=50000, n_true=50, n_anchor=50, n_observed=50, metric='mean')







