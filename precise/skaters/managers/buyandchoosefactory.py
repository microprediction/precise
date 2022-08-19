
import math
from precise.skaters.locationutil.vectorfunctions import normalize
from copy import deepcopy
import numpy as np


def index_of_closest(w, ws):
    l1s = [ sum(abs(np.array(w)-np.array(wsi))) for wsi in ws ]
    return l1s.index(min(l1s))


def buy_and_choose_manager_factory(mgr, j:int, y, s:dict, e=1000, q=1.0, n_seed=5):
    """ Every j data points, call mgr repeatedly with identical state then most q towards closest weights
        This won't have any effect on purely deterministic managers, except to slow them down
        However stochastic managers might benefit, as might others who anticipate an obscure
        convention: namely the receipt of a 'choose_hint' field in the state

         For this to make any sense, 'y' must be changes in log prices.
         For this to be efficient, the manager must respect the "e" convention. That is, the
                                    manager must do little work when e<0

    :param mgr:
    :param j:
    :param y:
    :param s:              State
    :param q:              New portfolio is  q*w + (1-q)*w_prev
    :param n_seed          Number of times to call the manager repeatedly with (almost) the same state
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
            # Sporadically use the manager repeatedly.

            w_prev = s['w']
            w_roll = normalize([wi * math.exp(yi) for wi, yi in zip(w_prev, y)])

            w_mgrs = list()
            for l in n_seed:
                s_mgr = deepcopy(s['s_mgr'])

                # Drop a hint to the manager, just in case it is alert
                # to this obscure convention. If by chance these fields
                # already exist, don't clobber
                if '_seed' in s_mgr or '_seed_max' in s_mgr:
                    raise ValueError('Warning: managers uses a _seed field so is not compatible with buy_and_choose_manager_factory')
                else:
                    s_mgr['_seed'] = l
                    s_mgr['_seed_max'] = n_seed - 1

                w_mgr, s_mgr = mgr(y=y, s=s_mgr, e=1000)
                w_mgrs.append(w_mgr)
            # Use the last call to set new manager state.
            s['s_mgr'] = s_mgr

            # Now select the closest weights in L1-norm to the current portfolio
            pos = index_of_closest(w_roll,w_mgrs)
            w_mgr = w_mgrs[pos]

            # Then move towards it.
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


