from functools import partial, update_wrapper


def buy_and_hold(mgr, j, q=1.0):
    """
        Use this to make a canonically named manager with j and q fixed that does not expect j, q arguments

    :param mgr:
    :param j:
    :return:
    """
    mgr_j_q = partial(mgr,j=j, q=q)
    mgr_j_q = update_wrapper(mgr_j_q, mgr)
    mgr_j_q.__name__ = mgr.__name__+'_j'+str(j)+'_q'+str(int(100*q)).zfill(3)
    return mgr_j_q
