from precise.whereami import SKATER_WIN_DATA
from glob import glob
import json
from collections import Counter
from pprint import pprint

# Retrieving collections of battles

def win_data():
    """
    :return: [ ( category, counter ) ]
    """
    return [ (category, load_win_data(cat_files)) for (category,cat_files) in win_files() ]


def win_dirs():
    return [ d[:-1] for d in glob(SKATER_WIN_DATA+"/*/", recursive = False) ]


def win_files():
    return [ (wd.split('/')[-1], glob(wd+"/*.json")) for wd in win_dirs() ]


def load_win_data(cat_files):
    data = Counter()
    for fn in cat_files:
        with open(fn,'rt') as fh:
            new_data = Counter(json.load(fh))
            data.update(new_data)
    return data



if __name__=='__main__':
    wd = win_data()
    print([c for c,_ in win_data()])

