import os
import pandas as pd


repo = '..'
dir_datos_abiertos = os.path.join(repo, 'datos_abiertos', '')
dir_series = os.path.join(dir_datos_abiertos, 'series_de_tiempo', 'nuevos', '')
dir_formato = os.path.join(dir_datos_abiertos, 'formato_especial', '')

dir_datos_JH = os.path.join(repo, 'datos', '')
dir_series_JH = os.path.join(dir_datos_JH, 'series_de_tiempo', '')

pos = (pd.read_csv(dir_series + 'covid19_mex_confirmados.csv')
       .set_index('Fecha')['Nacional']
       .rename('positivos'))
pos.index = pd.to_datetime(pos.index)
neg = (pd.read_csv(dir_series + 'covid19_mex_negativos.csv')
       .set_index('Fecha')['Nacional']
       .rename('negativos'))
neg.index = pd.to_datetime(neg.index)
pend = (pd.read_csv(dir_series + 'covid19_mex_pendientes.csv')
        .set_index('Fecha')['Nacional']
        .rename('pendientes'))
pend.index = pd.to_datetime(pend.index)

muertes_abiertos = (pd.read_csv(dir_series + 'covid19_mex_muertes.csv')
           .set_index('Fecha')['Nacional']
           .rename('datos_abiertos')
muertes_abiertos.index = pd.to_datetime(muertes_abiertos.index)
muertes_JH = (pd.read_csv(dir_series_JH + 'covid19_mex_muertes.csv')
           .set_index('Fecha')['Nacional']
           .rename('JH')
muertes_JH.index = pd.to_datetime(muertes_JH.index)


left = pd.concat((pos, neg), axis=1)

pruebas_diarias = left.join(pend,  how='outer').fillna(0).astype(int)
pruebas_acumuladas = pruebas_diarias.cumsum()

muertes_diarias = pd.concat((muertes_JH, muertes_abiertos), axis = 1)
muertes_acumuladas = muertes_diarias.cumsum()

cutoff = '2020-02-28'
order = ['positivos', 'pendientes', 'negativos']


# Escribimos archivos
(pruebas_diarias.loc[cutoff:, :][order]
 .to_csv(dir_formato + 'pruebas_casos_nuevos.csv'))

(pruebas_acumuladas.loc[cutoff:, ][order]
 .to_csv(dir_formato + 'pruebas_casos_acumulados.csv'))

(muertes_diarias.loc[cutoff:, :]
 .to_csv(dir_formato + 'comparativo_muertes_nuevas.csv'))

 (muertes_acumuladas.loc[cutoff:, :]
  .to_csv(dir_formato + 'comparativo_muertes_acumuladas.csv'))
