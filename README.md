# Datos para el monitoreo del COVID-19 en México

Los datos sobre el número de casos confirmados, sospechosos y negativos de SARS-COV-2 (COVID-19) en México son publicados por el gobierno a través de la Secretaría de Salud (SSa). Sin embargo, estos datos se publican de manera fragmentada, con errores y omisiones, y por lo general en un formato que no es fácil de manejar en computadora. Tampoco se ha hecho público  archivo de datos, y por lo tanto no es posible seguir la evolución a través del tiempo.

Este repositorio funge como una base de datos (no-oficial) para toda la información que publica la SSa. Archivamos, normalizamos y convertimos los datos a formatos que son fáciles de manipular en computadora (CSV, JSON, etc).

**Este repositorio es actualizado a diario,** y trabajamos mucho para mejorarlo. Si tienes algún comentario, queja o sugerencia, por favor escríbenos al correo mexicovid19contacto@gmail.com, abre un issue o realiza un pull request.

Si estás interesado/a en una visualización de los datos que aquí se encuentran, puedes visitar [nuestra página para el monitoreo del coronavirus en México](https://mexicovid19.github.io/Mexico/) (y el [repositorio](https://github.com/mexicovid19/Mexico) con su respectivo código fuente).

<!-- **Este repositorio es actualizado a diario.** La fecha y hora de la última actualización la encontrarás en `last_updated.csv` que se encuentra [aquí](https://github.com/mexicovid19/Mexico-datos/blob/master/datos/last_updated.csv). -->


## Datos

1. Los datos publicados por la Secretaría de Salud (SSa) en encuentran en los siguientes directorios. **Datos oficiales:**
    - [datos/reportes_oficiales_ssa](datos/reportes_oficiales_ssa): se archivan las dos tablas en formato PDF de casos confirmados y sospechosos que se publican junto con el Comunicado Técnico Diario (CDT), así como las tablas en formato CSV. Para más información sobre la normalización, referirse a este [README](datos/reportes_oficiales_ssa/README.md).
    - [datos/sinave](datos/sinave): se archivan los datos en formato JSON que se obtienen a diario a partir del mapa de SINAVE.
    - [datos/datos_abiertos](datos/datos_abiertos): a partir del lunes 13 de abril, la SSa publica tablas en formato CSV con todos los casos relacionados (confimados o no). Para facilitar su procesamiento, estos archivos se han incorporado a una base de datos sqlite.


2. Procesamos los datos de Salud a diario para obtener el historial de los casos a nivel nacional y desglosados por estado, así como un resumen con el que construimos una pirámide poblacional según el sexo del paciente y el rango de edad. **Datos procesados:**
    - [datos/series_de_tiempo/covid19_mex_casos_totales.csv](datos/series_de_tiempo/covid19_mex_casos_totales.csv)
    - [datos/series_de_tiempo/covid19_mex_muertes.csv](datos/series_de_tiempo/covid19_mex_muertes.csv)
    - [datos/series_de_tiempo/covid19_mex_casos_nuevos.csv](datos/series_de_tiempo/covid19_mex_casos_nuevos.csv)
    - [datos/series_de_tiempo/covid19_mex_sospechosos.csv](datos/series_de_tiempo/covid19_mex_sospechosos.csv)
    - [datos/series_de_tiempo/covid19_mex_negativos.csv](datos/series_de_tiempo/covid19_mex_negativos.csv)
    - [datos/demograficos_variables/piramide_sexo_edad.json](datos/demograficos_variables/piramide_sexo_edad.json)


## Fuentes para los datos del COVID-19

- Tabla de casos positivos y Tabla de casos sospechosos en formato PDF: [Coronavirus (COVID-19)-Comunicado Técnico Diario](https://www.gob.mx/salud/documentos/coronavirus-covid-19-comunicado-tecnico-diario-238449) de la Secretaría de Salud Federal.

- [Mapa interactivo del Sistema Nacional de Vigilancia Epidemiológica (SINAVE)](https://ncov.sinave.gob.mx/mapa.aspx)

- [Datos abiertos de la Dirección General de Epidemiología](https://www.gob.mx/salud/documentos/datos-abiertos-152127) publicados por la Secretaría de Salud Federal.


Otras fuentes que **no se incluyen aquí**

- [Serendipia - Periodismo de datos](https://serendipia.digital/2020/03/datos-abiertos-sobre-casos-de-coronavirus-covid-19-en-mexico/)
- [Blog de @mayrop](https://www.covid19in.mx/docs/datos/tablas-casos/)
- [Our World in Data](https://ourworldindata.org/coronavirus)
- [Worldometers](https://www.worldometers.info/coronavirus/country/mexico/): reporta casos recuperados pero no menciona la fuente.
- [John Hopkins University](https://github.com/CSSEGISandData/COVID-19): para México reporta como fuente a Worldometers
- [IIGEA](iigea.com/amag/covid-19/): recopila información de las Secretarías Estatales de Salud.
- [verificovid](https://verificovid.mx/);

Otros repositorios con datos similares:

- [carranco-sga/Mexico-COVID-19](https://github.com/carranco-sga/Mexico-COVID-19)
- [covidctdmx/covid_ctd_mx](https://github.com/covidctdmx/covid_ctd_mx)
- [guzmart/covid19_mex](https://github.com/guzmart/covid19_mex)

Un repositorio con datos para otros países de América Latina:
- [DataScienceResearchPeru/covid-19_latinoamerica](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica)

Un repositorio con datos del Reino Unido que nos ha servido de inspiración en algunas cosas:

- [tomwhite/covid-19-uk-data](https://github.com/tomwhite/covid-19-uk-data)


### Otros datos
- Población y número promedio de familia por estados, 2015: [Inegi, Encuesta Intercensal 2015](https://www.inegi.org.mx/programas/intercensal/2015/default.html#Tabulados);

- Polígonos de los estados del país en formato  GEOJSON: [Blocks](http://bl.ocks.org/ponentesincausa/46d1d9a94ca04a56f93d)


## Herramientas

Para convertir las tablas PDF de casos confirmados y sospechosos a formato CSV utilizamos primero Python y luego Julia (por el tiempo reducido para correr el código)

- [codigo/scrap.py](codigo/scrap.py): (Deprecado) `python scrapy.py`; Requerimientos: `pip install -r requirements.txt`
- [codigo/scrap.jl](codigo/scrap.jl): `julia scrap.jl Tabla.pdf [-o output.csv]`; Requerimientos: `TODO` (Esta función fue tomada de @carranco-sga y extendida para nuestros propósitos)

Para descargar de forma autómatica los datos del mapa de SINAVE utilizamos un script en JS que corre en node.js.

- [codigo/descarga_sinave.js](codigo/descarga_sinave.js) `node download_sinave.js 2>/dev/null`; Requerimientos: `npm install jsdom jquery`

## Workflow diario

```
node download_sinave.js
python update_from_json.py 20200415.json true

julia scrap.jl Tabla_casos_positivos_2020.04.15.pdf -o covid19_mex_confirmados_20200415.csv
julia scrap.jl Tabla_casos_sospechosos_2020.04.15.pdf -o covid19_mex_sospechosos_20200415.csv
mv covid19_mex* ../datos/reportes_oficiales_ssa
python update_pyramid.py
```
