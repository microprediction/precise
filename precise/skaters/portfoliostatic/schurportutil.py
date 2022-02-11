import numpy as np

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