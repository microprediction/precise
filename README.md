# precise

A collection of *autonomous* *incremental* estimators for covariance, precision, correlation and associated quantities.  

## Install 

    pip install precise 
    
## Examples
See [/examples_basic_usage](https://github.com/microprediction/precise/tree/main/examples_basic_usage)

## Explanation
You use state updaters, then functions of the state. 

### State updates  
All updaters take a prior state and return a posterior state (dict). An empty dict is passed to initialize. 

Example: 

    from precise.synthetic.generate import create_correlated_dataset
    from precise.covariance.empirical import emp_pcov
 
    if __name__=='__main__':
        xs = create_correlated_dataset(n=500)
        s = {}
        for x in xs:
            s = emp_pcov(s=s, x=x)
        pprint(s['scov'])
     
Naming hints: 

| Shorthand | Intent                |
|-----------|-----------------------|
| scov      | Sample covariance     |
| pcov      | Population covariance |
| spre      | Sample precision      |
| ppre      | Population precision  |
     
     
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
     
### State functions & mutations
Three types of utilities exist

   1. The [covariance/statefunctions](https://github.com/microprediction/precise/blob/main/precise/covariance/statefunctions.py) are illustrated by the example [running_oas_covariance](https://github.com/microprediction/precise/blob/main/examples_basic_usage/running_oas_covariance.py). 
   2. State [covariatnce/statemutations](https://github.com/microprediction/precise/blob/main/precise/covariance/statemutations.py) do things like ensuring both covariance and precision matrices exist in the state. Or for instance:  s = both_cov(s) ensures both sample and population covariances are present. 
   3. Miscellaneous [/covariance/matrixfunctions](https://github.com/microprediction/precise/blob/main/precise/covariance/util.py) functions act directly on matrices. 
     

## Miscellaneous 

 - Here is some related, and potentially related, [literature](https://github.com/microprediction/precise/blob/main/LITERATURE.md). 
 - This is a piece of the microprediction project, should you ever care to [cite](https://github.com/microprediction/microprediction/blob/master/CITE.md) the same. The uses include mixtures of experts models for time-series analysis, buried in [timemachines](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools) somewhere. 
 - If you just want univariate calculations, and don't want numpy as a dependency, there is [momentum](https://github.com/microprediction/momentum). However if you want univariate forecasts I would suggest checking the [time-series elo ratings](https://microprediction.github.io/timeseries-elo-ratings/html_leaderboards/special-k_001.html) and the "special" category in particular. 
 - The name of this package refers to precision matrices, not numerical precision. This isn't a good source of covariance *calculations* per se. The intent is more forecasting related. Perhaps I'll include some more numerically stable methods from [this survey](https://dbs.ifi.uni-heidelberg.de/files/Team/eschubert/publications/SSDBM18-covariance-authorcopy.pdf) to make the name more fitting. Pull requests are welcome!
 - The intent is that methods are parameter free. However some not-quite autonomous methods admit just one additional scalar parameter *r* and that can make the creation of fully autonomous methods simpler (somewhat akin to the tuning of skaters explained [here](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools/tuning) in the timemachines package, with the same space-filling curve conventions encouraged).    

