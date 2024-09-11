#!/bin/bash

#SBATCH --job-name=exporting_resp
#SBATCH --output=output_%j.txt
#SBATCH --ntasks=4  # Requesting 16 processors
#SBATCH --nodes=1
#SBATCH --hint=nomultithread


#SBATCH --exclude=w[1-2,8-12]


# Call the merged Python script with the passed argument
python /CSNG/baroni/mozaik-models/export/export.py $1 $2