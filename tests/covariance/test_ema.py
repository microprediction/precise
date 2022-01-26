
# Ack: https://carstenschelp.github.io/2019/05/12/Online_Covariance_Algorithm_002.html
import numpy as np
from precise.skaters.covariance.runempfactory import emp_pcov
from precise.skaters.covariance.ewaempfactory import ema_scov
from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
from momentum import rvar


def test_same_burn_in():
    data = create_correlated_dataset(9, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7],[0.3, 0.2, 0.2],[0.5,0.3,0.1]]), (1, 5, 3))
    conventional_cov = np.cov(data, rowvar=False)
    se = {}
    for x in data:
        se = emp_pcov(s=se, x=x)

    sm = {}
    for x in data:
        sm = ema_scov(s=sm, x=x)

    assert np.isclose(se['pcov'], sm['pcov']).all()


def test_diag():
    data = create_correlated_dataset(19, (2.2, 4.4, 1.5), np.array([[0.2, 0.5, 0.7], [0.3, 0.2, 0.2], [0.5, 0.3, 0.1]]),
                                     (1, 5, 3))
    rho = 0.05
    r0 = {}
    r1 = {}
    for k,x in enumerate(data):
        r1 = ema_scov(s=r1, x=x,r=rho)
        r0 = rvar(m=r0,x=x[0],rho=rho)
        if k >= 1:
            c = r1['scov'][0, 0]
            c1 = r0['var']
            assert np.isclose(c,c1)








if __name__=='__main__':
    test_same_burn_in()
    test_diag()