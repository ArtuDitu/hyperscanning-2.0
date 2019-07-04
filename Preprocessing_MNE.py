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
import pybv
# set current working directory
os.chdir('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/mne_data/sourcedata')
# make directory to save the data in BIDS-format
home = os.path.expanduser('~')
mne_dir = os.path.join(home,'/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/mne_data/')

# %%

# ADDING ADDITIONAL INFORMATION TO THE .INFO-DICT OF THE EEG-FILE
# I.e., adding the events from the STIM-channel and creating annotations that
# will be visible in the raw data (as color-coded triggers with event description)
def add_info(raw):
    # CREATE EVENTS
    events = mne.find_events(raw, stim_channel = 'STI 014')
    # raw.info['events'] = events

    # CREATE ANNOTATIONS FROM EVENTS: To visualize the events + event-description in the data
    # Read in trigger description txt-file and create mapping dict (e.g. trigger 49 = Trial end)
    mapping = dict()
    with open('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/info_files/triggers_events_markers.txt', mode = 'r', encoding = 'utf-8-sig') as file:
        #print(file.read())
        for line in file:
            temp = line.strip().split('. ')
            mapping.update({int(temp[0]) : temp[1]})

    # for each trigger-key, map the corresponding trigger definition
    descriptions = np.asarray([mapping[event_id] for event_id in events[:, 2]])
    # add annotations to eeg-struct
    srate = raw.info['sfreq']
    onsets = events[:,0] / srate
    durations = np.zeros_like(onsets) # assuming instantaneous events
    # mne.Annotations input:
    # 1. supply the onset timestamps of each event (in sec.)
    # 2. the duration of event (set to 0sec.)
    # 3. the event description
    # 4. the onset of first sample
    annot = mne.Annotations(onsets, durations, descriptions, orig_time = None)
    raw.set_annotations(annot)
    # raw.plot(start = 1103, duration = 3)
    return raw

# %%
# # TEST: Try to save and reload the data-subsets bc in order to use 'write_raw_bids',
# # the data must not be loaded, i.e. preload = False
# def save_and_reload(sub_raw):
#     if not os.path.exists(mne_dir+'temp_saving_subsets'):
#         os.makedirs(mne_dir+'temp_saving_subsets')
#     id = sub_raw.info['subject_info']
#     path_to_temp = mne_dir+'temp_saving_subsets/{:s}.fif'.format(id)
#     sub_raw.save(path_to_temp, overwrite=True)
#     # TEST: Load sub_raw from "mne_dir+'temp_saving_subsets'" with preload = False
#     sub_raw = mne.io.read_raw_fif(fname = path_to_temp, preload = False)
#     return sub_raw


if __name__=='__main__':
    #############################################
    # STEP ONE: Load data, split into two structs
    #############################################

    # visualize data structure of raw files
    # print_dir_tree('/home/student/m/mtiessen/link_hyperscanning/hyperscanning-2.0/mne_data')

    # do for each subject
    for subject in ['203']:
        # LOAD THE MNE-COMPATIBLE DATA-FILES
        fname = mne_dir+'sourcedata/sub-{}/eeg/sub-{}-task-hyper_eeg.fif'.format(subject,subject)
        raw = mne.io.read_raw_fif(fname = fname, preload = False)
        # add additional information to the data-struct
        raw = add_info(raw)

        # SUBSET THE DATA-STRUCT
        sub2_raw = subsetting_script.sub2(raw, subject)
        sub2_raw.info['subject_info']
        sub2_raw.info
        sub1_raw = subsetting_script.sub1(raw, subject)
        sub1_raw.info['subject_info']
        sub1_raw.info
        # %%


        ######################################################
        # STEP 2: SAVE DATA IN BIDS-FORMAT
        ######################################################
        help(make_bids_basename)
        help(write_raw_bids)
        # automatize process for each sub_file
        for subset in ([sub1_raw, sub2_raw]):
            # DEBUG-Variables
            # subject = '203'
            # subset = sub1_raw
            # print(subset)

            # CREATE subdirectory for each subject-pair
            mne_subdir = mne_dir+'sub-{}/'.format(subject)
            if not os.path.exists(mne_subdir):
                os.makedirs(mne_subdir)

            # DEFINE BIDS-compatible parameters
            # if subset.info['subject_id'] == 'sub2':
            #     subject_id = subject+'|2'
            # else:
            #     subject_id = subject+'|1'
            subject_id = subject+'|1'
            task = 'hyper'
            raw_file = subset
            # output_path = os.path.join(mne_subdir, 'sub-{}'.format(subject_id))
            events, event_id = mne.events_from_annotations(subset)
            bids_basename = make_bids_basename(subject = subject_id, task = task)

            # CREATE the files for each subject in accordance to BIDS-format
            write_raw_bids(raw_file, bids_basename, output_path = mne_subdir, event_id = event_id, events_data = events, overwrite = True)
            print_dir_tree(mne_subdir)

subset.info
    sub2_raw.info
    print(make_bids_basename.__doc__)
help(mne.events_from_annotations)

test = raw.info['ch_names'][0:72]


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
