# -*- coding: utf-8 -*-

#### Split data into two structures ###

import os, sys
import mne
import numpy as np
import pandas as pd

# subset1 is generated from amplifier 1; thus it must be sub2
def subset1(raw):
    raw.get_data(picks = [0:71])
