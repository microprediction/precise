from precise.skatervaluation.battlelatex.tables import elo_latex_table

if __name__=='__main__':
     ltx = elo_latex_table(genre='cov_likelihood',category='stocks_5_days_p50_n150')
     print(ltx)
