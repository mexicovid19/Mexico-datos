import os
import argparse
import json
import pandas as pd
from datetime import date, timedelta

pd.set_option('mode.chained_assignment', None)


def por_edad_sexo(datos_filtrados, reindex=False,
                  cat_sexo={1: 'MUJER', 2: 'HOMBRE', 99: 'NO ESPECIFICADO'}):
    """
    Calcula el número de pacientes confirmados por edad y por sexo.

    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - json: Los casos agrupados por grupos de edad de 5 años (0-4, 5-9, etc)
        para hombres `male` y mujeres `female`.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127

    """
    df = datos_filtrados[['SEXO', 'EDAD', 'ID_REGISTRO']]
    df['EDAD'] = df['EDAD'].apply(lambda x: x // 5)

    gby = (df.groupby(['SEXO', 'EDAD'])
           .count()['ID_REGISTRO']
           .unstack(level=0))

    if reindex:
        idx = range(gby.index.min(), gby.index.max() + 1)
        gby = gby.reindex(idx)

    gby = gby.fillna(0).astype('int')
    gby.index = gby.index.map(lambda x: f'{5*x}-{5*x+4}')
    gby = gby.rename(columns=cat_sexo)

    # convertimos a JSON
    json_list = []
    for idx, row in gby.iterrows():
        d = dict(age=idx, male=int(row['HOMBRE']), female=int(row['MUJER']))
        json_list.append(d)

    return json.dumps(json_list)


if __name__ == '__main__':

    ## Casos por sexo y edad (en formato JSON) ##

    dat = date.today() - timedelta(days=1)
    date_filename = dat.strftime('%Y%m%d')
    # date_iso = date.strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser(description='procesa archivo de datos abiertos')
    parser.add_argument('input_file', help='el archivo csv comprimido como zip')
    args = parser.parse_args()
    input_file = args.input_file
    assert input_file.endswith(f'{date_filename}.zip'), \
        'error: archivo deberia ser zip con la fecha más reciente'


    repo = os.pardir
    dir_datos_abiertos = os.path.join(repo, 'datos_abiertos', '')
    dir_datos = os.path.join(repo, 'datos', '')
    dir_demograficos = os.path.join(dir_datos, 'demograficos_variables', '')
    confirmados_file = dir_demograficos + 'piramide_sexo_edad.json'
    defunciones_file = dir_demograficos + 'defunciones_sexo_edad.json'

    # dir_input = os.path.join(dir_datos_abiertos, 'raw', '')
    # input_filename = dir_input + f'datos_abiertos_{dat_filename}.zip'

    # Lee los datos abiertos
    datos_abiertos_df = pd.read_csv(input_file)

    idx_confirmados = datos_abiertos_df['RESULTADO'] == 1
    idx_defunciones = idx_confirmados & (
        datos_abiertos_df['FECHA_DEF'] != '9999-99-99')

    confirmados_json = por_edad_sexo(datos_abiertos_df.loc[idx_confirmados])
    with open(confirmados_file, 'w') as f:
        f.write(confirmados_json)

    defunciones_json = por_edad_sexo(datos_abiertos_df.loc[idx_defunciones])
    with open(defunciones_file, 'w') as f:
        f.write(defunciones_json)
