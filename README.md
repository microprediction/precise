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
    
    {'count': 10000,
     'cov': array([[0.38549265, 1.55198303, 0.73809891],
           [1.55198303, 9.41813338, 6.20756741],
           [0.73809891, 6.20756741, 4.79042088]]),
     'identity': array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]]),
     'mean': array([2.19919374, 4.42189785, 1.52406171]),
     'n_dim': 3,
     'ones': array([1., 1., 1.]),
     'shape': (3, 3)}
     
 To covert to corrcoef, 
 
      from precision.covariance.util import cov_to_corrcoef
      pprint( cov_to_corrcoef(s['cov']) )
      
 returns:
      
      array([[1.        , 0.81749783, 0.55345955],
       [0.81749783, 1.        , 0.92689045],
       [0.55345955, 0.92689045, 1.        ]])


### See also

If you only need univariate, there is a really minimalise package [momentum](https://github.com/microprediction/momentum) which avoids use of numpy.  

