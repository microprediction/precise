import numpy as np
from precise.skaters.covariance.movingaveragepre import ema_scov
from precise.skaters.covariance.huberpre import huber_pcov
from precise.skatertools.syntheticdata.factor import create_factor_dataset
from precise.skaters.covarianceutil.matrixfunctions import cov_to_corrcoef
from pprint import pprint

TOL = 1E-10


def test_against_emp():
    big_data = create_factor_dataset(n=1000,n_dim=10)
    tru_corr = np.corrcoef(big_data, rowvar=False)
    tru_cov = np.cov(big_data, rowvar=False)

    data = big_data[:500]
    n_obs, n_dim = np.shape(data)

    # Pollute sample with affine noise
    multi_noise = 5.0
    add_noise = 5.0
    mean_std = np.std(data)
    for i in range(n_obs):
        data[i,i % n_dim] = data[i,i % n_dim]*np.random.choice([multi_noise])+np.random.randn()*add_noise*mean_std

    np_corrcoef = np.corrcoef(data, rowvar=False)
    s_emp = {}
    s_hub = {}
    b = 3.0
    a = 1.0
    r = 0.025
    n_buffer=int(2/r)
    for k,x in enumerate(data):
        if k>10:
            pass
            # print('now')
        if k>n_obs-3*n_buffer:
            s_emp = ema_scov(s=s_emp, x=x, r=r)
        s_hub = huber_pcov(s=s_hub, x=x, a=a, b=b, r=r, n_buffer=n_buffer)
    ratio1 = s_hub['pcov_e']/s_emp['pcov']
    ratio2 = s_hub['pcov']/s_emp['pcov']
    print('emp_check/emp')
    pprint(ratio1)
    print('huber/emp')
    pprint(ratio2)
    s_hub['pcorr'] = cov_to_corrcoef(s_hub['pcov'])
    s_emp['pcorr'] = cov_to_corrcoef(s_emp['pcov'])
    print('huber corr')
    print(s_hub['pcorr'])
    print('huber corr ratio')
    print(s_hub['pcorr']/s_emp['pcorr'])
    print('true corr')
    print(tru_corr)
    print('huber corr error')
    print(s_hub['pcorr']-tru_corr)
    print('emp corr error')
    print(s_emp['pcorr'] - tru_corr)
    print(np.linalg.norm(s_emp['pcorr'] - tru_corr))
    print(np.linalg.norm(s_hub['pcorr'] - tru_corr))
    print('huber corr ratio')
    print(s_hub['pcorr']/tru_corr)
    print('emp corr ratio')
    print(s_emp['pcorr'] / tru_corr)
    hub_inv = np.linalg.inv(s_hub['pcorr'])
    emp_inv = np.linalg.inv(s_emp['pcorr'])
    tru_inv = np.linalg.inv(tru_corr)
    pprint({'inv hub':np.linalg.norm(hub_inv-tru_inv),
            'inv emp': np.linalg.norm(emp_inv - tru_inv),
            'cov hub':np.linalg.norm(s_hub['pcov'] - tru_cov),
            'cov emp': np.linalg.norm(s_emp['pcov'] - tru_cov),
            'corr hub': np.linalg.norm(s_hub['pcorr'] - tru_corr),
            'corr emp': np.linalg.norm(s_emp['pcorr'] - tru_corr)
            })



if __name__=='__main__':
    test_against_emp()
