from precise.whereami import BATTLE_RESULTS_DIR
from glob import glob
import json
from collections import Counter
import os

# Retrieving collections of battles


def win_dirs(genre='cov_likelihood', category=None):
    all_dirs = [ d[:-1] for d in glob(BATTLE_RESULTS_DIR + os.path.sep + genre + "/*/", recursive = False) ]
    if category is None:
        return all_dirs
    else:
        return [d for d in all_dirs if category in d]



def win_data(genre='cov_likelihood', category=None):
    """
    :return: [ ( category, counter ) ]
    """
    return [(category, load_win_data(cat_files)) for (category,cat_files) in win_files(genre=genre, category=category)]


def win_files(genre='likelihood', category=None):
    return [(wd.split('/')[-1], glob(wd+"/*.json")) for wd in win_dirs(genre=genre, category=category)]


def load_win_data(cat_files):
    data = Counter()
    for fn in cat_files:
        with open(fn,'rt') as fh:
            try:
                new_data = Counter(json.load(fh))
                data.update(new_data)
            except json.decoder.JSONDecodeError:
                print('Issue with '+fn)
                print('huh')

    return data



if __name__=='__main__':
    wd = win_data(genre='likelihood')
    print([c for c,_ in win_data()])

