import numpy as np
import pandas as pd
from precise.skaters.covarianceutil.covfunctions import try_invert
from precise.skaters.covarianceutil.pdutil import dict_or_series_to_scalar, square_and_vector_to_scalar, vector_to_vector
from precise.skaters.locationutil.vectorfunctions import normalize

# Some common operations and functionals of portfolios
# Here the portfolio w can be a list, ndarray, dict or Series


def positive_mass(w):
    if isinstance(w,(dict,pd.Series)):
        return dict_or_series_to_scalar(d=w, func=positive_mass )
    else:
        return sum([wi for wi in w if wi>0])


def negative_mass(w):
    if isinstance(w, (dict, pd.Series)):
        return dict_or_series_to_scalar(d=w, func=negative_mass)
    else:
        return sum([-wi for wi in w if wi<0])


def relative_negative_mass(w):
    if isinstance(w, (dict, pd.Series)):
        return dict_or_series_to_scalar(d=w, func=relative_negative_mass)
    else:
        pm = positive_mass(w)
        nm = negative_mass(w)
        return nm/(pm-nm)


def portfolio_variance(w, cov=None, pre=None):
    if cov is None:
        cov = try_invert(a=pre)
    if isinstance(cov,pd.DataFrame):
        return square_and_vector_to_scalar(a=cov, w=w, func=portfolio_variance)
    else:
        w1 = np.atleast_2d(w)
        wt = np.atleast_2d(w).transpose()
        return np.matmul( np.matmul(w1, np.array(cov)), wt)[0][0]


def normalize_portfolio(w):
    """ Ensure sum(w) = 1 """
    if isinstance(w,(dict,pd.Series)):
        return vector_to_vector(w=w, func=normalize)
    else:
        return normalize(w)


def exclude_negative_weights(w, with_neg_mass=False):
    """
         Take out negative weights, preserving presumed total mass
         :param w   1d array, list, Series or dict
    """
    if isinstance(w,(dict,pd.Series)):
        assert with_neg_mass==False
        return vector_to_vector(w=w, func=exclude_negative_weights, with_neg_mass=False)
    else:
        pos_mass = sum([wi for wi in w if wi>0])
        neg_mass = sum([-wi for wi in w if wi<0])
        if neg_mass>1e-10:
            presumed_mass = pos_mass-neg_mass
            ratio = presumed_mass/pos_mass
            w_pos = np.array([ wi*ratio if wi>0 else 0.0 for wi in w])
        else:
            w_pos = np.array( [ wi/pos_mass for wi in w] )
        return (w_pos, neg_mass) if with_neg_mass else w_pos


def var_scaled_returns(cov, mu:float, r:float, noise=0.01):
    """ Set returns as function of variance.
        Plenty of quibbles here.
    :param cov:
    :param mu:
    :param r:
    :param noise:
    :return:
    """
    import warnings
    warnings.filterwarnings('error')
    vars = np.diag(cov)
    typical_var = np.mean(vars)

    try:
        result = r+(mu-r)*np.array([ v/typical_var*(1+np.random.rand()*noise) for v in vars])
    except RuntimeWarning as e:
        print(e)
        pass

    return result


# Some portfolio features


def herfandahl(w):
    # There's a name for everything!
    # Related to https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_index
    return np.linalg.norm(w)


def relative_herfandahl(w):
    n = len(w)
    if n==1:
        return 1
    else:
        H = np.linalg.norm(w)
        return (H-1/n)/(1-1/n)


def std_herfandal(w):
    from scipy.stats import invgauss
    r = relative_herfandahl(w)
    if r > (1-1e-8):
        return 10.
    if r < 1e-8:
        return -10.0
    return invgauss(r)



if __name__=='__main__':
    sgma = np.array([[1,4],[4,20]])
    w = [0.3,0.4]
    print( portfolio_variance(cov=sgma,w=w) )