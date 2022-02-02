from precise.whereami import BATTLE_RESULTS_DIR
from glob import glob
import json
from collections import Counter
import os

# Retrieving collections of battles


def win_dirs(genre='likelihood'):
    return [ d[:-1] for d in glob(BATTLE_RESULTS_DIR + os.path.sep + genre + "/*/", recursive = False)]


def win_data(genre='likelihood'):
    """
    :return: [ ( category, counter ) ]
    """
    return [(category, load_win_data(cat_files)) for (category,cat_files) in win_files(genre=genre)]


def win_files(genre='likelihood'):
    return [(wd.split('/')[-1], glob(wd+"/*.json")) for wd in win_dirs(genre=genre)]


def load_win_data(cat_files):
    data = Counter()
    for fn in cat_files:
        with open(fn,'rt') as fh:
            new_data = Counter(json.load(fh))
            data.update(new_data)
    return data



if __name__=='__main__':
    wd = win_data(genre='likelihood')
    print([c for c,_ in win_data()])

