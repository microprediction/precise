# precise

Online covariance, correlation and precision matrix computations

## Install 

    pip install precise 
    
## Example

    from precise.covariance.util import create_correlated_dataset
    from precise.covariance.onlineempirical import online_empirical_cov
    import numpy as np
    from pprint import pprint

    data = create_correlated_dataset(10000, (2.2, 4.4, 1.5),
                                     np.array([[0.2, 0.5, 0.7], [0.3, 0.2, 0.2], [0.5, 0.3, 0.1]]), (1, 5, 3))
    s = online_empirical_cov(n_dim=data.shape[1])
    for observation in data:
        s = online_empirical_cov(s=s, y=observation)
    pprint(s)
    
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

