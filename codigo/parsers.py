import pandas as pd

from utils import get_formato_series


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
