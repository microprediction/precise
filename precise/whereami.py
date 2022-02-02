import os
from pathlib import Path
from pprint import pprint
TOP = os.path.dirname(os.path.abspath(__file__))
BATTLE_RESULTS_DIR = os.path.join(TOP, 'skatervaluation', 'battleresults')
GITHUB_COV_SKATERS = 'https://github.com/microprediction/precise/blob/main/precise/skaters/covariance/'
ROOT = Path(TOP).parent.absolute()
M6_EXAMPLES = os.path.join(ROOT,'examples_m6')


def url_from_skater_name(name:str)->str:
    """
         Infer the location in GitHub for the skater's code
         e.g.  buf_emp_pcov_d0_n100 ->https://github.com/microprediction/precise/blob/main/precise/skaters/covariance/bufemp.py
    """
    if any([cv in name for cv in ['_pcov_','_cov_','_scov_']]):
        return GITHUB_COV_SKATERS + ''.join(name.split('_')[:2])+'.py'


if __name__=='__main__':
    print(TOP)
    print(url_from_skater_name(name='buf_emp_pcov_d0_n100'))
    print(M6_EXAMPLES)
