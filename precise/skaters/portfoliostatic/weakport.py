from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory


# Fast long-only approximately min-var portfolios where the only constraints are sum(w)=1, w>0

def weak_long_port(cov=None, pre=None):
    """
          Approximately min-var portfolio using optimized weakening parameter b
    """
    return weak_portfolio_factory(cov=cov, pre=pre, a=1.0, b=None, with_neg_mass=False)



WEAK_LONG_PORT = [weak_long_port]
WEAK_LS_PORT = []
WEAK_PORT = WEAK_LONG_PORT + WEAK_LS_PORT

