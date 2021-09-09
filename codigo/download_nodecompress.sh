#!/bin/bash

set -euo pipefail


URL="https://www.gob.mx/salud/documentos/datos-abiertos-152127"
URL_ZIP="http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip"

DATE_CMD='date -d yesterday'  # date -d funciona en linux (bash)
# En MacOS utilizar date -v (descomentar línea de abajo)
# DATE_CMD='date -v -1d'

# El patrón que se utiliza para saber si la página está actualizada
DATE_PATTERN="[Bb]ase de [Dd]atos.*$( $DATE_CMD +"%d/%m/%Y" )"

# después de descargar se renombra el archivo usando la fecha
TARGET_BASENAME="$( $DATE_CMD +"%Y%m%d" )"

# dentro del archivo zip, el archivo csv tiene uno de los siguientes nombres
CSV_FALLBACK="COVID19MEXICO.csv"
CSV_FILENAME="$( $DATE_CMD +"%y%m%d" )$CSV_FALLBACK"

# La linea abajo consigue el directorio donde se encuentra el script sin
# importar de donde se llame (no funciona si el último componente es un symlink)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"


if curl -sSL "$URL" | tac | tac | grep -q "$DATE_PATTERN"; then
    echo -e "Pagina esta actualizada; inicia descarga\n"
else
    echo  -e "ERROR: pagina no esta actualizada"
    exit 1
fi


# Creamos directorio temporal
TMP_DIR=$(mktemp -dp .)  # -p "$REPO_DIR
echo -e "Directorio temporal es: $TMP_DIR\n"

# La descarga se hace dentro del directorio temporal
cd "$TMP_DIR"

# Borrar archivos temporales en caso de error
trap 'cd ..; rm -rf "$TMP_DIR"' EXIT


# Descarga el archivo zip
curl -L "$URL_ZIP" -o "$TARGET_BASENAME.zip"


# TODO: usar unzip -l abajo
# if [[ -f "$CSV_FILENAME" ]]; then
#     INPUT_FILENAME="$CSV_FILENAME"

# elif [[ -f "$CSV_FALLBACK" ]]; then
#     INPUT_FILENAME="$CSV_FALLBACK"

# else
#     echo "ERROR: archivo csv no encontrado o hay ambiguedad"
#     exit 1
# fi


echo -e "\nMoviendo el archivo fuera de $TMP_DIR"
mv "$TARGET_BASENAME.zip" ..

# Borramos archivos temporales
cd ..
rm -rf "$TMP_DIR"

echo -e "\nTermina script download.sh\n"

