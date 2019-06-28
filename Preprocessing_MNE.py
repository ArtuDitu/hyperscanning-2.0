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
from mne_bids import write_raw_bids, make_bids_basename
from mne.datasets import sample
from mne_bids.utils import print_dir_tree
os.chdir('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0')
import subsetting_script


#############################################
# STEP ONE: Load data, split into two structs
#############################################
# set current working directory
os.chdir('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/mne_data/sourcedata')

# make directory to save the data in BIDS-format
home = os.path.expanduser('~')
mne_dir = os.path.join(home,'/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/mne_data')

# visualize data structure of raw files
print_dir_tree('/home/student/m/mtiessen/link_hyperscanning/hyperscanning-2.0/mne_data')

# help(mne.io.read_raw_fif)
for i in ['203']:
    # Load the mne compatible data-files
    raw = mne.io.read_raw_fif(fname = mne_dir+'/sourcedata/sub-{}/eeg/sub-{}-task-hyper_eeg.fif'.format(i,i), preload = False)

# SUBSET THE DATA-STRUCT
sub2_raw = subsetting_script.sub2(raw)
sub2_raw.info['ch_names']
sub1_raw = subsetting_script.sub1(raw)
sub1_raw.info['ch_names']
sub1_raw.info['subject_info']


    ######################################################
    # STEP 2: ADD INFORMATION AND SAVE DATA IN BIDS-FORMAT
    ######################################################
    for subset in ([sub2_raw, sub1_raw]):
        print(subset)
        # include the bids-params here to automatize process for each sub_file

sub2_raw.info
print(make_bids_basename.__doc__)
# Create Events ###########################
# stim = raw.copy().load_data().pick_types(eeg=False, stim=True)
# stim.plot(start=750, duration=10)
# stim.info
events = mne.find_events(raw, stim_channel = 'STI 014')
raw.info['events'] = events

# create Annotations ######################
srate = raw.info['sfreq']
# Read in trigger description txt-file and create mapping dict
mapping = dict()
with open('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/triggers_events_markers.txt', mode = 'r', encoding = 'utf-8-sig') as file:
    # print(file.read())
    for line in file:
        temp = line.strip().split('. ')
        mapping.update({int(temp[0]) : temp[1]})
# include the annotations into the raw structure
descriptions = [mapping[event_id] for event_id in events[:, 2]]
annot = mne.Annotations(0, len(raw)/srate, mapping)
raw.set_annotations(annot)


# TEST-Variables
i = '203'
subset = sub2_raw
# DEFINE BIDS-COMPATIBLE PARAMETERS
subject_id = i
task = 'hyper'
raw_file = subset
output_path = os.path.join(mne_dir, '/sub%s' %(i))
# trial_type = {}

bids_basename = make_bids_basename(subject = subject_id, task = task)
write_raw_bids(raw_file, bids_basename, output_path = output_path, overwrite = True)
print_dir_tree(output_path)

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
