from precise.skatervaluation.battleutil.compilingeloratings import elo_from_win_files
from pprint import pprint


if __name__=='__main__':
    category_sub_string = 'stocks_1_days'  # e.g. m6_daily, p100, whatever
    ratings = elo_from_win_files(genre='manager_info', category='stocks_1_days_p500_n90')
    pprint([r for r in ratings if category_sub_string in r[0]])

