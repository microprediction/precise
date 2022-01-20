from precise.skaters.covarianceutil.conventions import X_TYPE
from precise.skaters.covariance.bufferedpre import buf_sk_factory
from precise.skaters.covarianceutil.differencing import d1_factory
from sklearn.covariance import GraphicalLasso, GraphicalLassoCV, LedoitWolf, MinCovDet, OAS, EmpiricalCovariance





def buf_ec_pcov_d0(y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """ Sklearn empirical covariance based estimator for IID observations """
    return buf_sk_factory(cls=EmpiricalCovariance, y=y, s=s, n_buffer=n_buffer)


def buf_ld_pcov_d0(y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """ Ledoit-Wolf covariance based estimator for IID observations """
    return buf_sk_factory(cls=LedoitWolf, y=y, s=s, n_buffer=n_buffer)


def buf_gl_pcov_d0(y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """ Graphical Lasso covariance based estimator for IID observations """
    return buf_sk_factory(cls=GraphicalLasso, y=y, s=s, n_buffer=n_buffer)


def buf_glcv_pcov_d0(y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """ Graphical Lasso CV covariance based estimator for IID observations """
    return buf_sk_factory(cls=GraphicalLassoCV, y=y, s=s, n_buffer=n_buffer)


def buf_mcd_pcov_d0(y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """ Minimumn covariance based estimator for IID observations """
    # https://scikit-learn.org/stable/modules/generated/sklearn.covariance.MinCovDet.html#sklearn.covariance.MinCovDet
    return buf_sk_factory(cls=MinCovDet, y=y, s=s, n_buffer=n_buffer)


def buf_oas_pcov_d0(y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """ OAS based estimator for IID observations """
    return buf_sk_factory(cls=OAS, y=y, s=s, n_buffer=n_buffer)


# Differenced versions to be applied to time-series with independent increments



def buf_ec_pcov_d1( y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    return d1_factory( f = buf_ec_pcov_d0, y=y, s=s, n_buffer=n_buffer )

def buf_ld_pcov_d1(y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """ Ledoit-Wolf covariance based estimator for IID changes """
    return d1_factory(f=buf_ld_pcov_d0, y=y, s=s, n_buffer=n_buffer)


def buf_oas_pcov_d1(y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """ OAS based estimator for IID changes  """
    return d1_factory(f=buf_oas_pcov_d0, y=y, s=s, n_buffer=n_buffer)


def buf_gl_pcov_d1(y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """ GL based estimator for IID changes  """
    return d1_factory(f=buf_gl_pcov_d0, y=y, s=s, n_buffer=n_buffer)


def buf_glcv_pcov_d1(y:X_TYPE=None, s:dict=None,  n_buffer:int=100):
    """ GL CV based estimator for IID changes  """
    return d1_factory(f=buf_glcv_pcov_d0, y=y, s=s, n_buffer=n_buffer)





