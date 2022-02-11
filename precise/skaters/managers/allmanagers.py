from precise.skaters.managers.weakmanagers import WEAK_LONG_MANAGERS
from precise.skaters.managers.ppomanagers import PPO_LONG_MANGERS
from precise.skaters.managers.hrpmanagers import HRP_LONG_MANAGERS
from precise.skaters.managers.schurmanagers import SCHUR_LONG_MANAGERS

# d0 managers unless otherwise stated

LONG_MANAGERS = WEAK_LONG_MANAGERS + PPO_LONG_MANGERS + HRP_LONG_MANAGERS + SCHUR_LONG_MANAGERS
LS_MANAGERS = []
MANAGERS = LONG_MANAGERS + LS_MANAGERS