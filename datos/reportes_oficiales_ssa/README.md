# Datos publicados por la Secretaría de Salud

En este directorio se encuentran las tablas de casos sospechosos y confirmados que publica la SSA todos los días. Para facilitar cualquier análisis en la computadora (usando Excel, Python, R, etc), se encuentran en formato `csv`. También incluimos los archivos PDF originales ya que la SSA no hace proporciona un archivo de las fechas anteriores.

## Metodología y normalización de los datos

- Nombres: corregimos acentos, cambiamos Ciudad de México en lugar de Distrito Federal, etc.
- Sexo: Utilizamos `M` y `F`.
- Fecha: Siguiendo a [mayrop](https://www.covid19in.mx/docs/datos/tablas-casos/normalizacion/fecha/) interpretamos el error de fecha como una fecha en Excel. Restamos un día debido a [un bug](https://docs.microsoft.com/en-gb/office/troubleshoot/excel/wrongly-assumes-1900-is-leap-year).  Gracias a @carranco-sga por señalar la correción.


## Actualizaciones

- **Abril 9**: Los documentos PDF preparados por la SSA el día 8 de Abril no incluyen la penúltima columna que correspondería al país de procedencia del caso.


- **Abril 7**: Los documentos PDF preparados por la SSA el día 6 de Abril no incluyen la última columna que correspondería a la fecha de llegada al país. Los nombres de los estados han perdido sus acentos, y se utiliza el nombre de `DISTRITO FEDERAL` en lugar de `CIUDAD DE MÉXICO`. El sexo del paciente se reporta como `MASCULINO` y `FEMENINO` en lugar de `M` y `F` como antes.

- **Abril 2**: Las tablas de casos sospechosos de los días 23 a 16 de marzo están marcadas con `_star` para indicar que tienen un formato especial: tienen una columna extra llamada localidad. Por algún motivo la SSA incluyó más información durante cuatro días.
