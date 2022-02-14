from precise.skaters.portfoliostatic.ppoport import PPO_LS_PORT, PPO_LONG_PORT
from precise.skaters.portfoliostatic.weakport import WEAK_LONG_PORT, WEAK_LS_PORT
from precise.skaters.portfoliostatic.diagport import DIAG_LONG_PORT
from precise.skaters.portfoliostatic.hrpport import HRP_LONG_PORT, HRP_LS_PORT
from precise.skaters.portfoliostatic.schurport import SCHUR_LONG_PORT, SCHUR_LS_PORT
from precise.skaters.portfoliostatic.unitport import UNIT_LS_PORT, UNIT_LONG_PORT
from precise.skaters.portfoliostatic.equalport import EQUAL_LONG_PORT, EQUAL_LS_PORT

import random

LONG_PORT = PPO_LONG_PORT + WEAK_LONG_PORT + DIAG_LONG_PORT + HRP_LONG_PORT + UNIT_LONG_PORT + SCHUR_LONG_PORT + EQUAL_LONG_PORT
LS_PORT = PPO_LS_PORT + HRP_LS_PORT + WEAK_LS_PORT + SCHUR_LS_PORT + UNIT_LS_PORT + EQUAL_LS_PORT
PORT = LONG_PORT + LS_PORT


def random_port():
    return random.choice(PORT)


if __name__=='__main__':
    from precise.skaters.portfolioutil.portcomparison import stock_portfolio_variance_points_race
    report = stock_portfolio_variance_points_race(n_iter=5000, ports=LONG_PORT, n_dim=500, n_obs=100, k=5, n_top=100)
    from pprint import pprint
    pprint(report)