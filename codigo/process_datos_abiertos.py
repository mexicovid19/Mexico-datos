import os
import csv
import pandas as pd
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

    date = datetime.now() - timedelta(days=1)
    date_filename = date.strftime('%Y%m%d')
    date_iso = date.strftime('%Y-%m-%d')

    repo = '..'
    dir_datos_abiertos = os.path.join(repo, 'datos_abiertos', '')
    dir_datos = os.path.join(repo, 'datos', '')

    dir_series_dge = os.path.join(dir_datos_abiertos, 'series_de_tiempo', '')
    dir_series = os.path.join(dir_datos, 'series_de_tiempo', '')

    dir_input = os.path.join(dir_datos_abiertos, 'raw', '')
    input_filename = dir_input + f'datos_abiertos_{date_filename}.csv'

    ## READING ##

    # Lee los datos abiertos
    datos_abiertos_df = pd.read_csv(input_filename)

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
    df = dfs[0].cumsum()  # confirmados_diarios_por_estado
    with open(totales_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + df.tail(1).values[0].tolist())

    # Casos ultimas 24h
    nuevos_file = dir_series + 'covid19_mex_casos_nuevos.csv'
    totales_df = pd.read_csv(totales_file)
    diff = totales_df.iloc[-1, 1:] - totales_df.iloc[-2, 1:]
    with open(nuevos_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + diff.values.tolist())  # diff is series

    # Muertes por estado
    muertes_file = dir_series + 'covid19_mex_muertes.csv'
    df = dfs[4].cumsum()  # defunciones_diarias_por_estado
    with open(muertes_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + df.tail(1).values[0].tolist())

    # Sospechosos por estado
    sospechosos_file = dir_series + 'covid19_mex_sospechosos.csv'
    df = dfs[2].cumsum()  # pruebas_pendientes_diarias_por_estado
    with open(sospechosos_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + df.tail(1).values[0].tolist())

    # Sospechosos por estado
    negativos_file = dir_series + 'covid19_mex_negativos.csv'
    df = dfs[1].cumsum()  # negativos_diarios_por_estado
    with open(negativos_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + df.tail(1).values[0].tolist())

    print(f'Se procesaron exitosamente los datos abiertos de {input_filename}')
