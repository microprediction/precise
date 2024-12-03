import numpy as np
#from scipy.spatial._qhull import QhullError
from itertools import combinations
from scipy.linalg import lstsq
from precise.skaters.portfolioutil.portfunctions import exclude_negative_weights


def shortlist_by_l1_norm(origin, xs, tol=0.2, n_max=None):
    """ Pick some points that aren't too close to each other, in order of increasing distance from origin
    :param n_max:
    :return:
    """
    try:
        dxs = sorted( [ ( sum(np.abs(np.array(origin) - np.array(xsi))),xsi) for xsi in xs], key=lambda t: t[0])
    except ValueError:
        raise NotImplementedError('huh?')
    w_shortlist = [ dxs[0][1] ]
    for _,wj in dxs[1:]:
        separation = min([sum(np.abs(np.array(wj) - np.array(wk))) for wk in w_shortlist])
        if separation>tol:
            w_shortlist.append(wj)
        if (n_max is not None) and len(w_shortlist)>=n_max:
            break
    return w_shortlist


def np_linalg_norms(xs, ord=1, origin=None):
    if origin is None:
        origin = np.zeros_like(xs[0])
    return [np.linalg.norm(np.array(origin) - np.array(wsi), ord=ord) for wsi in xs]


def closest_point_l1(xs, ord=1, origin=None) -> int:
    """ Choose from a list of points ws in space the one closest to w """
    l1s = np_linalg_norms(origin=origin, xs=xs, ord=ord)
    j = np.argmin(l1s)
    return xs[j]


def closest_weak_l1(xs, origin, n_max=50, verbose=False):
    """ Find a postiive combination of ws that is closer to w in L1-norm
        This is a little heuristic. It doesn't solve the optimization problem.
    :param origin:       anchor portfolio
    :param xs:      target portfolio list
    :param verbose:
    :return:
    """
    ws_short = shortlist_by_l1_norm(origin=origin, xs=xs, n_max=n_max)
    xs = [np.array(wj) - np.array(origin) for wj in ws_short]
    x = verbosely_choose_close_point_on_boundary_of_convex_hull(xs=xs, verbose=verbose)
    return np.array(origin) + np.array(x)


def verbosely_choose_close_point_on_boundary_of_convex_hull(xs, verbose=False)->[float]:
    """ Work in progress
     There are some insights in https://arxiv.org/pdf/math/0606426
     This is a heuristic algorithm !
    :return:
    """
    l1s = np_linalg_norms(xs=xs, ord=1)
    d_upper = min(l1s)
    if d_upper<1e-4:
        return closest_point_l1(xs=xs)

    best_x = closest_point_l1(xs=xs)
    best_ratio = np.linalg.norm(best_x, ord=1) / d_upper
    best_discount = -1

    W_points = np.vstack(xs)
    n_points, n_dim = np.shape(W_points)
    HEAVY = 100
    HEAVIER = 1000
    W = np.hstack([W_points, HEAVY*np.ones(shape=(n_points,1)) ])

    for lmbd in [10.0, 4.0, 2.0, 1.5, 1.0, 0.5]:
        for sng in [-1,1]:
            for k in range(n_dim):
                Wk = np.copy(W)
                for j in range(n_points):
                    Wk[j,k] = HEAVIER*W[j,k]
                yk = np.zeros(n_dim+1)
                yk[n_dim] = HEAVY
                yk[k] = d_upper*sng*lmbd
                b = yk
                a = np.transpose(Wk)
                res = lstsq(a=a,b=b)
                u_raw = res[0]
                u = exclude_negative_weights(u_raw)
                x_guess = np.dot( np.transpose(W_points),u )
                d_ = np.linalg.norm(x_guess, ord=1)
                d_ratio = d_/d_upper
                if d_ratio < best_ratio:
                    best_ratio = d_ratio
                    best_discount = lmbd
                    best_x = x_guess
    if verbose:
        print({'d_ratio': best_ratio, 'discount': best_discount})
    return best_x




if __name__=='__main__':
    import random
    n_dim = 500
    n_port = random.choice([1,2,25])
    x1 = np.random.randn(n_dim)
    xs = [ xi+x1 for xi in np.random.randn(n_port,n_dim) ]
    x  = verbosely_choose_close_point_on_boundary_of_convex_hull(xs, verbose=True)











