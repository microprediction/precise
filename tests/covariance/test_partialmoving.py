import numpy as np
from precise.skaters.covariance.ewapm import EWA_PM_EMP_D0_COV_SKATERS
from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset


def test_random_partial_moving():
    data = create_correlated_dataset(100, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))
    for _ in range(5):
        f = np.random.choice(EWA_PM_EMP_D0_COV_SKATERS)
        s = {}
        for j,y in enumerate(data[:100]):
            x, x_cov, s = f(s=s, y=y, k=1)
            assert (np.diag(x_cov) >= 0).all()


if __name__=='__main__':
    test_random_partial_moving()