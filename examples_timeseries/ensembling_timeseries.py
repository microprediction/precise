# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html

from precise.skaters.precision.lezhong import _lz_ema_spre_init, _lz_ema_spre_update
from precise.skaters.covarianceutil.matrixfunctions import multiply_diag, grand_shrink, make_diagnonal, mean_off_diag
from pprint import pprint
from precise.skaters.precisionutil.adjacency import centroid_precision_adjacency
from precise.skatertools.data.skaterresiduals import random_multivariate_residual
import numpy as np
from collections import Counter
from precise.skaters.portfolioutil.longonly import long_from_pre, long_from_cov

# Stacking time-series models

# c.f. https://arxiv.org/pdf/1806.08200.pdf


def evaluate(do_plot=False):
    # Select some models-
    n_adj = 15000  # <--- Use these points to estimate pre sparsity
    n_cov = 500  # <--- Use this many to estimate cov
    n_test = 500  # <--- Then use this many to judge

    big_data_df = random_multivariate_residual(n_obs=n_adj+n_cov+n_test+100,random_start=True).dropna()
    if False:
        # Filter out some?
        models = list(big_data_df.columns)
        models_to_use = ['empirical_last_value', 'sluggish_moving_average', 'slowly_moving_average', 'quickly_moving_average',
         'rapidly_moving_average', 'balanced_ema_ensemble', 'aggressive_ema_ensemble',
         'thinking_fast_and_fast', 'thinking_fast_and_slow', 'thinking_slow_and_slow', 'thinking_slow_and_fast',
        'quick_balanced_ema_ensemble', 'slow_balanced_ema_ensemble',
         'quick_aggressive_ema_ensemble', 'slow_aggressive_ema_ensemble', 'quick_precision_ema_ensemble']
        if True:
             models_to_use = [ 'thinking_fast_and_slow', 'thinking_slow_and_slow', 'thinking_slow_and_fast',
                              'rapidly_moving_average','quickly_moving_average','empirical_last_value','thinking_fast_and_fast',
                               'slow_aggressive_ema_ensemble', 'quick_precision_ema_ensemble']

        big_data_df = big_data_df[models_to_use]

    return evaluate_lz(df=big_data_df, n_adj=n_adj, n_cov=n_cov, n_test=n_test, do_plot=do_plot)


def evaluate_lz(df, n_adj,n_cov, n_test, do_plot):

    adj_data_df = df[:n_adj+n_cov]
    cov_data_df = df[n_adj:n_adj+n_cov]
    test_data_df = df[n_adj+n_cov:n_adj+n_cov+n_test]

    test_data = test_data_df.values
    test_data_shape = np.shape(test_data)
    n_dim = test_data_shape[1]
    test_cov = np.cov(test_data, rowvar=False)

    try:
        true_pre = np.linalg.inv(test_cov)
    except:
        # print('Using pseudo-inverse')
        true_pre =  np.linalg.pinv(test_cov)

    # Use some data to estimate structure
    phi, lmbd = 1.1, 0.2
    adj_data = adj_data_df.values
    small_cov = np.cov(adj_data, rowvar=False)
    small_pre = np.linalg.inv(multiply_diag(small_cov, phi=phi))
    adj = centroid_precision_adjacency(small_pre)
    mean_adj = mean_off_diag(adj)
    if np.random.rand()<0.02:
        print('Mean adj = '+str(mean_adj))

    # Then use recent data to estimate cov
    cov_data = cov_data_df.values
    emp_cov = np.cov(cov_data, rowvar=False)

    phi, lmbd = 1.3, 0.5
    ridge_cov = multiply_diag(emp_cov, phi=phi, copy=True)
    affine_cov = grand_shrink(ridge_cov, lmbd=lmbd, copy=True)
    shrink_cov = grand_shrink(emp_cov, lmbd=lmbd, copy=True)
    ridge_pre = np.linalg.inv(ridge_cov)
    shrink_pre = np.linalg.inv(shrink_cov)
    affine_pre = np.linalg.inv(affine_cov)
    diag_cov = make_diagnonal(emp_cov)


    # LZ estimate
    rho, phi, lmbd = 1 / n_cov, 1.01, 0.05   # 1.01, 0.25 works okayish
    pre = _lz_ema_spre_init(adj=adj, rho=rho, n_emp=n_cov)
    for x in cov_data[:-1, :]:
        pre = _lz_ema_spre_update(m=pre, x=x, update_precision=False, lmbd=lmbd, phi=phi)
    pre = _lz_ema_spre_update(m=pre, x=cov_data[-1, :], update_precision=True, lmbd=lmbd, phi=phi)

    lz_pre = pre['spre']
    try:
        lz_cov = np.linalg.pinv(lz_pre)
    except:
        pass # don't need it

    # Portfolios
    n_dim = np.shape(test_data)[1]
    w_lz = long_from_pre(lz_pre)
    w_diagonal = long_from_cov(diag_cov)
    w_ridge = long_from_pre(ridge_pre)
    w_affine = long_from_pre(affine_pre)
    w_shrink = long_from_pre(shrink_pre)
    w_perfect = long_from_cov(grand_shrink(a=test_cov, lmbd=0.01, copy=True))
    w_uniform = np.ones(shape=(n_dim,)) / n_dim

    w_half = (w_lz+w_uniform)/2
    W = np.array([ w_lz, w_diagonal, w_ridge, w_affine, w_shrink, w_perfect ])

    import matplotlib.pyplot as plt
    descreasing = list(range(len(w_lz), 0, -1))

    true_var_uniform = np.matmul(np.matmul(w_uniform.T, test_cov), w_uniform)
    true_var_lz = np.matmul(np.matmul(w_lz.T, test_cov), w_lz)
    true_var_diagonal = np.matmul(np.matmul(w_diagonal.T, test_cov), w_diagonal)
    true_var_shrink = np.matmul(np.matmul(w_shrink.T, test_cov), w_shrink)
    true_var_ridge = np.matmul(np.matmul(w_ridge.T, test_cov), w_ridge)
    true_var_perfect = np.matmul(np.matmul(w_perfect.T, test_cov), w_perfect)
    true_var_affine = np.matmul(np.matmul(w_affine.T, test_cov), w_affine)
    true_var_half = np.matmul(np.matmul(w_half.T, test_cov), w_half)

    uniform_var_ratio = true_var_uniform / true_var_perfect
    lz_var_ratio = true_var_lz / true_var_perfect
    ridge_var_ratio = true_var_ridge / true_var_perfect
    shrink_var_ratio = true_var_shrink / true_var_perfect
    affine_var_ratio = true_var_affine / true_var_perfect
    diagonal_var_ratio = true_var_diagonal / true_var_perfect
    half_var_ratio = true_var_half / true_var_perfect

    if do_plot:
        plt.plot(descreasing, n_dim*w_uniform,
                 descreasing, sorted(n_dim*w_lz, reverse=True),
                 descreasing, sorted(n_dim*w_affine, reverse=True),
                 descreasing, sorted(n_dim*w_ridge, reverse=True),
                 descreasing, sorted(n_dim*w_shrink, reverse=True),
                 descreasing, sorted(n_dim*w_diagonal, reverse=True))
        plt.grid()
        plt.ylabel('Portfolio weight')
        plt.xlabel('Asset number')
        plt.title('Estimator Variance')
        plt.legend(['uniform ' + str(uniform_var_ratio),
                    'affine ' + str(affine_var_ratio),
                    'lz ' + str(lz_var_ratio),
                    'ridge ' + str(ridge_var_ratio),
                    'shrink ' + str(shrink_var_ratio),
                    'diagonal' + str(diagonal_var_ratio)])
        plt.show()

    report = {      'lz': lz_var_ratio-1,
                    'diagonal':diagonal_var_ratio-1,
                    'half':half_var_ratio-1,
                    'ridge': ridge_var_ratio-1,
                     'uniform': uniform_var_ratio-1,
                     'affine':affine_var_ratio-1,
                     'shrink':shrink_var_ratio-1}

    return report

if __name__=='__main__':
    running = Counter()
    while True:
        report = evaluate()
        running.update(Counter(report))
        if np.random.rand()<0.03:
            pprint(running.most_common())
