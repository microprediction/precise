from precise.covariance.generate import create_correlated_dataset
from precise.covariance.empirical import cov_init
import numpy as np
from pprint import pprint
from precise.covariance.util import cov_to_corrcoef

if __name__=='__main__':
    data = create_correlated_dataset(10000, (2.2, 4.4, 1.5),
                                     np.array([[0.2, 0.5, 0.7], [0.3, 0.2, 0.2], [0.5, 0.3, 0.1]]), (1, 5, 3))
    ocov = cov_init(n_dim=data.shape[1])
    for observation in data:
        ocov = cov_init(m=ocov, x=observation)

    ocorr = cov_to_corrcoef(ocov['cov'])
    pprint(ocorr)
