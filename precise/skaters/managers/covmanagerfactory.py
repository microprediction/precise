from precise.skaters.portfoliostatic.equalport import equal_long_port
import math
from precise.skaters.locationutil.vectorfunctions import normalize
from precise.skaters.portfolioutil.zetaport import zeta_port
from precise.skaters.portfolioutil.portgeometry import closest_weak_l1, closest_point_l1


# A family of managers characterized as follows:
#
#    1. They maintain online estimates of covariancecomparisonutil
#    2. Periodic application of a static portfolio method (or multiple, or repeated).
#    3. An ad-hoc compromise between adjusting to new weights versus trading cost.
#
# In this context one can employ:
#     - Any skater in precise.skaters.covariancecomparisonutil
#     - Any portfolio methods in precise.skaters.portfoliostatic
#
# See examples in precise.managers.ppomanagers, rpmanagers, weakmanagers etc


def closest_random_nudge(port, cov, q, l, w, port_kwargs, zeta=None):
    """ Apply portfolio method l times, then choose the closest to w or some convex combo

        :param l:      Number of times to apply port, (presumably port is stochastic)
                       We allow l=None to treat the case l=1 separately, just as a little check
                       Also: if l is odd --> use convex hull
                             if l is even --> just use closest point

        :param q:      How far to move towards target
        :param zeta:   Just here for the heck of it. Set to anything other than None or zero at your peril.

        :param cov:
        :param port:   Function taking cov, ***port_kwargs -> w
        :param port_kwargs: Additional params to port
        :param w:      Previous portfolio

    """

    if l is None:
        w_target = zeta_port(port=port, cov=cov, zeta=zeta, **port_kwargs)  # <-- just port(cov,**port_kwargs) usually
    else:
        # Run port several times
        w_ports = list()
        for _ in range(l):
            w_ = zeta_port(port=port, cov=cov, zeta=zeta, **port_kwargs)
            w_ports.append(w_)

        # Find a portfolio near to w
        if (l is not None) and (l >= 3) and is_odd(l):
            w_target = closest_weak_l1(origin=w, xs=w_ports, verbose=False)
        else:
            w_target = closest_point_l1(origin=w, xs=w_ports)

    w = [q * wi + (1 - q) * wpi for wi, wpi in zip(w_target, w)]
    return w


def is_odd(l):
    return (l % 2) == 1


def _periodic_nudge(port, j: int, y, s: dict, cov, port_kwargs, nudger, **nudger_kwargs):
    """
    :param nudger: A method of producing a portfolio using the prior one
                   See closest_random_nudge above for example

          nudger_kwargs: For the default nudger,
                     l - Number of times to call port
                     q - Distance to move towards target
                     zeta - Optional compromise with corr versus cov
    """

    n_dim = len(y)
    if s.get('w') is None:
        s['multiplier'] = [1 for _ in range(n_dim)]
        s['count'] = 0
        w = port(cov=cov, **port_kwargs)
        s['w'] = [wi for wi in w]
        return w, s
    else:
        s['count'] = s['count'] + 1
        if s['count'] % j == 0:
            # Compute roll forward weights
            s['multiplier'] = [mi * math.exp(yi) for mi, yi in zip(s['multiplier'], y)]
            w_roll = normalize([wi * mi for wi, mi in zip(s['w'], s['multiplier'])])

            # Move towards new target, informed by port
            w = nudger(port=port, cov=cov, w=w_roll, port_kwargs=port_kwargs, **nudger_kwargs)

            # Save state needed
            s['w'] = [wi for wi in w]
            s['multiplier'] = [1 for _ in range(n_dim)]
            return w, s
        else:
            # Let it ride
            s['multiplier'] = [mi * math.exp(yi) for mi, yi in zip(s['multiplier'], y)]
            w = normalize([wi * mi for wi, mi in zip(s['w'], s['multiplier'])])
            return w, s


def static_cov_manager_factory_d0(y, s, f, port, e=1, f_kwargs: dict = None, port_kwargs: dict = None, n_cold=5, j=1,
                                  nudger=None, **nudger_kwargs):
    """
     A family of managers characterized as follows:

    1. They maintain online estimates of covariancecomparisonutil
    2. Periodic application of a static portfolio method (or multiple, or repeated) to determine a new target composition
    3. An ad-hoc compromise between the new target and trading cost, here refered to as "nudging"

    In this context one can employ:
     - Any skater in precise.skaters.covariancecomparisonutil
     - Any portfolio methods in precise.skaters.portfoliostatic
     - Any nudging method

     Typical usage with default nudger:

         static_cov_manager_factory_d0(y, s, f, port, e=1, f_kwargs, port_kwargs, n_cold=5, j=1, q=0.1, l=5)
                                        l: how many times to repeatedly run the static portfolio construction
                                        q: how far to move towards the target

    See examples in precise.managers.ppomanagers, rpmanagers, weakmanagers etc

    Financial remark: This is at the moment a basic manager pattern ignoring mean.
    If you have opinions on means, you'll have to incorporate them into variance somehow via a covariancecomparisonutil skater you modify.

          :param f     cov skater ("d0" hints that it expects to receive *changes* in log(price) so won't do any differencing itself)
          :param port  portfolio constructor
          :param j     How often to run the static portfolio construction.
                           (Remark: if j>1 this will be nonsense unless 'y' represents changes in log prices)
          :param nudger Any method of producing a portfolio using the prior one. See closest_random_nudge above for an example
          :params **nudger_kwargs  For the default stochastic nudger we use
                                        l: how many times to repeatedly run the static portfolio construction
                                        q: how far to move towards the target
                                        zeta: how far to shrink towards corr port (default 0)

       :returns w, s
    """

    if f_kwargs is None:
        f_kwargs = {}
    if port_kwargs is None:
        port_kwargs = {}
    if nudger is None:
        nudger = closest_random_nudge
        assert 'q' in nudger_kwargs, 'You probably forgot to supply q '
        if not 'l' in nudger_kwargs:
            nudger_kwargs['l'] = None

    if not s:
        s = {'f_state': {},
             'port_state': {},
             'count': 0,
             'account_state': {}}

    x_mean, x_cov, s['f_state'] = f(y=y, s=s['f_state'], k=1, e=e, **f_kwargs)
    s['count'] += 1
    if s['count'] >= n_cold and (e > 0):
        s_account = s['account_state']
        w, s_account = _periodic_nudge(port=port, y=y, j=j, s=s_account, cov=x_cov, port_kwargs=port_kwargs,
                                       nudger=nudger, **nudger_kwargs)
        s['account_state'] = s_account

    else:
        w = equal_long_port(cov=x_cov)
    return w, s
