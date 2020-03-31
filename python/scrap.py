import sys
import os
import camelot
import pandas as pd

pd.set_option('mode.chained_assignment', None)


ssa_cols = ['id', 'estado', 'sexo', 'edad', 'fecha_sintomas',
            'confirmacion', 'procedencia', 'fecha_llegada']
ssa_date_cols = ['fecha_sintomas', 'fecha_llegada']


def format_df(df):
    df.columns = ssa_cols
    # df = df.astype(dict(id=int, edad=int))
    df[ssa_date_cols] = df[ssa_date_cols].apply(
        pd.to_datetime, errors='coerce',  infer_datetime_format=True)
    df = df.replace(r'\n', '', regex=True)
    return df


def scrap(file, npages=None, verbose=True):
    pag = '1-end' if npages is None else f'1-{npages}'
    tab = camelot.read_pdf(file, pages=pag)

    df = pd.DataFrame(columns=ssa_cols)

    # La primera tabla tiene nombres de columnas en la primera fila
    df = df.append(format_df(tab[0].df.loc[1:]))
    if verbose:
        print(tab[0].parsing_report)

    for t in tab[1:]:
        df = df.append(format_df(t.df), ignore_index=True)

        if verbose:
            print(t.parsing_report)

    return df


if __name__ == '__main__':
    file = sys.argv[1]
    assert file.endswith('.pdf')

    output = sys.argv[2]
    assert output.endswith('.csv')

    df = scrap(file)

    repo = '..'
    csv_dir = os.path.join(repo, 'datos', 'reportes_oficiales_ssa', '')

    print(f'\nEscribiendo archivo con filas: {len(df)}')
    df.to_csv(csv_dir + output, index=False)
