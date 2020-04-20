#!/bin/bash

# PATH="$PATH:/home/user/miniconda3/condabin"

CONDA_BASE="$(conda info --base)"
CONDA_ENV="csv"
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate  "$CONDA_ENV"


set -euo pipefail


URL="https://www.gob.mx/salud/documentos/datos-abiertos-152127"
URL_ZIP="http://187.191.75.115/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip" 
ZIP_FILE="datos_abiertos_covid19.zip"
DATE_PATTERN="[Bb]ase de [Dd]atos.*$(date -d "yesterday" +"%d/%m/%Y")"

WORK_DIR="$HOME/Documents/covid/repo/codigo"
cd "$WORK_DIR"

DATA_DIR="../datos/datos_abiertos"
FILENAME="covid19_mex_$(date -d "yesterday" +"%Y%m%d").csv"


# Creamos directorio temporal
TMP_DIR=$(mktemp -d)  # -p "$WORK_DIR"
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
    echo  -e "\nERROR: pagina no esta actualizada"
    exit 1
fi


# Verifica que el archivo zip descomprimido correponda a un un solo archivo csv, renombra
if [ $(ls -1 "$TMP_DIR" | wc -l) -eq  "1" ]; then
    mv $TMP_DIR/*.csv "$DATA_DIR/$FILENAME"
    # NB: globs are not expanded in quotes
    echo -e "Archivo csv renombrado: $FILENAME\n" 
else
    echo "ERROR: archivo csv no encontrado o hay ambiguedad"
    exit 1
fi


# Eliminamos archivos temporales
rm -rf "$TMP_DIR"
rm "$ZIP_FILE"

echo "Termina script"
