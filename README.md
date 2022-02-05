# precise ![tests](https://github.com/microprediction/precise/workflows/tests/badge.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A collection of incremental estimators for covariance, precision, correlation, portfolios and ensembles.   

## TLDR: "Just a pile of functions that forecast covariance in online fashion"
The [running_empirical_covariance](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/running_empirical_population_covariance.ipynb) colab notebook illustrates the style. To see all the other online methods of covariance estimation supplied here, run the [cov skaters manifest](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/list_all_cov_methods.ipynb) notebook. Or to look at Elo ratings,
run the [elo_ratings_and_urls](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/elo_ratings_and_code_urls.ipynb). 

<img src="https://github.com/microprediction/precise/blob/main/images/incremental.png" width="700">


## Install 

    pip install precise 
    
or for latest:

    pip install git+https://github.com/microprediction/precise.git

## M6 Financial forecasting contest utilities
You *could* use this library to enter the M6 Financial Forecasting competition:

   1. Pick a cov estimator (i.e. a "cov skater"), if you wish
   2. Pick a portfolio generator, if you wish
   3. Pick extra shrinkage params, if you wish
   4. Pick love and hate ticker lists, if you wish

See [precise/examples_m6](https://github.com/microprediction/precise/tree/main/examples_m6) and register at the [m6 competition](https://m6competition.com/). See disclaimer below.  

## Covariance skaters  
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
     
### Elo ratings 

As noted, see the [elo_ratings_and_urls](https://github.com/microprediction/precise/blob/main/examples_colab_notebooks/elo_ratings_and_code_urls.ipynb).  
     
### Browsing for skaters
     
You can hunt for skaters other than *run_emp_pcov_d0* in [precise/skaters/covariance](https://github.com/microprediction/precise/tree/main/precise/skaters/covariance). There are some location utilities in [precise/whereami](https://github.com/microprediction/precise/blob/main/precise/whereami.py). 

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

   1. The [covariance/statefunctions](https://github.com/microprediction/precise/blob/main/precise/skaters/covarianceutil/statefunctions.py) are illustrated by the example [running_oas_covariance](https://github.com/microprediction/precise/blob/main/examples_basic_usage/running_oas_covariance.py). 
   2. State [covariatnce/statemutations](https://github.com/microprediction/precise/blob/main/precise/skaters/covarianceutil/statemutations.py) do things like ensuring both covariance and precision matrices exist in the state. Or for instance:  s = both_cov(s) ensures both sample and population covariances are present. 
   3. Some [/covariance/datascatterfunctions](https://github.com/microprediction/precise/blob/main/precise/skaters/covarianceutil/datascatterfunctions.py)
   4. The [/covariance/datafunctions](https://github.com/microprediction/precise/blob/main/precise/skaters/covarianceutil/datafunctions.py) take data and produce covariance functions. 
   5. The  [/covariance/covfunctions](https://github.com/microprediction/precise/blob/main/precise/skaters/covarianceutil/covfunctions.pyy) manipulate 2d cov arrays. 

## Portfolios, ensembles & mixture of experts
Too fluid to document currently. See the portfolio directories in [skaters](https://github.com/microprediction/precise/tree/main/precise/skaters). 

## Miscellaneous remarks

 - Here is some related, and potentially related, [literature](https://github.com/microprediction/precise/blob/main/LITERATURE.md). 
 - This is a piece of the microprediction project, should you ever care to [cite](https://github.com/microprediction/microprediction/blob/master/CITE.md) the same. The uses include mixtures of experts models for time-series analysis, buried in [timemachines](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools) somewhere. 
 - If you just want univariate calculations, and don't want numpy as a dependency, there is [momentum](https://github.com/microprediction/momentum). However if you want univariate forecasts of the variance of something, as distinct from mere online calculations of the same, I would suggest checking the [time-series elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/special-k_001.html) and the "special" category in particular. 
 - The name of this package refers to precision matrices, not numerical precision. This isn't a source of high precision covariance *calculations* per se. The intent is more in forecasting future realized covariance. Perhaps I'll include some more numerically stable methods from [this survey](https://dbs.ifi.uni-heidelberg.de/files/Team/eschubert/publications/SSDBM18-covariance-authorcopy.pdf) to make the name more fitting. Pull requests are welcome!
 - The intent is that methods are parameter free. However some not-quite autonomous methods admit a few parameters (the factories). A few might even use just one additional scalar parameter *r* with a space-filling curve convention - somewhat akin to the tuning of skaters explained [here](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools/tuning) in the timemachines package).

## Disclaimer 
Not investment advice. 



