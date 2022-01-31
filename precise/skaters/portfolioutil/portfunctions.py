import numpy as np


def positive_mass(w):
    return sum([wi for wi in w if wi>0])


def negative_mass(w):
    return sum([-wi for wi in w if wi<0])


def relative_negative_mass(w):
    pm = positive_mass(w)
    nm = negative_mass(w)
    return nm/(pm-nm)


def portfolio_variance(cov, w):
    w1 = np.atleast_2d(w)
    wt = np.atleast_2d(w).transpose()
    return np.matmul( np.matmul(w1, np.array(cov)), wt)[0][0]


def exclude_negative_weights(w, with_neg_mass=False):
    """
         Take out negative weights, preserving presumed total mass
    """
    pos_mass = sum([wi for wi in w if wi>0])
    neg_mass = sum([-wi for wi in w if wi<0])
    presumed_mass = pos_mass-neg_mass
    ratio = presumed_mass/pos_mass
    w_pos = [ wi*ratio if wi>0 else 0.0 for wi in w]
    return w_pos, neg_mass if with_neg_mass else w_pos



if __name__=='__main__':
    sgma = np.array([[1,4],[4,20]])
    w = [0.3,0.4]
    print( portfolio_variance(cov=sgma,w=w) )