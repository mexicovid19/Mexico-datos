#!/bin/bash

echo -e "\n$(date)"

# Activa environment de conda
CONDA_BASE="$(conda info --base)"
CONDA_ENV="csv"
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate  "$CONDA_ENV"


set -euo pipefail


# La linea abajo consigue el direcororio donde se encuentra el script sin
# importar de donde se llame (no funcioa si el último componente es un symlink)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Descarga la ultima base de datos
/bin/bash ./download.sh
# /bin/bash ./download_mirror.sh

DATA_DIR=../tmp.*
FILENAME="$(date -d "yesterday" +"%Y%m%d").zip"
# si download_mirror, el nombre es el de abajo
# FILENAME="datos_abiertos_$(date -d "yesterday" +"%Y%m%d").zip"

if [ -f  $DATA_DIR/$FILENAME ]; then
    echo -e "\nDatos bajados, inicia script Python\n"
    python -u process_datos_abiertos.py $DATA_DIR/$FILENAME; echo
    # python update_tests.py
    python update_deceased.py
    python update_pyramids.py $DATA_DIR/$FILENAME

    rm -rf $DATA_DIR
    git add ../datos ; git add ../datos_abiertos
    git commit -m "Automatic update"
    git push #-f fork
else
    echo "Archivo no encontrado"
fi


# fin del script
