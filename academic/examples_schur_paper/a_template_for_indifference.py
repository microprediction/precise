from precise.skatervaluation.schurcomparisonutil.schurportpaperutils import gamma_comparison_and_plot, G_PORTS
from precise.skaters.covarianceutil.covrandom import rnd_symm_cov
from precise.skatervaluation.schurcomparisonutil.schurportpaperutils import g000, g100, g010
# Here we try to create an example where HRP and the weak portfolio are roughly commensurate
# The idea is to then see if moving from HRP towards optimization helps

RHO = 0.35         # Approx pairwise correlation
SEVERITY = 0.05    # Imbalance parameter for volatilities
N_DIM = 20         # Number of assets
N_SPLIT = 15       # Dimension to terminate splitting at
N_ANCHOR = 120     # Number of samples to create true matrix
N_TRUE = None      # Leave as None
N_OBSERVED = 19    # Number of observations seen when estimating Sigma
rnd_cov_kwargs = {'rho':RHO,'severity':SEVERITY,'n_dim':N_DIM}
MAX_TIME = 8*60*60    # Seconds to spend on each of three experiments


if __name__=='__main__':
    xlabel = r'$p= ' + str(N_DIM) + r'$ $\rho=' + str(RHO) + '$ $ a=' + str(N_ANCHOR) + '$ $ o=' + str(N_OBSERVED) + '$ '
    g_last_and_first = [ g000, g100 ]
    gamma_comparison_and_plot(rnd_cov=rnd_symm_cov,
                              rnd_cov_kwargs=rnd_cov_kwargs,
                              n_observed=N_OBSERVED,
                              n_anchor=N_ANCHOR,
                              n_split=N_SPLIT,
                              max_time=MAX_TIME,
                              n_true=None,
                              xlabel=xlabel,
                              g_ports=g_last_and_first)




