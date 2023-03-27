
from precise.skaters.covarianceutil.covrandom import random_band_cov, random_factor_cov, rnd_symm_cov
from precise.skaters.portfoliostatic.hrpport import hrp_diag_diag_s5_long_port as port
import time
import numpy as np

if __name__=='__main__':
    n_dim = 5000
    st = time.time()
    cov = rnd_symm_cov(n_dim=n_dim, rho=0.4, severity=0.1)
    print(time.time()-st)
    print(np.shape(cov))
    st = time.time()
    w = port(cov=cov)
    print(time.time()-st)
    import matplotlib.pyplot as plt
    plt.hist(w, bins=100)
    plt.show()
    print({'len':len(w)})
    print(w[:2])

