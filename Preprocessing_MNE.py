# -*- coding: utf-8 -*-

#######################
# Author: Max Tiessen
# Mail: mtiessen@uos.de
# Date: June 2019
#######################

import pandas as pd
import numpy as np
import mne
# from mne import io
from mne_bids import write_raw_bids
from mne.datasets import sample

write_raw_bids(raw, 'sub-01_ses-01_run-05', output_path='./bids_dataset')
