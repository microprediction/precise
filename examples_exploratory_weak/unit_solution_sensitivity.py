from precise.skaters.portfolioutil.portfunctions import portfolio_variance
import numpy as np
from precise.skaters.covarianceutil.covrandom import random_known_cov
from precise.skaters.portfoliostatic.unitport import unit_port


extreme_cov = np.array([[ 1.09948514, -1.02926114,  0.22402055,  0.10727343],
                       [-1.02926114,  2.54302628,  1.05338531, -0.12481515],
                       [ 0.22402055,  1.05338531,  1.79162765, -0.78962956],
                       [ 0.10727343, -0.12481515, -0.78962956,  0.86316527]])

less_extreme_cov = np.copy(extreme_cov)
for i in range(4):
    less_extreme_cov[i,i] *= 1.01


def w_v(anchor_cov):
    true_cov = random_known_cov(cov=anchor_cov)
    obs_cov = random_known_cov(cov=true_cov)
    w_true = unit_port(cov=true_cov)
    w_obs = unit_port(cov=obs_cov)
    v_obs = portfolio_variance(w=w_obs, cov=true_cov)
    v_true = portfolio_variance(w=w_true, cov=true_cov )
    return np.linalg.norm(w_obs - w_true)**2, v_obs-v_true


if __name__=='__main__':
    import matplotlib.pyplot as plt
    anchor_cov = extreme_cov
    anchor_cov = less_extreme_cov
    data = [ w_v(anchor_cov) for _ in range(500)]
    w_errors, v_errors = map(list, zip(*data))
    m, b = np.polyfit(w_errors, v_errors, 1)

    plt.scatter(w_errors,v_errors)
    plt.plot(w_errors, m*np.array(w_errors)+b)
    plt.xlabel('squared weight error')
    plt.ylabel('port var')
    plt.title('m='+str(round(m,4))+' b='+str(round(b,4)))
    plt.show()



