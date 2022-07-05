#!/bin/bash 

# Load plink 
module load plink 

# Read arguments
PROGNAME=$0

usage() {
  cat << EOF >&2
Usage: $PROGNAME [-p <plate>]
One or more of the following flags is missing:
-p <plate>:  Plate number to parse data from PLINK files.
-f <file-path>: Full path to the prefix of the file to binarize.
EOF
  exit 1
}

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
    echo '-p <plate>: Plate number to parse data from PLINK files.'
    echo '-f <file-path>: Full path to the prefix of the file to binarize.'
    shift
    shift
    ;;
    -p|--plate)
    PLATE="$2"
    shift # past argument
    shift # past value
    ;;
    -f|--file-prefix)
    FILEPATH="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    usage # save it in an array for later 
esac
done

# Path to GWAS data 
SETTINGS=$(pwd)/settings.json
RAWDATA_GWAS=$(jq -r '.raw_data_path' $SETTINGS)

# Process data 
FOLDER_PLATE=PMRA_Plate_${PLATE}
plink --bfile ${FILEPATH} --keep patList.txt --make-bed --out PMRA_Plate_${PLATE} > PMRA_Plate_${PLATE} 

# Create directory if it does not exist and move plate files 
if [ -d ${RAWDATA_GWAS}${FOLDER_PLATE} ]; 
then 
echo "Folder with plate data was already created. Please check that the files in ${FOLDER_PLATE} and delete accordingly."
else
mkdir ${RAWDATA_GWAS}${FOLDER_PLATE}
mv PMRA_Plate_${PLATE}* ${RAWDATA_GWAS}${FOLDER_PLATE}/
echo "Plate ${PLATE} stored in  ${RAWDATA_GWAS}${FOLDER_PLATE}"
fi

# Delete patient list 
rm patList.txt