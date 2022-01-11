from precise.covariance.generate import create_correlated_dataset
from precise.covariance.empirical import cov_init, cov_update
from pprint import pprint

# Basic example of running covariance

if __name__=='__main__':
    xs = create_correlated_dataset(n=500)
    ocov = cov_init(n_dim=xs.shape[1])
    for x in xs:
        ocov = cov_update(m=ocov, x=x)
    pprint(ocov)
