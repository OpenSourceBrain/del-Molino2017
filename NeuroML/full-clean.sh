#!/bin/bash

#Allowed files
allowed_files=("Fig1" "Fig2" "Fig3" "temp" "GenerateNeuroMLlite.py" "Sweep.py" "regenerateAndTest.sh" "clean.sh" "full-clean.sh" "RateBased.xml" "RateBasedSpecifications_high_baseline.xml" "RateBasedSpecifications_low_baseline.xml")

#Directory
directory="/home/ixanthakis/wsl_repos/PyNeuroMLTutorials/ClonedNeuroMLRepositories/del-Molino2017/NeuroML"

#Iterate over all files in the directory
for file in "$directory"/*; do
    #Check if the file is not in the list of allowed files
    if [[ ! " ${allowed_files[@]} " =~ " ${file##*/} " ]]; then
        #Remove the file
        rm "$file"
        echo "Removed: $file"
    fi
done
