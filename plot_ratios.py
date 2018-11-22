# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 10:23:34 2018

@author: Rijk

Data analysis of BK7 measurement data

For now requires 
- all data to have the same number of points and range
- to be in the same folder as the.csv files
"""
# Import libraries

import numpy as np
import matplotlib.pyplot as plt
import data_analysis as dat
import os
import pickle as pkl
#%% Parameters

delimiter       = ','

f_unit          = 'Hz'
s_unit          = 'dB'

f               = 'f'
s_param         = ['S21']

IF_bandwidth    = 200 # Hz
amplitude       = -40 # dBm

fs_min          = 4e9
fs_max          = 6e9


original_path       = r'C:\Users\Rijk\Documents\NAOJ Engineering\Vector Network Analyzer\Data_git\181122 df0 test'
#original_path       = ''
original_file_name  = 'VNAdata_S21_181122_122351'

comparison_path     = r'C:\Users\Rijk\Documents\NAOJ Engineering\Vector Network Analyzer\Data_git\181122 df0 test'
#comparison_path      = ''
comparison_file_name = 'VNAdata_S21_181122_120933'

ratio_path          = r'C:\Users\Rijk\Documents\NAOJ Engineering\Vector Network Analyzer\Data_git\181122 df0 test'

#%% Import data

original_file       = os.path.join(original_path, original_file_name)
original_data       = dat.load_data(original_file)

comparison_file     = os.path.join(comparison_path, comparison_file_name)
comparison_data     = dat.load_data(comparison_file)

name_original       = input('Give name for orignal file\n')
name_comparison     = input('Give name for comparison file\n')

mag_ratio_name  = 'ratio_%s_and_%s' %(name_original, name_comparison)
mag_ratio_file  = os.path.join(ratio_path, mag_ratio_name)

fs                  = dat.get_fs(original_file)

# Getting parameters from data
f_start             = np.min(fs)
f_stop              = np.max(fs)
num_points          = len(fs)

#%% Calculate ratios

# Magnitude ratio
original_data_mag   = dat.convert_mag(original_data)
comparison_data_mag = dat.convert_mag(comparison_data)

mag_ratio     = original_data_mag / comparison_data_mag

# Saving complex ratio

dat.save_data(mag_ratio, fs, mag_ratio_file)

#%% Plot results

plt.close('all')

#%% Plot magnitude ratio

fig = plt.figure()
ax = fig.gca()

#for i in range(len(original_data[:,0])):
#    plt.plot(fs, original_data)

plt.plot(fs, mag_ratio[0])

# Format the figures
plt.axis([np.min(fs), np.max(fs), dat.floor(np.min(mag_ratio), 1), dat.ceil(np.max(mag_ratio), 1) ])
#plt.xlim(fs_min, fs_max)
plt.ylim(0.8, 1.2)

plt.grid(True)
ax.xaxis.grid(which='minor')
#ax1.yaxis.grid(which='minor')

plt.title('Magnitude ratio between %s and %s \n%s num points, %s Hz IF bandwidth and %s dBm amplitude' % (name_original, name_comparison, num_points, IF_bandwidth, amplitude))
plt.legend(s_param)
plt.xlabel('Frequency (%s)' % (f_unit))

# Maximizes window size
#manager = plt.get_current_fig_manager()
#manager.window.showMaximized()

#%% Save plot magnitude ratio

# Both as pickle figure and as svg image
with open(mag_ratio_file + '.pkl', 'wb') as fid:
    pkl.dump(fig, fid)

plt.savefig(mag_ratio_file + '.svg')


# Make text file for future reference
f   = open(mag_ratio_file + '.txt', 'w+')

f.write('Figure \"%s\" is ratio between \n' % (mag_ratio_name))
f.write('- %s\n' %(original_file_name))
f.write('- %s\n' %(comparison_file_name))

f.write('\n' + input('Comments?\n'))

f.close()

