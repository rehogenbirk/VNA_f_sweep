# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 13:07:23 2018

@author: Rijk

Plotting calibration data and original data after calibration
"""

# Import libraries

import numpy as np
import matplotlib.pyplot as plt
import data_analysis as dat

#%% Parameters

delimiter       = ','

f_unit          = 'Hz'
s_unit          = 'dB'

f               = 'f'
s_param         = ['S21']
IF_bandwidth    = 200 # Hz

limit_f         = 0
fs_min          = 4.5e9
fs_max          = 5.75e9

#%% Import data

original_name           = 'VNAdataBK7_S21_181022_4to6GHz'
calibration_08k_name    = 'calibration_8_0K_S21_181019_4to6GHz'
calibration_10k_name    = 'calibration_10_0K_S21_181019_4to6GHz'
calibration_12k_name    = 'Calibration_11_7K_S21_181024_4to6GHz'

original_data       = dat.load_data(original_name)
cal_08k_data        = dat.load_data(calibration_08k_name)
cal_10k_data        = dat.load_data(calibration_10k_name)
cal_12k_data        = dat.load_data(calibration_12k_name)

fs                  = dat.get_fs(original_name)

# Getting parameters from data
f_start         = np.min(fs)
f_stop          = np.max(fs)
num_points      = len(fs)

#%% Data processing

og_08k  = original_data - cal_08k_data
og_10k  = original_data - cal_10k_data
og_12k  = original_data - cal_12k_data

#%% Plotting

plt.close('all')

#%% Plotting original data and calibrations

## Input
xs      = fs
ys      = original_data

ys1     = cal_08k_data
ys2     = cal_10k_data
ys3     = cal_12k_data

xlabel  = 'Frequency (%s)' % (f_unit)
ylabel  = 'Magnitude (%s)' % (s_unit)
title   = 'Transmission (S21) and calibration at different temperatures'
legend  = ['Original', '08K', '10K', '12K']

## Plotting
# Creating new figure and getting axis
figure  = plt.figure()
axis    = figure.gca()


# Plot either one or more graphs, depending on how many are in the data
#for i in range(len(data[:,0])):
#    plt.plot(fs, data)
plt.plot(xs, ys)
plt.plot(xs, ys1)
plt.plot(xs, ys2)
plt.plot(xs, ys3)

## Format the figures

# Sets origin in upper-left corner
plt.axis([min(xs), max(xs), -15, -5]) 

# Turns on grid
plt.grid(True)
#axis.xaxis.grid(which='minor')
#axis.yaxis.grid(which='minor')

# Sets labels, legend and title
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.legend(legend)
plt.title(title)

#%% Plotting calibration data individually

## Input
xs      = fs
ys      = original_data

xlabel  = 'Frequency (%s)' % (f_unit)
ylabel  = 'Magnitude (%s)' % (s_unit)
title   = 'Transmission (S21)'
legend  = ['S21']

## Plotting
# Creating new figure and getting axis
figure  = plt.figure()
axis    = figure.gca()


# Plot either one or more graphs, depending on how many are in the data
#for i in range(len(data[:,0])):
#    plt.plot(fs, data)
plt.plot(xs, ys)

## Format the figures

# Sets origin in upper-left corner
#plt.axis([min(xs), max(xs), min(ys), max(ys)])
plt.xlim([min(xs), max(xs)])
#plt.ylim([min(ys), max(ys)]) 

# Turns on grid
plt.grid(True)
#axis.xaxis.grid(which='minor')
#axis.yaxis.grid(which='minor')

# Sets labels, legend and title
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.legend(legend)
plt.title(title)

#%% Plotting orginal data and calibrations

## Input
xs      = fs
ys      = original_data - np.average(original_data)

ys1     = og_08k
ys2     = og_10k
ys3     = og_12k

xlabel  = 'Frequency (%s)' % (f_unit)
ylabel  = 'Magnitude (%s)' % (s_unit)
title   = 'Transmission (S21) with calibration at different temperatures subtracted'
legend  = ['Original minus average', '08K', '10K', '12K']

## Plotting
# Creating new figure and getting axis
figure  = plt.figure()
axis    = figure.gca()


# Plot either one or more graphs, depending on how many are in the data
#for i in range(len(data[:,0])):
#    plt.plot(fs, data)
plt.plot(xs, ys)
plt.plot(xs, ys1)
plt.plot(xs, ys2)
plt.plot(xs, ys3)

## Format the figures

# Sets origin in upper-left corner
#plt.axis([min(xs), max(xs), min(ys), max(ys)])
plt.xlim([min(xs), max(xs)])
#plt.ylim([min(ys), max(ys)]) 

# Turns on grid
plt.grid(True)
#axis.xaxis.grid(which='minor')
#axis.yaxis.grid(which='minor')

# Sets labels, legend and title
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.legend(legend)
plt.title(title)