
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.precision.fixed import fixed_rpre_init, fixed_rpre_update
from precise.covariance.util import multiply_diag, normalize
from precise.covariance.generate import create_correlated_dataset, create_factor_dataset
from pprint import pprint
from precise.covariance.adjacency import infer_adjacency

def test_fixed_rpre_init():
    n_dim = 50
    big_data = create_factor_dataset(n=10000, n_dim=n_dim)
    true_cov = np.cov(big_data, rowvar=False)
    true_pre = np.linalg.inv(true_cov)

    lmbd = 1.5
    small_data = big_data[:5000]
    small_cov = np.cov(small_data,rowvar=False)
    small_pre = np.linalg.inv(multiply_diag(small_cov, lmbd=lmbd))
    adj = infer_adjacency(small_pre)

    data = big_data[:100]
    conventional_cov = np.cov(data, rowvar=False)

    sgma = multiply_diag(conventional_cov, lmbd=lmbd, make_copy=True)
    cpre = np.linalg.inv(sgma) # Conventional

    rho = 0.05
    pre = fixed_rpre_init(adj=adj, rho=rho)
    for x in data:
        pre = fixed_rpre_update(m=pre, x=x, with_precision=True, lmbd=lmbd)
    #pprint(pre['pre'][:5,:5])
    #pprint(cpre[:5,:5])
    implied_sgma = np.linalg.inv(pre['pre'])
    n_dim = np.shape(big_data)[1]
    wones = np.ones(shape=(n_dim,1))
    w1 = normalize( np.squeeze(np.matmul( pre['pre'],wones )) )
    w2 = normalize( np.squeeze(np.matmul( cpre, wones)))
    w_tru = normalize( np.squeeze(np.matmul( true_pre, wones)))
    w_uniform = normalize( np.copy(wones))
    true_var_u = np.squeeze(np.matmul(np.matmul(w_uniform.T, true_cov), w_uniform))
    true_var_1 = np.matmul(np.matmul( w1.T, true_cov), w1)
    true_var_2 = np.matmul(np.matmul( w2.T, true_cov), w2)
    true_var_0 = np.matmul(np.matmul(w_tru.T, true_cov), w_tru)

    if true_var_1<true_var_2:
        print('*** BETTER ***')
    else:
        print('*** WORSE ***')

    report = {'var1':true_var_1,'var2':true_var_2,'vart':true_var_0,'varu':true_var_u,'w1':w1[:10],'w2':w2[:10],'wt':w_tru[:10]}
    pprint(report)
    print('---implied sgma-')
    pprint(implied_sgma[:5,:5])
    print('---true sgma-')
    pprint(true_cov[:5,:5])
    print('---conventional-')
    pprint(conventional_cov[:5,:5])
    print('---block precision---')
    pprint(pre['pre'])
    print('---true precision---')
    pprint(np.linalg.inv(true_cov[:5,:5]))
    print('---conv precision---')
    pprint(cpre[:5,:5])


if __name__=='__main__':
    test_fixed_rpre_init()
