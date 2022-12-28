from precise.skatervaluation.battleutil.compilingeloratings import elo_from_win_files
from pprint import pprint


# View a list of method of combining models


if __name__=='__main__':
    category_sub_string = 'tm'  # e.g. m6_daily, p100, whatever
    ratings = elo_from_win_files(genre='manager_var', category=category_sub_string)
    pprint(ratings)

