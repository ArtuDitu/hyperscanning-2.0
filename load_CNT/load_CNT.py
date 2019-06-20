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
import libeep
import numpy as np
import mne
import read_antcnt
# make sure "read_antcnt.py" is in your pythonpath
sys.path.append('/home/student/m/mtiessen/link_hyperscanning/hyperscanning-2.0/load_CNT/')
print(sys.path)
os.chdir('/net/store/nbp/projects/hyperscanning/hyperscanning-2.0/load_CNT/')
mne.sys_info()
#eeg = libeep.read_cnt('/home/student/m/mtiessen/link_hyperscanning/EEG_data/sub202/sub202.cnt')

raw = read_antcnt('')
raw.set_channel_types({ch:'misc' for ch in raw.ch_names if (ch.find('AUX')==0) | (ch.find('BIP')==0)})
raw.plot()
