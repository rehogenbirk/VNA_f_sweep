# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 16:04:35 2018

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
# #Setup measurement
# =============================================================================

PNA, rm = sweep.init()

sweep.standard_sweep(PNA)

# =============================================================================
# Test code
# =============================================================================

meas_names = vna.get_meas_names(PNA)

# =============================================================================
# Reset VNA
# =============================================================================

## Wipe the settings and terminate the session
PNA.close()
rm.close()
