# precise ![tests](https://github.com/microprediction/precise/workflows/tests/badge.svg) ![tests-scipy-173](https://github.com/microprediction/precise/workflows/tests-scipy-173/badge.svg)![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## TLDR: "Functions that forecast covariance in online fashion"
... and some that produce portfolios, weights for mixtures of models, et cetera. This is a collection of incremental estimators
for covariance, precision, correlation, portfolios and ensembles that have very simple signatures. The [running_empirical_covariance](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/running_empirical_population_covariance.ipynb) colab notebook illustrates the style. To see all the other online methods of covariance estimation supplied here, run the [cov skaters manifest](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/list_all_cov_methods.ipynb) notebook. Or to look at Elo ratings,
run the [elo_ratings_and_urls](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/elo_ratings_and_code_urls.ipynb). 


## Install 

    pip install precise 
    
or for latest:

    pip install git+https://github.com/microprediction/precise.git

## M6 Financial forecasting contest
You *could* use this library to enter the M6 Financial Forecasting competition, if you wish. 

   1. Pick a cov estimator (i.e. a "cov skater"), if you wish
   2. Pick a portfolio generator, if you wish
   3. Pick extra shrinkage params, if you wish
   4. Pick love and hate ticker lists, if you wish

See [precise/examples_m6](https://github.com/microprediction/precise/tree/main/examples_m6) and register at the [m6 competition](https://m6competition.com/). See disclaimer below and note that ideally, it would be even better if you create new methods for step 1. above an make a pull request!    

# Covariance skaters and their [Elos](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/elo_ratings_and_code_urls.ipynb)
Similar in style to skaters used in the [timemachines](https://github.com/microprediction/timemachines) package, this package may be thought of as a collection of covariance prediction functions taking one vector at a time, and also the prior state, and spitting out a prediction mean vector *x*, a prediction covariance *x_cov*, and a posterior state whose interpretation is the responsibility of the skater, not the caller. 

    from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
    from precise.skaters.covariance.runemmp import run_emp_pcov_d0 # <-- Running empirical population covariance
    from pprint import pprint

    if __name__=='__main__':
        ys = create_correlated_dataset(n=500)
        s = {}
        for y in ys:
            x, x_cov, s = run_emp_pcov_d0(s=s, y=y)
        pprint(x_cov)
     
See [/examples_basic_usage](https://github.com/microprediction/precise/tree/main/examples_basic_usage). And yes, this mildly unusual convention requires the caller to maintain state from one call to the next:  See the timemachines [faq](https://github.com/microprediction/timemachines/blob/main/FAQ.md) for justification of this style. 
          
### Browsing for skaters
     
You can hunt for skaters other than *run_emp_pcov_d0* in [precise/skaters/covariance](https://github.com/microprediction/precise/tree/main/precise/skaters/covariance). There are some location utilities in [precise/whereami](https://github.com/microprediction/precise/blob/main/precise/whereami.py). As noted, see the [elo_ratings_and_urls](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/elo_ratings_and_code_urls.ipynb) which may, or may not, help guide you.  


### Interpreting skater names 
Examples:

| Skater name            | Location   | Meaning            |
|------------------------|------------|--------------------|
| buf_huber_pcov_d1_a1_b2_n50 | [skaters/covariance/bufhuber](https://github.com/microprediction/precise/blob/main/precise/skaters/covariance/bufhuber.py) | Applies an approach that exploits Huber pseudo-means to a buffer of data of length 50 in need of differencing once, with generalized Huber loss parameters a=1, b=2. | 
| buf_sk_ld_pcov_d0_n100 | [skaters/covariance/bufsk](https://github.com/microprediction/precise/blob/main/precise/skaters/covariance/bufsk.py) | Applies sk-learn's implementation of Ledoit-Wolf to stationary buffered data of length 100 | 
| ewa_pm_emp_scov_r01 | [skaters/covariance/ewapartial](https://github.com/microprediction/precise/blob/main/precise/skaters/covariance/ewapartial.py) | Performs an incremental, recency-weighted sample covariance estimate that exploits partial moments. Uses a memory parameter r=0.01 | 

Broad calculation style categories

| Shorthand | Interpretation                                                                  | Incremental ? |
|-----------|---------------------------------------------------------------------------------|---------------|
| buf       | Performs classical batch calculation on a fixed window of data each time        | No            |
| win       | Performs incremental fixed window calculation.                                  | Yes           |
| run       | Running calculation weighing all observations equally                           | Yes           |  
| ewa       | Running calculation weighing recent observations more                           | Yes           |

Methodology hints (can be combined)

| Shorthand | Inspiration                            |
|-----------|----------------------------------------|
| emp       | "Empirical" (not shrunk or augmented)  |
| lz        | Le-Zhong variable-by-variable updating |
| lw        | Ledoit-Wolf                            |
| pm        | Partial moments                        | 
| huber     | Generalized Huber pseudo-mean          |
| oas       | Oracle approximating shrinkage.        |
| gl        | Graphical Lasso                        |
| mcd       | Minimum covariance determinant         |

Intended main target (more than one may be produced in the state)

| Shorthand | Intent                            |
|-----------|-----------------------------------|
| scov      | Sample covariance                 |
| pcov      | Population covariance             |
| spre      | Inverse of sample covariance      |
| ppre      | Inverse of population covariance  |
     
Differencing hints:

| Shorthand | Intent                                                  |
|-----------|---------------------------------------------------------|
| d0        | For use on stationary, ideally IID data                 |
| d1        | For use on data that is iid after taking one difference | 
     

### Stand-alone covariance utilities
If you are hunting for useful functions for independent use (i.e. not "skating") then I suggest rummaging in 

   * [covarianceutil](https://github.com/microprediction/precise/tree/main/precise/skaters/covarianceutil) 
   * [locationutil](https://github.com/microprediction/precise/tree/main/precise/skaters/locationutil) 
   * [portfolioutil](https://github.com/microprediction/precise/tree/main/precise/skaters/portfolioutil)

or the "factory" modules, perhaps. 

# Portfolio "managers" and their [Elos](https://github.com/microprediction/precise/blob/main/examples_basic_usage/compile_elo_ratings_for_managers.py)
Hopefully it is clear that portfolio techniques map to other uses like smarter stacking of time-series forecasting methods. But this part is too fluid to document thoroughly. See the portfolio directories in [skaters](https://github.com/microprediction/precise/tree/main/precise/skaters) and also the
[managers](https://github.com/microprediction/precise/tree/main/precise/skaters/managers). Managers are just like cov skaterse except they emit portfolio holdings and state. 

        s = {}
        for y in ys:
            w, s = mgr(s=s, y=y)

Most managers pair a cov skater with a "static" portfolio construction estimator, although that may change. For provisional Elo ratings of managers see the [example script](https://github.com/microprediction/precise/blob/main/examples_basic_usage/compile_elo_ratings_for_managers.py) that collates manager Elo ratings. Here are some portfolio and manager hints:

| Shorthand | Intent                                                           |
|-----------|------------------------------------------------------------------|
| ppo       | Uses the PyPortfolioOpt package                                  |
| ppo_vol   |      ... and minimum volatility therein                          |
| ppo_quad  |      ... and maximum quadratic utility therein                   |
| ppo_sharpe|      ... and maximum Sharpe ratio therein                        |
| diag      | Use only diagonal entries of cov                                 |
| weak      | Homespun method that "weakens" some cov entries to make portfolio long only        | 
| hrp       | Hierarchical Risk Parity, or generalization of the same                            | 
| hrp_diag_diag |   ... and uses "diag" allocation/portfolio, like Lopez de Prado's 2016 paper   | 
| hrp_weak_weak |   ... and uses "weak" allocation and also "weak" portfolio construction.       | 
| schur     | Homespun method that generalizes on Hierarchical Risk Parity using Schur complements |
| schur_weak_diag     |    ... and uses weak allocation and diag portfolio  |

At present "weak" and "schur" are the only methods you may have trouble finding implemented elsewhere. The latter is my attempt to unify seemingly disparate approaches: namely those using a global optimization versus those using divide and conquer. 


## Miscellaneous remarks

 - Here is some related, and potentially related, [literature](https://github.com/microprediction/precise/blob/main/LITERATURE.md). 
 - This is a piece of the microprediction project, should you ever care to [cite](https://github.com/microprediction/microprediction/blob/master/CITE.md) the same. The uses include mixtures of experts models for time-series analysis, buried in [timemachines](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools) somewhere. 
 - If you just want univariate calculations, and don't want numpy as a dependency, there is [momentum](https://github.com/microprediction/momentum). However if you want univariate forecasts of the variance of something, as distinct from mere online calculations of the same, I would suggest checking the [time-series elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/special-k_001.html) and the "special" category in particular. 
 - The name of this package refers to precision matrices, not numerical precision. This isn't a source of high precision covariance *calculations* per se. The intent is more in forecasting future realized covariance. Perhaps I'll include some more numerically stable methods from [this survey](https://dbs.ifi.uni-heidelberg.de/files/Team/eschubert/publications/SSDBM18-covariance-authorcopy.pdf) to make the name more fitting. Pull requests are welcome!
 - The intent is that methods are parameter free. However some not-quite autonomous methods admit a few parameters (the factories). A few might even use just one additional scalar parameter *r* with a space-filling curve convention - somewhat akin to the tuning of skaters explained [here](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools/tuning) in the timemachines package).
 - I use Elo ratings, despite the shortcomings, because comparisions are extremely time intensive. Match results are recorded in hashed files for easy parallelization and avoidance of git merging. Pull requests for match results are welcome. 

## Disclaimer 
Not investment advice. Not M6 entry advice. Just a bunch of code subject to the MIT License disclaimers. 


<img src="https://github.com/microprediction/precise/blob/main/images/incremental.png" width="600">


