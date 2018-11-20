# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 15:54:07 2018

@author: Rijk

Loads pickled (saved) figures

"""

# Import libraries

import pickle as pkl
import matplotlib.pyplot as plt
import os

#%% Parameters

figure_path     = r'C:\Users\Rijk\Documents\NAOJ Engineering\Vector Network Analyzer\Data_git\181116 Data amplitude sweep\Sweep number 1'

figure_name     = 'VNAdata_S21_181116_162416'

#%% Get figure and open it

figure_file     = os.path.join(figure_path, figure_name + '.pkl')

plt.figure()

with open(figure_file, 'rb') as fid:
    fig = pkl.load(fid)

plt.show()  

axis    = fig.gca()

#%% Change plot parameters

xlabel  = 'Frequency (Hz)'
ylabel  = 'Magnitude (dB)'
title   = 'Ratio of transmission with closed 300K window and laser'
legend  = ['Closed window', 'Laser']

## Format the figures

# Sets origin in upper-left corner
#plt.axis([min(xs), max(xs), min(ys), max(ys)]) 

# Turns on grid
plt.grid(True)
axis.xaxis.grid(which='minor')
axis.yaxis.grid(which='minor')

# Sets labels, legend and title
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.legend(legend)
plt.title(title)