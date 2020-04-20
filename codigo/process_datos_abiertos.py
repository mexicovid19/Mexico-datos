import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

date = datetime.now() - timedelta(days=1)
date_str = date.strftime('%Y%m%d')

## READING ##
# Lee los datos abiertos
repo = '..'
directorio_lectura = os.path.join(repo, 'datos', 'datos_abiertos', '')
directorio_escritura = os.path.join(repo, 'datos', 'series_de_tiempo', '')
filename = directorio_lectura + f'covid19_mex_{date_str}.csv'

datos_abiertos = pd.read_csv( filename )
# Lee catalogo de entidades
# entidades = pd.read_excel(directorio_lectura+'/diccionario/Catalogos_0412.xlsx', sheet_name='Catálogo de ENTIDADES')
entidades = pd.read_csv(directorio_lectura + 'catalogo_entidades.csv')
# Crea diccionario entre entidades federales y sus claves
entidades = entidades.set_index('CLAVE_ENTIDAD')['ENTIDAD_FEDERATIVA'].to_dict()
# cambia mayúsculas de estados por formato título
entidades = {key: val.title()  for (key,val) in entidades.items()}

## PROCESSING FUNCTIONS ##
def casos_confirmados_diarios_por_estado( datos=datos_abiertos ):
    '''
    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - serie: Serie de tiempo de nuevos casos confirmados por dia para cada entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127
    '''
    series = datos[datos['RESULTADO'] == 1].groupby(['ENTIDAD_UM', 'FECHA_INGRESO']).count()['ORIGEN']
    return get_formato_series( series )

def casos_negativos_diarios_por_estado( datos=datos_abiertos ):
    '''
    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - serie: Serie de tiempo de nuevas pruebas negativas por dia para cada entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127
    '''
    series = datos[datos['RESULTADO'] == 2].groupby(['ENTIDAD_UM', 'FECHA_INGRESO']).count()['ORIGEN']
    return get_formato_series( series )

def casos_pruebas_pendientes_diarios_por_estado( datos=datos_abiertos ):
    '''
    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - serie: Serie de tiempo de nuevas pruebas pendientes por dia para cada entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127
    '''
    series = datos[datos['RESULTADO'] == 3].groupby(['ENTIDAD_UM', 'FECHA_INGRESO']).count()['ORIGEN']
    return get_formato_series( series )


def casos_pruebas_totales_diarios_por_estado( datos=datos_abiertos ):
    '''
    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - serie: Serie de tiempo de nuevas pruebas totales por dia para cada entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127
    '''
    series = datos.groupby(['ENTIDAD_UM', 'FECHA_INGRESO']).count()['ORIGEN']
    return get_formato_series( series )

def casos_decesos_diarios_por_estado( datos=datos_abiertos ):
    '''
    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - serie: Serie de tiempo de nuevas muertes por dia para cada entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127
    '''
    series = datos[(datos['RESULTADO'] == 1) &  (datos['FECHA_DEF'] != '9999-99-99')].groupby(['ENTIDAD_UM', 'FECHA_INGRESO']).count()['ORIGEN']
    return get_formato_series( series )

def casos_hospitalizados_diarios_por_estado( datos=datos_abiertos ):
    '''
    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - serie: Serie de tiempo de nuevos hospitalizados por dia para cada entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127
    '''
    # esta serie incluye UCI + noUCI
    series = datos[(datos['RESULTADO'] == 1) &  (datos['TIPO_PACIENTE'] == 2 )].groupby(['ENTIDAD_UM', 'FECHA_INGRESO']).count()['ORIGEN']
    return get_formato_series( series )

def casos_uci_diarios_por_estado( datos=datos_abiertos ):
    '''
    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - serie: Serie de tiempo de nuevos pacientes en UCI por dia para cada entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127
    '''
    series = datos[(datos['RESULTADO'] == 1) &  (datos['UCI'] == 1)].groupby(['ENTIDAD_UM', 'FECHA_INGRESO']).count()['ORIGEN']
    return get_formato_series( series )

def casos_ambulatorios_diarios_por_estado( datos=datos_abiertos ):
    '''
    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - serie: Serie de tiempo de nuevos pacientes infectados ambulatorios por dia para cada entidad federativa en México.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127
    '''
    series = datos[(datos['RESULTADO'] == 1) &  (datos['TIPO_PACIENTE'] == 1)].groupby(['ENTIDAD_UM', 'FECHA_INGRESO']).count()['ORIGEN']
    return get_formato_series( series )

## HELPER FUNCTIONS ##
diccionario_de_cambio_de_nombres = {'Ciudad De México': 'Ciudad de México',
                                    'Coahuila De Zaragoza': 'Coahuila',
                                    'Michoacán De Ocampo': 'Michoacán',
                                    'Veracruz De Ignacio De La Llave': 'Veracruz'}

def get_formato_series( series ):
    '''
    Construye las series por estado en el formato listo para mexicovid/Mexico-datos a partir de los datos abiertos de [1].
    Se asume que existe la variable `entidades`: diccionario de clave_de_entidad: nombre_de_entidad.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127
    '''

    series = series.unstack(level=0).fillna(0)
    series = series.astype('int')

    # Formato para mexicovid19/Mexico-datos
    series.index.name = 'Fecha'
    # Formato oficial de DGE
    series.rename( entidades, axis=1, inplace=True )
    # Formato específico de nuestro repositorio
    series.rename( diccionario_de_cambio_de_nombres, axis=1, inplace=True )
    # Formato de agregado nacional
    series.loc[:,'Nacional'] = series.sum(axis=1)
    # Reordenar columnas para que los casos nacionales queden primero
    cols = list(series.columns)
    cols = cols[-1:] + cols[:-1]
    series = series[cols]

    return series

if __name__ == '__main__':

    # Series de tiempo de nuevos casos
    casos_confirmados_diarios_por_estado( ).to_csv( directorio_escritura+'nuevos/covid19_mex_confirmados.csv' )
    casos_negativos_diarios_por_estado( ).to_csv( directorio_escritura+'nuevos/covid19_mex_negativos.csv' )
    casos_pruebas_pendientes_diarios_por_estado( ).to_csv( directorio_escritura+'nuevos/covid19_mex_pendientes.csv' )
    casos_pruebas_totales_diarios_por_estado( ).to_csv( directorio_escritura+'nuevos/covid19_mex_pruebas-totales.csv' )
    casos_decesos_diarios_por_estado( ).to_csv( directorio_escritura+'nuevos/covid19_mex_muertes.csv' )
    casos_hospitalizados_diarios_por_estado( ).to_csv( directorio_escritura+'nuevos/covid19_mex_hospitalizados.csv' )
    casos_uci_diarios_por_estado( ).to_csv( directorio_escritura+'nuevos/covid19_mex_uci.csv' )
    casos_ambulatorios_diarios_por_estado( ).to_csv( directorio_escritura+'nuevos/covid19_mex_ambulatorios.csv' )

    # Series de tiempo de casos acumulados
    casos_confirmados_diarios_por_estado( ).cumsum().to_csv( directorio_escritura+'acumulados/covid19_mex_confirmados.csv' )
    casos_negativos_diarios_por_estado( ).cumsum().to_csv( directorio_escritura+'acumulados/covid19_mex_negativos.csv' )
    casos_pruebas_pendientes_diarios_por_estado( ).cumsum().to_csv( directorio_escritura+'acumulados/covid19_mex_pendientes.csv' )
    casos_pruebas_totales_diarios_por_estado( ).cumsum().to_csv( directorio_escritura+'acumulados/covid19_mex_pruebas-totales.csv' )
    casos_decesos_diarios_por_estado( ).cumsum().to_csv( directorio_escritura+'acumulados/covid19_mex_muertes.csv' )
    casos_hospitalizados_diarios_por_estado( ).cumsum().to_csv( directorio_escritura+'acumulados/covid19_mex_hospitalizados.csv' )
    casos_uci_diarios_por_estado( ).cumsum().to_csv( directorio_escritura+'acumulados/covid19_mex_uci.csv' )
    casos_ambulatorios_diarios_por_estado( ).cumsum().to_csv( directorio_escritura+'acumulados/covid19_mex_ambulatorios.csv' )

    print(f'Se procesaron exitosamente los datos abiertos de {filename}')
