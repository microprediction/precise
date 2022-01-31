import numpy as np

def portfolio_factory(fs, s:dict, y, k=1, n_burn=10, skater_type='cov', meta_f=None):
    """
    :param g:
    :return:
    """
    if not s:
        n_dim = max(np.shape(y))
        s = {'s_fs': dict([(f.__name__, {}) for f in fs]),  # State for skaters
             's_g': {},  # State for meta-model
             'n_obs': 0,
             's_fs_p': dict([(f.__name__, {}) for f in fs]),  # Holds parades for skaters
             's_p': {},  # Self parade
             }
    s['n_samples']+=1
    # Evaluate?


    # Apply all skaters
    for i, f in enumerate(fs):
        s_prev = s['states'][i]
        x, x_pre_or_cov, s_post = f(s=s_prev, y=y, k=k)
        s['states'][i] = s_post
        if skater_type=='cov':
            s['cov_prevs'][i] = x_pre_or_cov
        elif skater_type=='pre':
            s['pre_prevs'][i] = x_pre_or_cov










        y_hat_prev = None
        y_pre_prev = None
        for m, y in enumerate(xs[n_burn:]):
            if y_hat_prev is not None:
                dy = np.array(y) - np.array(y_hat_prev)
                ll_delta = min(vector_log_likelihood(pre=y_pre_prev, y=dy, lb=lb), ub)
                ll += ll_delta

            # Store predictions for assessment against next data point
            y_hat_prev = y_hat
            y_pre_prev = y_cov

            # Make next prediction
            y_hat, y_cov, s = f(s=s, y=y, k=1)