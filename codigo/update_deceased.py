import os
import pandas as pd


rolling_window = 7  # promedio sobre 7 días

repo = '..'
dir_series = os.path.join(repo, 'datos', 'series_de_tiempo', '')

dir_datos_abiertos = os.path.join(repo, 'datos_abiertos', '')
dir_series_abiertos = os.path.join(
    dir_datos_abiertos, 'series_de_tiempo', 'nuevos', '')
dir_save = os.path.join(dir_datos_abiertos, 'formato_especial', '')

# Series de tiempo 'interpretacion JH'
muertes_df = (pd.read_csv(dir_series + 'covid19_mex_muertes_nuevas.csv')
              .set_index('Fecha')['Nacional']
              .rename('Nuevas_JH'))
muertes_df.index = pd.to_datetime(muertes_df.index)

casos_df = (pd.read_csv(dir_series + 'covid19_mex_casos_nuevos.csv')
            .set_index('Fecha')['Nacional']
            .rename('Nuevos_JH'))
casos_df.index = pd.to_datetime(casos_df.index)

# Series de tiempo 'datos abiertos'
muertes_abiertos_df = (pd.read_csv(dir_series_abiertos + 'covid19_mex_muertes.csv')
                       .set_index('Fecha')['Nacional']
                       .rename('Nuevas_abiertos'))
muertes_abiertos_df.index = pd.to_datetime(muertes_abiertos_df.index)

casos_abiertos_df = (pd.read_csv(dir_series_abiertos + 'covid19_mex_confirmados.csv')
                     .set_index('Fecha')['Nacional']
                     .rename('Nuevos_abiertos'))
casos_abiertos_df.index = pd.to_datetime(casos_abiertos_df.index)

# Creamos dfs
muertes_nuevas = pd.concat(
    (muertes_df, muertes_abiertos_df), axis=1).fillna(0).astype(int)
muertes_acumuladas = muertes_nuevas.cumsum()

# agregamos el promedio
muertes_promedio = (muertes_nuevas.rolling(window=rolling_window, center=True)
                    .mean()
                    .round(2))  # 2 decimales
muertes_nuevas = muertes_nuevas.join(muertes_promedio, rsuffix='_promedio')

casos_nuevos = pd.concat((casos_df, casos_abiertos_df),
                         axis=1).fillna(0).astype(int)
casos_acumulados = casos_nuevos.cumsum()

# el promedio
casos_promedio = (casos_nuevos.rolling(window=rolling_window, center=True)
                  .mean()
                  .round(2))  # 2 decimales
casos_nuevos = casos_nuevos.join(casos_promedio, rsuffix='_promedio)

# cutoff = '2020-02-28'


# Escribimos archivos
# .loc[cutoff:, :]

muertes_nuevas.to_csv(dir_save + 'comparativo_muertes_nuevas.csv')
muertes_acumuladas.to_csv(dir_save + 'comparativo_muertes_acumuladas.csv')

casos_nuevos.to_csv(dir_save + 'comparativo_casos_nuevos.csv')
casos_acumulados.to_csv(dir_save + 'comparativo_casos_acumulados.csv')
