from precise.skaters.covarianceutil.covrandom import random_band_cov
from precise.skaters.portfolioutil.parity import prc_hrp_diag_5
from precise.skaters.portfolioutil.enhanced import prc_ep_diag_5
import numpy as np
from pprint import pprint


def test_equivalence():
    cov = random_band_cov()
    w_hrp = prc_hrp_diag_5(cov=cov)
    w_ep = prc_ep_diag_5(cov=cov)
    if not np.allclose(w_ep,w_hrp):
        w_ratio = w_ep/w_hrp
        pprint(w_ratio)



if __name__=='__main__':
    test_equivalence()
