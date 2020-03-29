import sys
import os
import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta

from util import captura

edos_from = ['AGUASCALIENTES', 'BAJA CALIFORNIA', 'BAJA CALIFORNIA SUR',
             'CAMPECHE', 'CHIAPAS', 'CHIHUAHUA', 'CIUDAD DE MÉXICO',
             'COAHUILA', 'COLIMA', 'DURANGO', 'MÉXICO', 'GUANAJUATO',
             'GUERRERO', 'HIDALGO', 'JALISCO', 'MICHOACÁN', 'MORELOS',
             'NAYARIT', 'NUEVO LEÓN', 'OAXACA', 'PUEBLA', 'QUERETARO',
             'QUINTANA ROO', 'SAN LUIS POTOSÍ', 'SINALOA', 'SONORA', 'TABASCO',
             'TAMAULIPAS', 'TLAXCALA', 'VERACRUZ', 'YUCATÁN', 'ZACATECAS']

edos = ['Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche',
        'Chiapas', 'Chihuahua', 'Ciudad de México', 'Coahuila', 'Colima',
        'Durango', 'Estado de México', 'Guanajuato', 'Guerrero', 'Hidalgo',
        'Jalisco', 'Michoacán', 'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca',
        'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí', 'Sinaloa',
        'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán',
        'Zacatecas']


def total_edos(update_df, date):
    counts = (update_df.groupby('estado')
              .count()['id']
              .rename('total'))
    # cambiamos nombres en mayusculas a nombres estándar
    counts.index = counts.index.map(dict(zip(edos_from, edos)))
    date = pd.Series(date, index=['Fecha'], name='total')
    total = pd.Series(counts.sum(), index=['México'], name='total')

    return pd.concat((date, total, counts))


def nuevos_edos(totales_df, date):
    delta = totales_df.iloc[-1, 1:] - totales_df.iloc[-2, 1:]
    delta = delta.rename('total')
    date = pd.Series(date, index=['Fecha'], name='total')

    return pd.concat((date, delta))


def activos_edos(totales_df, muertes_df, recuperados_df, date):
    activos = (totales_df.iloc[-1, 1:] - muertes_df.iloc[-1, 1:]
               - recuperados_df.iloc[-1, 1:]).rename('total')
    date = pd.Series(date, index=['Fecha'], name='total')

    return pd.concat((date, activos))


def list2row(list, date):
    date = pd.Series(date, index=['Fecha'], name='total')
    counts = pd.Series(dict(zip(edos, list)), name='total')
    total = pd.Series(counts.sum(), index=['México'], name='total')

    return pd.concat((date, total, counts))


if __name__ == '__main__':

    date_str = sys.argv[1]
    assert len(date_str) == 8
    assert date_str.startswith('2020')

    # Fechas formateadas
    date = datetime.strptime(date_str, '%Y%m%d')
    date_formatted = date.strftime('%Y-%m-%d')
    # previous_date = date - timedelta(days=1)
    # previous_date_formatted = previous_date.strftime('%Y-%m-%d')

    # repo = 'https://raw.githubusercontent.com/mexicovid19/Mexico-datos/master/'
    repo = '..'
    data_dir = os.path.join(repo, 'datos', '')
    csv_dir = os.path.join(data_dir, 'reportes_oficiales_ssa', '')
    aggr_dir = os.path.join(data_dir, 'series_de_tiempo', '')
    geo_dir = os.path.join(data_dir, 'geograficos', '')

    # Input: Los nuevos datos recien extraidos
    update_file = csv_dir + f'covid19_mex_confirmados_{date_str}.csv'
    update_df = pd.read_csv(update_file)

    # Updates

    # Nuevos totales por estado
    totales_file = aggr_dir + 'covid19_mex_casos_totales.csv'
    totales_df = pd.read_csv(totales_file)
    row = total_edos(update_df, date_formatted)
    totales_df = totales_df.append(row, ignore_index=True)

    # Casos nuevos por estado
    nuevos_file = aggr_dir + 'covid19_mex_casos_nuevos.csv'
    nuevos_df = pd.read_csv(nuevos_file)
    row = nuevos_edos(totales_df, date_formatted)
    nuevos_df = nuevos_df.append(row, ignore_index=True)

    # Muertes por estado
    muertes_file = aggr_dir + 'covid19_mex_muertes.csv'
    muertes_df = pd.read_csv(muertes_file)
    print('\nMuertes:')
    muertes = captura()
    row = list2row(muertes, date_formatted)
    muertes_df = muertes_df.append(row, ignore_index=True)

    # Recuperados por estado
    recuperados_file = aggr_dir + 'covid19_mex_recuperados.csv'
    recuperados_df = pd.read_csv(recuperados_file)
    print('\nRecuperados:')
    recuperados = captura()
    row = list2row(recuperados, date_formatted)
    recuperados_df = recuperados_df.append(row, ignore_index=True)

    activos_file = aggr_dir + 'covid19_mex_casos_activos.csv'
    activos_df = pd.read_csv(activos_file)
    row = activos_edos(totales_df, muertes_df, recuperados_df, date_formatted)
    # activos_df = activos_df.append(row, ignore_index=True)

    pairs_file_df = [(totales_file, totales_df),
                     (nuevos_file, nuevos_df),
                     (muertes_file,  muertes_df),
                     (recuperados_file, recuperados_df),
                     (activos_file, activos_df)]

    for file, df in pairs_file_df:
        print(f'\nUltimos cambios {file}')
        print(df.tail(2))

        write = input('\nEscribir cambios (y/n) : ')
        write = True if write == 'y' else False

        if write:
            with open(file, 'a') as f:
                f.write('\n')
                df.tail(1).to_csv(path_or_buf=f,
                                  header=False, index=False)

    # Archivo de geojson
    geojson_file = geo_dir + 'mexico.geojson'
    edos_hoy_file = data_dir + 'estados_hoy.csv'
    updated_file = data_dir + 'last_updated.csv'

    gdf = gpd.read_file(geojson_file).sort_values(by='name').reset_index()
    # gdf = gdf.set_index('name')  # nombres de estado en orden alfabetico

    gdf.totales = totales_df.iloc[-1, 2:].values.astype('int')
    gdf.nuevos = nuevos_df.iloc[-1, 2:].values.astype('int')
    gdf.muertes = muertes_df.iloc[-1, 2:].values.astype('int')
    gdf.recuperaciones = recuperados_df.iloc[-1, 2:].values.astype('int')
    gdf.activos = activos_df.iloc[-1, 2:].values.astype('int')

    # gdf = gdf.reset_index()
    now = datetime.now() - timedelta(hours=6)  # hora mexico
    gdf.updated_at = now

    cols_edos_hoy = ['name', 'totales', 'nuevos',
                     'activos', 'muertes', 'recuperaciones']
    map_cols = {'name': 'Estado',
                'totales': 'Casos totales',
                'nuevos': 'Casos nuevos ultimas 24h',
                'activos': 'Casos activos',
                'muertes': 'Muertes',
                'recuperaciones': 'Recuperaciones'}
    edos_hoy_df = gdf[cols_edos_hoy].rename(columns=map_cols)

    write = input('\nEscribir cambios GeoJSON (y/n) : ')
    write = True if write == 'y' else False
    if write:
        gdf.to_file(geojson_file, driver='GeoJSON')
        gdf.loc[0:0, ['updated_at']].to_csv(updated_file, index=False)
        edos_hoy_df.to_csv(edos_hoy_file, index=False)
