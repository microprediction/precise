# Ack: https://arxiv.org/pdf/2108.12627.pdf

import numpy as np
import math
from precise.skaters.vectorutil.bisection import parallel_bisection_root_finder


def huber_mean(xs:[[float]], a:float=1.0, b=2.0, n_iter=20, atol=1e-8, with_gradients=False)->[float]:
    """ Compute a columnwise pseudo-mean of xs, by minimizing a generalized Huber error that is
        proportional to x^2 near zero and asymptotes to |x| as |x|->infinity.
               f(x) = 1/a log( exp(a*(x-mu)) + exp(-(a*(x-mu)) + b )
        This is the same as the function below, except the parameter a will multiply std(x)
        :param xs:    (n_samples, n_vars)
        :param a:    Generalized Huber parameter as per formula
        :param b:    Generalized Huber parameter as per formula above, scalar or (nvars,)
        :param with_gradients: If True, will return the Huber gradients at the minimum found in addition to the pesudo-mean
        :return:      (n_vars,)   location parameters

    """
    x_std = np.nanstd(xs,axis=0)
    a_abs = a*x_std
    return huber_mean_absolute_params(xs=xs, a=a_abs, b=b, n_iter=n_iter, atol=atol, with_convergence=with_gradients)


def huber_mean_absolute_params(xs:[[float]], a, b, n_iter=20, atol=1e-8, with_convergence=False)->[float]:
    """ Finds the generalized Huber locations for many variables at once
        Each column of xs represents a different variable whose pseudo-mean will be computed
        Thus the result mu might be compared to np.mean(xs, axis=0)

        The function being minimized w.r.t mu is
              f(x) = 1/a log( exp(a*(x-mu)) + exp(-(a*(x-mu)) + b )
        and for |x|->0 this has asymptote:
             f(x) ->  log(2+b)/a + a/(2+b) * (x-mu)^2
        whereas for |x|->infinity
             f(x) -> |x-mu|

        This Huber function is not the standard Huber loss https://en.wikipedia.org/wiki/Huber_loss
        Rather, it is based on https://arxiv.org/pdf/2108.12627.pdf

    :param xs:    (n_samples, n_vars)
    :param a:    Generalized Huber parameter as per formula above, scalar or (nvars,)
    :param b:    Generalized Huber parameter as per formula above, scalar or (nvars,)
    :return:      (n_vars,)   location parameters
    """
    x_median = np.median(xs, axis=0)
    x_mean = np.mean(xs, axis=0)
    lb = np.where(x_median < x_mean, x_median, x_mean)
    ub = np.where(x_median > x_mean, x_median, x_mean)
    mu, all_converged = parallel_bisection_root_finder(f=huber_deriv, lb=lb, ub=ub, a=a, b=b, xs=xs, atol=atol, n_iter=n_iter)
    return mu, all_converged if with_convergence else mu


def huber_deriv(mu, a, b, xs):
    """ Derivative of generalized Huber loss w.r.t. mu

         f'(x) = 1/a log( exp(a*(x-mu)) + exp(-(a*(x-mu)) + b )

    :param mu:   (n_samples,)                    # Vector of location parameters
    :param xs :   (n_samples,n_vars)              # Data
    :param a:    Generalized Huber parameter(s)
    :param b:    Generalized Huber parameter(s)
    :return:
    """
    n_samples, n_vars = np.shape(xs)
    mu_rep = np.tile(np.atleast_2d(mu), (n_samples,1))
    y = xs - mu_rep
    chain_rule = -1.0
    numer = np.exp(np.dot(y,a) ) - np.exp(-np.dot(a,y))  # (n_samples, n_params)
    denom = numer + b
    gradient = chain_rule*numer/denom
    return np.mean(gradient,axis=0)


def huber_abs_error(mu, a, b, xs):
    """ Generalized Huber loss which is "like" abs error, as it approaches |x-mu| as |x-mu|-> infinity
          f(x) = 1/a log( exp(a*(x-mu)) + exp(-(a*(x-mu)) + b )
     """
    n_samples, n_vars = np.shape(xs)
    mu_rep = np.tile(np.atleast_2d(mu), (n_samples, 1))
    y = xs - mu_rep
    numer = np.log(np.exp(np.dot(y, a)) + np.exp(np.dot(a, y)) + b)  # (n_samples, n_params)
    denom = a
    return numer / denom


def mean_huber_linear_error(mu, a, b, xs):
    """
        This convenience function returns columnwise mean.
    """
    f_val = huber_abs_error(mu=mu, a=a, b=b, xs=xs)
    return np.mean(f_val, axis=0)


def huber_squared_error(mu, a, b, xs):
    """ Rescaled generalized Huber loss which is "like" squared error, in
    the sense that it approaches (x-mu)^2 as |x-mu|-> 0

        If
         f(x) = 1/a log( exp(a*(x-mu)) + exp(-(a*(x-mu)) + b )
        Then
         f(x) -> log(2+b)/a + a/(2+b) * x^2   as x->0
        by Taylor. So we define
         g(x) :=  ( f(x) - log(2+b)/a ) * (2+b)/a

    """
    f = huber_abs_error(mu=mu,a=a,b=b,xs=xs)
    c = math.log(2 + b) / a
    d = a / (2 + b)
    g = ( f - c ) / d
    return g


def mean_huber_squared_error(mu, a, b, xs):
    """
        This convenience function returns columnwise mean.
    """
    f_val = huber_squared_error(mu=mu, a=a, b=b, xs=xs)
    return np.mean(f_val, axis=0)


def mean_quadratic_error(mu, xs):
    """
       Here as a useful comparison to the below
    """
    n_samples, n_vars = np.shape(xs)
    mu_rep = np.tile(np.atleast_2d(mu), (n_samples, 1))
    y = xs - mu_rep
    return np.nanmean(y**2, axis=0)


if __name__=='__main__':
    n_vars = 5
    n_samples = 500
    xs = np.random.randn(n_samples,n_vars)
    a = 1.0
    b = 1.5
    x_median = np.median(xs,axis=0)
    x_mean = np.mean(xs,axis=0)
    lb = np.where( x_median < x_mean, x_median, x_mean )
    ub = np.where( x_median > x_mean, x_median, x_mean)

    xStar, all_converged = parallel_bisection_root_finder(f=huber_deriv, lb=lb, ub=ub, a=a, b=b, xs=xs)
    print(xStar)
    print(all_converged)