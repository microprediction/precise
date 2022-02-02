
from precise.skaters.covarianceutil.covrandom import random_band_cov
import numpy as np
from precise.skaters.portfolioutil.allstaticport import PORT
from pypfopt.exceptions import OptimizationError


def test_all():
    cov = random_band_cov()
    n_dim = np.shape(cov)[0]
    for port in PORT:
        print(port)
        try:
            w = port(cov=cov)
            w_dim = len(w)
            if not len(w) == np.shape(cov)[0]:
                print(' ... and something is askew with ' + port.__name__ + ' as len=' + str(w_dim) + ' not ' + str(
                    n_dim))
                pass
        except OptimizationError:
            print(' ... and for n_dim='+str(n_dim)+ ' the optimization failed when calling '+str(port.__name__))



if __name__=='__main__':
    test_all()