from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef
import numpy as np
from precise.skaters.locationutil.vectorfunctions import normalize


def zeta_port(port, cov, zeta=None, **port_kwargs):
    """
         Creates a compromise between cov and corr induced portfolios
         Just an idea. Not particularly well studied :)
    :param port:
    :param cov:
    :param zeta:
    :param port_kwargs:
    :return:
    """
    if zeta is None or abs(zeta)<1e-10:
        return port(cov=cov, **port_kwargs)
    else:
        w_cov = port(cov=cov, **port_kwargs)
        x_diag = np.diag(cov)
        x_corr = cov_to_corrcoef(cov)
        w_corr_raw = port(cov=x_corr, **port_kwargs)
        w_corr = normalize(w_corr_raw / x_diag)
        w = (1 - zeta)*np.array(w_cov) + zeta*np.array(w_corr)
        return list(w)