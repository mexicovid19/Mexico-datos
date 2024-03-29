import os
import argparse
import json
import pandas as pd

from utils import parse_date

pd.set_option("mode.chained_assignment", None)


def casos_por_edad_sexo(
    datos_filtrados,
    reindex=False,
    cat_sexo={1: "MUJER", 2: "HOMBRE", 99: "NO ESPECIFICADO"},
):
    """
    Calcula el número de pacientes confirmados por edad y por sexo.

    Input:
    - datos: datos abiertos de COVID-19 en México disponibles en [1].

    Output:
    - json: Los casos agrupados por grupos de edad de 5 años (0-4, 5-9, etc)
        para hombres `male` y mujeres `female`.

    [1]: https://www.gob.mx/salud/documentos/datos-abiertos-152127

    """
    df = datos_filtrados[["SEXO", "EDAD", "ID_REGISTRO"]]
    df["EDAD"] = df["EDAD"].apply(lambda x: x // 5)

    gby = df.groupby(["SEXO", "EDAD"]).count()["ID_REGISTRO"].unstack(level=0)

    if reindex:
        idx = range(gby.index.min(), gby.index.max() + 1)
        gby = gby.reindex(idx)

    gby = gby.fillna(0).astype("int")
    # Esto tiene que hacerse afuera de la funcion debido a los chunks desordenan los rangos
    # gby.index = gby.index.map(lambda x: f'{5*x}-{5*x+4}')
    gby = gby.rename(columns=cat_sexo)

    return gby


def convierte_json(df):
    # convertimos a JSON
    json_list = []
    for idx, row in df.iterrows():
        d = dict(age=idx, male=int(row["HOMBRE"]), female=int(row["MUJER"]))
        json_list.append(d)

    return json.dumps(json_list)


if __name__ == "__main__":

    ## Casos por sexo y edad (en formato JSON) ##

    parser = argparse.ArgumentParser(description="procesa archivo de datos abiertos")
    parser.add_argument("input_file", help="el archivo csv comprimido como zip")
    parser.add_argument(
        "-d",
        "--date",
        type=str,
        default=None,
        help="specify the date to use as yyymmdd",
    )
    args = parser.parse_args()
    date_filename, _ = parse_date(args)

    input_file = args.input_file
    assert input_file.endswith(
        f"{date_filename}.zip"
    ), "error: archivo deberia ser zip con la fecha más reciente"

    repo = os.pardir
    dir_datos_abiertos = os.path.join(repo, "datos_abiertos", "")
    dir_datos = os.path.join(repo, "datos", "")
    dir_demograficos = os.path.join(dir_datos, "demograficos_variables", "")
    confirmados_file = dir_demograficos + "piramide_sexo_edad.json"
    defunciones_file = dir_demograficos + "defunciones_sexo_edad.json"

    # dir_input = os.path.join(dir_datos_abiertos, 'raw', '')
    # input_filename = dir_input + f'datos_abiertos_{dat_filename}.zip'

    # Lee los datos abiertos en chunks
    columns = [
        "ENTIDAD_UM",
        "FECHA_INGRESO",
        "CLASIFICACION_FINAL",
        "TOMA_MUESTRA_LAB",
        "TOMA_MUESTRA_ANTIGENO",
        "FECHA_DEF",
        "TIPO_PACIENTE",
        "UCI",
        "SEXO",
        "EDAD",
        "ID_REGISTRO",
    ]

    datos_abiertos_chunks = pd.read_csv(
        input_file, compression="zip", usecols=columns, chunksize=1_000_000
    )

    # Para almacenar los totales
    confirmados_df = pd.DataFrame()
    defunciones_df = pd.DataFrame()

    for chunk in datos_abiertos_chunks:
        idx_confirmados = chunk["CLASIFICACION_FINAL"].isin([1, 2, 3])
        idx_defunciones = idx_confirmados & (chunk["FECHA_DEF"] != "9999-99-99")

        confirmados_df = confirmados_df.add(
            casos_por_edad_sexo(chunk.loc[idx_confirmados]), fill_value=0
        )

        defunciones_df = defunciones_df.add(
            casos_por_edad_sexo(chunk.loc[idx_defunciones]), fill_value=0
        )

    # Despues de haber procesado todos los chunks, cambiamos indices a rangos
    confirmados_df.index = confirmados_df.index.map(lambda x: f"{5*x}-{5*x+4}")
    defunciones_df.index = defunciones_df.index.map(lambda x: f"{5*x}-{5*x+4}")

    with open(confirmados_file, "w") as f:
        f.write(convierte_json(confirmados_df))
        # conversion a int no es necesaria porque json lo hace automaticamente

    with open(defunciones_file, "w") as f:
        f.write(convierte_json(defunciones_df))

    print(f"Se procesaron exitosamente las piramides para {input_file}")
