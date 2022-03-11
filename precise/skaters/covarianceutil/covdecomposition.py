import numpy as np


def diagonalize(cov):
    """ Returns D, P s.t.  P^T D P = cov
       :param cov:
       :return:
    """
    from precise.skaters.covarianceutil.covfunctions import nearest_pos_def
    pos_def_cov = nearest_pos_def(cov)
    (d, P) = np.linalg.eigh(pos_def_cov)
    D = np.diag(d)
    cov_check = np.dot(np.dot(P,D),P.transpose())
    assert np.allclose(pos_def_cov, cov_check)
    return D, P.transpose()


def random_w(n_dim,n_obs):
    w_raw = np.random.randn(n_obs,n_dim)
    w_norms = np.linalg.norm(w_raw, axis=1)
    w_norms_tile = np.tile(np.reshape(w_norms, newshape=(n_obs, 1)), n_dim)
    w_norm = w_raw/w_norms_tile
    return w_norm


def random_portfolio_vars(cov, n_obs)->[float]:
    """
         Generate random portfolios
         Report sequence of portfolio variances
    """
    D, P = diagonalize(cov=cov)
    n_dim = np.shape(cov)[0]
    ws = random_w(n_dim=n_dim, n_obs=n_obs).transpose()
    v = np.dot(P,ws)
    vv = v * v
    d = np.diag(D)
    dRep = np.tile(np.atleast_2d(d).transpose(),reps=n_obs)
    dvv = vv*dRep
    return np.sum(dvv,axis=0)


def random_portfolio_features(cov, n_obs):
    """ Quantities that may or may not help delineate relative success
    :param cov:
    :param n_obs:
    :return:
    """
    vs = random_portfolio_vars(cov=cov, n_obs=n_obs)
    f0 = np.quantile(vs,0.001) / min(vs)
    f1 = np.quantile(vs,0.01) / np.quantile(vs,0.001)
    f2 = np.quantile(vs,0.1) / np.quantile(vs,0.01)
    f3 = np.quantile(vs,0.5) / np.quantile(vs, 0.1)
    f4 = np.quantile(vs,0.99) / np.quantile(vs, 0.5)
    f5 = np.quantile(vs,0.999) / np.quantile(vs, 0.99)
    f6 = np.max(vs) / np.quantile(vs, 0.999)
    return np.log( [ f0, f1, f2, f3, f4, f5, f6  ])

RANDOM_PORTFOLIO_FEATURE_NAMES = ['f'+str(i) for i in range(7) ]


if __name__=='__main__':
    from precise.skaters.covarianceutil.covrandom import random_factor_cov
    n_dim = 10
    n_obs = 1557
    cov1 = random_factor_cov(n_dim=n_dim)
    vs1 = random_portfolio_vars(cov=cov1, n_obs=n_obs)
    cov2 = np.eye(n_dim) + 0.1*random_factor_cov(n_dim=n_dim)
    vs2 = random_portfolio_vars(cov=cov2, n_obs=n_obs)
    import matplotlib.pyplot as plt
    plt.hist(vs1,bins=100)
    plt.hist(vs2,bins=100)
    plt.legend(['cov 1','cov 2'])
    plt.show()



