# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 10:55:54 2018

@author: Rijk
"""

# =============================================================================
# ## Import libraries
# =============================================================================
import visa
import time
import numpy as np
import matplotlib.pyplot as plt
import sys

import sweep_functions as sweep
import vna_functions as vna

# =============================================================================
# Code
# =============================================================================

PNA, rm = sweep.init()

vna.reset(PNA)
PNA.close()
rm.close()
print('MESSAGE: VNA reset and session closed')