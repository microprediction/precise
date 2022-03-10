from precise.skatervaluation.battleutil.compilingeloratings import elo_from_win_files
from pprint import pprint


if __name__=='__main__':
<<<<<<< HEAD
    category_sub_string = 'm6_daily_p100'  # e.g. m6_daily, p100, whatever, 'stocks_5_days'
=======
    category_sub_string = 'm6_daily_p100_n200_implied'  # e.g. m6_daily, p100, whatever, 'stocks_5_days'
>>>>>>> 4086d5934ed594b637d4f334bf1e2d1f6328114b
    ratings = elo_from_win_files(genre='cov_likelihood',category=category_sub_string)
    pprint(ratings)

