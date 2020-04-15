
import sys
import os
import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta


edos = ['Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche',
        'Chiapas', 'Chihuahua', 'Ciudad de México', 'Coahuila', 'Colima',
        'Durango', 'Estado de México', 'Guanajuato', 'Guerrero', 'Hidalgo',
        'Jalisco', 'Michoacán', 'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca',
        'Puebla', 'Querétaro', 'Quintana Roo', 'San Luis Potosí', 'Sinaloa',
        'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán',
        'Zacatecas']


file = sys.argv[1]
global_write = sys.argv[2].lower() == 'true'


update_time = datetime.now() - timedelta(hours=6)
date = datetime.now() - timedelta(days=1)
# date_formatted = date.strftime('%Y-%m-%d')
date_s = pd.Series(date.strftime('%Y-%m-%d'), ['Fecha'])


# Datos en formato correcto
cols = {1: 'estado', 2: 'poblacion', 4: 'positivos',
        5: 'negativos', 6: 'sospechosos', 7: 'defunciones'}

df = (pd.read_json(file, orient='records')
      .drop([0, 3, 8], axis=1)  # columnas de indices
      .rename(columns=cols)
      .drop(32))

df['poblacion'] = df['poblacion'].astype(float).round()
df.loc[14, 'estado'] = 'Estado de México'
df.loc[21, 'estado'] = 'Querétaro'
df = df.sort_values('estado')
# .reset_index(drop=True) no necesarion por concat con ignore_index=True

totales = pd.concat((pd.Series('México', ['estado']), df.iloc[:, 1:].sum()))
sinave_df = (pd.concat((totales.to_frame().T, df), ignore_index=True)
             .set_index('estado')
             .astype(int))

assert (sinave_df.index[1:] == edos).all()


repo = '..'
data_dir = os.path.join(repo, 'datos', '')
# csv_dir = os.path.join(data_dir, 'reportes_oficiales_ssa', '')
series_dir = os.path.join(data_dir, 'series_de_tiempo', '')
geo_dir = os.path.join(data_dir, 'geograficos', '')
demo_dir = os.path.join(data_dir, 'demograficos_variables', '')


# Updates

# Nuevos totales por estado
totales_file = series_dir + 'covid19_mex_casos_totales.csv'
totales_df = pd.read_csv(totales_file)
diff = totales_df.iloc[-1, 1:] - totales_df.iloc[-2, 1:]
row = pd.concat((date_s, sinave_df.positivos))
totales_df = totales_df.append(row, ignore_index=True)

# Casos nuevos por estado
nuevos_file = series_dir + 'covid19_mex_casos_nuevos.csv'
nuevos_df = pd.read_csv(nuevos_file)
row = pd.concat((date_s, totales_df.iloc[-1, 1:] - totales_df.iloc[-2, 1:]))
nuevos_df = nuevos_df.append(row, ignore_index=True)

# Muertes por estado
muertes_file = series_dir + 'covid19_mex_muertes.csv'
muertes_df = pd.read_csv(muertes_file)
row = pd.concat((date_s, sinave_df.defunciones))
muertes_df = muertes_df.append(row, ignore_index=True)

# Sospechosos por estado
sospechosos_file = series_dir + 'covid19_mex_sospechosos.csv'
sospechosos_df = pd.read_csv(sospechosos_file)
row = pd.concat((date_s, sinave_df.sospechosos))
sospechosos_df = sospechosos_df.append(row, ignore_index=True)

# Negativos por estado
negativos_file = series_dir + 'covid19_mex_negativos.csv'
negativos_df = pd.read_csv(negativos_file)
row = pd.concat((date_s, sinave_df.negativos))
negativos_df = negativos_df.append(row, ignore_index=True)


pairs_file_df = [(totales_file, totales_df),
                 (nuevos_file, nuevos_df),
                 (muertes_file,  muertes_df),
                 (sospechosos_file, sospechosos_df),
                 (negativos_file, negativos_df)]

for file, df in pairs_file_df:
    print(f'\nUltimos cambios {file}')
    print(df.tail(2))

    if global_write:
        write = True
    else:
        write = input('\nEscribir cambios (y/n) : ')
        write = True if write == 'y' else False

    if write:
        with open(file, 'a') as f:
            # f.write('\n')
            df.tail(1).to_csv(path_or_buf=f,
                              header=False, index=False)

# Eliminamos totales para el país
sinave_df = sinave_df.iloc[1:]

# Archivo de geojson
geojson_file = geo_dir + 'mexico.geojson'
edos_hoy_file = data_dir + 'estados_hoy.csv'
updated_file = data_dir + 'last_updated.csv'

gdf = gpd.read_file(geojson_file).set_index('name')

gdf[['totales', 'muertes']] = sinave_df[['positivos', 'defunciones']]
gdf.nuevos = nuevos_df.iloc[-1, 2:].astype('int')
# gdf.recuperaciones = recuperados_df.iloc[-1, 2:].values.astype('int')
# gdf.activos = activos_df.iloc[-1, 2:].values.astype('int')
gdf.totales_100k = gdf.totales * 100000 / gdf.population
gdf.updated_at = str(update_time).replace(' ', 'T')

gdf = gdf.reset_index()
assert gdf.shape[1] == 12


cols_edos_hoy = ['name', 'totales', 'nuevos',
                 'activos', 'muertes', 'recuperaciones']
map_cols = {'name': 'Estado',
            'totales': 'Casos totales',
            'nuevos': 'Casos nuevos ultimas 24h',
            'activos': 'Casos activos',
            'muertes': 'Muertes',
            'recuperaciones': 'Recuperaciones'}
edos_hoy_df = gdf[cols_edos_hoy].rename(columns=map_cols)

if global_write:
    write = True
else:
    write = input('\nEscribir cambios GeoJSON (y/n) : ')
    write = True if write == 'y' else False

if write:
    gdf.to_file(geojson_file, driver='GeoJSON')
    gdf.loc[0:0, ['updated_at']].to_csv(updated_file, index=False)
    edos_hoy_df.to_csv(edos_hoy_file, index=False)
