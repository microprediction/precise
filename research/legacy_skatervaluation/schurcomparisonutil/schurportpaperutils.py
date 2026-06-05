# These are merely here as a convenience for gamma academic
from precise.skaters.portfoliostatic.weakportfactory import weak_portfolio_factory
from precise.skaters.portfoliostatic.schurportfactory import schur_portfolio_factory
from precise.skaters.portfoliostatic.hrpportfactory import hierarchical_risk_parity_portfolio_factory
from precise.skaters.portfoliostatic.weakalloc import weak_long_alloc
from precise.skaters.portfoliostatic.diagalloc import diag_alloc
from precise.skaters.portfoliostatic.unitport import unit_port
from precise.skaters.portfoliostatic.diagport import diag_long_port
import numpy as np
from precise.inclusion.matplotlibinclusion import using_matplotlib
from precise.skatervaluation.portfoliocomparisonutil.portcomparison import port_kurtosis
from pprint import pprint

# Some utilities used in the Schur paper
# Intent is examination of the impact of the gamma parameter

if using_matplotlib:
    import matplotlib.pyplot as plt

    def gamma_comparison_and_plot(rnd_cov, rnd_cov_kwargs, n_anchor, n_true,
                                  n_observed, max_time, n_split, xlabel, g_ports=None):

        if g_ports is None:
            g_ports = G_PORTS

        def moment_plot(moments: dict, sty='go'):
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
            plt.plot(x_plot, y_plot, sty)
            plt.grid()
            plt.xlabel('Gamma')
            plt.ylabel('Portfolio variance')

        stys = ['go', 'r+', 'b*']
        stys = ['go']
        bps = list()
        ports = g_ports + OTHER_PORTS
        for sty in stys:
            seed_cov = rnd_cov(**rnd_cov_kwargs)
            moments = port_kurtosis(ports=ports, seed_cov=seed_cov, n_true=n_true,
                                    n_anchor=n_anchor, n_observed=n_observed,
                                    metric='mean', port_kwargs={'n_split': n_split},
                                    max_time=max_time)
            pprint(moments)
            try:
                # Assumes 10% return annually
                bps_saved = int(10000 * 0.1 * (moments['g000'] - moments['g100']) / (2 * moments['g000']))
                bps.append(bps_saved)
                pprint({'bps_saved': np.mean(bps)})
            except:
                pass
            normalized_moments = dict([(k, v / moments['g000']) for k, v in moments.items()])
            moment_plot(moments=normalized_moments, sty=sty)

        plt.title('Portfolio variance as $\gamma$ is varied')
        full_xlabel = xlabel + ' benefit=' + str(round(np.mean(bps))) + ' bps'
        plt.xlabel(full_xlabel)
        plt.show()
        plt.savefig('schur.png')


else:
    def gamma_comparison_and_plot(**kwargs):
        print('pip install matplotlib')


def deep_gamma_port(cov, gamma, n_split, jiggle=False):
    assert gamma is not None
    return schur_portfolio_factory(port=weak_portfolio_factory,
                                   alloc=weak_long_alloc, cov=cov,
                                   n_split=n_split, gamma=gamma, jiggle=jiggle)


def gamma_port(cov, gamma, n_split, jiggle=False):
    """
         A shallow version of Schur intended to try to separate out the effect
         of using Schur at the top division step, versus not using it there.
    """

    # Only one schur step and then HRP
    assert gamma is not None
    return schur_portfolio_factory(port=hierarchical_risk_parity_portfolio_factory,
                                   port_kwargs={'n_split':n_split},
                                   alloc=diag_alloc, cov=cov,
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
def week(cov, **ignore):
    return weak_long_port(cov=cov)

from precise.skaters.portfoliostatic.unitport import unit_port_p050, unit_port_p090
def u050(cov, **ignore):
    return unit_port_p050(cov=cov)
def u090(cov, **ignore):
    return unit_port_p090(cov=cov)


def d005(cov, n_split, **ignore):
    return deep_gamma_port(cov=cov, gamma=0.05, n_split=n_split)


def d095(cov, n_split, **ignore):
    return deep_gamma_port(cov=cov, gamma=0.95, n_split=n_split)


def d050(cov, n_split, **ignore):
    return deep_gamma_port(cov=cov, gamma=0.5, n_split=n_split)

def d075(cov, n_split, **ignore):
    return deep_gamma_port(cov=cov, gamma=0.75, n_split=n_split)


def d025(cov, n_split, **ignore):
    return deep_gamma_port(cov=cov, gamma=0.25, n_split=n_split)




G_PORTS = [g000, g000i, g050, g010, g010j, g015, g020, g020j, g025,
           g030, g035, g040, g050, g060, g070, g080, g090, g100]
OTHER_PORTS = [u050, d005, d025, d050, d075, d095]
