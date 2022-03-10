from precise.skaters.portfolioutil.portcomparison import port_sample_var
from precise.skaters.portfoliostatic.allstaticport import PORT
from precise.skaters.covarianceutil.covrandom import random_factor_cov
import numpy as np
from pprint import pprint


def sample_var_suggestions(n_dim=None, cov=None,  n_anchor=1000, n_observed=1000, n_true=100, n_draws=5):
    """ Produces a list of suggested static portfolio functions based on sampled true and obs cov
    :param n_dim:    Dimension of problem
    :param cov:      Anchor cov that is 'typical' in some sense
    :return: leaderboard in increasing order
    """
    if cov is None:
        cov = random_factor_cov(n_dim=n_dim)
    return port_sample_var(ports=PORT, n_draws=n_draws, cov=cov, n_anchor=n_anchor,
                           n_observed=n_observed, n_true=n_true, show_progress=True)



if __name__=='__main__':
    suggestions = sample_var_suggestions(n_dim=5, n_draws=1, n_samples=60)
    pprint(suggestions)