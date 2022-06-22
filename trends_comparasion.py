import pandas as pd
from pytrends.request import TrendReq
import datetime as dt

#--------------------------
  # kw_list = Lista de KWs a serem buscadas no Trends
#--------------------------

def trends_table(kw_list): 
  pytrends = TrendReq(hl='pt-BR', tz=180)

  for i in kw_list:
    pytrends.build_payload(kw_list=[f'{i}'], geo='BR', timeframe='today 12-m')
    if df.empty:
      df = pytrends.interest_over_time()
    else:
      df[f'{i}'] = pytrends.interest_over_time().iloc[:,0]

  df = df.reset_index(level=0)
  df.drop('isPartial', axis=1, inplace=True)

  df['date-str'] = df['date'].dt.strftime('%B/%Y')
  df_final = df.groupby('date-str').max().reset_index().sort_values('date')
  df_final.drop('date', axis=1, inplace=True)
