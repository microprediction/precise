import numpy as np
from precise.skaters.covariance.ewalz import EWA_LZ_D0_COV_SKATERS
from precise.skatertools.syntheticdata.factor import create_disjoint_factor_dataset


def test_random_partial_moving():
    n_dims = [5,3,3,3,2,2]
    data = create_disjoint_factor_dataset(n=500,n_dims=n_dims)
    f = np.random.choice(EWA_LZ_D0_COV_SKATERS)
    print(f.__name__)
    s = {}
    for j,y in enumerate(data):
        x, x_cov, s = f(s=s, y=y, k=1)


if __name__=='__main__':
    test_random_partial_moving()