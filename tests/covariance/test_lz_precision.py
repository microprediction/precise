
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.precision.lezhong import _lz_ema_spre_init, _lz_ema_spre_update
from precise.covariance.util import multiply_diag, normalize, grand_shrink
from precise.synthetic.generate import create_disjoint_dataset, create_band_dataset
from precise.structure.adjacency import centroid_precision_adjacency
import random


def test_fixed_rpre_init():
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
    # lz_cov = np.linalg.inv(lz_pre)
    
    # Portfolios
    n_dim = np.shape(big_data)[1]
    wones = np.ones(shape=(n_dim,1))
    w_lz = normalize( np.squeeze(np.matmul( pre['spre'],wones )) )
    w_ridge = normalize( np.squeeze(np.matmul( ridge_pre, wones)))
    w_affine = normalize(np.squeeze(np.matmul(affine_pre, wones)))
    w_shrink = normalize(np.squeeze(np.matmul( shrink_pre, wones)))
    w_perfect = normalize( np.squeeze(np.matmul( true_pre, wones)))

    ridge_pre_error = np.linalg.norm(ridge_pre-true_pre)
    lz_pre_error = np.linalg.norm(lz_pre-true_pre)
    affine_pre_error = np.linalg.norm(affine_pre - true_pre)



