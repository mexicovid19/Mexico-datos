#!/bin/bash

set -euo pipefail

# El siguiente espejo fue creado para nuestro equipo
URL="https://repounam.org/data/.input"

# El unicode del archivo csv es arreglado, sin embargo puede haber un typo
# en el nombre del archivo
PATTERN="$(date -d "yesterday" +"%Y-%m-%d")_u(tf|ft)8.zip"
ZIP_FILE="$(curl -sSL "$URL" | tac | tac | grep -Eo "$PATTERN" | head -1)"
echo -e "Nombre de zip file es $ZIP_FILE\n"


# La linea abajo consigue el direcororio donde se encuentra el script sin
# importar de donde se llame (no funcioa si el último componente es un symlink)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

FILENAME="datos_abiertos_$(date -d "yesterday" +"%Y%m%d").zip"


# Descarga el archivo zip
if [ ! -z "$ZIP_FILE" ]; then
    echo "Pagina esta actualizadañ inicia descarga"

    # Creamos directorio temporal
    TMP_DIR=$(mktemp -dp ..)
    echo -e "Directorio temporal es $TMP_DIR\n"

    # Nos aseguramos de que los archivos nuevos se eliminen en caso de error
    trap 'rm -rf "$TMP_DIR"' ERR
    #TODO: parece que esto no esta funcionando

    curl -L "$URL/$ZIP_FILE" -o "$TMP_DIR/$FILENAME"
    echo -e "\nTermino descarga\n"
else
    echo  -e "ERROR: pagina no esta actualizada"
    exit 1
fi

# fin del script
