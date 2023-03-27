from precise.skatervaluation.battleutil.compilingeloratings import elo_from_win_files
from pprint import pprint
from precise.skatervaluation.battleutil.interpretingelo import gamma_plot


if __name__=='__main__':

    k = 2        # Elo speed parameter
    lmbda = 1e4  # Stiffness

    GENRE = 'manager_info'
    CATEGORY_MATCH = 'stocks_3_days'
    CATEGORY_SUB_STRING = 'stocks_3_days'
    MODEL_SUB_STRING = 'schur_weak_weak'
    ratings = elo_from_win_files(genre=GENRE, category=CATEGORY_MATCH, k=k)
    gamma_plot(ratings, model_sub_string=MODEL_SUB_STRING, max_gamma=10)
    gamma_plot(ratings,  model_sub_string=MODEL_SUB_STRING, max_gamma=30)
    gamma_plot(ratings,  model_sub_string=MODEL_SUB_STRING, max_gamma=40)
    gamma_plot(ratings, model_sub_string=MODEL_SUB_STRING, min_gamma=40, max_gamma=100)
    gamma_plot(ratings,  model_sub_string=MODEL_SUB_STRING, max_gamma=100)
    gamma_plot(ratings, model_sub_string=MODEL_SUB_STRING, max_gamma=20, lmbda =lmbda)
    pprint(ratings)



