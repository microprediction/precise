

import numpy as np
from precise.skaters.covariance.bufferedempirical import buf_pcov_d0_n20, buf_pcov_d1_n100
from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
from precise.skaters.covarianceutil.matrixfunctions import cov_to_corrcoef, np_pcorrcoef


TOL = 1E-10


def test_empirical_buffer():
    data = create_correlated_dataset(100, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))
    s = {}
    for j,y in enumerate(data[:5]):
        x, x_cov, s = buf_pcov_d0_n20(s=s, y=y, k=1)
        if j>=1:
            np_mean = np.mean(data[:j+1,:],axis=0)
            np_pop_cov = np.cov(data[:j+1,:], rowvar=False, bias=True)
            np_corrcoef = np.corrcoef(data[:j+1,:], rowvar=False)
            np_corrcoef2 = np_pcorrcoef(data[:j+1,:])
            ocorr = cov_to_corrcoef(x_cov)
            assert np.isclose(np_pop_cov, x_cov, atol=TOL).all()
            assert np.isclose(np_mean, x, atol=TOL).all()
            assert np.isclose(np_corrcoef, ocorr, atol=TOL).all()
            assert np.isclose(np_corrcoef2, ocorr, atol=TOL).all()

if __name__=='__main__':
    test_empirical_buffer()
