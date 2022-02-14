from precise.skaters.covariance.runempfactory import emp_pcov
import numpy as np

# Running empirical covariance with infinite memory, equal weighting

def run_emp_pcov_d0(y, s:dict, k=1, a=None, t=None, e=1):
    """
        Empirical covariance skater that assumes y's are iid

    :param y:  (n_dim,)   Incoming vector of observations
    :param s:             State
    :param k:             Steps ahead to predict (this won't change anything)
    :param a:             Variables know in advance (ignored)
    :param t:             Epoch time (ignored)
    :param e:             Allocated computation time (ignored)
    :return:  (n_dim,), (n_dim,n_dim), dict
              Point estimate, cov estimate, posterior state
    """
    assert k==1
    s = emp_pcov(s=s,x=y)
    x = s['mean']
    x_cov = s['pcov']
    return x, x_cov, s


def run_emp_pcov_d1(y, s:dict, k=1, a=None, t=None, e=None):
    """
       Empirical covariance skater that assumes changes in y's are iid
    """
    assert k==1
    if not s or s.get('dy'):
        s = {'prev_y':y,
             'dy':{}}
        return y, np.eye(len(y)), s
    else:
        dy = y-s['prev_y']
        dy_hat, dy_cov, s['dy'] = run_emp_pcov_d0(y=dy, s=s['dy'], k=1)
        y['prev_y'] = y
        x = s['prev_y'] + dy_hat
        return x, dy_cov, s


RUN_EMP_DO_COV_SKATERS = [run_emp_pcov_d0]
RUN_EMP_D1_COV_SKATERS = [run_emp_pcov_d1]


