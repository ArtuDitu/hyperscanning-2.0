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
os.chdir('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/load_CNT/fif_files/')

# make directory to save the data in BIDS-format
home = os.path.expanduser('~')
mne_dir = os.path.join(home,'/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/mne_data')
if not os.path.exists(mne_dir):
    os.makedirs(mne_dir)

# visualize data structure of raw files
print_dir_tree('/home/student/m/mtiessen/link_hyperscanning/hyperscanning-2.0/load_CNT/fif_files')

# help(mne.io.read_raw_fif)
for i in ['203']:
    # Load the mne compatible data-files
    raw = mne.io.read_raw_fif(fname = 'sub{}.fif'.format(i), preload = False)

# SUBSET THE DATA-STRUCT
sub2_raw = subsetting_script.sub2(raw)
sub2_raw.info['ch_names']
sub1_raw = subsetting_script.sub1(raw)
sub1_raw.info['ch_names']
sub1_raw.info['subject_info']







# Get some information about the eeg structure.
# display the dictionary of the raw_file
print(raw.info)
print(len(raw.ch_names))
# pd.set_option('display.max_rows', 100)
ch_list = pd.DataFrame({'channel_names':raw.ch_names})
print(ch_list.to_string())

###################### TEST: save specific data ###############################
raw.info
raw.save(fname='sub{name:d}_2.fif'.format(name=203), picks=channel_names)
raw_subset = mne.io.read_raw_fif('sub{name:d}_2.fif'.format(name=index), preload = False)
raw_subset.info

# sub2_data = raw.get_data(picks=channel_names) # extracts np.array which is not what i want
# sub2_data.shape

# channel_indices1 = np.arange(72,144, 1)
# channel_indices2 = np.arange(0,72, 1)
# zippy = dict(zip(channel_indices1,channel_indices2))
# channel_indices.shape










print(make_bids_basename.__doc__)
i = '203'
# define BIDS-compatible parameters
subject_id = i
task = 'blind'
raw_file = raw
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


'%s.fif' %(i)
