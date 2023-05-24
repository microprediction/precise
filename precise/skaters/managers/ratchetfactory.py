
import math
from precise.skaters.locationutil.vectorfunctions import normalize
from copy import deepcopy
import numpy as np


def index_of_closest(w, ws):
    l1s = [ sum(abs(np.array(w)-np.array(wsi))) for wsi in ws ]
    return l1s.index(min(l1s))


def ratchet_manager_factory(mgr, y, s:dict, e=-1, j:int=1000000, q=0.8, vup=1.1, vdn=0.85):
    """

        Sets a new target weight when either s['count'] % j = 0 or e>0
        Otherwise, we use the stale target and ratchet towards it.

        For this to make any sense, 'y' must be changes in log prices.
        The manager must respect the "e" convention. That is, the
                                    manager must do little work when e<0

    :param mgr:            Any "manager"
    :param y:
    :param s:              State
    :param e:              If e>0 is send, this will be passed to the manager and we assume a full update
    :param j:
    :param q:              New portfolio is  q*w + (1-q)*w_prev
    :param vup:            Upper multiplier of target weights
    :param vdn:            Lower multiplier of target weights
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
        if (s['count'] % j == 0) or (e>0):
            # Sporadically use the manager to change the target weights
            s_mgr = s['s_mgr']
            s['w_target'] = mgr(y=y, s=s_mgr, e=e)

            # Buy and hold
            w_prev = s['w']
            w_roll = normalize([wi * math.exp(yi) for wi, yi in zip(w_prev, y)])

            # Use the last call to set new manager state.
            s['s_mgr'] = s_mgr

            # Then move towards target
            w = [ wi*q + (1-q)*wpi for wi, wpi in zip(s['w_target'], w_roll) ]
            s['w'] = [wi for wi in w]
            return w, s
        else:
            # Tell the manager not to worry too much about this data point, as the weights won't be used
            s_mgr = s['s_mgr']
            _ignore_w, s_mgr = mgr(y=y, s=s_mgr, e=e)
            s['s_mgr'] = s_mgr
            # ... instead we let it ride
            w_prev = s['w']
            w_roll = normalize( [ wi*math.exp(yi) for wi,yi in zip(w_prev,y)] )

            # Now we ratchet by generating possible trades outside the no-trade zone
            w_upper = [ wi*vup for wi in s['w_target']]
            w_lower = [ wi*vdn for wi in s['w_target']]

            # Convert trade list to weight changes
            from precise.skaters.managerutil.ratcheting import ratchet_trades
            dw = ratchet_trades(w=w_roll, w_lower=w_lower, w_upper=w_upper)
            w = [wi+dwi for wi,dwi in zip(w_roll,dw )]

            return w, s


