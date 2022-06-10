
import math
from precise.skaters.locationutil.vectorfunctions import normalize
from functools import partial, update_wrapper


def buy_and_hold(mgr, j):
    """ Make a manager with frequency j
    :param mgr:
    :param j:
    :return:
    """
    mgr_j = partial(mgr,j=j)
    mgr_j = update_wrapper(mgr_j, mgr)
    mgr_j.__name__ = mgr.__name__+'_j'+str(j)
    return mgr_j





def buy_and_hold_manager_factory(mgr, j:int, y, s:dict, e=1000):
    """ Ignores manager preference except every j data points

         For this to make any sense, 'y' must be changes in log prices.
         For this to be efficient, the manager must respect the "e" convention. That is, the
                                    manager must do little work when e<0

    :param mgr:
    :param j:
    :param y:
    :param s:              State
    :param mgr_kwargs:
    :return:  w   Portfolio weights
    """
    if j==1:
        # Special case: just use the manager
        # This is the only time the user's e parameter is passed on.
        s_mgr = s['s_mgr']
        w, s_mgr = mgr(y=y,s=s_mgr, e=e)
        s['s_mgr'] = s_mgr
        return w, s
    else:
        if s.get('w') is None:
            # Initialization
            s['count']=0
            s_mgr = {}
            w, s_mgr = mgr(y=y,s=s_mgr, e=1000)
            s['s_mgr'] = s_mgr
            s['w'] = w
            return w, s
        else:
            s['count'] = s['count']+1
            if s['count'] % j == 0:
                # Sporadically use the manager
                s_mgr = s['s_mgr']
                w, s_mgr = mgr(y=y, s=s_mgr, e=1000)
                s['s_mgr'] = s_mgr
                s['w'] = w
                return w, s
            else:
                # Tell the manager not to worry too much about this data point, as the weights won't be used ...
                s_mgr = s['s_mgr']
                _ignore_w, s_mgr = mgr(y=y, s=s_mgr, e=-1)
                s['s_mgr'] = s_mgr
                # ... instead we let it ride
                w_prev = s['w']
                w = normalize( [ wi*math.exp(yi) for wi,yi in zip(w_prev,y)] )
                s['w'] = w
                return w, s
