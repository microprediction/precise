from precise.synthetic.generate import create_correlated_dataset
from precise.covariance.empirical import ecov_init, ecov_update
from pprint import pprint

# Basic example of running covariance

if __name__=='__main__':
    xs = create_correlated_dataset(n=500)
    ocov = ecov_init(n_dim=xs.shape[1])
    for x in xs:
        ocov = ecov_update(m=ocov, x=x)
    pprint(ocov)
