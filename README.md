# precise

A collection of *autonomous* *online* (incremental) covariance matrix estimators. 

## Install 

    pip install precise 
    
## Examples
See [/examples_basic_usage](https://github.com/microprediction/precise/tree/main/examples_basic_usage)


## State updates  
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
     
This package contains similar updaters. Their states typically one of the following:

| Shorthand | Intent                |
|-----------|-----------------------|
| scov      | Sample covariance     |
| pcov      | Population covariance |
| spre      | Sample precision      |
| ppre      | Population precision  |
     
     
Names of updaters contain hints of what is updated, and the method:

| Shorthand | Meaning               |
|-----------|-----------------------|
| emp       | Empirical     |
| ema      | Exponential weighted moving average |

Maybe more by the time you read this. 
     
## State functions & mutations
Three types of utilities exist

   1. State [functions](https://github.com/microprediction/precise/blob/main/precise/covariance/statefunctions.py) are illustrated by the example [running_oas_covariance](https://github.com/microprediction/precise/blob/main/examples_basic_usage/running_oas_covariance.py). 
   2. State [mutations](https://github.com/microprediction/precise/blob/main/precise/covariance/statemutations.py) do things like ensuring both covariance and precision matrices exist in the state. Or for instance:  s = both_cov(s) ensures both sample and population covariances are present. 
   3. Miscellaneous [util](https://github.com/microprediction/precise/blob/main/precise/covariance/util.py) functions act directly on matrices. 
     

## Hyper-parameters
The intent is that methods are parameter free. However some admit just one additional scalar parameter *r* and that can make tuning simpler, akin to the tuning of skaters explained [here](https://github.com/microprediction/timemachines/tree/main/timemachines/skatertools/tuning) in the timemachines package. 


## Related 

If you just want univariate, and don't want numpy as a dependency, there is [momentum](https://github.com/microprediction/momentum). 

