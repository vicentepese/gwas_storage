#!/bin/bash 

# Load plink 
module load plink 

# Read arguments
PROGNAME=$0

usage() {
  cat << EOF >&2
Usage: $PROGNAME [-f <file-prefix>]
One or more of the following flags is missing:
-f <file-prefix>:  Full path to the prefix of the file to binarize.
EOF
  exit 1
}

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
    echo '-f <file-prefix>: Full path to the prefix of the file to binarize'
    shift
    shift
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

# Binarize
echo "Binarizing data"
plink --file ${FILEPATH} --make-bed --allow-no-sex --no-fid --no-parents --no-sex --no-pheno --out ${FILEPATH} > ${FILEPATH}