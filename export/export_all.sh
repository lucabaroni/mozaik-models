#!/bin/bash

# Define an array of base folders
base_folders=(
    '/path/to/simulation/folder'
    # "/CSNG/baroni/mozaik-models/LSV1M/20240117-111742[param_nat_img.defaults]CombinationParamSearch{trial:[0],baseline:500}"  # example of simulation folder path
    )
sheets=(
    "V1_Exc_L4"
    "V1_Inh_L4"
    "X_ON"
    "X_OFF"
    "V1_Exc_L2/3"
    "V1_Inh_L2/3"
    )


# Loop over each base folder
for base_folder in "${base_folders[@]}"; do
    for sheet in "${sheets[@]}"; do 
        # Loop through each directory starting with "NewDataset_Images"
        find "$base_folder" -type d -name "NewDataset_Images*" | while read folder; do
            sbatch /CSNG/baroni/mozaik-models/export/export_single.sh "$folder" "$sheet" './path/to/folder/to/save/results'
        done
    done
done



