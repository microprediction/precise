from precise.skaters.portfoliostatic.ppoport import PPO_PORT, PPO_LONG_PORT
from precise.skaters.portfoliostatic.weakport import WEAK_PORT, WEAK_LONG_PORT
from precise.skaters.portfoliostatic.diagport import DIAG_PORT, DIAG_LONG_PORT
from precise.skaters.portfoliostatic.hrpport import HRP_PORT, HRP_LONG_PORT
from precise.skaters.portfoliostatic.schurport import SCHUR_PORT, SCHUR_LONG_PORT
from precise.skaters.portfoliostatic.unitport import UNIT_PORT, UNIT_LONG_PORT

import random


PORT = PPO_PORT + WEAK_PORT + DIAG_PORT + HRP_PORT + UNIT_PORT + SCHUR_PORT
LONG_PORT =  PPO_LONG_PORT + WEAK_LONG_PORT + DIAG_LONG_PORT + HRP_LONG_PORT + UNIT_LONG_PORT + SCHUR_LONG_PORT


def random_port():
    return random.choice(PORT)


if __name__=='__main__':
    from precise.skaters.portfoliostatic.porttesting import ports_test
    ports_test(ports=PORT,n_dim=50)