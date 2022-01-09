
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.covariance.empirical import cov_init, cov_update
from precise.covariance.recent import rcov_init, rcov_update
from precise.covariance.util import create_correlated_dataset


def test_same_burn_in():
    data = create_correlated_dataset(9, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))
    conventional_cov = np.cov(data, rowvar=False)
    ocov = cov_init(n_dim=data.shape[1])
    for observation in data:
        ocov = cov_update(m=ocov, x=observation)
    rcov = rcov_init(n_dim=data.shape[1])
    for observation in data:
        rcov = rcov_update(m=rcov, x=observation)

    assert np.isclose(rcov['pcov'], ocov['pcov']).all()

def test_diag():
    data = create_correlated_dataset(19, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7], [0.3, 0.2, 0.2], [0.5, 0.3, 0.1]]),
                                     (1, 5, 3))
    from momentum import rvar_init, rvar_update
    rho = 0.05
    r1 = rvar_init(rho=rho,n=1)
    r = rcov_init(rho=rho, n_dim=3, n_cold=1)
    for observation in data:
        r = rcov_update(m=r, x=observation)
        c = r['cov'][0, 0]
        r1 = rvar_update(m=r1,x=observation[0])
        c1 = r1['var']
        assert np.isclose(c,c1)








if __name__=='__main__':
    test_same_burn_in()
    test_diag()