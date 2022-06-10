from precise.skaters.portfoliostatic.equalport import equal_long_port
from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef
import numpy as np
import math
from precise.skaters.locationutil.vectorfunctions import normalize


def _buy_and_hold_port(port, j:int, y, s:dict, cov, port_kwargs):
    """

         Sporadically calls port() but uses buy and hold in between.
         For this to work, 'y' must be changes in log prices.

    :param port:
    :param j:
    :param y:
    :param s:
    :param cov:
    :param port_kwargs:
    :return:  w   Portfolio weights
    """
    if j==1:
        return port(cov=cov, **port_kwargs)
    else:
        n_dim = len(y)
        if s.get('w') is None:
            s['multiplier']=[1 for _ in range(n_dim)]
            s['count']=0
            s['w'] = port(cov=cov, **port_kwargs)
            return s['w']
        else:
            s['count'] = s['count']+1
            if s['count'] % j == 0:
                s['multiplier'] = [1 for _ in range(n_dim)]
                s['w'] = port(cov=cov, **port_kwargs)
                return s['w']
            else:
                s['multiplier'] = [ mi*math.exp(yi) for mi,yi in zip(s['multiplier'],y)]
                w = normalize( [ wi*mi for wi,mi in zip(s['w'],s['multiplier']) ] )
                return w


def static_cov_manager_factory_d0(y, s, f, port, e=1, f_kwargs:dict=None, port_kwargs:dict=None, n_cold=5, zeta=0.0, j=1):
    """
       Basic manager pattern ignoring mean.
       Expects to receive changes in log(price).
       If you have opinions on means, you'll have to incorporate them into variance somehow
       via the covariance skater. 

          :param f     cov skater ("d0")
          :param port  portfolio constructor
          :param zeta  Compromise between cov and corr portfolio (zeta=0, use cov only)
          :param j     How often to run the static portfolio construction.
                       (Warning: if j>1 this will be nonsense unless 'y' represents changes in log prices)

       :returns w, s
    """

    if f_kwargs is None:
        f_kwargs = {}
    if port_kwargs is None:
        port_kwargs = {}
    if not s:
        s = {'f_state':{},
             'port_state':{},
             'count':0,
             'hodl_state':{}}


    x_mean, x_cov, s['f_state'] = f(y=y,s=s['f_state'], k=1, e=e, **f_kwargs)
    s['count']+=1
    if s['count']>=n_cold and (e>0):
        s_hodl = s['hodl_state']
        w = _buy_and_hold_port(port=port, y=y, j=j, s=s_hodl, cov=x_cov, port_kwargs=port_kwargs)
        if zeta is not None and (zeta>0):
            x_diag = np.diag(x_cov)
            x_corr = cov_to_corrcoef(x_cov)
            w_corr_raw = port(cov=x_corr, **port_kwargs)
            w_corr = normalize(w_corr_raw/x_diag)
            w = (1-zeta)*w + zeta*w_corr
    else:
        w = equal_long_port(cov=x_cov)
    return w, s



