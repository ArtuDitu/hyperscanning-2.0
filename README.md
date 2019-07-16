# General instructions for Python MNE Hyperscanning Project
In this directory, you'll find all necessary files to get the project running.

## Directory tree
|hyperscanning-2.0 \n
|--- .gitignore \n
|--- Preprocessing\_MNE.py \n
|--- subsetting\_script.py \n
|--- functions_MNE.py \n
|--- rename\_brainvision\_files.py \n
|--- _virtual\_environment\_setup_ \n
|------ requirements.txt \n
|------ setup\_readme.md \n
|------ environment.yml \n
|--- _load\_CNT_ \n
|------ load\_CNT.py \n
|------ read\_antcnt.py \n
|------ README.md \n
|------ libeep-3.3.177.zip \n
|------ load\_CNT\_oldvers.py \n
|------ read\_antcnt.pyc \n
|--- _mne\_data_ \n
|--- _info\_files_ \n
|--- _temp\_saving\_subsets_ \n

## Detailed description
1. FOLDER virtual\_environment\_setup:  
In this folder you find the necessary files and instructions for setting up a virtual-environment in order to run the scripts

2. The various scripts:  
Preprocessing\_MNE.py		--> Main script to execute  
subsetting\_script.py		--> functions that split raw data into two seperate files  
functions\_MNE.py		--> outsourcing the different functions that are called by main script  
rename\_brainvision\_files.py	--> example script for renaming BrainVision files without corrupting them  

3. FOLDER load\_CNT:  
Contains the files and scripts that enable conversion from Neuroscan.cnt file-format to MNE-compatible format.
This is necessary, since .cnt files can't be loaded with the function provided from MNE-toolbox. Thus we use a
script written by Benedikt Ehinger, which only works in python 2, hence a different virtual-environment (running python2) 
is used for initial loading of .cnt files in Python (see seperate Readme file for further instructions)

4. FOLDER info\_files:  
Folder contains files with necessary background information of the experiment (e.g. trigger description, subject-information)

5. FOLDER mne\_data:  
Main folder which stores all the source-data, raw-data and preprocessed-data in BIDS-compatible manner.

6. FOLDER temp\_saving\_subsets:  
A place to temporarily store eeg-files. Needs to be done during the splitting-process.

