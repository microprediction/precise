from precise.skatervaluation.battlelatex.tables import elo_latex_table

if __name__=='__main__':
     ltx = elo_latex_table(genre='manager_var',category='stocks_20_days_p2_n60')
     print(ltx)