"""
Rijk Hogenbirk, started on 24/09/18

Description:
Script to let the VNA perform a measurement of S-parameters with a variable frequency and a set amplitude.

Allowed input values for Agilent PNA E8361C:

f_start, f_stop:    Between 10 MHz and 67 MHz
IF_bandwith:        1, 2, 3, 5, 7, 10, 15, 20, 30, 50, 70, 100, 150, 200, 300, 500, 
                    700, 1k, 1.5k, 2k, 3k, 5k, 7k, 10k, 15k, 20k, 30k, 35k, 40k
num_points:         Between 1 and 32001

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
# %%
# ## Input parameters
# =============================================================================

file_name       = 'calibration_11_7K'

#f_start         = 100      # MHz
#f_stop          = 10000    # MHz
f_start         = 4000      # MHz
f_stop          = 6000    # MHz

num_points      = 8001
IF_bandwidth    = 200    # Hz

amplitude       = -50     # dBm

#s_param         = ['S11']  # List of strings
#s_param         = ['S21']
s_param         = ['S21', 'S11', 'S22']
#s_param         = ['S21', 'S11']

error_correction = 1

#%%
### Code

PNA, rm         = sweep.init()

#%%
meas_names      = sweep.setup(PNA, f_start, f_stop, num_points, IF_bandwidth, amplitude, s_param)

#%% Autoscale
vna.autoscale(PNA, 1)

#%%
data, elapsed   = sweep.get_data(PNA, error_correction=1)


#%%
sweep.save_data(PNA, file_name, data, s_param)

#%%
sweep.plot_data(data, s_param, num_points, IF_bandwidth, only_S21=0)
#sweep.plot_data(data, s_param, num_points, IF_bandwidth, only_S21=1)

#%%
sweep.close(PNA, rm)



