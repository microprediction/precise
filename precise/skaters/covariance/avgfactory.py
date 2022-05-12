
import numpy as np
from precise.skaters.location.empirical import emp_d0


def avg_factory(y, fs, s:dict, k=1, e=1, draw_probability=1.0, **f_kwargs):
    """ Average the predictions of several cov skaters

         fs  list of cov skaters
         p   Probability of using any given data point for any given skater

    """
    if not s:
        s = {'s_fs':[{} for f in fs]}

    avg_mean_s = {}
    ravel_cov_s = {}
    count = 0
    for f_ndx,f in enumerate(fs):
        if (np.random.rand()<draw_probability) or ((f_ndx==len(fs)-1) and (count==0)):
           x_mean, x_cov, s['s_fs'][f_ndx] = f(y=y, s=s['s_fs'][f_ndx], k=k, e=e, **f_kwargs)
           ravel_cov, _, ravel_cov_s = emp_d0(y=np.ravel(x_cov), s=ravel_cov_s)
           avg_mean, _, avg_mean_s = emp_d0(y=x_mean, s=avg_mean_s)
    avg_cov = np.reshape( ravel_cov, newshape=np.shape(x_cov) )

    return avg_mean, avg_cov, s

