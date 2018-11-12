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

#%% ===========================================================================
# #Setup measurement
# =============================================================================

PNA, rm = sweep.init()

sweep.standard_sweep(PNA)

#%% ===========================================================================
# Test code
# =============================================================================

data    = vna.get_meas_data(PNA, 'meas_S11')

channel_num = 1
meas_name   = 'meas_S11'

num_points = vna.get_num_points(PNA)
meas_names = vna.get_meas_names(PNA)

command = ':CALCulate%d:PARameter:SELect "%s"' % (channel_num, meas_name)
PNA.write(command)

data2   = PNA.query_ascii_values(':CALCulate:DATA? %s' % ('SDATA'))

#%% Plotting

plt.plot(data[0])


#plt.figure()
plt.plot(data[1])
plt.title('Complex measurement data')
plt.legend(['Real part', 'Imaginary part'])

#%% ===========================================================================
# Reset VNA
# =============================================================================

## Wipe the settings and terminate the session
PNA.close()
rm.close()
