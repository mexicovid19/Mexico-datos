import numpy as np
import pandas as pd
import os

## READING ##
# Lee los datos abiertos
directorio_lectura = '../datos/datos_abiertos/'
archivos = os.listdir( directorio_lectura )
archivos = [archivo for archivo in archivos if archivo not in {'README.md', 'diccionario'}]
direccion_archivo = max([directorio_lectura+a for a in archivos], key=os.path.getctime)
del archivos

# filename = '200419COVID19MEXICO.csv' # este debería automatizarse
datos_abiertos = pd.read_csv( direccion_archivo )
# Lee catalogo de entidades
entidades = pd.read_excel(directorio_lectura+'/diccionario/Catalogos_0412.xlsx', sheet_name='Catálogo de ENTIDADES')
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
def get_formato_series( series ):
    '''
    Construye las series por estado en el formato listo para mexicovid/Mexico-datos a partir de los datos abiertos de [1].
    Se asume que existe la variable `entidades`: diccionario de clave_de_entidad: nombre_de_entidad.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127
    '''

    series = series.unstack(level=0).fillna(0)
    series = series.astype('int')

    # formato para mexicovid19/Mexico-datos
    series.index.name = 'Fecha'
    series.rename( entidades, axis = 1, inplace=True )
    # {key.title(): val  for (key,val) in entidades.items()}
    # series.rename({'México': 'Estado de México'}, axis=1, inplace=True)
    # series.loc[:,'México'] = series.sum(axis=1)
    series.loc[:,'Nacional'] = series.sum(axis=1)
    # serie nacional va primero
    cols = list(series.columns)
    cols = cols[-1:] + cols[:-1]
    series = series[cols]

    return series

if __name__ == '__main__':

    # Carpeta donde se guarda el csv
    directorio_escritura = '../datos/series_de_tiempo/'

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

    print('Se procesaron exitosamente los datos abiertos de {}'.format( direccion_archivo ))
