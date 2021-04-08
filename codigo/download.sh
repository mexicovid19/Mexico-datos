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

# dentro del archivo zip, el archivo csv tiene el siguiente nombre
CSV_FILENAME="$( $DATE_CMD +"%y%m%d" )COVID19MEXICO.csv"

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
trap 'rm -rf "$TMP_DIR"' EXIT


# Descarga el archivo zip
curl -L "$URL_ZIP" -o "$TARGET_BASENAME.zip"

echo -e "\nDescomprimiendo"
unzip "$TARGET_BASENAME.zip"

if [ -f "$CSV_FILENAME" ]; then
    # TODO: limpiar columnas por nombre
    # awk -F, '{print $3","$5","$10","$11","$13","$36}' "$CSV_FILENAME" > "$TARGET_BASENAME.csv"
    # echo -e "Archivo csv reducido: solo las columnas necesarias fueron conservadas\n"

    echo -e "\nCorriendo script fix_latin sobre: $CSV_FILENAME"
    fix_latin "$CSV_FILENAME" > "$TARGET_BASENAME.csv"
    echo -e "Archivo corregido es: $TARGET_BASENAME.csv\n"

else
    echo "ERROR: archivo csv no encontrado o hay ambiguedad"
    exit 1
fi


# Conprimimos archivo csv y generamos zip
if [ -f "$TARGET_BASENAME.csv" ]; then
    echo -e "Comprimiendo (sobreescribe zip original)"
    zip - "$TARGET_BASENAME.csv" > "$TARGET_BASENAME.zip"
    # la redireccion a stdout sobreescribe zip original
    
    echo -e "\nMoviendo el archivo fuera de $TMP_DIR"
    mv "$TARGET_BASENAME.zip" ..

    # Borramos archivos temporales
    cd ..
    rm -rf "$TMP_DIR"
else
    echo "ERROR: archivo csv no encontrado (paso de compresion)"
    exit 1
fi


echo -e "\nTermina script download.sh\n"

