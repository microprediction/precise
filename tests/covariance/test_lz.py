
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.skaters.covariance.ewalzfactory import _lz_scov_init, _lz_scov_update
from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
from precise.skaters.covariance.ewaempfactory import _ema_scov_update, _ema_scov_init


def test_fixed_rcov():
    data = create_correlated_dataset(9, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))
    conventional_cov = np.cov(data, rowvar=False)
    adjacency = np.array( [[1,1,0],[1,1,0],[0,0,1]] )
    rho = 0.01
    kcov = _lz_scov_init(adj=adjacency, rho=rho)
    for observation in data:
        kcov = _lz_scov_update(m=kcov, x=observation)

    # Check against running
    data01 = data[:,:2]
    cov01 = _ema_scov_init(n_dim=2, r=rho)
    for x in data01:
        cov01 = _ema_scov_update(s=cov01, x=x)
    assert np.allclose(cov01['scov'],kcov['states'][0]['scov'] )


if __name__=='__main__':
    test_fixed_rcov()