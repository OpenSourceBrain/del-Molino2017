#!/bin/bash

#Iterate Through and Eliminate All Unwanted Files in a Specific Directory
remove_files_except_allowed() {
    local directory="$1"
    shift
    local allowed_files=("$@")

    # Iterate over all files in the directory
    for file in "$directory"/*; do
        #Check if the file is not in the list of allowed files
        if [[ ! " ${allowed_files[@]} " =~ " ${file##*/} " ]]; then
            rm -rf "$file"
            echo "Removed: $file"
        fi
    done
}

#Allowed Files
declare -a allowed_files=(".github" "NeuroML" "notebooks" "Python" ".gitignore" "clean-repository.sh" "README.md" "requirements.txt" "delMolino2017.ipynb" ".test.omt" "delMolino.py")

#Clear the Repository
directory="/home/ixanthakis/wsl_repos/PyNeuroMLTutorials/ClonedNeuroMLRepositories/del-Molino2017"
remove_files_except_allowed $directory "${allowed_files[@]}"

directory="/home/ixanthakis/wsl_repos/PyNeuroMLTutorials/ClonedNeuroMLRepositories/del-Molino2017/notebooks"
remove_files_except_allowed $directory "${allowed_files[@]}"

directory="/home/ixanthakis/wsl_repos/PyNeuroMLTutorials/ClonedNeuroMLRepositories/del-Molino2017/Python"
remove_files_except_allowed $directory "${allowed_files[@]}"

source ~/wsl_repos/PyNeuroMLTutorials/ClonedNeuroMLRepositories/del-Molino2017/NeuroML/full-clean.sh