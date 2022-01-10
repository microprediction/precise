
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.precision.fixed import fixed_rpre_init, fixed_rpre_update
from precise.covariance.util import multiply_diag, normalize
from precise.covariance.generate import create_correlated_dataset, create_factor_dataset, create_disjoint_dataset
from pprint import pprint
from precise.covariance.adjacency import infer_adjacency
import random


def test_fixed_rpre_init():
    n_clusters = 20
    n_dims = [ random.choice([5]) for _ in range(n_clusters)]
    big_data = create_disjoint_dataset(n=10000, n_dims=n_dims)
    true_cov = np.cov(big_data, rowvar=False)
    true_pre = np.linalg.inv(true_cov)


    lmbd = 1.1
    n_small=250
    small_data = big_data[:n_small,:]
    small_cov = np.cov(small_data,rowvar=False)
    small_pre = np.linalg.inv(multiply_diag(small_cov, lmbd=lmbd))
    adj = infer_adjacency(small_pre)
    
    n_tiny = 100
    tiny_data = big_data[:n_tiny]
    emp_cov = np.cov(tiny_data, rowvar=False)
    lmbd = 1.2
    ridge_cov = multiply_diag(emp_cov, lmbd=lmbd, make_copy=True)
    ridge_pre = np.linalg.inv(ridge_cov) # Conventional ridge approach 

    rho = 1/n_tiny
    lmbd = 1.2
    pre = fixed_rpre_init(adj=adj, rho=rho, n_emp=n_tiny)
    for x in tiny_data[:-1,:]:
        pre = fixed_rpre_update(m=pre, x=x, with_precision=False, lmbd=lmbd)
    pre = fixed_rpre_update(m=pre, x=tiny_data[-1,:], with_precision=True, lmbd=lmbd)

    block_pre = pre['pre']
    # block_cov = np.linalg.inv(block_pre)
    
    # Portfolios
    n_dim = np.shape(big_data)[1]
    wones = np.ones(shape=(n_dim,1))
    w_block = normalize( np.squeeze(np.matmul( pre['pre'],wones )) )
    w_ridge = normalize( np.squeeze(np.matmul( ridge_pre, wones)))
    w_perfect = normalize( np.squeeze(np.matmul( true_pre, wones)))
    wu = np.ones(shape=(n_dim,1))/n_dim
    true_var_uniform = np.matmul(np.matmul( wu.T, true_cov), wu)[0,0]
    true_var_block = np.matmul(np.matmul( w_block.T, true_cov), w_block)
    true_var_ridge = np.matmul(np.matmul( w_ridge.T, true_cov), w_ridge)
    true_var_perfect = np.matmul(np.matmul(w_perfect.T, true_cov), w_perfect)

    uniform_var_ratio = true_var_uniform/true_var_perfect
    block_var_ratio = true_var_block/true_var_perfect
    ridge_var_ratio = true_var_ridge/true_var_perfect

    ridge_pre_error = np.linalg.norm(ridge_pre-true_pre)
    block_pre_error = np.linalg.norm(block_pre-true_pre)


    if true_var_block < min( true_var_ridge, true_var_uniform):
        print('*** BETTER ***')
    else:
        print('*** WORSE ***')

    from collections import OrderedDict
    report = OrderedDict({'optimal_var':true_var_perfect,'uniform_var':true_var_uniform,'block_var':true_var_block,'ridge_var':true_var_ridge,
              'block_ratio':block_var_ratio, 'uniform_ratio':uniform_var_ratio,
                          'ridge_ratio':ridge_var_ratio,
              'block_pre_norm':block_pre_error,'conv_pre_norm':ridge_pre_error,
              'w1':w_block[:10],'w2':w_ridge[:10],'wt':w_perfect[:10]})
    pprint(report)
    if False:
        print('---implied sgma-')
        pprint(block_cov[:5,:5])
        print('---true sgma-')
        pprint(true_cov[:5,:5])
        print('---conventional-')
        pprint(emp_cov[:5,:5])
        print('---block precision---')
        pprint(pre['pre'])
        print('---true precision---')
        pprint(np.linalg.inv(true_cov[:5,:5]))
        print('---conv precision---')
        pprint(ridge_pre[:5,:5])


if __name__=='__main__':
    test_fixed_rpre_init()
