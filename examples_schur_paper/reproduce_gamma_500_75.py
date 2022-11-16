from precise.skaters.portfolioutil.portcomparison import port_kurtosis
import numpy as np
from precise.skatervaluation.schurcomparisonutil.schurportpaperutils import G_PORTS, OTHER_PORTS, moment_plot
from pprint import pprint

# Varying gamma in the case of a cov matrix "seeded" by a symmetric one
# Interestingly, if the true cov is randomly generated from this starting point,
# then gamma=1.0 might outperform even the diagonal allocation (and certainly
# it outperforms the case g=0.0)


# Make a "seed" cov matrix somehow
rho = 0.35
N_DIM = 500
seed_cov = rho * (np.ones(shape=(N_DIM, N_DIM)) - np.eye(N_DIM)) + np.eye(N_DIM)

# This will be modified...
N_ANCHOR = 75   # e.g. 50, 100 We create the "anchor" cov matrix using simulation of anchor_cov
N_TRUE = None    # True matrix is same as anchor matrix if this is None
N_OBSERVED = 60  # Number of observations used when constructing the portfolio
                 # Optimization approaches tend to struggle when N_OBSERVED < N_DIM


if __name__=='__main__':
    stys = ['go','r+','b*']
    n_split = 5
    max_time = 5*60   # <--- How long to run before terminating this script
    ports = G_PORTS+OTHER_PORTS
    for sty in stys:

        moments = port_kurtosis(ports=ports, seed_cov=seed_cov, n_true=N_TRUE,
                                n_anchor=N_ANCHOR, n_observed=N_OBSERVED,
                                metric='mean', port_kwargs={'n_split':n_split}, max_time=max_time)
        pprint(moments)
        try:
            bps_saved = int(10000*(moments['g000']-moments['g100'])/(2*moments['g000']))
            pprint({'bps_saved':bps_saved})
        except:
            pass
        normalized_moments = dict( [(k,v/moments['g000']) for k,v in moments.items()])
        moment_plot(moments=normalized_moments, sty=sty)

    import matplotlib.pyplot as plt
    plt.show()
    plt.savefig('schur.png')








