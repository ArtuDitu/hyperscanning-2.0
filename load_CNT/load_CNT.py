# -*- coding: utf-8 -*-

############ Load the raw EEG .cnt files and convert to Python_MNE compatible format ##############
# Credits: Benedikt Ehinger
"""
Created on June 19, 2019
# @author: mtiessen
# Mail: mtiessen@uos.de
"""

# Since code was written in Python 2.x, use Python 2 kernel to run the code
# with virtual environment "load_cnt"

import os, sys
# make sure "read_antcnt.py" is in your pythonpath
sys.path.append('/home/student/m/mtiessen/link_hyperscanning/hyperscanning-2.0/load_CNT/')
# print(sys.path)
import libeep
import numpy as np
import mne
import read_antcnt
from matplotlib import pyplot as plt

# set current working directory
os.chdir('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/')
# mne.sys_info()

# eeglab_montage = '/net/home/student/m/mtiessen/link_hyperscanning/M_tools/eeglab14_1_2b/plugins/dipfit2.3/standard_BESA/standard-10-5-cap385.elp'
# mne_montage = mne.channels.read_montage(kind = 'standard_1005') #path = '~/.virtualenvs/hyper-2.0_env/lib/python3.5/site-packages/mne/channels/data/montages'

# load the .cnt data with read_antcnt.py script
raw = read_antcnt.read_raw_antcnt('/home/student/m/mtiessen/link_hyperscanning/EEG_data/sub203/sub203.cnt')
# apply specific NBP channel settings
raw.set_channel_types({ch:'misc' for ch in raw.ch_names if (ch.find('AUX')==0) | (ch.find('BIP')==0)})
# save mne data in .fif format
raw.save('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/load_CNT/fif_files/sub203.fif', overwrite=False)
