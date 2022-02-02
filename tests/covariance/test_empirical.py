

import numpy as np
from precise.skaters.covariance.runempfactory import emp_pcov, merge_emp_scov
from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef
from precise.skaters.covarianceutil.datafunctions import data_population_covariance

# Some cut and paste https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
# However I've removed the confusion between sample and population estimates, and taken the tolerance
# down to 1e-10 

TOL = 1E-10


def test_onlineempirical():
    data = create_correlated_dataset(100, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))

    np_corrcoef = np.corrcoef(data, rowvar=False)
    s = {}
    for j,x in enumerate(data[:2]):
        s = emp_pcov(s=s, x=x, k=1)
        if j>=1:
            np_mean = np.mean(data[:j+1,:],axis=0)
            np_pcov = np.cov(data[:j+1,:], rowvar=False, bias=True)
            np_pcov2 = data_population_covariance(data[:j + 1, :])
            np_corrcoef = np.corrcoef(data[:j+1,:], rowvar=False)
            ocorr = cov_to_corrcoef(s['pcov'])
            assert np.isclose(np_pcov, s['pcov'], atol=TOL).all()
            assert np.isclose(np_pcov2, s['pcov'], atol=TOL).all()
            assert np.isclose(np_mean, s['mean'], atol=TOL).all()
            assert np.isclose(np_corrcoef, ocorr, atol=TOL).all()



def test_merging():
    data_part1 = create_correlated_dataset(500, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7], [0.3, 0.2, 0.2], [0.5, 0.3, 0.1]]), (1, 5, 3))
    data_part2 = create_correlated_dataset( \
        1000, (5, 6, 2), np.array([[0.2, 0.5, 0.7], [0.3, 0.2, 0.2], [0.5, 0.3, 0.1]]), (1, 5, 3))
    ocov_part1 = {}
    ocov_part2 = {}
    ocov_both = {}

    for row in data_part1:
        ocov_part1 = emp_pcov(s=ocov_part1, x=row)
        ocov_both = emp_pcov(s=ocov_both, x=row)

    for row in data_part2:
        ocov_part2 = emp_pcov(s=ocov_part2, x=row)
        ocov_both = emp_pcov(s=ocov_both, x=row)

    ocov_merged = merge_emp_scov(s=ocov_part1, other_s=ocov_part2)
    assert ocov_both['n_samples'] == ocov_merged['n_samples']
    assert np.isclose(ocov_both['mean'], ocov_merged['mean']).all()
    assert np.isclose(ocov_both['pcov'], ocov_merged['pcov']).all()


if __name__=='__main__':
    test_onlineempirical()
    test_merging()
