
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.covariance.empirical import _emp_pcov_init, _emp_pcov_update
from precise.covariance.movingaverage import _ema_scov_init, _ema_scov_update
from precise.synthetic.generate import create_correlated_dataset


def test_same_burn_in():
    data = create_correlated_dataset(9, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))
    conventional_cov = np.cov(data, rowvar=False)
    ocov = _emp_pcov_init(n_dim=data.shape[1])
    for observation in data:
        ocov = _emp_pcov_update(s=ocov, x=observation)
    rcov = _ema_scov_init(n_dim=data.shape[1])
    for observation in data:
        rcov = _ema_scov_update(s=rcov, x=observation)

    assert np.isclose(rcov['pcov'], ocov['pcov']).all()

def test_diag():
    data = create_correlated_dataset(19, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7], [0.3, 0.2, 0.2], [0.5, 0.3, 0.1]]),
                                     (1, 5, 3))
    from momentum import rvar_init, rvar_update
    rho = 0.05
    r1 = rvar_init(rho=rho,n=1)
    r = _ema_scov_init(r=rho, n_dim=3, n_emp=1)
    for observation in data:
        r = _ema_scov_update(s=r, x=observation)
        c = r['scov'][0, 0]
        r1 = rvar_update(m=r1,x=observation[0])
        c1 = r1['var']
        assert np.isclose(c,c1)








if __name__=='__main__':
    test_same_burn_in()
    test_diag()