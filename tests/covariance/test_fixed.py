
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.covariance.fixed import fixed_rcov_init, fixed_rcov_update
from precise.covariance.generate import create_correlated_dataset
from precise.covariance.recent import rcov_update, rcov_init


def test_fixed_rcov():
    data = create_correlated_dataset(9, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))
    conventional_cov = np.cov(data, rowvar=False)
    adjacency = np.array( [[1,1,0],[1,1,0],[0,0,1]] )
    rho = 0.01
    kcov = fixed_rcov_init(adj=adjacency, rho=rho)
    for observation in data:
        kcov = fixed_rcov_update(m=kcov, x=observation)

    # Check against running
    data01 = data[:,:2]
    cov01 = rcov_init(n_dim=2,rho=rho)
    for x in data01:
        cov01 = rcov_update(m=cov01, x=x)
    assert np.allclose(cov01['cov'],kcov['states'][0]['cov'] )


if __name__=='__main__':
    test_fixed_rcov()