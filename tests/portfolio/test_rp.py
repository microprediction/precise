from precise.skaters.covarianceutil.covrandom import random_band_cov
from precise.inclusion.riskparityportfolioinclusion import using_riskparityportfolio
if using_riskparityportfolio:
    from precise.skaters.portfoliostatic.rpportfactory import rp_portfolio_factory
    import numpy as np
    from precise.skaters.locationutil.vectorfunctions import scatter


    def test_rp():
        cov = random_band_cov(n_dim=5)
        print(np.shape(cov))
        w = rp_portfolio_factory(cov=cov)
        assert len(w) == np.shape(cov)[0], ' dim mismatch '
        contrib = w * np.dot(cov, w)
        print(contrib)


    def test_rp_diag():
        cov = np.diag(list(np.ones(5)) + list(2 * np.ones(5)))
        print(np.shape(cov))
        w = rp_portfolio_factory(cov=cov, mu=0.02, risk_free_rate=0.02)
        assert len(w) == np.shape(cov)[0], ' dim mismatch '
        contrib = w * np.dot(cov, w)
        print(contrib)


if __name__ == '__main__':
    if using_riskparityportfolio:
        test_rp()
