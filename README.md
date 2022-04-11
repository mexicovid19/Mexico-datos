# Datos para el monitoreo del COVID-19 en México

Los datos sobre el número de casos confirmados, sospechosos y negativos de SARS-COV-2 (COVID-19) en México son publicados por el gobierno a través de la Secretaría de Salud (SSa). ~~Estos datos se publicaban de manera fragmentada, con errores y omisiones, y por lo general en formato PDF lo que dificulta manejarlos en computadora. Tampoco se ha hecho público  archivo de datos, y por lo tanto no es posible seguir la evolución a través del tiempo.~~

Desde el lunes 13 de abril, la SSa a través de Dirección General de Epidemiología publica [una base de "datos abiertos"](https://www.gob.mx/salud/documentos/datos-abiertos-152127) muy completa y en formato CSV. Desde entonces, este repositorio funciona principalmente como una base de datos (no-oficial) donde se archiva la información actualizada, así como los datos previos publicados en PDF (que han sido archivados, normalizados y convertidos a CSV).

También mantenemos series de tiempo (formato *tidy*) de diferentes variables para facilitar el análisis de la base de datos abiertos.

**Este repositorio es actualizado a diario,** y trabajamos constantemente para mejorarlo. Si tienes algún comentario, queja o sugerencia, abre un issue o realiza un pull request. También puedes escribirnos al correo mexicovid19contacto@gmail.com.

Si estás interesado/a en una visualización de los datos que aquí se encuentran, puedes visitar [nuestra página para el monitoreo del coronavirus en México](https://mexicovid19.github.io/Mexico/) (y el [repositorio](https://github.com/mexicovid19/Mexico) con su respectivo código fuente).

<!-- **Este repositorio es actualizado a diario.** La fecha y hora de la última actualización la encontrarás en `last_updated.csv` que se encuentra [aquí](https://github.com/mexicovid19/Mexico-datos/blob/master/datos/last_updated.csv). -->


### Avisos

**Mayo 19:** Los archivos de la base de datos abiertos se encuentran en formato zip. **No son solamente los archivos que publica Salud**, todos los días bajamos éstos, los descomprimimos, arreglamos el encoding, y los comprimimos de nuevo. También hemos eliminado las carpetas con los archivos PDF que sumaban más de 150 MB. 

**Mayo 14:** Dado que los archivos CSV superan a diario 20MB de espacio, estamos en proceso de refactorizar nuestra base de datos para que solamente utilice archivos comprimidos (en formato zip). Tenemos planeado que a partir de mañana 15 de mayo los archivos de datos abiertos en formato CSV hayan sido eliminados (con todo y el overhead de trackearlos con git). Si bien Salud publica sus archivos comprimidos, vale la pena mencionar que hasta el día de hoy la Secretaría **los sigue publicando con el error de encoding** y nosotros seguimos corrigiéndolo. 

**Abril 28:** Desde el lunes 24 de Abril los archivos presentan problemas con el *encoding*. Aunque deberían de ser en principio UTF-8, el comando `file -i` en bash detecta ISO-8859-1 (también conocido como latin-1). El problema es que se utilizan ambos encodings para los acentos y éstos son incompatibles.

Por ejemplo, en el archivo del día 27 que se puede bajar [del portal de Salud](https://www.gob.mx/salud/documentos/datos-abiertos-152127) hay 26 filas donde la letra é en "Estados Unidos de América" está codificada con latin-1. En todos los demás casos se utiliza correctamente UTF-8. Para solucionar el problema hemos recurrido a la librería [Encoding::FixLatin](https://metacpan.org/pod/Encoding::FixLatin) escrita en perl y que se llama en nuestra script de bash `download_datos_abiertos.sh`.


**Abril 22:** Puedes leer una explicación más completa en [nuestra página](https://mexicovid19.github.io/Mexico/datos_abiertos.html) pero a continuación aclaramos por qué nuestro equipo ha encontrado que la base de datos abiertos de la DGE *no presenta inconsistencias* con respecto a los datos que Salud publicaba previamente:

- La base de datos abiertos tiene información mucho más completa y cada caso se puede seguir de individual. Para cada paciente, es posible conocer qué día fue atendido y el estado (confirmado, negativo o pendiente) de la prueba que se le realizó.

- Al confirmarse que la prueba de un paciente fue positiva (o negativa), la entrada del paciente se actualiza. Sin embargo, no tiene sentido llevar cuenta de la fecha en que el resultado de la prueba se dio a conocer; en la nueva base de datos tiene más sentido contabilizar la prueba el día que el paciente visitó una Unidad Médica (la columna `FECHA_INGRESO` en la nueva base de datos).

- Esto significa en la base de datos abiertos la información se propaga de manera retroactiva y que los casos de los días anteriores van a cambiar. Esto sucede por ejemple en [el tablero oficial de la Secretaría de Salud](https://coronavirus.gob.mx/datos/).
.
- Esto contrasta con una serie de tiempo "usual" donde todos los casos que se confirmaron cierto día son contabilizados ese mismo día, y por lo tanto las fechas anteriores no cambian.

- Nuestra base de datos refleja las dos maneras de contabilizar los datos.


## Datos

1. Datos abiertos:
    - [datos_abiertos/raw](datos_abiertos/raw): los datos publicados por la DGE a partir del lunes 13 de abril.

2. Datos abiertos en formato *tidy*:
    - [datos_abiertos/series_de_tiempo/nuevos](datos_abiertos/series_de_tiempo/nuevos):
    diferentes variables contabilizadas por día y por estado.
    - [datos_abiertos/series_de_tiempo/acumulados](datos_abiertos/series_de_tiempo/acumulados):
    diferentes variables contabilizadas por día y por estado y acumuladas hasta la fecha más reciente.

3. Datos correspondientes a formatos antiguos (PDFs, SINAVE) y publicados hasta el 19 de abril (SSa ha dejado de actualizarlos):
    - [datos/reportes_oficiales_ssa](datos/reportes_oficiales_ssa): se archivan las tablas de confirmados y sospechosos en formato CSV generadas a partir de los archivos PDF que SSa publicaba.
    - [datos/sinave](datos/sinave): se archivan los datos en formato JSON que se extraían  del mapa de SINAVE.

4. Datos correspondientes a formatos antiguos en formato *tidy*:
    - [datos/series_de_tiempo](datos/series_de_tiempo): el historial de casos a nivel nacional y desglosados por estado. **Estas series de tiempo se siguen actualizando con la base de datos abiertos** (el total de casos confirmados se asocia con el día de publicación).


<!-- 2. un resumen con el que construimos una pirámide poblacional según el sexo del paciente y el rango de edad.

    - [datos/demograficos_variables/piramide_sexo_edad.json](datos/demograficos_variables/piramide_sexo_edad.json) -->


## Fuentes para los datos del COVID-19

- [Datos abiertos de la Dirección General de Epidemiología](https://www.gob.mx/salud/documentos/datos-abiertos-152127) publicados por la Secretaría de Salud Federal. Estos datos has sido publicados con una licencia `Libre Uso MX` como consta en el [portal de datos abiertos del gobierno](https://datos.gob.mx/busca/dataset/informacion-referente-a-casos-covid-19-en-mexico).


- ~~Tabla de casos positivos y Tabla de casos sospechosos en formato PDF: [Coronavirus (COVID-19)-Comunicado Técnico Diario](https://www.gob.mx/salud/documentos/coronavirus-covid-19-comunicado-tecnico-diario-238449) de la Secretaría de Salud Federal.~~ Ya no se actualiza.

- ~~[Mapa interactivo del Sistema Nacional de Vigilancia Epidemiológica (SINAVE)](https://covid19.sinave.gob.mx)~~ Ya no se actualiza con casos confirmados, negativos o sospechosos (solo con casos activos).

- [Hospitalizaciones en la Red IRAG](https://www.gits.igg.unam.mx/red-irag-dashboard/reviewHome#) son descargadas mediante el scrapper en [@CapacidadHospitalariaMX](https://github.com/RodrigoZepeda/CapacidadHospitalariaMX)



Otras fuentes que **no se incluyen aquí**

- [Serendipia - Periodismo de datos](https://serendipia.digital/2020/03/datos-abiertos-sobre-casos-de-coronavirus-covid-19-en-mexico/)
- [Blog de @mayrop](https://www.covid19in.mx/docs/datos/tablas-casos/)
- [Our World in Data](https://ourworldindata.org/coronavirus)
- [Worldometers](https://www.worldometers.info/coronavirus/country/mexico/): reporta casos recuperados pero no menciona la fuente.
- [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19): para México reporta como fuente a Worldometers
- [IIGEA](iigea.com/amag/covid-19/): recopila información de las Secretarías Estatales de Salud.
- [verificovid](https://verificovid.mx/);

Otros repositorios con datos similares:

- [carranco-sga/Mexico-COVID-19](https://github.com/carranco-sga/Mexico-COVID-19)
- [covidctdmx/covid_ctd_mx](https://github.com/covidctdmx/covid_ctd_mx)
- [guzmart/covid19_mex](https://github.com/guzmart/covid19_mex)

Un repositorio con datos para otros países de América Latina:
- [DataScienceResearchPeru/covid-19_latinoamerica](https://github.com/DataScienceResearchPeru/covid-19_latinoamerica)

Un repositorio con datos del Reino Unido que nos ha servido de inspiración:

- [tomwhite/covid-19-uk-data](https://github.com/tomwhite/covid-19-uk-data)


### Otros datos

- Población y número promedio de familia por estados, 2015: [Inegi, Encuesta Intercensal 2015](https://www.inegi.org.mx/programas/intercensal/2015/default.html#Tabulados);

- Polígonos de los estados del país en formato GEOJSON: [Blocks](http://bl.ocks.org/ponentesincausa/46d1d9a94ca04a56f93d)


## Código

Para reproducir nuestro análisis puedes consultar nuestro código:

- [codigo](codigo): se encuentra un script de bash para bajar la base de datos (si está actualizada y corresponde al día anterior); un script de python para actualizar las series de tiempo y un segundo script de python para hacer un resumen en CSV de los casos diarios.

- [codigo/deprecated](codigo/deprecated): los scripts que se utilizaban anteriormente para convertir los PDF a CSV (`julia scrap.jl Tabla.pdf [-o output.csv]`; Requerimientos: `...`) o para descargar los datos en formato JSON del mapa de SINAVE (`node download_sinave.js 2>/dev/null`; Requerimientos: `npm install jsdom jquery`)

### Requerimientos

Para instalar [Encoding::FixLatin](https://metacpan.org/pod/Encoding::FixLatin) hemos seguido [los pasos en CPAN](https://www.cpan.org/modules/INSTALL.html) para instalar `cpanm` (un instalador de módulos). Utilizamos [el método de bootstrapping](https://metacpan.org/pod/local::lib#The-bootstrapping-technique) con `local::lib` para instalar las librerías en el directorio `~/.perl`, lo cual requiere descargar localmente el módulo `local::lib`, descomprimirlo, y haber hecho `cd` a él. Una vez hecho esto, la instalación completa se hace con los siguientes pasos:

```
cpan App::cpanminus  # instala cpanm

perl Makefile.PL --bootstrap=~/.perl
make test && make install  # instala local::lib en ~/.perl
echo 'eval "$(perl -I$HOME/.perl/lib/perl5 -Mlocal::lib=$HOME/.perl)"' >> ~/.bashrc
# Arriba, se configura el el environment desde el directorio ~/.perl

# después de volver a leer .bashrc
cpanm Encoding::FixLatin
```

Si todo está configurado correctamente, el ejecutable `fix_latin` debería de estar disponible en la terminal y se puede llamar desde un script de bash.

**Paso opcional:** también podemos instalar la [librería compilada de C](https://metacpan.org/pod/Encoding::FixLatin::XS) para que la conversión sea más rápida utilizando `cpanm Encoding::FixLatin::XS`.



<!-- - [codigo/scrap.py](codigo/scrap.py): (Deprecado) `python scrapy.py`; Requerimientos: `pip install -r requirements.txt` -->


## Workflow diario

```
./download_datos_abiertos.sh
python process_datos_abiertos.py
python update_tests.py
python update_pyramids.py
```

<!-- ```
node download_sinave.js
python update_from_json.py 20200415.json true

julia scrap.jl Tabla_casos_positivos_2020.04.15.pdf -o covid19_mex_confirmados_20200415.csv
julia scrap.jl Tabla_casos_sospechosos_2020.04.15.pdf -o covid19_mex_sospechosos_20200415.csv
mv covid19_mex* ../datos/reportes_oficiales_ssa
python update_pyramid.py
``` -->
