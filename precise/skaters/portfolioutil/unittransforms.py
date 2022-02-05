import numpy as np
from precise.skaters.portfoliostatic.unitportfactory import unitary_from_cov
from precise.skaters.covarianceutil.covfunctions import multiply_by_inverse

# Provides the transforms necessary to reduce
#
#       min  w^t C R w  subject to w^t c = 1
#
# to the special case R=I, c=1

# (So yeah, nothing really to do with unitary operators, just transforms of the unitary portfolio problem)


def scaled_unitary_problem(C, c):
    """ Find equivalent problem to:

          min w^t C w subject to w^t c = 1

        Namely:
           w = u/c
        where u solves:
           min u^t C' u subject to u^t v = 1
        where
           v = [1,..,1]

        :param   C   Covariance
        :param   c   Linear coef as above
        :returns C'   Covariance playing role above

    """
    assert len(c) == np.shape(C)[0]
    assert all([ci > 0 for ci in c])
    cij = np.dot(np.atleast_2d(c), np.transpose(np.atleast_2d(c)))
    assert np.shape(cij) == np.shape(C)
    C_prime = C / cij
    return C_prime


def scaled_unitary_problem_solution(C, c):
    """
        Solve argmin   w^t C w  subject to w^t c = 1
    """
    Q, _ = scaled_unitary_problem(C=C, c=c)
    u = unitary_from_cov(cov=Q)
    w = u/ c
    assert np.dot(w, c) == 1
    return w


def left_multiplied_unitary_problem(C, R, c=None):
    """ Find equivalent problem to

          min w^t R C w   subject to w^t c ==1      (1)

        Instead find H^t H = R and set u = H w, w = H^{-1} u

          min  u^t  H  C  H^{-1} u    subject to u^t H^{-1}^t c = 1     (2)

        So set
                  c' = H^{-1}^t c
                  C' = H  C  H^{-1}

        Given  C', H, c' we can thus find
        w by solving the transformed problem (2), re-written:

           min u^t C' u subject to u^t c' = 1

        and then substituting back:

           w = H^{-1} u             (3)

        which is to say  w = solve(H,u)

        :param C   Covariance
        :param R   Additional tranform matrix


    """
    n = np.shape(C)[0]
    if c is None:
        c = np.ones(n)

    L = np.linalg.cholesky(R)
    H = np.transpose(L)
    assert np.linalg.norm( np.dot(np.transpose(L),L)-R ) < 1e-6
    c_prime = np.linalg.solve(L,c)
    C_Hinv = multiply_by_inverse(C,H)
    C_prime = np.dot( H, C_Hinv )

    return C_prime, H, c_prime


def left_multiplied_unitary_solution(C, R, c, verify=False):
    """ Find portfolio in a rather indirect way ... useful for checking

         min w^t R C w   subject to w^t c == 1
    """
    C_prime, H, c_prime = left_multiplied_unitary_problem(C=C, R=R)
    u = scaled_unitary_problem_solution(C=C_prime, c=c_prime)
    w = np.linalg.solve(H,u)

    if verify:
        RC = np.dot(R,C)
        w_check = scaled_unitary_problem_solution(C=RC,c=c)
        assert np.allclose( w, w_check )

    return w


def left_multiplied_unitary_reduction(C, R, c=None):
    """  Returns C'' and H and c'' such that if
             min u^t C'' u  subject to u^t 1 = 1
         and
             w = H^{-1} u/c'  = solve(H,u)/c''
         then w also solves
             min w^t R C w  subject to w^t c = 1

         (This unravels the transforms above)

         :return C', H, c'
    """
    C_intermediate, H, c_prime = left_multiplied_unitary_problem(C=C, R=R, c=c)
    C_prime = scaled_unitary_problem(C=C_intermediate, c=c_prime)
    return C_prime, H, c_prime