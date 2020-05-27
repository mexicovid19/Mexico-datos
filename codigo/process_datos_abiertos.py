import os
import csv
import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta


## PROCESSING FUNCTIONS ##

def confirmados_diarios_por_estado(datos, entidades):
    """
    Calcula el número total de casos confirmados por fecha y por estado.

    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - serie: Serie de tiempo de nuevos casos confirmados por dia para cada
        entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127
    """
    series = (datos[datos['RESULTADO'] == 1]
              .groupby(['ENTIDAD_UM', 'FECHA_INGRESO'])
              .count()['ORIGEN'])
    return get_formato_series(series, entidades)


def negativos_diarios_por_estado(datos, entidades):
    """
    Calcula el número total de casos negativos por fecha y por estado.

    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - series: Serie de tiempo de nuevas pruebas negativas por dia para cada
        entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127

    """
    series = (datos[datos['RESULTADO'] == 2]
              .groupby(['ENTIDAD_UM', 'FECHA_INGRESO'])
              .count()['ORIGEN'])
    return get_formato_series(series, entidades)


def pruebas_pendientes_diarias_por_estado(datos, entidades):
    """
    Calcula el número de pruebas pendientes por fecha y por estado.

    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - series: Serie de tiempo de nuevas pruebas pendientes por dia para cada
        entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127

    """
    series = (datos[datos['RESULTADO'] == 3]
              .groupby(['ENTIDAD_UM', 'FECHA_INGRESO'])
              .count()['ORIGEN'])
    return get_formato_series(series, entidades)


def pruebas_totales_diarias_por_estado(datos, entidades):
    """
    Calcula el número total de pruebas realizadas por fecha y por estado.

    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - series: Serie de tiempo de nuevas pruebas totales por dia para cada
        entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127

    """
    series = (datos
              .groupby(['ENTIDAD_UM', 'FECHA_INGRESO'])
              .count()['ORIGEN'])
    return get_formato_series(series, entidades)


def defunciones_diarias_por_estado(datos, entidades):
    """
    Calcula el número de defunciones por fecha y por estado.

    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - series: Serie de tiempo de nuevas muertes por dia para cada entidad
    federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127

    """
    idx = (datos['RESULTADO'] == 1) & (datos['FECHA_DEF'] != '9999-99-99')
    series = (datos[idx]
              .groupby(['ENTIDAD_UM', 'FECHA_DEF'])
              .count()['ORIGEN'])
    return get_formato_series(series, entidades)


def hospitalizados_diarios_por_estado(datos, entidades):
    """
    Calcula el número de pacientes hopitalizados por fecha y por estado.

    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - series: Serie de tiempo de nuevos hospitalizados por dia para cada entidad
        federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127

    """
    # esta serie incluye UCI + noUCI
    idx = (datos['RESULTADO'] == 1) & (datos['TIPO_PACIENTE'] == 2)
    series = (datos[idx]
              .groupby(['ENTIDAD_UM', 'FECHA_INGRESO'])
              .count()['ORIGEN'])
    return get_formato_series(series, entidades)


def ambulatorios_diarios_por_estado(datos, entidades):
    """
    Calcula el número de pacientes ambulatorios por fecha y por estado.

    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - series: Serie de tiempo de nuevos pacientes infectados ambulatorios por
        dia para cada entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127

    """
    idx = (datos['RESULTADO'] == 1) & (datos['TIPO_PACIENTE'] == 1)
    series = (datos[idx]
              .groupby(['ENTIDAD_UM', 'FECHA_INGRESO'])
              .count()['ORIGEN'])
    return get_formato_series(series, entidades)


def uci_diarios_por_estado(datos, entidades):
    """
    Calcula el número de pacientes ingresados a una UCI por fecha y por estado.

    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - series: Serie de tiempo de nuevos pacientes en UCI por dia para cada
        entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127

    """
    idx = (datos['RESULTADO'] == 1) & (datos['UCI'] == 1)
    series = (datos[idx]
              .groupby(['ENTIDAD_UM', 'FECHA_INGRESO'])
              .count()['ORIGEN'])
    return get_formato_series(series, entidades)


## HELPER FUNCTIONS ##

def get_formato_series(series, entidades):
    """
    Convierte groupby a formato tidy (columnas son estados e indice es la fecha).

    Input:
    - series:
        DataFrame en formato groupby agrupada for una columna que corresponde a
        entidades federativas y otra columna que corresponde a una fecha.
    - entidades:
        diccionario de clave_de_entidad => nombre_de_entidad.

    Output:
    - series:
        DataFrame en formato tidy, con los nombres de los estados como columnas
        (la primer columna es el total nacional) y con la fecha como indice.

    """
    diccionario_cambio_edos = {'Ciudad De México': 'Ciudad de México',
                               'Coahuila De Zaragoza': 'Coahuila',
                               'Michoacán De Ocampo': 'Michoacán',
                               'Veracruz De Ignacio De La Llave': 'Veracruz'}

    series = series.unstack(level=0).fillna(0).astype('int')

    # Formato para mexicovid19/Mexico-datos
    series.index.name = 'Fecha'
    series.index = pd.to_datetime(series.index)
    # Formato oficial de DGE
    series = series.rename(columns=entidades)
    # Formato específico de nuestro repositorio
    series = series.rename(columns=diccionario_cambio_edos)
    series = series.reindex(sorted(series.columns), axis=1)
    # Formato de agregado nacional
    series.loc[:, 'Nacional'] = series.sum(axis=1)
    # Reordenar columnas para que los casos nacionales queden primero
    cols = list(series.columns)
    cols = cols[-1:] + cols[:-1]
    series = series[cols]

    # Llenamos ceros para fechas sin informacion
    idx = pd.date_range(series.index.min(), series.index.max())
    series = series.reindex(idx, fill_value=0)
    series.index.name = 'Fecha'

    return series


if __name__ == '__main__':

    update_time = datetime.now() - timedelta(hours=6)
    date = datetime.now() - timedelta(days=1)
    date_filename = date.strftime('%Y%m%d')
    date_iso = date.strftime('%Y-%m-%d')

    repo = '..'
    dir_datos_abiertos = os.path.join(repo, 'datos_abiertos', '')
    dir_datos = os.path.join(repo, 'datos', '')
    dir_geo = os.path.join(dir_datos, 'geograficos', '')
    dir_demograficos = os.path.join(dir_datos, 'demograficos_variables', '')

    dir_series_dge = os.path.join(dir_datos_abiertos, 'series_de_tiempo', '')
    dir_series = os.path.join(dir_datos, 'series_de_tiempo', '')

    dir_input = os.path.join(dir_datos_abiertos, 'raw', '')
    input_filename = dir_input + f'datos_abiertos_{date_filename}.zip'

    ## READING ##

    # Lee los datos abiertos
    datos_abiertos_df = pd.read_csv(input_filename, compression='zip')

    # Lee catalogo de entidades (hoja de calculo 'Catálogo de ENTIDADES' en
    # el archivo 'diccionario_datos/Catalogos_0412.xlsx''; ha sido convertido a csv)
    cat = (pd.read_csv(dir_input + 'diccionario_datos/catalogo_entidades.csv')
           .set_index('CLAVE_ENTIDAD')['ENTIDAD_FEDERATIVA']
           .to_dict())
    # cambia mayúsculas de estados por formato título
    entidades = {key: val.title() for (key, val) in cat.items()}

    # Datos abiertos
    files = ['covid19_mex_confirmados.csv',
             'covid19_mex_negativos.csv',
             'covid19_mex_pendientes.csv',
             'covid19_mex_pruebas-totales.csv',
             'covid19_mex_muertes.csv',
             'covid19_mex_hospitalizados.csv',
             'covid19_mex_uci.csv',
             'covid19_mex_ambulatorios.csv']

    funciones = [confirmados_diarios_por_estado,
                 negativos_diarios_por_estado,
                 pruebas_pendientes_diarias_por_estado,
                 pruebas_totales_diarias_por_estado,
                 defunciones_diarias_por_estado,
                 hospitalizados_diarios_por_estado,
                 uci_diarios_por_estado,
                 ambulatorios_diarios_por_estado]

    dfs = [func(datos_abiertos_df, entidades) for func in funciones]

    for f, df in zip(files, dfs):
        df.to_csv(f'{dir_series_dge}/nuevos/{f}')
        df.cumsum().to_csv(f'{dir_series_dge}/acumulados/{f}')

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
<<<<<<< HEAD
    gdf.muertes_nuevas = fila_muertes_nuevas.drop('Nacional').squeeze()
=======
    gdf.muertes_nuevas = fila_nuevas.drop('Nacional').squeeze()  # series
>>>>>>> 1f173a1ca995776c79adc0f90b056728f92823b0
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

    print(f'Se procesaron exitosamente los datos abiertos de {input_filename}')
