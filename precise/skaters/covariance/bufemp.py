import numpy as np
from precise.skaters.covarianceutil.conventions import Y_DATA_TYPE
from precise.skaters.covarianceutil.differencing import d1_factory
from precise.skaters.covariance.bufempfactory import buf_emp_pcov_d0_factory

# Simple, inefficient skaters that use operations on a buffer of past values


def buf_emp_pcov_d0_n20(y:Y_DATA_TYPE, s:dict, k=1, e=1):
    assert k==1
    return buf_emp_pcov_d0_factory(y=y, s=s, n_buffer = 20, e=e)


def buf_emp_pcov_d0_n50(y:Y_DATA_TYPE, s:dict, k=1, e=1):
    assert k==1
    return buf_emp_pcov_d0_factory(y=y, s=s, n_buffer = 50, e=e)


def buf_emp_pcov_d0_n100(y:Y_DATA_TYPE, s:dict, k=1, e=1):
    return buf_emp_pcov_d0_factory(y=y, s=s, n_buffer = 100, e=e)


def buf_emp_pcov_d1_n20(y:Y_DATA_TYPE, s:dict, k=1, e=1):
    assert k==1
    return buf_emp_pcov_d1(y=y, s=s, n_buffer = 20, e=e)


def buf_emp_pcov_d1_n100(y:Y_DATA_TYPE, s:dict, k=1, e=1):
    assert k==1
    return buf_emp_pcov_d1(y=y, s=s, n_buffer = 100, e=e)


def buf_emp_pcov_d1(y:Y_DATA_TYPE, s:dict, n_buffer:int=100, k=1, e=1):
    """
        For when changes are iid gaussian
    """
    assert k==1
    return d1_factory(f = buf_emp_pcov_d0_factory, y=y, s=s, n_buffer=n_buffer, e=e)


def buf_emp_pcov_d1_long_form(y:Y_DATA_TYPE, s:dict, n_buffer:int=100, k=1, e=1):
    # A long form version of the above, just for clarity and testing
    assert k==1
    if not s or s.get('dy'):
        s = {'prev_y': y,
             'dy': {}}
        return y, np.eye(len(y)), s
    else:
        dy = y - s['prev_y']
        dy_hat, dy_cov, s['dy'] = buf_emp_pcov_d0_factory(y=dy, s=s['dy'], n_buffer=n_buffer)
        y['prev_y'] = y
        x = s['prev_y'] + dy_hat
        return x, dy_cov, s
    

BUF_EMP_D0_SKATERS = [buf_emp_pcov_d0_n20, buf_emp_pcov_d0_n50, buf_emp_pcov_d0_n100]
BUF_EMP_D1_SKATERS = [buf_emp_pcov_d1_n20, buf_emp_pcov_d1_n100]
BUFFERED_EMPIRICAL_SKATERS = BUF_EMP_D0_SKATERS + BUF_EMP_D1_SKATERS