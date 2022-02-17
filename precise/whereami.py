import os
from pathlib import Path
from pprint import pprint
TOP = os.path.dirname(os.path.abspath(__file__))
BATTLE_RESULTS_DIR = os.path.join(TOP, 'skatervaluation', 'battleresults')
GITHUB_COV_SKATERS = 'https://github.com/microprediction/precise/blob/main/precise/skaters/covariance/'
GITHUB_MANAGERS = 'https://github.com/microprediction/precise/blob/main/precise/skaters/managers/'
ROOT = Path(TOP).parent.absolute()
M6_EXAMPLES = os.path.join(ROOT,'examples_m6')
MANAGER_MANIFEST = os.path.join(ROOT,'LISTING_OF_MANAGERS.md')
COV_SKATER_MANIFEST = os.path.join(ROOT,'LISTING_OF_COV_SKATERS.md')
TESTSERROR = os.path.join(ROOT,'testserrors')


def url_from_skater_name(name:str)->str:
    """
         Infer the location in GitHub for the skater's code
         e.g.  buf_emp_pcov_d0_n100 ->https://github.com/microprediction/precise/blob/main/precise/skaters/covariance/bufemp.py
    """
    return GITHUB_COV_SKATERS + ''.join(name.split('_')[:2])+'.py'


def url_from_manager_name(name:str)->str:
    return GITHUB_MANAGERS + ''.join(name.split('_')[:1])+'managers.py'



if __name__=='__main__':
    print(TOP)
    print(url_from_skater_name(name='buf_emp_pcov_d0_n100'))
    print(M6_EXAMPLES)
