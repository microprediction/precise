# These are merely here as a convenience for gamma studies
from precise.skaters.portfoliostatic.diagportfactory import diagonal_portfolio_factory
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfoliostatic.unitportfactory import unit_portfolio_factory
from precise.skaters.portfoliostatic.schurportfactory import schur_portfolio_factory
from precise.skaters.portfoliostatic.diagalloc import diag_alloc
from precise.skaters.portfoliostatic.unitalloc import unit_alloc
from precise.skaters.portfoliostatic.weakalloc import weak_long_alloc
from precise.skaters.portfoliostatic.unitport import unit_port
from precise.skaters.portfoliostatic.diagport import diag_long_port


# Some utilities used in the Schur paper
# Intent is examination of the impact of the gamma parameter

def moment_plot(moments:dict, sty='go'):
    """ Plot portfolio var against gamma
    """
    x_plot = list()
    y_plot = list()
    for stp in range(0, 100, 5):
        ky = 'g' + str(stp).zfill(3)
        if ky in moments:
            x_plot.append(stp / 100)
            y_plot.append(moments[ky])
    import matplotlib.pyplot as plt
    plt.plot(x_plot, y_plot, sty )
    plt.grid()
    plt.xlabel('Gamma')
    plt.ylabel('Portfolio variance')



def gamma_port(cov, gamma, n_split, jiggle=False):
    assert gamma is not None
    return schur_portfolio_factory(port=weak_portfolio_factory,
                                   alloc=weak_long_alloc, cov=cov,
                                   n_split=n_split, gamma=gamma, jiggle=jiggle)


def unitary(cov, **ignore):
    return unit_port(cov=cov)


def diagn(cov, **ignore):
    return diag_long_port(cov=cov)


def g000(cov, n_split, **ignore):
    return gamma_port(cov=cov, gamma=0, n_split=n_split)


def g000i(cov, n_split):
    return gamma_port(cov=cov, gamma=0, n_split=n_split)


def g005(cov, n_split):
    return gamma_port(cov=cov, gamma=0.05, n_split=n_split)


def g010(cov, n_split):
    return gamma_port(cov=cov, gamma=0.10, n_split=n_split)


def g010j(cov, n_split):
    return gamma_port(cov=cov, gamma=0.10, n_split=n_split, jiggle=True)


def g015(cov, n_split):
    return gamma_port(cov=cov, gamma=0.15, n_split=n_split)


def g020(cov, n_split):
    return gamma_port(cov=cov, gamma=0.20, n_split=n_split)


def g020j(cov, n_split):
    return gamma_port(cov=cov, gamma=0.20, n_split=n_split, jiggle=True)


def g025(cov, n_split):
    return gamma_port(cov=cov, gamma=0.25, n_split=n_split)


def g030(cov, n_split):
    return gamma_port(cov=cov, gamma=0.30, n_split=n_split)


def g035(cov, n_split):
    return gamma_port(cov=cov, gamma=0.35, n_split=n_split)


def g040(cov, n_split):
    return gamma_port(cov=cov, gamma=0.40, n_split=n_split)


def g040i(cov, n_split):
    return gamma_port(cov=cov, gamma=0.40, n_split=n_split)


def g050(cov, n_split):
    return gamma_port(cov=cov, gamma=0.50, n_split=n_split)


def g060(cov, n_split):
    return gamma_port(cov=cov, gamma=0.60, n_split=n_split)


def g070(cov, n_split):
    return gamma_port(cov=cov, gamma=0.70, n_split=n_split)


def g080(cov, n_split):
    return gamma_port(cov=cov, gamma=0.80, n_split=n_split)


def g090(cov, n_split):
    return gamma_port(cov=cov, gamma=0.90, n_split=n_split)


def g100(cov, n_split):
    return gamma_port(cov=cov, gamma=1.00, n_split=n_split)

from precise.skaters.portfoliostatic.equalport import equal_long_port
def eql(cov, **ignore):
    return equal_long_port(cov=cov)

from precise.skaters.portfoliostatic.weakport import weak_long_port
def wk(cov,**ignore):
    return weak_long_port(cov=cov)

G_PORTS = [g000, g000i, g050, g010, g010j, g015, g020, g020j, g025,
           g030, g035, g040, g050, g060, g070, g080, g090, g100]
OTHER_PORTS = [unitary, diagn, eql, wk]
