# precise

Online covariance, correlation and precision matrix computations

## Install 

    pip install precise 
    
## Example

    from precise.synthetic.generate import create_correlated_dataset
    from precise.covariance.empirical import ecov_init, ecov_update
    from pprint import pprint

    xs = create_correlated_dataset(n=500)
    ocov = ecov_init(n_dim=xs.shape[1])
    for x in xs:
        ocov = ecov_update(m=ocov, x=x)
    pprint(ocov)
    
 This will return the running state, which includes the mean and cov
 
### Examples

See [examples](https://github.com/microprediction/precise/tree/main/examples).

### See also

If you only need univariate, there is a really minimalise package [momentum](https://github.com/microprediction/momentum) which avoids use of numpy.  

