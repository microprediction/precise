from precise.skaters.portfoliostatic.unitport import unit_port
import numpy as np
from precise.skatervaluation.portfoliocomparisonutil.portcomparison import port_kurtosis
from functools import partial


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
    max_time = 10*60
    moments = port_kurtosis(ports=ports, seed_cov=anchor_cov, max_time=max_time,
                            n_true=50, n_anchor=50, n_observed=50, metric='mean')







