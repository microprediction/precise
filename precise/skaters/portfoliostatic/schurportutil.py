import numpy as np
from precise.skaters.covarianceutil.covfunctions import schur_complement, \
    to_symmetric, multiply_by_inverse, inverse_multiply, is_positive_def, nearest_pos_def
from scipy.optimize import root_scalar


def schur_augmentation(A,B,C,D, gamma):
    """
       Mess with A, D to try to incorporate some off-diag info
    """
    if gamma>0.0:
        max_gamma = _maximal_gamma(A=A, B=B, C=C, D=D)
        augA, bA = pseudo_schur_complement(A=A, B=B, C=C, D=D, gamma=gamma * max_gamma)
        augD, bD = pseudo_schur_complement(A=D, B=C, C=B, D=A, gamma=gamma * max_gamma)

        augmentation_fail = False
        if not is_positive_def(augA):
            try:
                Ag = nearest_pos_def(augA)
            except np.linalg.LinAlgError:
                augmentation_fail=True
        else:
            Ag = augA
        if not is_positive_def(augD):
            try:
                Dg = nearest_pos_def(augD)
            except np.linalg.LinAlgError:
                augmentation_fail=True
        else:
            Dg = augD

        if augmentation_fail:
            print('Warning: augmentation failed')
            reductionA = 1.0
            reductionD = 1.0
            reductionRatioA = 1.0
            Ag = A
            Dg = D
        else:
            reductionD = np.linalg.norm(Dg)/np.linalg.norm(D)
            reductionA = np.linalg.norm(Ag)/np.linalg.norm(A)
            reductionRatioA = reductionA/reductionD
    else:
        reductionRatioA = 1.0
        reductionA = 1.0
        reductionD = 1.0
        Ag = A
        Dg = D

    info = {'reductionA': reductionA,
                'reductionD': reductionD,
                'reductionRatioA': reductionRatioA}
    return Ag, Dg, info



def  pseudo_schur_complement(A, B, C, D, gamma, lmbda=None, warn=False):
    """
       Augmented cov matrix for "A" inspired by the Schur complement
    """
    if lmbda is None:
        lmbda=gamma
    try:
        Ac_raw = schur_complement(A=A, B=B, C=C, D=D, gamma=gamma)
        nA = np.shape(A)[0]
        nD = np.shape(D)[0]
        Ac = to_symmetric(Ac_raw)
        M = symmetric_step_up_matrix(n1=nA, n2=nD)
        Mt = np.transpose(M)
        BDinv = multiply_by_inverse(B, D, throw=False)
        BDinvMt = np.dot(BDinv, Mt)
        Ra = np.eye(nA) - lmbda * BDinvMt
        Ag = inverse_multiply(Ra, Ac, throw=False, warn=False)
    except np.linalg.LinAlgError:
        if warn:
            print('Pseudo-schur failed, falling back to A')
        Ag = A
    n = np.shape(A)[0]
    b = np.ones(shape=(n,1))
    return Ag, b


def _maximal_gamma(A,B,C,D):
    """
        Tries to find a large value of gamma where both augmented matrixes where is_positive_def(Ag) and is_positive_def(Dg)
    """

    Ag, _ = pseudo_schur_complement(A=A, B=B, C=C, D=D, gamma=1.0, lmbda=1.0)
    Dg, _ = pseudo_schur_complement(A=D, B=C, C=B, D=A, gamma=1.0, lmbda=1.0)
    pos_def = is_positive_def(Ag) and is_positive_def(Dg)
    if pos_def:
        return 1.0
    else:
        def _gamma_objective(gamma, A, B, C, D):
            Ag, _ = pseudo_schur_complement(A=A, B=B, C=C, D=D, gamma=gamma, lmbda=gamma)
            Dg, _ = pseudo_schur_complement(A=D, B=C, C=B, D=A, gamma=gamma, lmbda=gamma)
            pos_def = is_positive_def(Ag) and is_positive_def(Dg)
            return -0.01 if pos_def else 1.0

        try:
            sol = root_scalar(f=_gamma_objective, args=(A,B,C,D), method='bisect', x0=0.25,
                              x1=0.5, xtol=0.05, bracket=(0,0.95), maxiter=5)
            return min(max(sol.root - 0.1, 0), 1.0)
        except ValueError:
            return 0.0



def symmetric_step_up_matrix(n1, n2):
    """
       :return M such that M np.ones(n2) = np.ones(n1)
    """

    def _Mj(n1, n2, j):
        assert abs(n1 - n2) <= 1
        nd = n2 - n1
        if nd == 0:
            return np.eye(n1)
        else:
            j_row = np.ones(shape=(1, n2)) / n2
            E = np.eye(n2)
            Mj = np.concatenate([E[:j], j_row, E[j:]], axis=0)
            assert np.linalg.norm(np.dot(Mj, np.ones(n2)) - np.ones(n1)) < 1e-8
            return Mj

    if n1 <n2:
        M = symmetric_step_up_matrix(n2, n1).transpose() * n1 / n2
    elif n1==n2:
        M = np.eye(n1)
    else:
        M = np.zeros(shape=(n1 ,n2))
        for j in range(n1):
            M = M + _Mj(n1 ,n2 ,j ) /n1
    assert np.linalg.norm(np.dot(M, np.ones(n2)) - np.ones(n1)) < 1e-8
    return M


def even_split(cov, n_split=5)->(float,float):
    """
        Parity methods require some way of splitting assets into two groups
        This simple method is the default
    """
    n_dim = np.shape(cov)[0]
    if n_dim<=n_split:
        return (n_dim,0)
    else:
        n1 = int(n_dim / 2)
        n2 = n_dim - n1
        return n1, n2
