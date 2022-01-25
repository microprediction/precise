import numpy as np





def parallel_bisection_root_finder(f, lb, ub, atol=1e-6, n_iter=10, copy=True, guess=None, *args, **kwargs):
    """  Find many zeros of f for many different choices of function parameters

        f:  function acting on 1d arrays return 1d arrays
        lb: (n_vars,) lower bounds
        ub: (n_vars,) upper bounds
        *args, **kwargs   Additional arguments for f that, we presume, vary from one variable to the next
        :returns vector of roots, vector of function vals (close to zero)
    """

    # Ack: https://stackoverflow.com/questions/13088115/finding-the-roots-of-a-large-number-of-functions-with-one-variable
    x0 = np.copy(lb) if copy else lb
    x1 = np.copy(ub) if copy else ub
    converged = False
    for i in range(n_iter):
        if i==0 and guess is not None:
            assert len(guess)==len(x0)
            x_mid = guess
        else:
            x_mid = (x0 + x1)/2.0
        f0 = f(x0, *args, **kwargs)
        f1 = f(x1, *args, **kwargs)
        f_mid = f(x_mid, *args, **kwargs)
        x0 = np.where( np.sign(f_mid) == np.sign(f0), x_mid, x0 )
        x1 = np.where( np.sign(f_mid) == np.sign(f1), x_mid, x1 )
        error_max = np.amax(np.abs(x1 - x0))
        if error_max < atol:
            converged = True
            break
    fraction_converged = np.mean(np.abs(x1 - x0) < atol)
    return (x0+x1)/0.5, fraction_converged
