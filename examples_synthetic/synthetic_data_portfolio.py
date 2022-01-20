
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.skaters.precision.lezhong import _lz_ema_spre_init, _lz_ema_spre_update
from precise.skaters.covariance import multiply_diag, normalize, grand_shrink
from precise.skatertools.syntheticdata import create_disjoint_dataset
from pprint import pprint
from precise.skaters.precisionutil.adjacency import centroid_precision_adjacency
import random
from precise.skaters.portfolioutil import long_from_pre

LONG_ONLY=True

if __name__=='__main__':
    if True:
        n_clusters = 30
        n_per_group = 5
        n_dims = [ random.choice([n_per_group]) for _ in range(n_clusters)]
        big_data = create_disjoint_dataset(n=10000, n_dims=n_dims)
    else:
        n_dim = 100
        big_data = create_band_dataset(n=10000, n_dim=n_dim, n_bands=3)
        n_per_group = 2
    true_cov = np.cov(big_data, rowvar=False)
    true_pre = np.linalg.inv(true_cov)


    phi = 1.1
    n_small=240
    small_data = big_data[:n_small,:]
    small_cov = np.cov(small_data,rowvar=False)
    small_pre = np.linalg.inv(multiply_diag(small_cov, phi=phi))
    adj = centroid_precision_adjacency(small_pre)
    
    n_tiny = 24
    tiny_data = big_data[:n_tiny]
    emp_cov = np.cov(tiny_data, rowvar=False)
    phi = 1.3
    lmbd = 0.75
    ridge_cov = multiply_diag(emp_cov, phi=phi, copy=True)
    affine_cov = grand_shrink(ridge_cov, lmbd=lmbd, copy=True)
    shrink_cov = grand_shrink(emp_cov, lmbd=lmbd, copy=True)
    ridge_pre = np.linalg.inv(ridge_cov)
    shrink_pre = np.linalg.inv(shrink_cov)
    affine_pre = np.linalg.inv(affine_cov)

    rho = 1/n_tiny
    phi = 1.3
    lmbd = 0.75
    pre = _lz_ema_spre_init(adj=adj, rho=rho, n_emp=n_tiny)
    for x in tiny_data[:-1,:]:
        pre = _lz_ema_spre_update(m=pre, x=x, update_precision=False, lmbd=lmbd, phi=phi)
    pre = _lz_ema_spre_update(m=pre, x=tiny_data[-1, :], update_precision=True, lmbd=lmbd, phi=phi)

    lz_pre = pre['spre']
    lz_cov = np.linalg.inv(lz_pre)
    
    # Portfolios
    n_dim = np.shape(big_data)[1]
    wones = np.ones(shape=(n_dim,1))

    if LONG_ONLY:
        w_lz = long_from_pre(pre['spre'], as_dense=True)
        w_ridge = long_from_pre(ridge_pre, as_dense=True)
        w_affine = long_from_pre(affine_pre, as_dense=True)
        w_shrink = long_from_pre(shrink_pre, as_dense=True)
        w_perfect = long_from_pre(true_pre, as_dense=True)
    else:
        w_lz = normalize( np.squeeze(np.matmul( pre['spre'],wones )) )
        w_ridge = normalize( np.squeeze(np.matmul( ridge_pre, wones)))
        w_affine = normalize(np.squeeze(np.matmul(affine_pre, wones)))
        w_shrink = normalize(np.squeeze(np.matmul( shrink_pre, wones)))
        w_perfect = normalize( np.squeeze(np.matmul( true_pre, wones)))
    import matplotlib.pyplot as plt
    descreasing = list(range(len(w_lz),0,-1))


    w_uniform = np.ones(shape=(n_dim,1))/n_dim
    true_var_uniform = np.matmul(np.matmul( w_uniform.T, true_cov), w_uniform)[0,0]
    true_var_lz = np.matmul(np.matmul( w_lz.T, true_cov), w_lz)
    true_var_shrink = np.matmul(np.matmul(w_shrink.T, true_cov), w_shrink)
    true_var_ridge = np.matmul(np.matmul( w_ridge.T, true_cov), w_ridge)
    true_var_perfect = np.matmul(np.matmul(w_perfect.T, true_cov), w_perfect)
    true_var_affine = np.matmul(np.matmul(w_affine.T, true_cov), w_affine)

    uniform_var_ratio = true_var_uniform/true_var_perfect
    lz_var_ratio = true_var_lz/true_var_perfect
    ridge_var_ratio = true_var_ridge/true_var_perfect
    shrink_var_ratio = true_var_shrink / true_var_perfect
    affine_var_ratio = true_var_affine / true_var_perfect

    plt.plot(descreasing, w_uniform,
             descreasing,sorted(w_lz,reverse=True),
             descreasing, sorted(w_affine, reverse=True),
             descreasing, sorted(w_ridge,reverse=True),
             descreasing, sorted(w_shrink,reverse=True),
             descreasing, sorted(w_perfect,reverse=True))
    plt.grid()
    plt.ylabel('Portfolio weight')
    plt.xlabel('Asset number')
    plt.title('Porfolio Variance ('+str(n_per_group)+' per group)')
    plt.legend(['uniform '+str(uniform_var_ratio),
                'affine ' + str(affine_var_ratio),
                'lz '+str(lz_var_ratio),
                'ridge '+str(ridge_var_ratio),
                'shrink '+str(shrink_var_ratio),
                'perfect '+str(1)])
    plt.show()


    ridge_pre_error = np.linalg.norm(ridge_pre-true_pre)
    lz_pre_error = np.linalg.norm(lz_pre-true_pre)
    affine_pre_error = np.linalg.norm(affine_pre - true_pre)

    leaderboard =  sorted([ (lz_var_ratio,'lz_ratio'),
                     (uniform_var_ratio,'uniform_ratio'),
                     (ridge_var_ratio,'ridge_ratio'),
                     (shrink_var_ratio,'shrink_var_ratio') ])


    if true_var_lz < min( true_var_ridge, true_var_uniform):
        print('*** BETTER ***')
    else:
        print('*** WORSE ***')
    pprint(leaderboard)
    print('---------------')
    from collections import OrderedDict
    report = OrderedDict({'optimal_var':true_var_perfect,'uniform_var':true_var_uniform,'lz_var':true_var_lz,'ridge_var':true_var_ridge,
              'lz_ratio':lz_var_ratio, 'uniform_ratio':uniform_var_ratio,
                          'ridge_ratio':ridge_var_ratio,'shrink_var_ratio':shrink_var_ratio,
              'lz_pre_norm':lz_pre_error,'ridge_pre_norm':ridge_pre_error,'affine_pre_norm':affine_pre_error,
              'w1':w_lz[:10],'w2':w_ridge[:10],'wt':w_perfect[:10]})
    pprint(report)
    if False:
        print('---implied sgma-')
        pprint(lz_cov[:5,:5])
        print('---true sgma-')
        pprint(true_cov[:5,:5])
        print('---conventional-')
        pprint(emp_cov[:5,:5])
        print('---lz precision---')
        pprint(pre['pre'])
        print('---true precision---')
        pprint(np.linalg.inv(true_cov[:5,:5]))
        print('---conv precision---')
        pprint(ridge_pre[:5,:5])


