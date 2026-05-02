# LSH Similarity Checker

A simple tool to compare NetPyne simulation configuration files using Locality-Sensitive Hashing (LSH).

* Loads NetPyne JSON configuration files
* Extracts key model parameters (e.g., `connParams`)
* Compares configurations using LSH (`LSH_compare.py`)

Usage:
python LSH_compare.py <input_folder> <threshold> [--data] [--diff]


Example:
python netpyne_lsh.py ./configs 0.95 --diff

Exampel output:
Results for popParams
1 pairs with similarity >= 80.0% were found.
poster_files/tut02.json and poster_files/tut02_mod.json have a similarity score of 0.93
Data for netpynne_poster_files/tut02.json
{   'E2': {'cellType': 'E', 'numCells': 50, 'yRange': [100, 300]},
    'E4': {'cellType': 'E', 'numCells': 50, 'yRange': [300, 600]},
    'E5': {'cellType': 'E', 'numCells': 50, 'ynormRange': [0.6, 1.0]},
    'I2': {'cellType': 'I', 'numCells': 50, 'yRange': [100, 300]},
    'I4': {'cellType': 'I', 'numCells': 50, 'yRange': [300, 600]},
    'I5': {'cellType': 'I', 'numCells': 50, 'ynormRange': [0.6, 1.0]}}

Data for netpynne_poster_files/tut02_mod.json
{   'E2': {'cellType': 'E', 'numCells': 50, 'yRange': [100, 300]},
    'E4': {'cellType': 'E', 'numCells': 50, 'yRange': [300, 800]},
    'E5': {'cellType': 'E', 'numCells': 50, 'ynormRange': [1.6, 1.0]},
    'I2': {'cellType': 'I', 'numCells': 50, 'yRange': [100, 300]},
    'I4': {'cellType': 'I', 'numCells': 50, 'yRange': [300, 600]},
    'I5': {'cellType': 'I', 'numCells': 50, 'ynormRange': [0.6, 1.0]}}

Differences for popParams
{   'values_changed': {   "root['E4']['yRange'][1]": {   'new_value': 800,
                                                         'old_value': 600},
                          "root['E5']['ynormRange'][0]": {   'new_value': 1.6,
                                                             'old_value': 0.6}}}

LSH concept link:
[https://github.com/mattilyra/LSH/tree/master](https://github.com/mattilyra/LSH/tree/master)


ISSUES: 

This project provided simialrity score within various versions of the same model. The code was tested with both M1 and A1 models. Some issues observed
1. Error similar to : Exception: Error occured in h.load_file() when loading ../cells/PTcell.hoc. See above for details.
   Fix is to run nrnivmodl on the mod files
2. Error: wrap.c:224:40: error: incompatible function pointer types passing 'void (void *)' to parameter of type 'double (*)(void *)' [-Wincompatible-function-pointer-types]
   Fix: Presence of wrap.mod file causes issues with the lateste version of NEURON and NetPyNE. Removal of the line is the only solution as it doesnt affect the comparison of parameters. 
   
