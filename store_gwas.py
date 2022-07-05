import numpy as np 
import pandas as pd
import json 
import os
import subprocess

def binarize_data(settings:dict) -> None:
    """
    Description:        Binarize the data if not binarized.

    Inputs:
    settings (dict)     Settings dictionnary with all variables.
    """

    # Check if files is binarized
    path_file = os.path.join(settings['file_path'])
    file_name = os.path.basename(path_file)
    folder_file = os.path.dirname(path_file)
    files_folder = os.listdir(folder_file)

    if file_name + ".bed" not in files_folder:
        subprocess.call("bash sh_scripts/binarize.sh -f " + settings['file_path'], shell=True)

def parse_pat_info(settings:dict) -> pd.DataFrame:
    """
    Description:        Read .fam file, get GWAS IDs, and check IDs inconsistencies

    Inputs:
    settings (dict)     Settings dictionnary with all variables.
    """

    # Read fam file 
    fam_file = pd.read_csv(settings['file_path'] + '.fam', sep=' ', header=None)
    fam_file.columns = ['FID', 'IID', 'patID', 'matID', 'sex', 'pheno']

    # Parse plates and GWAS IDs
    fam_file["plate"] = fam_file.IID.apply(lambda x: x.split('_')[2] if 'SU' in x else x.split('_')[1])
    fam_file["pat_id"] = fam_file.IID.apply(lambda x: x.split('_')[3] if 'SU' in x else x.splot('_')[2])
    fam_file["GWASID"] = fam_file.IID.apply(lambda x: x.split('.CEL')[0].split('_')[-1] if '.CEL' in x else x.split('.cel')[0].split('_')[-1])
    fam_file["GWASID_mid"] = fam_file.plate + fam_file.pat_id
    fam_file["comp"] = fam_file.GWASID == fam_file.GWASID_mid

    # Write down incompatible GWAS IDs
    if any(fam_file.comp == False):
        fam_file[fam_file.comp == False][['FID', 'IID']].to_csv('incompatible_GWASIDs.csv', header=True, index=False)
        print("A total number of %s incompatible GWAS IDs have been found. The list of patients with incompatible GWAS IDs has been saved in incompatible_GWASIDs.csv".format(fam_file[fam_file.comp == True][['FID', 'IID']].shape[0]))

    # Write and return
    master_file = fam_file[['IID', 'FID', 'plate']]
    master_file.to_csv("master_file_" + os.path.basename(settings['file_path']) + '.csv', header=True, index=False)
    return master_file

def process_data(settings:dict, master_file:pd.DataFrame) -> None:

    # Separate into plates and save file into directory 
    plates = master_file.plate.unique()
    for plate in plates:
        patient_list_plate = master_file[master_file.plate == plate]
        patient_list_plate[['FID', 'IID']].to_csv("patList.txt", sep = " ", header=False, index=False)
        print("Processing Plate " + str(plate))
        subprocess.call(["bash", "sh_scripts/separate_plates.sh", "--plate", str(plate), "--file-prefix", settings['file_path']])

    pass

def main():

    # Read settings 
    with open('settings.json', 'r') as inFile:
        settings = json.load(inFile)
    
    # Binarize data
    binarize_data(settings)

    # Get patient info
    master_file = parse_pat_info(settings)

    # Process data 
    process_data(settings, master_file)





    


if __name__ == "__main__":
    main()