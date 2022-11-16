from pprint import pprint
from precise.skaters.portfolioutil.portcomparison import port_kurtosis
from precise.skaters.portfoliostatic.allstaticport import LONG_PORT
import numpy as np

# Comparing out-of-sample portfolio variance

if __name__=='__main__':
    ports = LONG_PORT
    anchor_cov = np.eye(40)
    moments = port_kurtosis(ports=ports, seed_cov=anchor_cov, max_time=5 * 60,
                            n_true=50, n_anchor=50, n_observed=50, metric='mean')
    pprint(moments)






