# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 11:23:39 2018

@author: Rijk

Script to make plots and save them from stored data

"""

# Import libraries

import numpy as np
import matplotlib.pyplot as plt
import data_analysis as dat
import sweep_functions as sweep
import os

#%% Parameters


delimiter       = ','

f_unit          = 'Hz'
s_unit          = 'dB'

f               = 'f'
s_param         = ['S21']

IF_bandwidth    = 200   # Hz
amplitude       = -77   # dBm

limit_f         = 0
fs_min          = 4e9
fs_max          = 6e9


file_path       = r'C:\Users\Rijk\Documents\NAOJ Engineering\Vector Network Analyzer\Data_git\Data Third Light 181112'
file_name       = 'VNAdata4K_S21_181112_161347'

full_file_name  = os.path.join(file_path, file_name)

# Import data

original_data       = dat.load_complex_data(full_file_name)


#%% Get stuff from data

fs                  = dat.get_fs(full_file_name)

# Getting parameters from data
f_start             = np.min(fs)
f_stop              = np.max(fs)
num_points          = len(fs)

#%% Calculate ratios

original_data   = dat.convert_mag(original_data)

#%% Plot results

plt.close('all')


#%% Original transmission

fig1 = plt.figure()
ax1 = fig1.gca()


plt.plot(fs, original_data[0])

# Format the figures
plt.axis([np.min(fs), np.max(fs), np.floor(np.min(original_data)), np.ceil(np.max(original_data)) ])
#plt.axis([fs_min, fs_max, np.floor(np.min(original_data)), np.ceil(np.max(original_data)) ])

plt.grid(True)
ax1.xaxis.grid(which='minor')
#ax1.yaxis.grid(which='minor')

plt.title('Transmission \n%s num points, %s Hz IF bandwidth and %s dBm amplitude' % (num_points, IF_bandwidth, amplitude))
plt.legend(s_param)
plt.xlabel('Frequency (%s)' % (f_unit))
plt.ylabel('Magnitude (%s)' % ('dB'))

## Save original transmission

plt.savefig(full_file_name + '.svg')  