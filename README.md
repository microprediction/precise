# precise

A collection of *autonomous* *online* (incremental) covariance matrix estimators. 

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

| Shorthand | Meaning               |
|-----------|-----------------------|
| emp       | Empirical     |
| ema      | Exponential weighted moving average |
| lz      | Le-Zhong variable-by-variable updating |
| lw      | (inspired by) Ledoit-Wolf              |

Some, such as OAS, don't need their own state tracking. See [examples](https://github.com/microprediction/precise/blob/main/examples_basic_usage/running_oas_covariance.py). 
     
### State functions & mutations
Three types of utilities exist

   1. The [covariance/statefunctions](https://github.com/microprediction/precise/blob/main/precise/covariance/statefunctions.py) are illustrated by the example [running_oas_covariance](https://github.com/microprediction/precise/blob/main/examples_basic_usage/running_oas_covariance.py). 
   2. State [covariatnce/statemutations](https://github.com/microprediction/precise/blob/main/precise/covariance/statemutations.py) do things like ensuring both covariance and precision matrices exist in the state. Or for instance:  s = both_cov(s) ensures both sample and population covariances are present. 
   3. Miscellaneous [/covariance/matrixfunctions](https://github.com/microprediction/precise/blob/main/precise/covariance/util.py) functions act directly on matrices. 
     

### Updater hyper-parameters
The intent is that methods are parameter free. However some not-quite autonomous methods admit just one additional scalar parameter *r* and that can make the creation of fully autonomous methods simpler, akin to the tuning of skaters explained [here](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools/tuning) in the timemachines package. 


## Miscellaneous 

 - Care to cite, some ideas [here](https://github.com/microprediction/microprediction/blob/master/CITE.md)
 - If you just want univariate, and don't want numpy as a dependency, there is [momentum](https://github.com/microprediction/momentum). 

