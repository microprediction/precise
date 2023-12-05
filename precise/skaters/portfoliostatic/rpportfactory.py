
import numpy as np
from precise.skaters.covarianceutil.covfunctions import try_invert
from precise.inclusion.riskparityportfolioinclusion import using_riskparityportfolio

if using_riskparityportfolio:
    import riskparityportfolio as rp
    from precise.skaters.portfolioutil.portfunctions import var_scaled_returns
    import pandas as pd
    from precise.skaters.covarianceutil.covfunctions import multiply_off_diag
    from precise.skaters.portfoliostatic.equalport import equal_long_port
    from precise.skaters.covarianceutil.covrandom import jiggle_cov
    from precise.skaters.covarianceutil.covfunctions import to_symmetric, nearest_pos_def


    # Thin wrapper for riskparityportfolio package

    def rp_portfolio_factory(pre=None, cov=None, mu=0.02, risk_free_rate=0.02, phi=1.0, noise=0.0):
        """ Signed min var portfolio summing to unity """

        if cov is None:
            cov = try_invert(pre)
        cov = multiply_off_diag(cov,phi=phi)

        expected_returns = var_scaled_returns(cov=cov,mu=mu,r=risk_free_rate)

        if noise>1e-12:
            # Jiggle cov
            jiggled_cov = jiggle_cov(cov=cov)
        else:
            jiggled_cov = np.copy(cov)

        # Tidy up cov and send to optimizer ... repeatedly with more shrinkage as needed
        shrunk_cov = nearest_pos_def(to_symmetric(jiggled_cov))

        w = rp.vanilla.design(shrunk_cov, b=expected_returns)
        if any([np.isnan(wi) for wi in w]):
            return equal_long_port(cov=cov)
        return w




