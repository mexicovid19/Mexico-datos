import os
from datetime import datetime, timedelta
import csv
import numpy as np
import pandas as pd

date = datetime.now() - timedelta(days=1)
date_filename = date.strftime('%Y%m%d')
date_iso = date.strftime('%Y-%m-%d')


## READING ##
# Lee los datos abiertos
repo = '..'
directorio_lectura = os.path.join(repo, 'datos_abiertos', 'raw', '')
directorio_escritura = os.path.join(
    repo, 'datos_abiertos', 'series_de_tiempo', '')
series_dir = os.path.join(repo, 'datos', 'series_de_tiempo', '')
input_filename = directorio_lectura + f'covid19_mex_{date_filename}.csv'

datos_abiertos = pd.read_csv(input_filename)
# Lee catalogo de entidades
# entidades = pd.read_excel(directorio_lectura+'/diccionario/Catalogos_0412.xlsx', sheet_name='Catálogo de ENTIDADES')
entidades = pd.read_csv(directorio_lectura + 'catalogo_entidades.csv')
# Crea diccionario entre entidades federales y sus claves
entidades = entidades.set_index('CLAVE_ENTIDAD')[
    'ENTIDAD_FEDERATIVA'].to_dict()
# cambia mayúsculas de estados por formato título
entidades = {key: val.title() for (key, val) in entidades.items()}


## PROCESSING FUNCTIONS ##

def confirmados_diarios_por_estado(datos=datos_abiertos):
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
    return get_formato_series(series)


def negativos_diarios_por_estado(datos=datos_abiertos):
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
    return get_formato_series(series)


def pruebas_pendientes_diarias_por_estado(datos=datos_abiertos):
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
    return get_formato_series(series)


def pruebas_totales_diarias_por_estado(datos=datos_abiertos):
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
    return get_formato_series(series)


def defunciones_diarias_por_estado(datos=datos_abiertos):
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
    return get_formato_series(series)


def hospitalizados_diarios_por_estado(datos=datos_abiertos):
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
    return get_formato_series(series)


def ambulatorios_diarios_por_estado(datos=datos_abiertos):
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
    return get_formato_series(series)


def uci_diarios_por_estado(datos=datos_abiertos):
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
    return get_formato_series(series)


## HELPER FUNCTIONS ##
diccionario_cambio_edos = {'Ciudad De México': 'Ciudad de México',
                           'Coahuila De Zaragoza': 'Coahuila',
                           'Michoacán De Ocampo': 'Michoacán',
                           'Veracruz De Ignacio De La Llave': 'Veracruz'}


def get_formato_series(series):
    """
    Convierte groupby a formato tidy (columnas son estados e indice es la fecha).

    Se asume que existe la variable `entidades`:
        diccionario de clave_de_entidad: nombre_de_entidad.

    Input:
    - series:
        DataFrame en formato groupby agrupada for una columna que corresponde a
        entidades federativas y otra columna que corresponde a una fecha.
    Output:
    - series:
        DataFrame en formato tidy, con los nombres de los estados como columnas
        (la primer columna es el total nacional) y con la fecha como indice.

    """
    series = series.unstack(level=0).fillna(0).astype('int')

    # Formato para mexicovid19/Mexico-datos
    series.index.name = 'Fecha'
    series.index = pd.to_datetime(series.index)
    # Formato oficial de DGE
    series = series.rename(columns=entidades)
    # Formato específico de nuestro repositorio
    series = series.rename(columns=diccionario_cambio_edos)
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

    # Datos abiertos
    files = ['covid19_mex_confirmados.csv',
             'covid19_mex_negativos.csv',
             'covid19_mex_pendientes.csv',
             'covid19_mex_pruebas-totales.csv',
             'covid19_mex_muertes.csv',
             'covid19_mex_hospitalizados.csv',
             'covid19_mex_uci.csv',
             'covid19_mex_ambulatorios.csv']

    dfs = [confirmados_diarios_por_estado(),
           negativos_diarios_por_estado(),
           pruebas_pendientes_diarias_por_estado(),
           pruebas_totales_diarias_por_estado(),
           defunciones_diarias_por_estado(),
           hospitalizados_diarios_por_estado(),
           uci_diarios_por_estado(),
           ambulatorios_diarios_por_estado()]

    for fname, df in zip(files, dfs):
        df.to_csv(directorio_escritura + 'nuevos/' + fname)
        df.cumsum().to_csv(directorio_escritura + 'acumulados/' + fname)

    # Series de tiempo (solo cambia ultima fila)
    csv.register_dialect('unixnq', delimiter=',', lineterminator='\n',
                         quoting=csv.QUOTE_NONE)

    # Totales por estado
    totales_file = series_dir + 'covid19_mex_casos_totales.csv'
    df = confirmados_diarios_por_estado().cumsum()
    with open(totales_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + df.tail(1).values[0].tolist())

    # Casos ultimas 24h
    nuevos_file = series_dir + 'covid19_mex_casos_nuevos.csv'
    totales_df = pd.read_csv(totales_file)
    diff = totales_df.iloc[-1, 1:] - totales_df.iloc[-2, 1:]
    with open(nuevos_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + diff.values.tolist())  # diff is series

    # Muertes por estado
    muertes_file = series_dir + 'covid19_mex_muertes.csv'
    df = defunciones_diarias_por_estado().cumsum()
    with open(muertes_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + df.tail(1).values[0].tolist())

    # Sospechosos por estado
    sospechosos_file = series_dir + 'covid19_mex_sospechosos.csv'
    df = pruebas_pendientes_diarias_por_estado().cumsum()
    with open(sospechosos_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + df.tail(1).values[0].tolist())

    # Sospechosos por estado
    negativos_file = series_dir + 'covid19_mex_negativos.csv'
    df = negativos_diarios_por_estado().cumsum()
    with open(negativos_file, 'a') as f:
        writer = csv.writer(f, 'unixnq')
        writer.writerow([date_iso] + df.tail(1).values[0].tolist())

    print(f'Se procesaron exitosamente los datos abiertos de {input_filename}')
