import os
import pandas as pd


repo = '..'
dir_series = os.path.join(repo, 'datos', 'series_de_tiempo', '')

dir_datos_abiertos = os.path.join(repo, 'datos_abiertos', '')
dir_series_abiertos = os.path.join(dir_datos_abiertos, 'series_de_tiempo', 'nuevos', '')
dir_save = os.path.join(dir_datos_abiertos, 'formato_especial', '')

muertes_df = (pd.read_csv(dir_series + 'covid19_mex_muertes_nuevas.csv')
            .set_index('Fecha')['Nacional']
            .rename('Nuevas_JH'))
muertes_df.index = pd.to_datetime(muertes_df.index)

muertes_abiertos_df = (pd.read_csv(dir_series_abiertos + 'covid19_mex_muertes.csv')
           .set_index('Fecha')['Nacional']
           .rename('Nuevas_abiertos'))
muertes_abiertos_df.index = pd.to_datetime(muertes_abiertos_df.index)

nuevas = pd.concat((muertes_df, muertes_abiertos_df), axis = 1).fillna(0).astype(int)
acumuladas = nuevas.cumsum()

# cutoff = '2020-02-28'


# Escribimos archivos
# .loc[cutoff:, :]

nuevas.to_csv(dir_save + 'comparativo_muertes_nuevas.csv')
acumuladas.to_csv(dir_save + 'comparativo_muertes_acumuladas.csv')
