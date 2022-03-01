from precise.skaters.portfoliostatic.equalport import equal_long_port
from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef
import numpy as np
from precise.skaters.locationutil.vectorfunctions import normalize


def static_cov_manager_factory_d0(y, s, f, port, e=1, f_kwargs:dict=None, port_kwargs:dict=None, n_cold=5, zeta=0.0):
    """
       Basic manager pattern ignoring mean.
       Expects to receive changes in log(price).
       If you have opinions on means, you'll have to incorporate them into variance somehow
       via the covariance skater. 

          :param f     cov skater ("d0")
          :param port  portfolio constructor
          :param zeta  Compromise between cov and corr portfolio (zeta=0, use cov only)

       :returns w, s
    """

    if f_kwargs is None:
        f_kwargs = {}
    if port_kwargs is None:
        port_kwargs = {}
    if not s:
        s = {'f_state':{},
             'port_state':{},
             'count':0}

    x_mean, x_cov, s['f_state'] = f(y=y,s=s['f_state'], k=1, e=e, **f_kwargs)
    s['count']+=1
    if s['count']>=n_cold and (e>0):
        w = port(cov=x_cov, **port_kwargs)
        if zeta>0:
            x_diag = np.diag(x_cov)
            x_corr = cov_to_corrcoef(x_cov)
            w_corr_raw = port(cov=x_corr, **port_kwargs)
            w_corr = normalize(w_corr_raw/x_diag)
            w = (1-zeta)*w + zeta*w_corr
    else:
        w = equal_long_port(cov=x_cov)
    return w, s



