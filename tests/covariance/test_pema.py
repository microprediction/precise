
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.covariance.movingpartial import _pema_scov_init, _pema_scov_update
from precise.covariance.movingaverage import _ema_scov_update, _ema_scov_init
from precise.covariance.empirical import emp_pcov
from precise.synthetic.generate import create_correlated_dataset
from pprint import pprint


def test_compare():
    data = create_correlated_dataset(10000, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))

    known_mean = np.mean(data,axis=0)

    # Partial moments
    r = 0.001
    s1 = _pema_scov_init(n_dim=data.shape[1],target=known_mean)
    for x in data:
        s1 = _pema_scov_update(s=s1, x=x,r=r)

    from precise.covariance.matrixfunctions import cov_to_corrcoef
    corr1 = cov_to_corrcoef(s1['scov'])

    # MA
    s2 = _ema_scov_init(n_dim=data.shape[1])
    for x in data:
        s2 = _ema_scov_update(s=s2, x=x, r=r)

    # Empirical cov
    s3 = {}
    for x in data:
        s3 = emp_pcov(s=s3,x=x)

    pprint(corr1)
    print('--partial--')
    pprint(s1['scov'])
    print('---ma cov---')
    pprint(s2['scov'])
    print('--- emp cov ---')
    pprint(s3['pcov'])

    s12ratio = s1['scov']/s2['scov']
    print('-- ratio of MA cov to MA partial cov --')
    s23ratio = s2['scov']/s3['pcov']

    pprint(s23ratio)
    pass




if __name__=='__main__':
    test_compare()