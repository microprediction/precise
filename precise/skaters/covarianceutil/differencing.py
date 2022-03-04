
import numpy as np


def d1_factory( f, y, s, k=1, **kwargs ):
    """
         Skaters where changes to y are assumed iid

    :param f:   skater producing estimates of changes
    :param kwargs:   additional kwargs to f
    :return:
    """
    if not s or s.get('dy'):
        s = {'prev_y': y,
             'dy': {}}
        return y, np.eye(len(y)), s
    else:
        dy = y - s['prev_y']
        dy_hat, dy_cov, s['dy'] = f(y=dy, s=s['dy'], k=k, **kwargs)
        s['prev_y'] = y
        x = s['prev_y'] + dy_hat
        return x, dy_cov, s