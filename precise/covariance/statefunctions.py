
# Functions that respect typical key conventions
#
# i.e.   f(**s) usually works where s is the state

import numpy as np


def ledoit_wolf()


def naive_ledoit_wolf_shrinkage(n_samples, pcov, p2cov):
    """
    :param n_samples:
    :param pcov:        Covariance of X
    :param p2cov:       Covariance of
    :return:
    """
    # From https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/covariance/tests/test_covariance.py
    # A simple implementation of the formulas from Ledoit & Wolf
    # The computation below achieves the following computations of the
    # "O. Ledoit and M. Wolf, A Well-Conditioned Estimator for
    # Large-Dimensional Covariance Matrices"
    # beta and delta are given in the beginning of section 3.2
    n_features = np.shape(pcov)[0]
    mu = np.trace(pcov) / n_features
    delta_ = pcov.copy()
    delta_.flat[:: n_features + 1] -= mu
    delta = (delta_ ** 2).sum() / n_features
    beta_ = 1.0 / (n_features * n_samples) * np.sum(p2cov - pcov ** 2)

    beta = min(beta_, delta)
    shrinkage = beta / delta
    return shrinkage




def oas(n_samples:int, pcov=None, scov=None, **ignore):
    """ Compute shrunk covariance matrix from empirical
    :param pcov:         Covariance matrix
    :return:             Shrunk cov matrix
    """
    # In sklearn this is bundled with emp cov estimation, so we have to cut and paste a few lines. See
    # https://github.com/scikit-learn/scikit-learn/blob/7e1e6d09b/sklearn/covariance/_shrunk_covariance.py#L347
    assert n_samples > 1, 'Need n_samples>1'
    if pcov is None:
        assert scov is not None, 'Need pcov or scov to be supplied'
        pcov =  (n_samples-1)/n_samples*scov

    n_dim = np.shape(pcov)[0]
    mu = np.trace(pcov) / n_dim
    alpha = np.mean(pcov ** 2)
    num = alpha + mu ** 2
    den = (n_samples + 1.0) * (alpha - (mu ** 2) / n_dim)
    shrinkage = 1.0 if den == 0 else min(num / den, 1.0)
    b = (1.0 - shrinkage) * pcov
    b.flat[:: n_dim + 1] += shrinkage * mu
    return b
