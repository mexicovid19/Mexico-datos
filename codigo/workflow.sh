#!/bin/bash

set -euo pipefail


echo -e "\n$(date)"

# La linea abajo consigue el directorio donde se encuentra el script sin
# importar de donde se llame (no funciona si el último componente es un symlink)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"


# Descarga la ultima base de datos
# /bin/bash ./download.sh
/bin/bash ./download_nodecompress.sh
# /bin/bash ./download_mirror.sh


# Activa el ambiente virtual
VENV="virtualenv"
source "${VENV}/bin/activate"
# trap 'deactivate' EXIT  # deactivate not found, pero no es necesario

DATE_CMD='date -d yesterday'  # date -d funciona en linux (bash)
# En MacOS utilizar date -v (descomentar línea de abajo)
# DATE_CMD='date -v -1d'

FILENAME="$( $DATE_CMD +"%Y%m%d" ).zip"
# si download_mirror, el nombre es el de abajo
# FILENAME="datos_abiertos_$FILENAME"


if [[ -f  "$FILENAME" ]]; then
    echo -e "\nBase de datos encontrada, inician scripts de Python\n"
    python -u process_datos_abiertos.py "$FILENAME"; echo
    python update_tests.py
    python update_deceased.py
    python update_pyramids.py "$FILENAME"

    git add ../datos ../datos_abiertos
    git commit -m "Automatic update"
    git push  #-f fork
else
    echo "Archivo no encontrado"
fi

rm "$FILENAME"


echo -e "\nTermina script workflow.sh\n"

