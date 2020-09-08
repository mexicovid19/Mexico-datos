import os
import pandas as pd


dir_datos_abiertos = os.path.join(os.pardir, 'datos_abiertos', '')
dir_series = os.path.join(dir_datos_abiertos, 'series_de_tiempo', 'nuevos', '')
dir_formato = os.path.join(dir_datos_abiertos, 'formato_especial', '')

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

left = pd.concat((pos, neg), axis=1)

pruebas_diarias = left.join(pend,  how='outer').fillna(0).astype(int)
pruebas_acumuladas = pruebas_diarias.cumsum()

cutoff = '2020-02-28'
order = ['positivos', 'pendientes', 'negativos']


# Escribimos archivos
(pruebas_diarias.loc[cutoff:, :][order]
 .to_csv(dir_formato + 'pruebas_casos_nuevos.csv'))

(pruebas_acumuladas.loc[cutoff:, ][order]
 .to_csv(dir_formato + 'pruebas_casos_acumulados.csv'))
