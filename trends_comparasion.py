import pandas as pd
from pytrends.request import TrendReq
import datetime as dt

#--------------------------
   # Criar dataframe vazio e preenchê-lo consome mais memória do que
   # realizar a operação com listas, o ideal seria transformar o dataframe
   # resultante de .interest_over_time() em dict e, então, concatenar
   # a lista de dicts em um novo dataframe.
   # Por ora, como para meus fins a iteraço não ocorre mais que 5 vezes,
   # creio que esteja ok.

   # kw_list = lista de KWs a serem buscadas no Google Trends
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
  
  return df_final
