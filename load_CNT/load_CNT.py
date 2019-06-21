# -*- coding: utf-8 -*-

############ Load the raw EEG .cnt files and convert to Python_MNE compatible format ##############
# Credits:
# Benedikt Ehinger
"""
Created on June 19, 2019
# @author: mtiessen
# Mail: mtiessen@uos.de
"""

# Since code was written in Python 2.x, use Python 2 kernel to run the code
import os, sys
sys.path.append('/home/student/m/mtiessen/link_hyperscanning/hyperscanning-2.0/load_CNT/')
print(sys.path)

import libeep
import numpy as np
import mne
import read_antcnt
# make sure "read_antcnt.py" is in your pythonpath

os.chdir('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/load_CNT/')
mne.sys_info()
#eeg = libeep.read_cnt('/home/student/m/mtiessen/link_hyperscanning/EEG_data/sub202/sub202.cnt')
# eeglab_montage = '/net/home/student/m/mtiessen/link_hyperscanning/M_tools/eeglab14_1_2b/plugins/dipfit2.3/standard_BESA/standard-10-5-cap385.elp'
# mne_montage = mne.channels.read_montage(kind = 'standard_1005') #path = '~/.virtualenvs/hyper-2.0_env/lib/python3.5/site-packages/mne/channels/data/montages'
raw = os.system('python read_antcnt.py /home/student/m/mtiessen/link_hyperscanning/EEG_data/sub203/sub203.cnt')
raw = read_antcnt.read_raw_antcnt('/home/student/m/mtiessen/link_hyperscanning/EEG_data/sub203/sub203.cnt')
raw.set_channel_types({ch:'misc' for ch in raw.ch_names if (ch.find('AUX')==0) | (ch.find('BIP')==0)})

raw.plot()
