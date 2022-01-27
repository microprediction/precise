from runthis import parse_kwargs
from precise.skatertools.comparison.skaterbattle import skater_battle
import os

# Infers params from file name and runs a battle

if __name__=='__main__':
    kwargs = parse_kwargs(__file__.split(os.path.sep)[-1])
    m6_battle(**kwargs)