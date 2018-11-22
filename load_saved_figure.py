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
import data_analysis as dat

#%% Parameters

figure_path     = r'C:\Users\Rijk\Documents\NAOJ Engineering\Vector Network Analyzer\Data_git\181120 Final measurements\Narrow line test\Wider line\Ratios'

figure_name     = 'ratio_between4and5_and_column5'

fig, axis = dat.load_figure(figure_path, figure_name)

figure_path     = r'C:\Users\Rijk\Documents\NAOJ Engineering\Vector Network Analyzer\Data_git\181120 Final measurements\Narrow line test\Wider line\Ratios'

figure_name     = 'ratio_between4and5_and_column8'

fig2, axis2 = dat.load_figure(figure_path, figure_name)

#%% Change plot parameters

xlabel  = 'Frequency (Hz)'
ylabel  = 'Magnitude (dB)'
#title   = 'Magnitude ratio' #of transmission with closed 300K window and laser'
#legend  = ['S21']

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
#plt.legend(legend)
#plt.title(title)