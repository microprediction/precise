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

# Comparing out-of-sample portfolio variance

if __name__=='__main__':
    ports = LONG_PORT
    anchor_cov = np.eye(40)
    moments = port_kurtosis(ports=ports, cov=anchor_cov, n_draws=500, n_true=50, n_anchor=50, n_observed=50, metric='mean')
    pprint(moments)






