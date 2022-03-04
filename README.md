# precise ![tests](https://github.com/microprediction/precise/workflows/tests/badge.svg) ![tests-scipy-173](https://github.com/microprediction/precise/workflows/tests-scipy-173/badge.svg)![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Online covariance and precision forecasting, portfolios, and model ensembles in a simple functional style. 

## Covariance TLDR: "Functions that forecast covariance in online fashion"
Here y is a vector:

    from precise.skaters.covariance.ewapm import ewa_pm_emp_scov_r005_n100 as f 
    s = {}
    for y in ys:
        x, x_cov, s = f(s=s, y=y)

This package contains lots of different "f"s. There is a [LISTING_OF_COV_SKATERS](https://github.com/microprediction/precise/blob/main/LISTING_OF_COV_SKATERS.md) with links to the code. 

## Portfolio TLDR: "Functions that update portfolio weights in online fashion"
Here y is a vector:

        from precise.skaters.managers.schurmanagers import schur_weak_pm_t0_d0_r025_n50_g100_long_manager as mgr
        s = {}
        for y in ys:
            w, s = mgr(s=s, y=y)

This package contains lots of "mgr"'s. There is a [LISTING_OF_MANAGERS](https://github.com/microprediction/precise/blob/main/LISTING_OF_MANAGERS.md) with links to respective code.  

## Ensembles, mixtures of experts TLDR: "They are just portfolios"
Read this [article](https://medium.com/@microprediction/optimizing-a-portfolio-of-models-f1ed432d728b) exploring the connection between portfolio theory and combining models, or the [colab notebook](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/lazypredict_model_portfolio.ipynb) on which is is based. 

<img src="https://github.com/microprediction/precise/blob/main/images/lb_hightlight2.png" alt="Model Leaderboard" style="width:500px">


# $$ M6 Contest example entries $$
This package includes scripts to create entries for the lucrative M6 Financial Forecasting competition.  

1. See [precise/examples_m6](https://github.com/microprediction/precise/tree/main/examples_m6)
2. Register at the [m6 competition](https://m6competition.com/). 
3. Buy me, or the authors of PyPortfolio-Lib and PyPortfolioOpt, lots of beers when you win.   

## Install 

    pip install precise 
    
or for latest:

    pip install git+https://github.com/microprediction/precise.git
 
Trouble? 

    pip install --upgrade pip
    pip install --upgrade scipy
    pip insatll --upgrade precise 
        
# More about covariance skaters and their [Elos](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/elo_ratings_and_code_urls.ipynb)
Similar in style to skaters used in the [timemachines](https://github.com/microprediction/timemachines) package, this package may be thought of as a collection of covariance prediction functions taking one vector at a time, and also the prior state, and spitting out a prediction mean vector *x*, a prediction covariance *x_cov*, and a posterior state whose interpretation is the responsibility of the skater, not the caller. 
     
See [/examples_basic_usage](https://github.com/microprediction/precise/tree/main/examples_basic_usage). And yes, this mildly unusual convention requires the caller to maintain state from one call to the next:  See the timemachines [faq](https://github.com/microprediction/timemachines/blob/main/FAQ.md) for justification of this style. The [running_empirical_covariance](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/running_empirical_population_covariance.ipynb) colab notebook also illustrates the simple usage pattern. 
          
### Cov skater listing and Elo ratings
    
- Peruse the [listing](https://github.com/microprediction/precise/blob/main/LISTING_OF_COV_SKATERS.md)
- Or hunt for skaters in [precise/skaters/covariance](https://github.com/microprediction/precise/tree/main/precise/skaters/covariance). 
- Run the Elo ratings [colab notebook](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/elo_ratings_and_code_urls.ipynb) which may, or may not, help guide your shortlisting.   


### Interpreting covariance skater names 
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
| weak      | Novel shrinkage method by yours truly  |

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

# More on portfolio managers and their [Elos](https://github.com/microprediction/precise/blob/main/examples_basic_usage/compile_elo_ratings_for_managers.py)
Hopefully it is clear that portfolio techniques map to other uses like smarter stacking of time-series forecasting methods. But this part is too fluid to document thoroughly. See the portfolio directories in [skaters](https://github.com/microprediction/precise/tree/main/precise/skaters) and also the
[managers](https://github.com/microprediction/precise/tree/main/precise/skaters/managers). Managers are just like cov skaterse except they emit portfolio holdings and state. 

        s = {}
        for y in ys:
            w, s = mgr(s=s, y=y)

Most managers pair a cov skater with a "static" portfolio construction estimator, although that may change. For provisional Elo ratings of managers see the [example script](https://github.com/microprediction/precise/blob/main/examples_basic_usage/compile_elo_ratings_for_managers.py) that collates manager Elo ratings. Here are some portfolio and manager hints:

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


### Model ensembles, stacking, mixtures of experts et cetera
Same thing, sort of. See this [notebook example](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/lazypredict_model_portfolio.ipynb) or [these examples](https://github.com/microprediction/precise/tree/main/examples_ensembles_lazypredict).  


# Miscellaneous remarks

 - Here is some related, and potentially related, [literature](https://github.com/microprediction/precise/blob/main/LITERATURE.md). 
 - This is a piece of the microprediction project aimed at creating millions of autonomous critters to democratize AI, should you ever care to [cite](https://github.com/microprediction/microprediction/blob/master/CITE.md) the same. The uses include mixtures of experts models for time-series analysis, buried in [timemachines](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools) somewhere. 
 - If you just want univariate calculations, and don't want numpy as a dependency, there is [momentum](https://github.com/microprediction/momentum). However if you want univariate forecasts of the variance of something, as distinct from mere online calculations of the same, you might be better served by the timemachines package. In particular I would suggest checking the [time-series elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/special-k_001.html) and the "special" category in particular, as various kinds of empirical moment time-series (volatility etc) are used to determine those ratings. 
 - The name of this package refers to precision matrices, not numerical precision. This isn't a source of high precision covariance *calculations* per se. The intent is more in forecasting future realized covariance. Perhaps I'll include some more numerically stable methods from [this survey](https://dbs.ifi.uni-heidelberg.de/files/Team/eschubert/publications/SSDBM18-covariance-authorcopy.pdf) to make the name more fitting. Pull requests are welcome!
 - The intent is that methods are parameter free. However some not-quite autonomous methods admit a few parameters (the factories). A few might even use just one additional scalar parameter *r* with a space-filling curve convention - somewhat akin to the tuning of skaters explained [here](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools/tuning) in the timemachines package).
 - I use Elo ratings, despite the shortcomings, because comparisions are extremely time intensive. Match results are recorded in hashed files for easy parallelization and avoidance of git merging. You can run the battle scripts if you like. See [these examples](https://github.com/microprediction/precise/tree/main/precise/skatervaluation/battlescripts/manager_var) for instance. To make a different battle you modify the name of the script and nothing else. Pull requests for match results are welcome. 

# Disclaimer 
Not investment advice. Not M6 entry advice. Just a bunch of code subject to the MIT License disclaimers. 


<img src="https://github.com/microprediction/precise/blob/main/images/incremental.png" width="600">


