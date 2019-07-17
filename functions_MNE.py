# -*- coding: utf-8 -*-

"""
Created on July 16, 2019
# @author: mtiessen
# Mail: mtiessen@uos.de
"""

import os, sys
import mne
import numpy as np
import pandas as pd
import pybv
from mne_bids import write_raw_bids, make_bids_basename, read_raw_bids


# ADDING ADDITIONAL INFORMATION TO THE .INFO-DICT OF THE EEG-FILE
# I.e., adding the events from the STIM-channel and creating annotations that
# will be visible in the raw data (as color-coded triggers with event description)
def add_info(raw):
    # CREATE EVENTS
    # print(mne.find_events.__doc__)
    try:
        events = mne.find_events(raw, stim_channel = 'STI 014')
    except ValueError as err:
        print("ValueError: {}".format(err))
        print("--> trying to decrease length of 'shortest_event' from default(2) to 1 sample.")
        events = mne.find_events(raw, stim_channel = 'STI 014', shortest_event = 1)
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


# Returns a dict with subject-specific information (extracts from spreadsheet_subjects)
# ATTENTION: Make sure to give 'subject'-variable in integer-format,
# as it needs to be matched by an integer in the csv-file
def subject_info(subject, amplifier):
    # DEBUG-Variables
    # subject = 202
    # amplifier = 'Amp 1'

    # Check first if 'subject' is of type int, if false, throw exception & fix
    try:
        assert isinstance(subject, int)
    except AssertionError:
        print("First input variable is not an integer!\n--> Converting to integer...")
        subject = int(subject)
        print('\nDone.')

    # READ in subject information
    info_csv = pd.read_csv('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/info_files/spreadsheet_subjects.csv', na_values = ['\\N'], skipinitialspace = True)
    # Code gender 'male' = 1 and 'female' = 2
    info_csv = info_csv.replace(to_replace = 'male', value = 1)
    info_csv = info_csv.replace(to_replace = 'female', value = 2)
    # Code handness 'right'= 1 and 'left'=2
    info_csv = info_csv.replace(to_replace = 'right', value = 1)
    info_csv = info_csv.replace(to_replace = 'left', value = 2)
    # Handle missing data
    # %%time
    for i in range(0, len(info_csv)-1):
        # for each NaN-value in the amplifier column
        while pd.isna(info_csv.iloc[i]['Which amplifier?']):
            # replace the NaN value with respective 'Amplifier'
            if info_csv.iloc[i]['Screen Nr.'] == 1:
                info_csv.loc[i, 'Which amplifier?'] = 'Amp 2'
                break
            elif info_csv.iloc[i]['Screen Nr.'] == 2:
                info_csv.loc[i, 'Which amplifier?'] = 'Amp 1'
                break
            else:
                break

    # Select only the row of interest
    current_sub = info_csv[(info_csv['Which amplifier?'] == amplifier) & (info_csv['Experiment No.'] == subject)]
    # Extract the values
    if amplifier == 'Amp 1':
        his_id = '%s_sub2' %(subject)
    else:
        his_id = '%s_sub1' %(subject)

    last_name = current_sub.iloc[0]['Name'].split(' ',maxsplit = 1)[-1]
    first_name = current_sub.iloc[0]['Name'].split(' ',maxsplit = 1)[0]
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
