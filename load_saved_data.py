# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 15:33:57 2018

@author: Rijk
"""
# Goal:
# Load stored data and plot it



import numpy as np
import matplotlib.pyplot as plt
import os
import data_analysis as dat

## Parameters

file_path = r'C:\Users\Rijk\Documents\NAOJ Engineering\Vector Network Analyzer\Data_git\181120 Final measurements\Temperature sweep above Tc'
file_name = 'VNAdata_S21_181120_130318'

#file = file_path + file_name

file = os.path.join(file_path, file_name) 
delimiter = ','

f_unit = 'MHz'
s_unit = 'dB'

f       = 'f'
#s_param = ['S21', 'S11', 'S22']
s_param = ['S21']
IF_bandwidth = 200 # Hz

#%% Code

#IF_bandwidth    = input('What was the IF bandwidth for this data? (Hz)\n')
# Make these redundant by adding them to the saved data


data    = dat.load_data(file)

fs      = dat.get_fs(file)

f_start = np.min(fs)
f_stop  = np.max(fs)
num_points  = len(data[0])


##%% Changing the data and storing it again
#
#saved_data = '' 
#
#data_name = 'test' + '.csv'
#np.savetxt(data_name, saved_data, delimiter=',')


#%% Plotting

plt.plot(fs, data[0])

# Format the figures
#plt.axis([min(fs), max(fs), -10, -5]) # Sets origin in upper-left corner
#plt.axis([min(fs), max(fs), -40, 0]) # Sets origin in upper-left corner
plt.grid(True)

plt.title('Frequency between %s and %s %s for %s num points and %s Hz IF bandwidth' % (f_start, f_stop, f_unit, num_points, IF_bandwidth))
plt.legend(s_param)
plt.xlabel('Frequency (%s)' % (f_unit))
plt.ylabel('Magnitude (%s)' % ('dB'))