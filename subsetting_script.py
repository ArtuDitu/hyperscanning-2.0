# -*- coding: utf-8 -*-

#### Split data into two structures ###

import os, sys
import mne
import numpy as np
import pandas as pd
from pybv import write_brainvision

# class Subset:
#
#     def __init__(self, raw):
#         self.raw = raw
#
#     def __repr__(self):
#         return (self.raw) # 'subset-{} successfully created!'.format(self.raw.info['subject_info'])
# @classmethod

# Returns a dict with subject-specific information (extracts from spreadsheet_subjects)
def subject_info(subject, amplifier):
    # DEBUG-Variables
    # subject = 203
    # amplifier = 'Amp 1'

    # READ in subject information
    info_csv = pd.read_csv('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/info_files/spreadsheet_subjects.csv', na_values = ['\\N'], skipinitialspace = True)
    # Code gender 'male' = 1 and 'female' = 2
    info_csv = info_csv.replace(to_replace = 'male', value = 1)
    info_csv = info_csv.replace(to_replace = 'female', value = 2)
    # Code handness 'right'= 1 and 'left'=2
    info_csv = info_csv.replace(to_replace = 'right', value = 1)
    info_csv = info_csv.replace(to_replace = 'left', value = 2)

    # Select only the row of interest
    current_sub = info_csv[info_csv['Which amplifier?'] == amplifier][info_csv['Experiment No.'] == subject]
    # Extract the values
    if amplifier == 'Amp 1':
        his_id = '%s_sub2' %(subject)
    else:
        his_id = '%s_sub1' %(subject)
    last_name = current_sub.iloc[0]['Name'].split(' ',maxsplit = 1)[-1]
    first_name = current_sub.iloc[0]['Name'].split(' ')[0]
    sex = current_sub.iloc[0]['gender']
    handness = current_sub.iloc[0]['handness']

    # Create the dictionary with the values
    subject_dict = dict(
                    {'id':subject,
                    'his_id':his_id,
                    'last_name':last_name,
                    'first_name':first_name,
                    'middle_name':None,
                    'birthday':None,
                    'sex':sex,
                    'hand':handness})

    return subject_dict

# channels 0-72 is generated from amplifier 1; thus it must be sub2
def sub2(raw, subject):
    # DEBUG-Variables
    # subject = 203
    # fname = '/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/mne_data/sub-{}/sub-{}|2/eeg/sub-{}|2_task-hyper_eeg.fif'.format(subject, subject, subject)
    # raw = mne.io.read_raw_fif(fname = fname, preload = False)

    # add subject-specific information to the info struct
    raw.info['subject_info'] = subject_info(int(subject), 'Amp 1')

    # CREATE temporary path to save file
    home = os.path.expanduser('~')
    mne_dir = os.path.join(home,'/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/mne_data/')
    path_to_sub2 = mne_dir+'temp_saving_subsets/sub2.fif'
    # select first half of electrodes
    eeg_indices = raw.info['ch_names'][0:72]
    # cut data in half by saving only selected channels
    raw.save(path_to_sub2, picks = eeg_indices, overwrite = True)
    # Reload file while preload=False (needed to further operate on file in main-script)
    raw_temp = mne.io.read_raw_fif(fname = path_to_sub2, preload = False)

    return raw_temp

# channels 73-144 are generated from amplifier 2; thus it must be sub1
# @classmethod
def sub1(raw, subject):
    # add subject-specific information to the info struct
    raw.info['subject_info'] = subject_info(int(subject), 'Amp 2')
    # select correct subset of channels and save channel names for renaming
    channel_names_new = raw.info['ch_names'][0:72]
    channel_names_old = raw.info['ch_names'][72:144]
    channel_mapping = dict(zip(channel_names_old,channel_names_new))
    # CREATE temporary path to save file
    home = os.path.expanduser('~')
    mne_dir = os.path.join(home,'/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/mne_data/')
    path_to_sub1 = mne_dir+'temp_saving_subsets/sub1.fif'
    # cut data in half by saving only selected channels
    raw.save(path_to_sub1, picks = channel_names_old, overwrite = True)
    # Reload file while preload=False (needed to further operate on file in main-script)
    raw_temp = mne.io.read_raw_fif(fname = path_to_sub1, preload = False)
    # Rename the channels
    raw_temp.rename_channels(channel_mapping)
    return raw_temp


    # TEST: writing and reading BrainVision file (this file format is widely used)
    # help(pybv.write_brainvision)
    # path_to_sub2 = mne_dir+'temp_saving_subsets/'
    # raw_data, _ = raw[:]
    # eeg_indices = raw.info['ch_names']
    # events, _ = mne.events_from_annotations(raw)
    # # deletes second column in events
    # events_formatted = np.delete(np.array(events),1,1)
    # pybv.write_brainvision(
    #             data = raw_data,
    #             sfreq = raw.info['sfreq'],
    #             ch_names = eeg_indices,
    #             fname_base = 'sub2',
    #             folder_out = path_to_sub2,
    #             events = events_formatted)
    #
    # print(mne.io.read_raw_brainvision.__doc__)
    # raw_bv = mne.io.read_raw_brainvision(vhdr_fname = path_to_sub2+'sub2.vhdr', preload = False)
    # annot = mne.read_annotations(path_to_sub2+'sub2.vmrk')
    # raw_bv.set_annotations(annot)
    # raw_bv.annotations
