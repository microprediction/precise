import numpy as np
from precise.skaters.covariance.weakewa import WEAK_EWA_DO_COV_SKATERS
from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset


def test_random_cov_skater():
    data = create_correlated_dataset(400, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))
    for _ in range(1):
        f = np.random.choice(WEAK_EWA_DO_COV_SKATERS)
        s = {}
        for j,y in enumerate(data[:105]):
            x, x_cov, s = f(s=s, y=y, k=1)
            assert (np.diag(x_cov) >= 0).all()


if __name__=='__main__':
    for _ in range(50):
        test_random_cov_skater()