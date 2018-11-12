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

T               = 3.8

file_name       = 'VNAdata_%sK' % (T)

#
#f_start         = 100       # MHz
#f_stop          = 67000     # MHz
f_start         = 4000      # MHz
f_stop          = 6000      # MHz

num_points      = 16001
IF_bandwidth    = 200    # Hz

amplitude       = -50    # dBm

#s_param         = ['S11']  # List of strings
s_param         = ['S21']
#s_param         = ['S21', 'S11', 'S22']
#s_param         = ['S21', 'S11']

error_correction = 1

#%% Code

PNA, rm         = sweep.init()

sweep.reset(PNA)

#%%
meas_names      = sweep.setup(PNA, f_start, f_stop, num_points, IF_bandwidth, amplitude, s_param)

#%% Autoscale
vna.autoscale(PNA, 1)

print('MESSAGE: Autoscale succesful')

#%%
data, elapsed   = sweep.get_data(PNA, error_correction=1)

#%%
full_file_name       = sweep.save_data(PNA, file_name, data, s_param)

sweep.save_parameters(full_file_name, T, f_start, f_stop, num_points, IF_bandwidth, amplitude)

#%%
#sweep.plot_sdata(data, s_param, IF_bandwidth, only_S21=0)

sweep.plot_sdata_mag(data, s_param, IF_bandwidth, amplitude, only_S21=0)

plt.savefig(full_file_name + '.svg')
print('MESSAGE: Plot saved')

#%%
sweep.close(PNA, rm)



