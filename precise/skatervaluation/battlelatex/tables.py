
from precise.skatervaluation.battleutil.compilingeloratings import elo_from_win_files
from texttable import Texttable
from latextable import draw_latex


def leaderboard_to_latex(leaderboard, caption, label, max_rows=42):
     # Oh so ugly :)
     MANAGER_REPLACEMENTS = {'_t0':' target=0',
                     '_pm':' partial moments  ',
                     '_emp':' empirical ',
                     '_ppo':' ',
                     '_r':' r=0.',
                     '_g025': ' \gamma=0.5',
                     '_g050':' \gamma=0.5',
                     '_g100': ' \gamma=1',
                      '_l010': ' r_l=0.01',
                      '_l020': ' r_l=0.02',
                     '_l050': ' r_l=0.05',
                     '_n':' window=',
                     '_long_manager':'',
                     '_vol':' (min-vol)',
                    '_quad':' (quadratic)',
                    '_sharpe':' (Sharpe)',
                    '_weak':' (weak)',
                    '_schur':' (Schur)',
                    '_hrp':' (HRP)',
                    '_pcov':'',
                    '_lw':' Ledoit Wolf',
                    'lw_':'Ledoit Wolf ',
                             '_ld': ' Ledoit Wolf',
                             'ld_': 'Ledoit Wolf ',
                             '_oas':' Oracle Approximating',
                    'buf':'Buffered ',
                    'huber':'Huber',
                    '_glcv':' Graphical lasso w/ cv',
                    '_gl':' Graphical lasso',
                    '_mcd':' min-cov-det',
                    '_d0':'',
                    '_ewa':' expon weighted ',
                    'ewa_':'Expon weighted ',
                    '_d1':'',
                    '_sk':'',
                    'scov':' ',
                    'pcov':' ',
                    'weak':'Weak ',
                    'a1':'a=1','a05':'a=0.5',
                     'b1':'b=1',
                             '_b2': 'b=2','_b5': 'b=5',
                             'lz':'Lee Zhong',
                    'hrp':'HRP',
                    'ewa_':'Expon weighted ',
                    'run_':'running ',
                    'schur':'Schur',
                    'ppo':''}

     tbl = Texttable()
     tbl.set_cols_align(["l", "l", "c"])
     tbl.set_cols_valign(["t", "m", "b"])
     rows = [['Elo', 'Approach', 'CPU']]
     for name, res in leaderboard.most_common():
          for _ in range(2):
               for k,v in MANAGER_REPLACEMENTS.items():
                    name = name.replace(k,v)
          name = name.replace('_',' ')
          if isinstance(res,tuple):
               elo_rating = round(res[0],ndigits=0)
               cpu = round(res[1],ndigits=0) if res[1] is not None else 'N/A'
          else:
               elo_rating = round(res,ndigits=0)
               cpu = 'N/A'
          rows.append([elo_rating,name,cpu])
     tbl.add_rows(rows=rows[:max_rows])
     return draw_latex(tbl, caption=caption, label=label)


def elo_latex_table(genre, category, max_rows=42):
     elo_results = dict( elo_from_win_files(genre=genre) )
     try:
          leaderboard = elo_results[category]
     except KeyError:
          print(category+' is not in '+genre)
          print('Try one of '+str(list(elo_results.keys())))
          raise KeyError

     CATEGORY_REPLACEMENTS = {'_p':' with asset count ',
                              '_n':' using historical data length '}

     description = category
     for _ in range(3):
         for k,v in CATEGORY_REPLACEMENTS.items():
              description = description.replace(k,v)
     description = genre.replace('_',' ') + ' for ' + description.replace('_',' ') + '.'
     description = description[0].upper()+description[1:]
     label='tab:'+genre+'_'+category
     return leaderboard_to_latex(leaderboard=leaderboard, caption=description, label=label, max_rows=max_rows )


if __name__=='__main__':
     ltx = elo_latex_table(genre='manager_var',category='stocks_5_days_p50_n150')
     print(ltx)






