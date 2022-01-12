# precise

Online covariance, correlation and precision matrix computations

## Install 

    pip install precise 
    
## Examples
See [/examples_basic_usage](https://github.com/microprediction/precise/tree/main/examples_basic_usage)


## State updates  
All updaters return a posterior state. Pass an empty dict on first use. Return the state on the next call. 

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
     
If we want some related quantity, say a sample correlation estimate, we use the utility functions as follows:  
 
    from pprint import pprint
    from precise.covariance.util import both_cov, cov_to_corrcoef

    s = both_cov(s)  # <--- Adds 'pcov' to dictionary s 
    scorr = cov_to_corrcoef(s['scov'])
    pprint(scorr)    

### Related 

The minimalise package [momentum](https://github.com/microprediction/momentum) is similar, but limited to univariate updates. 

