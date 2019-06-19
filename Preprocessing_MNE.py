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
from mne_bids import write_raw_bids
from mne.datasets import sample


#############################################
# STEP ONE: Load data, split into two structs
#############################################
# set current working directory
os.chdir('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0')

eeglab_montage = '/net/home/student/m/mtiessen/link_hyperscanning/M_tools/eeglab14_1_2b/plugins/dipfit2.3/standard_BESA/standard-10-5-cap385.elp'
mne_montage = mne.channels.read_montage(kind = 'standard_1005') #path = '~/.virtualenvs/hyper-2.0_env/lib/python3.5/site-packages/mne/channels/data/montages'

raw = mne.io.read_raw_cnt(input_fname = sample, montage = mne_montage) # '/home/student/m/mtiessen/link_hyperscanning/EEG_data/sub202/sub202.cnt'
write_raw_bids(raw, 'sub-01_ses-01_run-05', output_path='./bids_dataset')
