# Using the portfolio functions

1. Choose a "port" by browsing [portfoliostatic](https://github.com/microprediction/precise/tree/main/precise/skaters/portfoliostatic).
2. Import it
3. Pass it either a covariance or a precision matrix

### Example usage
We need a cov matrix

       import numpy as np
       cov = np.array([[ 1.09948514, -1.02926114,  0.22402055,  0.10727343],
               [-1.02926114,  2.54302628,  1.05338531, -0.12481515],
               [ 0.22402055,  1.05338531,  1.79162765, -0.78962956],
               [ 0.10727343, -0.12481515, -0.78962956,  0.86316527]])

Then:

     from precise.skaters.portfoliostatic.unitport import unit_port
     w = unit_port(cov=cov)
     
     
### Model ensembles, stacking, mixtures of experts et cetera
Same thing, sort of. See this [notebook example](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/lazypredict_model_portfolio.ipynb) or [these examples](https://github.com/microprediction/precise/tree/main/examples_portfolios/ensembles).  

     
### Interpreting portfolio names


| PyPortfolioOpt | Intent                                                           |
|-----------|------------------------------------------------------------------|
| ppo       | Uses the PyPortfolioOpt package                                  |
| ppo_vol   |      ... and minimum volatility therein                          |
| ppo_quad  |      ... and maximum quadratic utility therein                   |
| ppo_sharpe|      ... and maximum Sharpe ratio therein                        |

| Riskfolio-Lib | Intent                                                           |
|-----------|------------------------------------------------------------------|
| rpl       | Uses the RiskFolio-Lib package                                   |
| rpl_hrp   |      ... and Hierarchical Risk Parity therein                    |
| rlp_hrp_cdar |          ... and Conditional Drawdown at Risk of uncompounded cumulative returns | 
| rlp_hrp_flpm |          ... and First Lower Partial Moment therein            | 
|           |          ... et cetera (see [the rest](https://github.com/microprediction/precise/blob/main/precise/skaters/managers/rplmanagers.py))    |  

| Homespun  | Intent                                                           |
|-----------|------------------------------------------------------------------|
| diag      | Use only diagonal entries of cov                                 |
| weak      | Method that "weakens" some cov entries to make portfolio long only        | 
| hrp       | Varieties of hierarchical allocation                             | 
| hrp_diag_diag |   ... and uses "diag" allocation/portfolio, like Lopez de Prado's 2016 paper   | 
| hrp_weak_weak |   ... and uses "weak" allocation and also "weak" portfolio construction.       | 
| schur     | Homespun method that exploits Schur complements |
| schur_weak_diag     |    ... and uses weak allocation and diag portfolio at the leaves  |

At present "weak" and "schur" are the only methods you may have trouble finding implemented elsewhere. The latter is my attempt to unify seemingly disparate approaches: namely those using a global optimization versus those using divide and conquer. 

### Other places to rummage
... for functionality. 

- [covarianceutil](https://github.com/microprediction/precise/tree/main/precise/skaters/covarianceutil) 
- [locationutil](https://github.com/microprediction/precise/tree/main/precise/skaters/locationutil) 
- [portfoliostatic](https://github.com/microprediction/precise/tree/main/precise/skaters/portfoliostatic) or [portfolioutil](https://github.com/microprediction/precise/tree/main/precise/skaters/portfolioutil)
     

-+-

Documentation [home](https://microprediction.github.io/precise)
