from precise.covariance.generate import create_correlated_dataset
from precise.covariance.empirical import cov_init, cov_update
from pprint import pprint
from precise.covariance.util import cov_to_corrcoef

# Basic example of running correlation matrix

if __name__=='__main__':
    data = create_correlated_dataset(n=5000)
    ocov = cov_init(n_dim=data.shape[1])
    for x in data:
        ocov = cov_update(m=ocov, x=x)
    ocorr = cov_to_corrcoef(ocov['pcov'])
    pprint(ocorr)
