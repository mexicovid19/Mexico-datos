#!/bin/bash

set -euo pipefail

URL="https://www.gob.mx/salud/documentos/datos-abiertos-152127"
URL_ZIP="http://epidemiologia.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip"
ZIP_FILE="datos_abiertos_covid19.zip"
DATE_PATTERN="[Bb]ase de [Dd]atos.*$(date -d "yesterday" +"%d/%m/%Y")"

# REPO_DIR="/direccion/al/repo/"  ##### <--- Modifica    ######
cd "$REPO_DIR"

DATA_DIR="./datos_abiertos/raw"
FILENAME="datos_abiertos_$(date -d "yesterday" +"%Y%m%d")"


# Creamos directorio temporal
TMP_DIR=$(mktemp -d)  # -p "$REPO_DIR"
echo -e "Directorio temporal es $TMP_DIR\n"

# Nos aseguramos de que los archivos nuevos se eliminen en caso de error
trap 'rm -rf "$TMP_DIR"' ERR
trap 'rm "$ZIP_FILE"' ERR


# Descarga el archivo zip
#curl -LO "$URL_ZIP" && unzip "$ZIP_FILE" -d "$TMP_DIR"
if curl -sSL "$URL" | tac | tac | grep -q "$DATE_PATTERN"; then
    echo -e "Pagina esta actualizada; inicia descarga\n"
    curl -LO "$URL_ZIP" && unzip "$ZIP_FILE" -d "$TMP_DIR"
    echo -e "\nTermino descarga y descompresion\n"
else
    echo  -e "ERROR: pagina no esta actualizada"
    exit 1
fi


# Verifica que el archivo zip descomprimido correponda a un un solo archivo, renombra
if [ $(ls -1 "$TMP_DIR" | wc -l) == "1" ]; then
    DOWNLOAD_NAME=($TMP_DIR/*.csv)  # NB: globs are not expanded in quotes

    FILE_ENCODING="$(file -b --mime-encoding $DOWNLOAD_NAME)"

    echo -e "Encoding era $FILE_ENCODING; corriendo script fix_latin\n"

    fix_latin "$DOWNLOAD_NAME" > "$DATA_DIR/$FILENAME.csv"
    echo -e "Archivo csv renombrado: $FILENAME.csv (conversion fix_latin exitosa)\n"
else
    echo "ERROR: archivo csv no encontrado o hay ambiguedad"
    exit 1
fi


# Conprimimos archivo csv y generamos zip
if [ -f "$DATA_DIR/$FILENAME.csv" ]; then
    zip -9  "$DATA_DIR/$FILENAME.zip" "$DATA_DIR/$FILENAME.csv"
    echo -e "\nArchivo zip creado\n"
else
    echo "ERROR: archivo csv no encontrado (paso de compresion)"
    exit 1
fi


# Eliminamos archivos temporales
rm -rf "$TMP_DIR"
rm "$ZIP_FILE"
rm "$DATA_DIR/$FILENAME.csv"

echo "Termina script"
