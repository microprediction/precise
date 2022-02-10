import numpy as np
from precise.skaters.locationutil.vectorfunctions import scatter
from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory
from precise.skaters.portfolioutil.portfunctions import portfolio_variance


# Portfolio "lemmas" - not sure what else to call this just now ;)

def bAb(A,b):
    return np.dot( np.dot( np.transpose(b), A), b )


def quirky_solve(A, b):
    """
        Nuts alternative to np.linalg.solve(A,b)
    """
    v = np.ones(len(b))
    A_tilde = A / scatter(b)
    A_inv = np.linalg.inv(A)
    A_tilde_inv = np.linalg.inv( A_tilde )
    numer = bAb(A_inv, b)
    denom = bAb(A_tilde_inv, v)
    x = numer/denom*np.dot(A_tilde_inv, v) / b
    return x



