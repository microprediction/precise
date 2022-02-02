
# Allocators

from precise.skaters.portfolioutil.ppo import ppo_quad_alloc, ppo_sharpe_alloc, ppo_vol_alloc
from precise.skaters.portfolioutil.weak import prc_weak_alloc
from precise.skaters.portfolioutil.unitary import prc_unit_alloc
from precise.skaters.portfolioutil.diagonal import prc_diag_alloc

PRC_ALLOC = [prc_diag_alloc, prc_unit_alloc, prc_weak_alloc]
PPO_ALLOC = [ppo_vol_alloc, ppo_sharpe_alloc, ppo_quad_alloc]
ALLOCATORS = PRC_ALLOC + PPO_ALLOC


# Portfolio generators

from precise.skaters.portfolioutil.ppo import ppo_quad_port, ppo_sharpe_port, ppo_vol_port
from precise.skaters.portfolioutil.weak import prc_weak_port
from precise.skaters.portfolioutil.unitary import prc_unit_port
from precise.skaters.portfolioutil.diagonal import prc_diag_port
from precise.skaters.portfolioutil.parity import HRP_PORT

PRC_PORT = [prc_weak_port, prc_diag_port, prc_unit_port ]
PPO_PORT = [ppo_vol_port, ppo_sharpe_port, ppo_quad_port]

PORT = PRC_PORT + PPO_PORT

import random


def random_port():
    return random.choice(PORT)
