
import sys
import os
import json
import pandas as pd
from datetime import datetime, timedelta

pd.set_option('mode.chained_assignment', None)


def total_sexo_edad(update_df):
    df = update_df[['sexo', 'edad', 'id']]
    df.edad = df.edad.apply(lambda a: a // 5)
    df = df.rename(columns=dict(edad='age'))

    m = (df.loc[df.sexo == 'M']
         .drop('sexo', axis=1)
         .groupby('age', as_index=False)
         .count()
         .rename(columns=dict(id='male')))
    m.age = m.age.map(lambda x: f'{5*x}-{5*x+4}')
    m = m.set_index('age')

    f = (df.loc[df.sexo == 'F']
         .drop('sexo', axis=1)
         .groupby('age', as_index=False)
         .count()
         .rename(columns=dict(id='female')))
    f.age = f.age.map(lambda x: f'{5*x}-{5*x+4}')
    f = f.set_index('age')

    out_df = f.join(m, how='left').fillna(0).astype(int)  # esto funciona porque f tiene mas edades

    json_list = []
    for idx, row in out_df.iterrows():
        d = dict(age=idx, male=int(row['male']), female=int(row['female']))
        json_list.append(d)

    out = json.dumps(json_list)
    return out


update_time = datetime.now() - timedelta(hours=6)
date = datetime.now() - timedelta(days=1)
date_str = date.strftime('%Y%m%d')
# date_formatted = date.strftime('%Y-%m-%d')
# date_s = pd.Series(date.strftime('%Y-%m-%d'), ['Fecha'])

repo = '..'
data_dir = os.path.join(repo, 'datos', '')
csv_dir = os.path.join(data_dir, 'reportes_oficiales_ssa', '')
demo_dir = os.path.join(data_dir, 'demograficos_variables', '')

update_file = csv_dir + f'covid19_mex_confirmados_{date_str}.csv'
update_df = pd.read_csv(update_file)

# Sexo y edad
sexo_edad_file = demo_dir + 'piramide_sexo_edad.json'
sexo_edad_json = total_sexo_edad(update_df)

write = input('\nEscribir cambios piramide_sexo_edad.json (y/n) : ')
write = True if write == 'y' else False
if write:
    with open(sexo_edad_file, 'w') as f:
        f.write(sexo_edad_json)
