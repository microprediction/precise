from precise.skatervaluation.schurcomparisonutil.schurportpaperutils import gamma_comparison_and_plot, G_PORTS
from precise.skaters.covarianceutil.covrandom import rnd_symm_cov

# Runs three experiments where gamma is varied and portfolio variance computed

RHO = 0.35         # Approx pairwise correlation
SEVERITY = 0.05    # Imbalance parameter for volatilities
N_DIM = 50         # Number of assets
N_SPLIT = 30       # Dimension to terminate splitting at
N_ANCHOR = 120     # Number of samples to create true matrix
N_TRUE = None      # Leave as None
N_OBSERVED = 120   # Number of observations seen when estimating Sigma
rnd_cov_kwargs = {'rho':RHO,'severity':SEVERITY,'n_dim':N_DIM}
MAX_TIME = 1*60    # Seconds to spend on each of three experiments


if __name__=='__main__':
    xlabel = r'$p= ' + str(N_DIM) + r'$ $\rho=' + str(RHO) + '$ $ a=' + str(N_ANCHOR) + '$ $ o=' + str(N_OBSERVED) + '$ '
    g_last_and_first = [ G_PORTS[-1], G_PORTS[0]]
    gamma_comparison_and_plot(rnd_cov=rnd_symm_cov,
                              rnd_cov_kwargs=rnd_cov_kwargs,
                              n_observed=N_OBSERVED,
                              n_anchor=N_ANCHOR,
                              n_split=N_SPLIT,
                              max_time=MAX_TIME,
                              n_true=None,
                              xlabel=xlabel,
                              g_ports=g_last_and_first)




