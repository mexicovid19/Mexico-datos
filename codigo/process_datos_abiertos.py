import os
import argparse
import csv
import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta

from parsers import (
    confirmados_diarios_por_estado,
    negativos_diarios_por_estado,
    pruebas_pendientes_diarias_por_estado,
    pruebas_totales_diarias_por_estado,
    defunciones_diarias_por_estado,
    hospitalizados_diarios_por_estado,
    ambulatorios_diarios_por_estado,
    uci_diarios_por_estado
)


# El archivo y la respectiva función que lo actualiza
func_dict = dict()
func_dict['covid19_mex_confirmados.csv'] = confirmados_diarios_por_estado
func_dict['covid19_mex_negativos.csv'] = negativos_diarios_por_estado
func_dict['covid19_mex_pendientes.csv'] = pruebas_pendientes_diarias_por_estado
func_dict['covid19_mex_pruebas-totales.csv'] = pruebas_totales_diarias_por_estado
func_dict['covid19_mex_muertes.csv'] = defunciones_diarias_por_estado
func_dict['covid19_mex_hospitalizados.csv'] = hospitalizados_diarios_por_estado
func_dict['covid19_mex_uci.csv'] = uci_diarios_por_estado
func_dict['covid19_mex_ambulatorios.csv'] = ambulatorios_diarios_por_estado



if __name__ == '__main__':

    update_time = datetime.now() - timedelta(hours=6)
    date = datetime.now() - timedelta(days=1)
    date_filename = date.strftime('%Y%m%d')
    date_iso = date.strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser(description='procesa archivo de datos abiertos')
    parser.add_argument('input_file', help='el archivo csv comprimido como zip')
    args = parser.parse_args()
    input_file = args.input_file
    assert input_file.endswith(f'{date_filename}.zip'), \
            'error: archivo deberia ser zip con la fecha más reciente'

    repo = os.pardir
    dir_datos_abiertos = os.path.join(repo, 'datos_abiertos', '')
    dir_datos = os.path.join(repo, 'datos', '')
    dir_geo = os.path.join(dir_datos, 'geograficos', '')
    dir_demograficos = os.path.join(dir_datos, 'demograficos_variables', '')

    dir_series_dge = os.path.join(dir_datos_abiertos, 'series_de_tiempo', '')
    dir_series = os.path.join(dir_datos, 'series_de_tiempo', '')

    dir_input = os.path.join(dir_datos_abiertos, 'raw', '')
    # input_filename = dir_input + f'datos_abiertos_{date_filename}.zip'

    ## READING ##

    # Lee los datos abiertos
    datos_abiertos_df = pd.read_csv(input_file, compression='zip')

    # Lee catalogo de entidades (hoja de calculo 'Catálogo de ENTIDADES' en
    # el archivo 'diccionario_datos/Catalogos_0412.xlsx''; ha sido convertido a csv)
    entidades = (pd.read_csv(dir_input + 'diccionario_datos/catalogo_entidades.csv')
                 .set_index('CLAVE_ENTIDAD')['ENTIDAD_FEDERATIVA']
                 .str.title()
                 .replace({'Ciudad De México':'Ciudad de México'})
                 .to_dict())


    # Escribe las series de tiempo a partir de los datos abiertos
    dfs = [func(datos_abiertos_df, entidades) for key, func in func_dict.items()]

    for key, func in func_dict.items():
        df = func(datos_abiertos_df, entidades)
        df.to_csv(f'{dir_series_dge}/nuevos/{key}')
        df.cumsum().to_csv(f'{dir_series_dge}/acumulados/{key}')

    ## Series de tiempo estaticas (solo actualiza ultima fila) ##

    # Formato unix sin quotes
    csv.register_dialect('unixnq', delimiter=',', lineterminator='\n',
                         quoting=csv.QUOTE_NONE)

    # Totales por estado
    totales_file = dir_series + 'covid19_mex_casos_totales.csv'
    fila_totales = dfs[0].cumsum().tail(1)  # confirmados_diarios_por_estado
    with open(totales_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + fila_totales.values[0].tolist())

    # Casos ultimas 24h
    nuevos_file = dir_series + 'covid19_mex_casos_nuevos.csv'
    totales_df = pd.read_csv(totales_file)
    fila_nuevos = (totales_df.iloc[-1, 1:] - totales_df.iloc[-2, 1:]).astype(int)
    with open(nuevos_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + fila_nuevos.values.tolist())  # a series

    # Muertes por estado
    muertes_file = dir_series + 'covid19_mex_muertes.csv'
    fila_muertes = dfs[4].cumsum().tail(1)  # defunciones_diarias_por_estado
    with open(muertes_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + fila_muertes.values[0].tolist())

    # Muertes nuevas por estado
    muertes_nuevas_file = dir_series + 'covid19_mex_muertes_nuevas.csv'
    muertes_df = pd.read_csv(muertes_file)
    fila_nuevas = (muertes_df.iloc[-1, 1:] - muertes_df.iloc[-2, 1:]).astype(int)
    with open(muertes_nuevas_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + fila_nuevas.values.tolist())  # a series

    # Sospechosos por estado
    sospechosos_file = dir_series + 'covid19_mex_sospechosos.csv'
    # pruebas_pendientes_diarias_por_estado
    fila_sospechosos = dfs[2].cumsum().tail(1)
    with open(sospechosos_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + fila_sospechosos.values[0].tolist())

    # Sospechosos por estado
    negativos_file = dir_series + 'covid19_mex_negativos.csv'
    fila_negativos = dfs[1].cumsum().tail(1)  # negativos_diarios_por_estado
    with open(negativos_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + fila_negativos.values[0].tolist())

    ## Totales por estado en el archivo geojson ##
    geojson_file = dir_geo + 'mexico.geojson'
    edos_hoy_file = dir_datos + 'estados_hoy.csv'
    updated_file = dir_datos + 'last_updated.csv'

    gdf = gpd.read_file(geojson_file).set_index('name')
    gdf.totales = fila_totales.drop('Nacional', axis=1).squeeze()
    gdf.nuevos = fila_nuevos.drop('Nacional').squeeze()  # series
    gdf.muertes = fila_muertes.drop('Nacional', axis=1).squeeze()
    gdf.muertes_nuevas = fila_nuevas.drop('Nacional').squeeze()  # series
    gdf.sospechosos = fila_sospechosos.drop('Nacional', axis=1).squeeze()
    gdf.negativos = fila_negativos.drop('Nacional', axis=1).squeeze()
    gdf.totales_100k = gdf.totales * 100000 / gdf.population
    gdf.muertes_100k = gdf.muertes * 100000 / gdf.population

    gdf.updated_at = str(update_time).replace(' ', 'T')

    gdf = gdf.reset_index()
    assert gdf.shape[1] == 14

    gdf.to_file(geojson_file, driver='GeoJSON')
    gdf.loc[0:0, ['updated_at']].to_csv(updated_file, index=False)

    ### Estados hoy ###
    cols_edos_hoy = ['name', 'totales', 'nuevos',
                     'muertes', 'muertes_nuevas', 'sospechosos', 'negativos']

    map_cols = {'name': 'Estado',
                'totales': 'Confirmados totales',
                'nuevos': 'Confirmados nuevos',
                'muertes': 'Defunciones',
                'muertes_nuevas': 'Defunciones nuevas',
                'sospechosos': 'Sospechosos totales',
                'negativos': 'Negativos totales'}

    edos_hoy_df = gdf[cols_edos_hoy].rename(columns=map_cols)
    edos_hoy_df.to_csv(edos_hoy_file, index=False)

    print(f'Se procesaron exitosamente los datos abiertos de {input_file}')
