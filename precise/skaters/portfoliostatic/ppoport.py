from precise.skaters.portfoliostatic.ppoportfactory import _ppo_portfolio, PPO_LONG_BOUNDS, PPO_UNIT_BOUNDS

# Using PyPortfolioOpt, with some minor tweaks


def ppo_sharpe_long_port(cov=None, pre=None, as_dense=True):
    return _ppo_portfolio(method='max_sharpe', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_LONG_BOUNDS)


def ppo_vol_long_port(cov=None, pre=None, as_dense=True):
    return _ppo_portfolio(method='min_volatility', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_LONG_BOUNDS)


def ppo_quad_long_port(cov=None, pre=None, as_dense=True):
    return _ppo_portfolio(method='max_quadratic_utility', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_LONG_BOUNDS)


def ppo_sharpe_port(cov=None, pre=None, as_dense=True):
    return _ppo_portfolio(method='max_sharpe', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_UNIT_BOUNDS)


def ppo_vol_port(cov=None, pre=None, as_dense=True):
    return _ppo_portfolio(method='min_volatility', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_UNIT_BOUNDS)


def ppo_quad_port(cov=None, pre=None, as_dense=True):
    return _ppo_portfolio(method='max_quadratic_utility', cov=cov, pre=pre, as_dense=as_dense, weight_bounds=PPO_UNIT_BOUNDS)


PPO_LONG_PORT = [ ppo_sharpe_long_port, ppo_vol_long_port, ppo_quad_long_port ]
PPO_PORT =  PPO_LONG_PORT + [ ppo_sharpe_port, ppo_vol_port, ppo_quad_port   ]