# -*- coding: utf-8 -*-

############ EEG-Preprocessing Script (Python_MNE toolbox) ##############
# Credits:
# Pernet, C. R., Appelhoff, S., Flandin, G., Phillips, C., Delorme, A., &
# Oostenveld, R. (2018, December 6). BIDS-EEG: an extension to the Brain
# Imaging Data Structure  (BIDS) Specification for electroencephalography.
# https://doi.org/10.31234/osf.io/63a4y
"""
Created on June 16, 2019
# @author: mtiessen
# Mail: mtiessen@uos.de
"""

import os, sys
import pandas as pd
import numpy as np
import mne
# from mne import io
from datetime import datetime
from mne_bids import write_raw_bids, make_bids_basename, read_raw_bids
from mne.datasets import sample
from mne_bids.utils import print_dir_tree
os.chdir('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0')
from subsetting_script import sub2, sub1
from functions_MNE import *
import pybv

# set current working directory
os.chdir('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/mne_data/sourcedata')
# make directory to save the data in BIDS-format
home = os.path.expanduser('~')
mne_dir = os.path.join(home,'/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/mne_data/')


# %%

if __name__=='__main__':
    #############################################
    # STEP ONE: Load data, split into two structs
    #############################################
    # visualize data structure of raw files
    # print_dir_tree('/home/student/m/mtiessen/link_hyperscanning/hyperscanning-2.0/mne_data')

    # do for each subject
    for subject in ['204']:
        # LOAD THE MNE-COMPATIBLE RAW DATA-FILE(S)
        fname = mne_dir+'sourcedata/sub-{}/eeg/sub-{}-task-hyper_eeg.fif'.format(subject,subject)
        raw = mne.io.read_raw_fif(fname = fname, preload = False)
        # add additional information to the data-struct
        raw = add_info(raw)

        # SUBSET THE DATA-STRUCT
        sub2_raw = sub2(raw, subject)
        sub2_raw.info['subject_info']
        sub2_raw.info
        sub1_raw = sub1(raw, subject)
        sub1_raw.info['subject_info']
        sub1_raw.info

        # %%

        ######################################################
        # STEP 2: SAVE DATA IN BIDS-FORMAT
        ######################################################
        # help(make_bids_basename)
        # help(write_raw_bids)
        # automatize process for each sub_file
        for subset in ([sub1_raw, sub2_raw]):
            # DEBUG-Variables
            # subject = '203'
            # subset = sub1_raw
            # print(subset)

            # DEFINE BIDS-compatible parameters
            if subset.info['subject_info']['his_id'] == subject+'_sub2':
                player = '02'
            else:
                player = '01'
            subject_id = subject
            task = 'hyper'
            events, event_id = mne.events_from_annotations(subset)

            # CREATE the correct naming for the file (e.g. 'sub-202_ses-01_task-hyper')
            # Subject 1 and 2 are distinguished via the session argument (ses-01 = subject-01; ses-02 = subject-02),
            # since MNE-BIDS provides no hyperscanning compatible folder structure (afaik)
            bids_basename = make_bids_basename(subject = subject_id, session = player, task = task)

            # CREATE the files for each subject in accordance to BIDS-format
            write_raw_bids(subset, bids_basename, output_path = mne_dir+'rawdata/', event_id = event_id, events_data = events, overwrite = True)

            # dir = '/net/store/nbp/projects/hyperscanning/hyperscanning-2.0'
            # print_dir_tree(mne_dir)
            # help(write_raw_bids)
            # %%

################################################################
# STEP 3: LOAD DATASET TO WORK WITH AND CREATE PREPROCESSING DIR
################################################################

# SELECT a subject-pair
while True:
    try:
        subj_pair = input("Select subject-pair to work on (e.g. '202'): ")
        assert subj_pair in ['202','203','204','205','206','207','208','209','211','212']
        break
    except AssertionError:
        print("Subject-pair does not exist, try a different subject-pair.")

# SELECT a participant_nr
# and specify 'amp' variable --> needed to retrieve subject-specific information
while True:
    try:
        participant_nr = input("Select participant to work on (either '01' or '02'): ")
        assert participant_nr in ['01', '02']
    except AssertionError:
        print("You provided a wrong input! \nFor subject 1 type '01' \nFor subject 2 type '02'\n...")
    else:
        if participant_nr == '01':
            amp = 'Amp 2'
        else:
            amp = 'Amp 1'
        break

# SELECT the correct file based on user-input
bids_subname = make_bids_basename(subject = subj_pair, session = participant_nr, task = 'hyper')
my_eeg, _, _ = read_raw_bids(bids_fname = bids_subname + '_eeg.vhdr', bids_root = mne_dir+'rawdata/')
# Alternatively, load via read_raw_brainvision function
# path_to_eeg = mne_dir+'rawdata/sub-{}/ses-{}/eeg/'.format(subj_pair, participant_nr)
# mne.io.read_raw_brainvision(vhdr_fname = path_to_eeg + bids_subname + '_eeg.vhdr', preload = False)

# ADD subject information manually as I did not find a solution to save it via write_raw_bids()
# make sure to give an int() value into function
my_eeg.info['subject_info'] = subject_info(int(subj_pair), amp)
my_eeg.info['subject_info']
# %%


# temp_dict = subject_info(int(subj_pair), 'Amp 2')
# mne.io.meas_info._merge_info(my_eeg.info, temp_dict, verbose = None)
# help(mne.io.meas_info._merge_info)

# Give the sample rate
# sfreq = raw.info['sfreq']
# print('sample rate:', sfreq, 'Hz')
# eeg, times = raw[0, :int(sfreq * 2)]
# plt.plot(times, eeg.T)


################### TEST ######################
# Get some information about the eeg structure.
# display the dictionary of the raw_file
# print(sub2_raw.info)
# print(len(sub2_raw.ch_names))
# # pd.set_option('display.max_rows', 100)
# ch_list = pd.DataFrame({'channel_names':sub2_raw.ch_names})
# print(ch_list.to_string())
# '%s.fif' %(i)

# stim = raw.copy().load_data().pick_types(eeg=False, stim=True)
# stim.plot(start=750, duration=10)
# stim.info
