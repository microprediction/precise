import numpy as np
from precise.synthetic.generate import create_correlated_dataset, create_factor_dataset
from precise.covariance.ledoitwolf import lw_ema_scov
from pprint import pprint


def test_lw():
    data = create_correlated_dataset(100)
    data = create_factor_dataset(1000,n_dim=25)

    from sklearn.covariance._shrunk_covariance import ledoit_wolf_shrinkage
    shrk_true = ledoit_wolf_shrinkage(X=data[-80:], assume_centered=True)
    shrk_false = ledoit_wolf_shrinkage(X=data[-80:], assume_centered=False)

    s = {}
    for x in data:
        s = lw_ema_scov(s=s, x=x, r=0.05)

    del s['s_c']
    del s['scov']
    del s['buffer']
    if False:
        pprint(s)
        print({'shrk_true': shrk_true,'shrk_false':shrk_false})





if __name__=='__main__':
    test_lw()