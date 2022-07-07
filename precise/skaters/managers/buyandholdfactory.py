
import math
from precise.skaters.locationutil.vectorfunctions import normalize
from functools import partial, update_wrapper


def buy_and_hold(mgr, j, q=1.0):
    """ Make a manager with frequency j
    :param mgr:
    :param j:
    :return:
    """
    mgr_j_q = partial(mgr,j=j, q=q)
    mgr_j_q = update_wrapper(mgr_j_q, mgr)
    mgr_j_q.__name__ = mgr.__name__+'_j'+str(j)+'_q'+str(int(100*q)).zfill(3)
    return mgr_j_q



def buy_and_hold_manager_factory(mgr, j:int, y, s:dict, e=1000, q=1.0):
    """ Ignores manager preference except every j data points

         For this to make any sense, 'y' must be changes in log prices.
         For this to be efficient, the manager must respect the "e" convention. That is, the
                                    manager must do little work when e<0

    :param mgr:
    :param j:
    :param y:
    :param s:              State
    :param q:              New portfolio is  q*w + (1-q)*w_prev
    :param mgr_kwargs:
    :return:  w   Portfolio weights
    """
    if s.get('w') is None:
        # Initialization
        s['count'] = 0
        s_mgr = {}
        w, s_mgr = mgr(y=y, s=s_mgr, e=1000)
        s['s_mgr'] = s_mgr
        s['w'] = w
        return w, s
    else:
        s['count'] = s['count']+1
        if s['count'] % j == 0:
            # Sporadically use the manager
            s_mgr = s['s_mgr']
            w_mgr, s_mgr = mgr(y=y, s=s_mgr, e=1000)
            s['s_mgr'] = s_mgr
            w_prev = s['w']
            w_roll = normalize([wi * math.exp(yi) for wi, yi in zip(w_prev, y)])
            w = [ wi*q + (1-q)*wpi for wi, wpi in zip(w_mgr, w_roll) ]
            s['w'] = [wi for wi in w]
            return w, s
        else:
            # Tell the manager not to worry too much about this data point, as the weights won't be used ...
            s_mgr = s['s_mgr']
            _ignore_w, s_mgr = mgr(y=y, s=s_mgr, e=-1)
            s['s_mgr'] = s_mgr
            # ... instead we let it ride
            w_prev = s['w']
            w = normalize( [ wi*math.exp(yi) for wi,yi in zip(w_prev,y)] )
            s['w'] = [wi for wi in w]
            return w, s


