from precise.skatertools.syntheticdata.factor import create_factor_dataset
import numpy as np
import pandas as pd


def test_rpl_hc_direct():
    import riskfolio as rpl
    xs = create_factor_dataset(n=200,n_dim=25)
    returns = pd.DataFrame(data=xs)
    port = rpl.HCPortfolio(returns=returns)
    w = port.optimization(model='HRP')
    assert len(w)==len(xs[0])
    assert np.allclose(np.sum(w.values),1.0)


def test_rpl_hc():
    xs = create_factor_dataset(n=200, n_dim=25)
    from precise.skaters.managers.rflmanagerfactory import _rpl_func
    w = _rpl_func(xs=xs, port_cls_name='HCPortfolio')
    assert len(w)==len(xs[0])
    assert np.allclose(sum(w),1.0)


if __name__=='__main__':
    test_rpl_hc_direct()
    test_rpl_hc


