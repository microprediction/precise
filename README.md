# precise [docs](https://microprediction.github.io/precise/) ![tests](https://github.com/microprediction/precise/workflows/tests/badge.svg) ![tests_312](https://github.com/microprediction/precise/workflows/tests_312/badge.svg) ![tests-sans-ppo](https://github.com/microprediction/precise/workflows/tests-sans-ppo/badge.svg)  ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Contents:

1. A collection of *online* (incremental) [covariance forecasting](https://github.com/microprediction/precise/blob/main/LISTING_OF_COV_SKATERS.md) and [portfolio construction](https://github.com/microprediction/precise/blob/main/LISTING_OF_MANAGERS.md) functions. See [docs](https://microprediction.github.io/precise/). 

2. "Schur Complementary" portfolio construction, a new approach that leans on connection between top-down (hierarchical) and bottom-up (optimization) portfolio construction revealed by block matrix inversion. See my posts on the [methodology](https://www.linkedin.com/posts/petercotton_schur-complementary-portfolios-a-unification-activity-7000535020381552640-ZWej?utm_source=share&utm_medium=member_desktop) and its role in the [hijacking of the M6 contest](https://www.linkedin.com/posts/alexander-fleiss-70b49410_does-option-volume-predict-stock-direction-activity-7021134433344749569-bxx4?utm_source=share&utm_medium=member_desktop). 
 
3. A small compendium of portfolio theory papers tilted towards my interests. See [literature](https://github.com/microprediction/precise/blob/main/LITERATURE.md). 

One observes that tools for portfolio construction might also be useful in [optimizing a portfolio of models](https://medium.com/geekculture/optimizing-a-portfolio-of-models-f1ed432d728b).

NEW: Some [slides](https://github.com/microprediction/precise/blob/main/academic/Schur_Complementary_Portfolios_CQF_Slides_Updated.pdf) for the CQF talk. 

---

<a href="https://medium.com/geekculture/schur-complementary-portfolios-fix-hierarchical-risk-parity-28b0efa1f35f">
<img src="https://github.com/microprediction/precise/blob/main/docs/assets/images/schur_reaction.png" width="600"></a>

---

# Usage 
See the [docs](https://microprediction.github.io/precise/) but briefly ...

### Covariance estimation
Here y is a vector:

    from precise.skaters.covariance.ewapm import ewa_pm_emp_scov_r005_n100 as f 
    s = {}
    for y in ys:
        x, x_cov, s = f(s=s, y=y)

This package contains lots of different "f"s. There is a [LISTING_OF_COV_SKATERS](https://github.com/microprediction/precise/blob/main/LISTING_OF_COV_SKATERS.md) with links to the code. See the [covariance documentation](https://microprediction.github.io/precise/covariance.html).

### Portfolio weights
Here y is a vector:

        from precise.skaters.managers.schurmanagers import schur_weak_pm_t0_d0_r025_n50_g100_long_manager as mgr
        s = {}
        for y in ys:
            w, s = mgr(s=s, y=y)

This package contains lots of "mgr"'s. There is a [LISTING_OF_MANAGERS](https://github.com/microprediction/precise/blob/main/LISTING_OF_MANAGERS.md) with links to respective code. See the [manager documentation](https://microprediction.github.io/precise/managers.html).

# Install 
Supported for Python 3.11 or earlier

    pip install precise 
    
or for latest:

    pip install git+https://github.com/microprediction/precise.git
 
Trouble? It probably isn't with precise per se. 

    pip install --upgrade pip
    pip install --upgrade setuptools 
    pip install --upgrade wheel
    pip install --upgrade ecos   # <--- Try conda install ecos if this fails
    pip install --upgrade osqp   # <-- Can be tricky on some systems see https://github.com/cvxpy/cvxpy/issues/1190#issuecomment-994613793
    pip install --upgrade pyportfolioopt # <--- Skip if you don't plan to use it
    pip install --upgrade riskparityportfolio
    pip install --upgrade scipy
    pip install --upgrade precise 


# Miscellaneous 

 - Here is some related, and potentially related, [literature](https://github.com/microprediction/precise/blob/main/LITERATURE.md). 
 - This is a piece of the microprediction project aimed at creating millions of autonomous critters to distribute AI at low cost, should you ever care to [cite](https://github.com/microprediction/microprediction/blob/master/CITE.md) the same. The uses include mixtures of experts models for time-series analysis, buried in [timemachines](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools) somewhere. 
 - If you just want univariate calculations, and don't want numpy as a dependency, there is [momentum](https://github.com/microprediction/momentum). However if you want univariate forecasts of the variance of something, as distinct from mere online calculations of the same, you might be better served by the timemachines package. In particular I would suggest checking the [time-series elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/special-k_001.html) and the "special" category in particular, as various kinds of empirical moment time-series (volatility etc) are used to determine those ratings. 
 - The name of this package refers to precision matrices, not numerical precision. This isn't a source of high precision covariance *calculations* per se. The intent is more in forecasting future realized covariance, conscious of the noise in the empirical distribution. Perhaps I'll include some more numerically stable methods from [this survey](https://dbs.ifi.uni-heidelberg.de/files/Team/eschubert/publications/SSDBM18-covariance-authorcopy.pdf) to make the name more fitting. Pull requests are welcome!
 - The intent is that methods are parameter free. However some not-quite autonomous methods admit a few parameters (the factories). 


# Disclaimer 
Not investment advice. Not M6 entry advice. Just a bunch of code subject to the MIT License disclaimers. 



