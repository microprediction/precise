from precise.skaters.location.empricalpre import emp
import numpy as np


def emp_d0(y, s:dict, k=1, **ignore):
    """ Rudimentary empirical skater with no cov estimation """
    # See precision.covariance.empirical.run_emp_pcov_d1 if you want cov estimates
    s = emp(s=s, x=np.array(y))
    y_hat = s['mean']
    return y_hat, np.eye(len(y)), s


def emp_d1(y, s:dict, k=1, **ignore):
    """ Rudimentary differenced empirical skater with no cov estimation """
    # See precision.covariance.empirical.run_emp_pcov_d1 if you want cov estimates
    if not s:
        s = {'prev_y':y,'dy':{}}
        return np.zeros_like(y), np.eye(len(y)), s
    else:
        dy = y - s['prev_y']
        dy_hat, _, s['dy'] = emp_d0(y=dy, s=s['dy'], k=1)
        y['prev_y'] = y
        y_hat = s['prev_y'] + dy_hat + s['dy']['v']['mean']
        y_cov = np.eye(len(y))
        return y_hat, y_cov, s


