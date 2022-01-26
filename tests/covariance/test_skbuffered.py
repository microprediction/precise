import numpy as np
from precise.skaters.covariance.bufsk import BUF_SK_D0_SKATERS
from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset


def test_random_buffered_sk_d0():
    data = create_correlated_dataset(100, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))
    for _ in range(5):
        f = np.random.choice(BUF_SK_D0_SKATERS)
        s = {}
        for j,y in enumerate(data[:100]):
            x, x_cov, s = f(s=s, y=y, k=1)




if __name__=='__main__':
    test_random_buffered_sk_d0()