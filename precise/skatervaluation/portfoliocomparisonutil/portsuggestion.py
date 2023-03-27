from precise.skatervaluation.portfoliocomparisonutil.portcomparison import port_sample_var
from precise.skaters.portfoliostatic.allstaticport import PORT
from precise.skaters.covarianceutil.covrandom import random_factor_cov
from pprint import pprint


def suggest_port_using_sample_cov(n_dim=None, cov=None, n_anchor=1000, n_observed=1000, n_true=100, max_time=30 * 60):
    """ Produces a list of suggested static portfolio functions based on sampled true and obs cov
    :param n_dim:    Dimension of problem
    :param cov:      Anchor cov that is 'typical' in some sense
    :return: leaderboard in increasing order
    """
    if cov is None:
        cov = random_factor_cov(n_dim=n_dim)
    return port_sample_var(ports=PORT, max_time=max_time, cov=cov, n_anchor=n_anchor,
                           n_observed=n_observed, n_true=n_true, show_progress=True)



if __name__=='__main__':
    suggestions = suggest_port_using_sample_cov(n_dim=5)
    pprint(suggestions)