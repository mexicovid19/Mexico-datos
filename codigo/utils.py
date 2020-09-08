import pandas as pd
from datetime import date, datetime, timedelta
from typing import Dict


def get_formato_series(counts: pd.Series, colnames: Dict[str, str], zero_dates=True):
    """
    Convierte groupby a formato tidy (columnas son estados e indice es la fecha).

    Input:
    - groupby_series:
        DataFrame en formato groupby agrupada for una columna que corresponde a
        entidades federativas y otra columna que corresponde a una fecha.
    - entidades:
        diccionario de clave_de_entidad => nombre_de_entidad.

    Output:
    - pd.DataFrame
        DataFrame en formato tidy, con los nombres de los estados como columnas
        (la primer columna es el total nacional) y con la fecha como indice.

    """
    df = counts.unstack(level=0)
    df.index = pd.to_datetime(df.index)
    cols = df.columns
    cols.name = None

    # We make sure that all 32 states are present (even with zero counts)
    missing = list(set(range(1, 33)).difference(cols))
    if missing:
        cols = cols.tolist() + missing
        # no need to sort because we use alpahbetically below
        df = df.reindex(columns=cols)

    df = df.rename(columns=colnames).fillna(0).astype('int')

    # Formato de agregado nacional
    cols = ['Nacional'] + sorted(df.columns)
    df.loc[:, 'Nacional'] = df.sum(axis=1)
    # Reordenar columnas para que los casos nacionales queden primero
    df = df[cols]

    if zero_dates:
        # Llenamos ceros para fechas sin informacion
        idx = pd.date_range(df.index.min(), df.index.max())
        df = df.reindex(idx, fill_value=0)

    df.index.name = 'Fecha'

    return df


def load_colnames(file: str) -> Dict[str, str]:
    out = (pd.read_csv(file)
           .set_index('CLAVE_ENTIDAD')['ENTIDAD_FEDERATIVA']
           .to_dict())

    return out


def parse_date(args, return_flag=False):
    # Use yesterday's date or a date provided
    yesterday = date.today() - timedelta(days=1)
    if args.date:
        assert len(args.date) == 8, 'specify the date using the format `yyyymmdd`'
        day = datetime.strptime(args.date, '%Y%m%d').date()
    else:
        day = yesterday

    if return_flag is False:
        # date_filename, date_iso
        out = day.strftime('%Y%m%d'), day.strftime('%Y-%m-%d')
    else:
        flag = day < yesterday
        out = day.strftime('%Y%m%d'), day.strftime('%Y-%m-%d'), flag

    return out
