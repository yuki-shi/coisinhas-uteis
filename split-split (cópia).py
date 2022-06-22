from oauth2client.service_account import ServiceAccountCredentials

import gspread
from gspread_dataframe import set_with_dataframe

import re
import pandas as pd
import numpy as np

#------------------------------------------------------------------
  # Função que, a partir de uma planilha do Google Sheets, colapsa uma célula
  # em várias novas linhas, tendo a possibilidade de alterar os valores de cada
  # uma conforme desejado. Acho


  # auth = autenticação em formato JSON
  # url = URL da planilha do Sheets a ser trabalhada
  # sep = caractere que separa cada string a ser splitada
  # column_to_split = coluna onde a ser splitada
  # column_to_replace = coluna que terá seus valores repetidos zerados, salvo a última ocorrência de cada repetição
  # aba_extracao = aba do Sheets com os dados brutos
  # aba_resultado = aba do Sheets onde os dados serão exportados
#------------------------------------------------------------------

def splitsplit(auth, url, sep,
               column_to_split,
               column_to_replace,
               aba_extracao,
               aba_resultado):

    for i in url:

        key = re.findall(r'.*\/d\/(.*)\/edit.*', i)
        key = ''.join([str(x) for x in key])

        ## Autenticação da API 

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            auth,
            scopes=scopes
        )

        gc = gspread.authorize(credentials)


        ## Abrir a planilha e convertê-la em dataframe

        sh = gc.open_by_key(key)

        worksheet = sh.get_worksheet(aba_extracao)
        worksheet_yuk = sh.get_worksheet(aba_resultado)

        rows = worksheet.get_all_values()
        df = pd.DataFrame.from_records(rows)

        columns = df.iloc[0].values
        df.columns = columns
        df.drop(index=0, axis=0, inplace=True)

        ## Criação da coluna 'Index'

        index = [x for x in range(len(df))]
        df['Index'] = index

        ## Separação em 2 dataframes

        mask = df[column_to_split].str.contains(sep)
        df_erro = df.loc[mask]
        df_certo = df.loc[~mask]

        ## Preparação para tornar column_to_split como index

        c = [x for x in columns if x not in column_to_split]
        c.append('Index')

        ## Split e order by

        df_erro2 = (df_erro.set_index(c)
                    .apply(lambda x: x.str.split(sep).explode())
                    .reset_index())

        df_erro2 = df_erro2.sort_values(['Index', column_to_split], ascending=[1,0])


        ## Mudança dos duplicados pelo valor dummy

        df_erro2.loc[df_erro2.duplicated([column_to_replace, 'Index']), column_to_replace] = np.nan
        df_erro2 = df_erro2.sort_values(['Index', column_to_split], ascending=[1, 1])

        ## Join e limpeza

        df_final = pd.concat([df_certo, df_erro2], ignore_index=True)
        df_final.drop('Index', axis=1, inplace=True)

        #if 'Story Points' in df_final.columns:
        #  df_final.loc[df_final[column_to_replace].isnull(), 'Story Points'] = np.nan

        set_with_dataframe(worksheet_yuk, df_final)