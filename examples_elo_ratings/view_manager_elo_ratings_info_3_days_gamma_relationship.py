from precise.skatervaluation.battleutil.compilingeloratings import elo_from_win_files
from pprint import pprint
from precise.skatervaluation.battleutil.interpretingelo import gamma_plot


if __name__=='__main__':
    GENRE = 'manager_info'
    CATEGORY_MATCH = 'stocks_3_days'
    CATEGORY_SUB_STRING = 'stocks_3_days'
    MODEL_SUB_STRING = 'schur_weak_weak'
    ratings = elo_from_win_files(genre=GENRE, category=CATEGORY_MATCH)
    gamma_plot(ratings,  model_sub_string=MODEL_SUB_STRING)



