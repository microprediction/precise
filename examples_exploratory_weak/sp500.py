
url = 'https://raw.githubusercontent.com/leosmigel/analyzingalpha/master/2019-09-18-sp500-historical-components-and-changes/2021-09-24-sp500-history.csv'
import pandas as pd
df = pd.read_csv(url)
print(df[:10])

