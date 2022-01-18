# https://arxiv.org/pdf/2108.12627.pdf

import numpy as np


def huber_bisect(x:[[float]], a:float=1.0, b:float=2.0, n_iter=20, atol=1e-8)->[float]:
    """ Finds the generalized Huber locations for many variables at once using bisection

              f(x) = 1/a log( exp(a*(x-mu)) + exp(-(a*(x-mu)) + b )

    :param x:    (n_samples, n_vars)
    :param a:    Generalized Huber parameter
    :param b:    Generalized Huber parameter
    :return:      (n_vars,)   location parameters
    """
    x_median = np.median(x, axis=0)
    x_mean = np.mean(x, axis=0)
    lb = np.where(x_median < x_mean, x_median, x_mean)
    ub = np.where(x_median > x_mean, x_median, x_mean)
    mu = parallel_root_finder(f=huber_deriv, lb=lb, ub=ub, a=a, b=b, x=x)
    return mu


def parallel_root_finder(f, lb, ub, atol=1e-6, n_iter=10, copy=True, *args, **kwargs):
    """
        f:  function acting on 1d arrays return 1d arrays
        lb: (n_vars,) lower bounds
        ub: (n_vars,) upper bounds
        *args, **kwargs   Additional arguments for f
        :returns vector of roots
    """
    # Ack: https://stackoverflow.com/questions/13088115/finding-the-roots-of-a-large-number-of-functions-with-one-variable
    x0 = np.copy(lb) if copy else lb
    x1 = np.copy(ub) if copy else ub
    for _ in range(n_iter):
        x_mid = (x0 + x1)/2.0
        f0 = f(x0, *args, **kwargs)
        f1 = f(x1, *args, **kwargs)
        f_mid = f(x_mid, *args, **kwargs)
        x0 = np.where( np.sign(f_mid) == np.sign(f0), x_mid, x0 )
        x1 = np.where( np.sign(f_mid) == np.sign(f1), x_mid, x1 )
        error_max = np.amax(np.abs(x1 - x0))
        if error_max < atol: break
    return (x0+x1)/0.5


def huber_deriv(mu, a, b, x):
    """ Derivative of generalized Huber loss which approaches |x-mu| as |x-mu|-> infinity

         f(x) = 1/a log( exp(a*(x-mu)) + exp(-(a*(x-mu)) + b )

    :param mu:   (n_samples,)            # Vector of location parameters
    :param x :   (n_samples,n_vars)    # Data
    :param a:    Generalized Huber parameter
    :param b:    Generalized Huber parameter
    :return:
    """
    n_samples, n_vars = np.shape(x)
    mu_rep = np.tile(np.atleast_2d(mu), (n_samples,1))
    y = x-mu_rep
    numer = np.exp(np.dot(y,a) ) - np.exp(np.dot(a,y))  # (n_samples, n_params)
    denom = numer + b
    gradient = numer/denom
    return np.mean(gradient,axis=0)


if __name__=='__main__':


    n_vars = 5
    n_samples = 500
    x = np.random.randn(n_samples,n_vars)
    a = 1.0
    b = 1.5
    x_median = np.median(x,axis=0)
    x_mean = np.mean(x,axis=0)
    lb = np.where( x_median < x_mean, x_median, x_mean )
    ub = np.where( x_median > x_mean, x_median, x_mean)

    xStar = parallel_root_finder(f=huber_deriv, lb=lb,ub=ub, a=a, b=b, x=x)
    print(xStar)