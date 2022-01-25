# precise

A collection of *autonomous* *incremental* estimators for covariance, precision, correlation and associated quantities.  

## Install 

    pip install precise 
    
## Examples
See [/examples_basic_usage](https://github.com/microprediction/precise/tree/main/examples_basic_usage)

## Explanation
You use state updaters, then functions of the state. 

### Covariance skaters  
Similar in style to skaters used in the [timemachines](https://github.com/microprediction/timemachines) package, covariance skaters take one data point at a time, and also the prior state, and spit out a prediction vector *x*, a prediction covariance *x_cov*, and the posterior state.

    from precise.skatertools.syntheticdata.miscellaneous import create_correlated_dataset
    from precise.skaters.covariance.empirical import emp_pcov_d0
    from pprint import pprint

    if __name__=='__main__':
        ys = create_correlated_dataset(n=500)
        s = {}
        for y in ys:
            x, x_cov, s = emp_pcov_d0(s=s, y=y)
        pprint(x_cov)
     
You can hunt for skaters in [precise/skaters/covariance](https://github.com/microprediction/precise/tree/main/precise/skaters/covariance). Naming hints for values in the state dict s:  

| Shorthand | Intent                            |
|-----------|-----------------------------------|
| scov      | Sample covariance                 |
| pcov      | Population covariance             |
| spre      | Inverse of sample covariance      |
| ppre      | Inverse of population covariance  |
     
     
Method hints: 

| Shorthand | Inspiration           |
|-----------|-----------------------|
| emp       | Empirical     |
| ema      | Exponential weighted moving average |
| lz      | Le-Zhong variable-by-variable updating |
| lw      | Ledoit-Wolf              |
| partial | Partial moments                        | 
| huber | Generalized Huber pseudo-mean            |
| oas   | Oracle approximating shrinkage.          |
| gl    | Graphical Lasso                          |
| mcd   | Minimum covariance determinant           |

Speed hints:

| Shorthand | Interpretation                          |
|-----------|-----------------------------------------|
| buffered  | Maintains fixed window of data          |

Others are incremental, taking one vector of data at a time. 
     
### Some stand-alone utilities

   1. The [covariance/statefunctions](https://github.com/microprediction/precise/blob/main/precise/skaters/covarianceutil/statefunctions.py) are illustrated by the example [running_oas_covariance](https://github.com/microprediction/precise/blob/main/examples_basic_usage/running_oas_covariance.py). 
   2. State [covariatnce/statemutations](https://github.com/microprediction/precise/blob/main/precise/skaters/covarianceutil/statemutations.py) do things like ensuring both covariance and precision matrices exist in the state. Or for instance:  s = both_cov(s) ensures both sample and population covariances are present. 
   3. Some [/covariance/datascatterfunctions](https://github.com/microprediction/precise/blob/main/precise/skaters/covarianceutil/datascatterfunctions.py)
   4. The [/covariance/datacovfunctions](https://github.com/microprediction/precise/blob/main/precise/skaters/covarianceutil/datacovfunctions.py) take data and produce covariance functions. 
   5. The  [/covariance/covfunctions](https://github.com/microprediction/precise/blob/main/precise/skaters/covarianceutil/covfunctions.pyy) manipulate 2d cov arrays. 
  

## Miscellaneous 

 - Here is some related, and potentially related, [literature](https://github.com/microprediction/precise/blob/main/LITERATURE.md). 
 - This is a piece of the microprediction project, should you ever care to [cite](https://github.com/microprediction/microprediction/blob/master/CITE.md) the same. The uses include mixtures of experts models for time-series analysis, buried in [timemachines](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools) somewhere. 
 - If you just want univariate calculations, and don't want numpy as a dependency, there is [momentum](https://github.com/microprediction/momentum). However if you want univariate forecasts of the variance of something, as distinct from mere online calculations of the same, I would suggest checking the [time-series elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/special-k_001.html) and the "special" category in particular. 
 - The name of this package refers to precision matrices, not numerical precision. This isn't a good source of covariance *calculations* per se. The intent is more forecasting related. Perhaps I'll include some more numerically stable methods from [this survey](https://dbs.ifi.uni-heidelberg.de/files/Team/eschubert/publications/SSDBM18-covariance-authorcopy.pdf) to make the name more fitting. Pull requests are welcome!
 - The intent is that methods are parameter free. However some not-quite autonomous methods admit just one additional scalar parameter *r* and that can make the creation of fully autonomous methods simpler (somewhat akin to the tuning of skaters explained [here](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools/tuning) in the timemachines package, with the same space-filling curve conventions encouraged).    

