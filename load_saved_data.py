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

## Parameters

file_name = 'VNAdataS21S11S22_with_laser.csv'
file_path = r'C:\Users\Rijk\Documents\NAOJ Engineering\Vector Network Analyzer\Data for Delft 181010'
#file = file_path + file_name

file = os.path.join(file_path, file_name) 
delimiter = ','

f_unit = 'MHz'
s_unit = 'dB'

f       = 'f'
s_param = ['S21', 'S11', 'S22']

## Code

IF_bandwidth    = input('What was the IF bandwidth for this data? (Hz)\n')
# Make these redundant by adding them to the saved data

for s in s_param:
    names = [f, s]

units = [f_unit, s_unit]

saved_data = np.loadtxt(file, delimiter=delimiter)

fs = saved_data[0,:]
data = saved_data[1:,:]

f_start = np.min(fs)
f_stop  = np.max(fs)
num_points  = len(data[0])


## Changing the data and storing it again
#saving_data = np.ones((len(saved_data[:,0]), len(saved_data[0,:])+2))
#saving_data[:,0] = names
#saving_data[:,1] = units
#saving_data[:,1:] = saved_data
    
#data_name = 'test' + '.csv'
#np.savetxt(data_name, saving_data, delimiter=',')


## Plotting

plt.figure(3)
for i in range(len(data[:,0])):
    plt.plot(fs, data[i])

# Format the figures
plt.axis([min(fs), max(fs), -40, 0]) # Sets origin in upper-left corner
plt.grid(True)

plt.title('Frequency between %s and %s %s for %s num points and %s Hz IF bandwidth' % (f_start, f_stop, f_unit, num_points, IF_bandwidth))
plt.legend(s_param)
plt.xlabel('Frequency (%s)' % (f_unit))
plt.ylabel('Magnitude (%s)' % ('dB'))