if __name__=='__main__:
  from precise import m6_competition_entry, m6_dump
  df = m6_competition_entry()
  m6_dump(df=df, file_name='my_entry.csv')
