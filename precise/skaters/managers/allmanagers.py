from precise.skaters.managers.weakmanagers import WEAK_LONG_MANAGERS
from precise.skaters.managers.ppomanagers import PPO_LONG_MANGERS
from precise.skaters.managers.hrpmanagers import HRP_LONG_MANAGERS
from precise.skaters.managers.schurmanagers import SCHUR_LONG_MANAGERS
from precise.skaters.managers.rflmanagers import RFL_HRP_LONG_MANAGERS
from precise.skaters.managers.equalmanagers import EQUAL_LONG_MANAGERS
from precise.skaters.managers.ldpmanagers import LDP_LONG_MANAGERS
from precise.skaters.managers.molybogamanagers import MOLYBOGA_LONG_MANAGERS
from tomark import Tomark
import random

# d0 managers unless otherwise stated

LONG_MANAGERS = WEAK_LONG_MANAGERS + PPO_LONG_MANGERS + HRP_LONG_MANAGERS + SCHUR_LONG_MANAGERS + RFL_HRP_LONG_MANAGERS
LONG_MANAGERS = WEAK_LONG_MANAGERS + PPO_LONG_MANGERS[:2] + HRP_LONG_MANAGERS +\
SCHUR_LONG_MANAGERS + RFL_HRP_LONG_MANAGERS[:2] + EQUAL_LONG_MANAGERS + LDP_LONG_MANAGERS + MOLYBOGA_LONG_MANAGERS


LS_MANAGERS = []
MANAGERS = LONG_MANAGERS + LS_MANAGERS



def manager_from_name(name):
    valid = [f for f in MANAGERS if f.__name__ == name]
    return valid[0] if len(valid)==1 else None


def manager_manifest():
    from precise.whereami import url_from_manager_name
    return dict([(f.__name__, url_from_manager_name(f.__name__)) for f in MANAGERS])


def random_cov_skater():
    return random.choice(MANAGERS)


def manager_manifest_markdown():
    manifest = manager_manifest()
    data = [ {'manager':mgr,'location':url} for mgr, url in manifest.items() ]
    markdown = Tomark.table(data)
    return markdown


def write_manager_manifest():
    from precise.whereami import MANAGER_MANIFEST
    markdown = manager_manifest_markdown()
    with open(MANAGER_MANIFEST,'wt') as fh:
        fh.write(markdown)



if __name__=='__main__':
    from pprint import pprint
    pprint(manager_manifest())
    write_manager_manifest()

