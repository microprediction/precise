from precise.skaters.portfoliostatic.equalport import equal_long_port
from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef
import numpy as np
import math
from precise.skaters.locationutil.vectorfunctions import normalize



def index_of_closest(w, ws):
    l1s = [ sum(abs(np.array(w)-np.array(wsi))) for wsi in ws ]
    return l1s.index(min(l1s))


def _buy_and_hold_and_choose_port(port, j:int, q:float, l:int, y, s:dict, cov, port_kwargs):
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
    n_dim = len(y)
    if s.get('w') is None:
        s['multiplier'] = [1 for _ in range(n_dim)]
        s['count'] = 0
        w = port(cov=cov, **port_kwargs)
        s['w'] = [ wi for wi in w ]
        return w, s
    else:
        s['count'] = s['count']+1
        if s['count'] % j == 0:
            # Compute roll forward weights
            s['multiplier'] = [mi * math.exp(yi) for mi, yi in zip(s['multiplier'], y)]
            w_roll = normalize([wi * mi for wi, mi in zip(s['w'], s['multiplier'])])

            # Run the portfolio optimizer a few times and pick portfolio closest to prior
            if l is None:
                w_port = port(cov=cov, **port_kwargs)
            else:
                w_ports = [ port(cov=cov, **port_kwargs) for _ in range(l) ]
                choice = index_of_closest(w_roll, w_ports)
                w_port = list(w_ports[choice])

            # Create a compromise between the roll forward portfolio and what the optimizer wants
            w = [q * wi + (1 - q) * wpi for wi, wpi in zip(w_port, w_roll)]
            s['w'] = [wi for wi in w]
            s['multiplier'] = [1 for _ in range(n_dim)]
            return w, s
        else:
            # Let it ride
            s['multiplier'] = [ mi*math.exp(yi) for mi,yi in zip(s['multiplier'],y)]
            w = normalize( [ wi*mi for wi,mi in zip(s['w'],s['multiplier']) ] )
            return w, s


def static_cov_manager_factory_d0(y, s, f, port, e=1, f_kwargs:dict=None, port_kwargs:dict=None, n_cold=5, zeta=0.0, j=1,q=1.0, l=None):
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
          :param l     How many times to run the static portfolio construction

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
             'account_state':{}}

    
    x_mean, x_cov, s['f_state'] = f(y=y,s=s['f_state'], k=1, e=e, **f_kwargs)
    s['count']+=1
    if s['count']>=n_cold and (e>0):
        s_account = s['account_state']
        w, s_account = _buy_and_hold_and_choose_port(port=port, y=y, j=j, q=q, l=l, s=s_account, cov=x_cov, port_kwargs=port_kwargs)
        s['account_state'] = s_account
        if zeta is not None and (zeta>0):
            # Drags towards the portfolio determined by cov
            # FIXME: This should be moved inside _buy_and_hold_and_choose_port
            x_diag = np.diag(x_cov)
            x_corr = cov_to_corrcoef(x_cov)
            w_corr_raw = port(cov=x_corr, **port_kwargs)
            w_corr = normalize(w_corr_raw/x_diag)
            w = (1-zeta)*w + zeta*w_corr
    else:
        w = equal_long_port(cov=x_cov)
    return w, s



