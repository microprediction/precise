
# Functions that respect typical key conventions
#
# i.e.   f(**s) usually works where s is the state

import numpy as np


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
