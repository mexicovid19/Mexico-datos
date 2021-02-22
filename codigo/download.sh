#!/bin/bash

set -euo pipefail

URL="https://www.gob.mx/salud/documentos/datos-abiertos-152127"
URL_ZIP="http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos"
ZIP_FILE="datos_abiertos_covid19.zip"

#DATE_CMD='date -d yesterday'  # date -d funciona en linux (bash)
# En MacOS utilizar date -v (descomentar línea de abajo)
DATE_CMD='date -v -1d'

# El patrón que se utiliza para saber si la página está actualizada
DATE_PATTERN="[Bb]ase de [Dd]atos.*$( $DATE_CMD +"%d/%m/%Y" )"

# después de descargar se renombra el archivo usando la fecha
FILENAME="$( $DATE_CMD +"%Y%m%d" )"

# La linea abajo consigue el direcororio donde se encuentra el script sin
# importar de donde se llame (no funciona si el último componente es un symlink)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"



# Creamos directorio temporal
TMP_DIR=$(mktemp -dp ..)  # -p "$REPO_DIR"
echo -e "Directorio temporal es $TMP_DIR\n"

# Nos aseguramos de que los archivos nuevos se eliminen en caso de error
trap 'rm -rf "$TMP_DIR"' ERR  # TODO: no funciona, arreglar


# Descarga el archivo zip
if curl -sSL "$URL" | tac | tac | grep -q "$DATE_PATTERN"; then
    echo -e "Pagina esta actualizada; inicia descarga\n"

    curl -LO "$URL_ZIP/$ZIP_FILE" && unzip "$ZIP_FILE" -d "$TMP_DIR"
    echo -e "\nTermino descarga y descompresion\n"
else
    echo  -e "ERROR: pagina no esta actualizada"
    exit 1
fi


# Verifica que el archivo zip descomprimido correponda a un un solo archivo, renombra
if [ $(ls -1 "$TMP_DIR" | wc -l) == "1" ]; then
    DOWNLOAD_NAME=($TMP_DIR/*.csv)  # NB: globs are not expanded in quotes
    echo -e "Corriendo script fix_latin\n"

    # Se descartan columns
    # awk -F, '{print $3","$5","$10","$11","$13","$36}' "$DATA_DIR/$FILENAME.csv" > "$DATA_DIR/$FILENAM    E.csv"
    # echo -e "Archivo csv reducido: solo las columnas necesarias fueron conservadas\n"

    fix_latin "$DOWNLOAD_NAME" > "$TMP_DIR/$FILENAME.csv"
    echo -e "Archivo csv renombrado: $FILENAME.csv (conversion fix_latin exitosa)\n"

else
    echo "ERROR: archivo csv no encontrado o hay ambiguedad"
    exit 1
fi


# Conprimimos archivo csv y generamos zip
if [ -f "$TMP_DIR/$FILENAME.csv" ]; then
    zip  "$TMP_DIR/$FILENAME.zip" "$TMP_DIR/$FILENAME.csv"
    echo -e "\nArchivo zip creado\n"
else
    echo "ERROR: archivo csv no encontrado (paso de compresion)"
    exit 1
fi


# Eliminamos archivos temporales
# rm -rf "$TMP_DIR"
rm "$ZIP_FILE"
rm $TMP_DIR/*.csv

echo "Termina script"
