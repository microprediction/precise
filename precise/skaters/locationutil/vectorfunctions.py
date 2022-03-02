import numpy as np

def normalize(x):
    ### See also portfolioutil.portfunctions.normalize_portfolio
    try:
        return x/sum(x)
    except (TypeError, ArithmeticError, RuntimeWarning):
        try:
            return [xi/sum(x) for xi in x]
        except (TypeError, ArithmeticError):
            if sum(x)<1e-12:
                return x
            else:
                raise ValueError('??')


def scatter(x):
    """
         matrix  x x^t
    """
    x1 = np.atleast_2d(x)
    xt = np.transpose(x1)
    s = np.dot(xt,x1)
    assert np.array_equal( np.shape(s), [len(x),len(x)] )
    return s


if __name__=='__main__':
    from pprint import pprint
    x = np.random.randn(5)
    pprint(scatter(x))