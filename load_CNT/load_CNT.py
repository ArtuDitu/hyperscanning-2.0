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
import libeep
import numpy as np
import read_antcnt
