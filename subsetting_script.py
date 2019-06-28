# -*- coding: utf-8 -*-

#### Split data into two structures ###

import os, sys
import mne
import numpy as np
import pandas as pd

# class Subset:
#
#     def __init__(self, raw):
#         self.raw = raw
#
#     def __repr__(self):
#         return (self.raw) # 'subset-{} successfully created!'.format(self.raw.info['subject_info'])

# channels 0-72 is generated from amplifier 1; thus it must be sub2
# @classmethod
def sub2(raw):
    raw.info['subject_info'] = 'sub2'
    # select correct subset of channels
    channel_indices = list(np.arange(0,72, 1))
    raw_temp = raw.copy().load_data().pick(picks=channel_indices)
    return raw_temp

# channels 72-144 are generated from amplifier 2; thus it must be sub1
# @classmethod
def sub1(raw):
    raw.info['subject_info'] = 'sub1'
    # save channel names for renaming
    channel_names_new = raw.info['ch_names'][0:72]
    channel_names_old = raw.info['ch_names'][72:144]
    channel_mapping = dict(zip(channel_names_old,channel_names_new))
    # select correct subset of channels
    channel_indices = list(np.arange(72,144, 1))
    raw_temp = raw.copy().load_data().pick(picks=channel_indices)
    raw_temp.rename_channels(channel_mapping)
    return raw_temp
