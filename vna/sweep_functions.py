# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 14:46:47 2018

@author: Rijk
"""

# VNA_f_sweep setup measurement parameters function

import visa
import sys
import time
import vna_functions as vna
import numpy as np
import matplotlib.pyplot as plt
import os

## Template for putting in measurement parameters

#f_start         = 100      # MHz
#f_stop          = 67000    # MHz
#num_points      = 201
#IF_bandwidth    = 35000    # Hz
#amplitude       = -17      # dBm
#s_param         = ['S11']  # List of strings

def init():
    """Initiates connection with VNA and clears all previous measurements"""
    ## Make contact with the VNA and initialise it
    rm = visa.ResourceManager()
    PNA = vna.connect('GPIB0::16::INSTR')
    vna.reset(PNA) 
    vna.clear(PNA)
    
    # Close all measurements
    vna.meas_close_all(PNA)
    
    print('MESSAGE: VNA initialised')
    bla = PNA
    return bla, rm

def close(instrument, rm):
    """Wipes the instrument settings and terminates the session"""
    vna.reset(instrument)
    instrument.close()
    rm.close()
    print('MESSAGE: VNA reset and session closed')

def setup(instrument, f_start, f_stop, num_points, IF_bandwidth, 
          amplitude, s_param):
    """Sets measurement parameters on the VNA"""
    
    f_unit = 'MHZ'
    A_unit = 'DBM'
    
    s_param_str = ''
    for s in s_param:
        s_param_str += s
    
    # Display numbers
    window_num  = 1
    
    ## Error checking and turning strings into numbers
    if num_points > 32001:
        sys.exit('num_points is larger than the maximum amount possible')
    
    if IF_bandwidth not in [1, 2, 3, 5, 7, 10, 15, 20, 30, 50, 70, 100, 
                                150, 200, 300, 500, 700, 1e3, 1.5e3, 2e3, 3e3,
                                5e3, 7e3, 10e3, 15e3, 20e3, 30e3, 35e3, 40e3]:
        sys.exit('IF_bandwidth is not set to any of the allowed values')
    
    # In case num_points is a string, for the next step, it needs to be converted to a number
    if type(num_points) == str:
        if num_points[0:3].upper() == 'MAX':
            num_points = 32001 # Maximum number of points possible on current VNA
        elif num_points[0:3].upper() == 'MIN':
            num_points = 1 # Minimum number of points possible on current VNA
        else:
            sys.exit('num_points has been assigned an incorrect string, please try again')
    
# =============================================================================
    # %%
    # Measurement setup
    # =============================================================================
    
    ## Create window and display measurement in it
    vna.display_window(instrument, window_num, 'ON') 
    # leads to VNA error when window is already open, but it is harmless
    
    ## Create a measurement and the s-parameters it measures, then feed it to a window
    meas_names = []
    
    for s in range(len(s_param)):
        trace_num = s+1
        meas_names.append('meas_%s' % (s_param[s]))
        vna.meas_create(instrument, meas_names[s], s_param[s])
        vna.meas_show(instrument, meas_names[s], window_num, trace_num) 
    
    ## Setup measurement parameters: 
    # frequency range, amplitude, number of points, and IF bandwidth
    vna.set_f_start(instrument, f_start, f_unit)
    vna.set_f_stop(instrument, f_stop, f_unit)   
    
    vna.set_amplitude(instrument, amplitude, A_unit)
    
    vna.set_num_points(instrument, num_points)
    vna.set_if_bandwidth(instrument, IF_bandwidth, window_num)
    
#    ## Autoscale window
#    # TODO: Find way to pause script and continue with Enter oid
#    input('Wait for measurement to be completed, then press enter')
#    vna.autoscale(instrument, 1)
    
    print('MESSAGE: Measurement setup complete')
    return meas_names
    


def standard_sweep(instrument):
    f_start         = 100 
    f_stop          = 67000
    num_points      = 201
    IF_bandwidth    = 35000
    amplitude       = -17
    s_param         = ['S11']
    meas_names = setup(instrument, f_start, f_stop, num_points, IF_bandwidth, amplitude, s_param)
    return meas_names
    


def get_data(instrument, error_correction=1):
    """Get the data from all measurements and time measurements took"""
    # Query for necessary data
    num_points      = vna.get_num_points(instrument)
    f_start, f_stop = vna.get_Df(instrument)
    meas_names      = vna.get_meas_names(instrument)
    
    # Intialise data array
    data = np.zeros((len(meas_names), num_points))
    
    elapsed         = np.zeros(len(meas_names))
    meas_time       = np.zeros(len(meas_names)+1)
    meas_time[0]    = time.time()
    
    for m in range(len(meas_names)):
        data[m]         = vna.get_meas_data(instrument, meas_names[m]) # very slow (~3 min) for max num_points or small IF bandwidth
        meas_time[m+1]  = time.time()
        elapsed[m]      = meas_time[m+1] - meas_time[m]
        print('MESSAGE: %s measurement done' % (meas_names[m]))
        
    ## Error correction
    # Does not work if two -200 values are adjacent
    if error_correction:
        for i in range(len(data[:, 0])):
            for j in range(len(data[i])-1):
                if data[i,j] == -200:
                    average = (data[i,j-1] + data[i,j+1]) / 2
                    data[i,j] = average
    
    # Add frequencies to S-parameter data
    fs      = np.linspace(f_start, f_stop, num_points) # Create x-axis (as none are gotten from get_meas_data)
    data = np.vstack((fs, data))
    
    print('MESSAGE: All measurements complete')
    
    return data, elapsed
    



def save_data(instrument, file_name, data, s_param):
    """"Saves data as csv file in root folder"""
    # Setting file name to VNAdata_date_time
    date_time = str(time.strftime("%y%m%d_%H%M%S"))
    
    s_param_str = ''
    for s in s_param:
        s_param_str += s
    
    file_name2   = '%s_%s_%s' % (file_name, s_param_str, date_time)
    
    data_name = file_name2 + '.csv'
    np.savetxt(data_name, data, delimiter=',')
        
    # perhaps use strutured arrays
    # https://docs.scipy.org/doc/numpy/user/basics.rec.html
    
    cwd = os.getcwd()
    print(cwd)
    
    print('MESSAGE: Measurement data saved in: \n%s' % (cwd))
    
def plot_data(data, s_param, num_points, IF_bandwidth, only_S21=0):   
    
    # Get x-axis
    fs = data[0,:]
    # Get stop and start frequency
    f_start = int(min(fs)*1e-6)
    f_stop  = int(max(fs)*1e-6)
    
    # Separate S-parameter data from the rest
    ydata = data[1:,:]
    
    ## Plotting
    
    # Only plot S21
    if only_S21:
        plt.plot(fs, ydata[1,:])
        
        # Format the figures
        plt.axis([min(fs), max(fs), np.floor(np.min(ydata[1,:])), np.ceil(np.max(ydata[1,:]))]) # Sets origin in upper-left corner
        plt.grid(True)
        
        plt.title('Frequency between %s and %s %s for %s num points and %s Hz IF bandwidth' % (f_start, f_stop, 'MHz', num_points, IF_bandwidth))
        plt.legend('S21')
        plt.xlabel('Frequency (%s)' % ('MHz'))
        plt.ylabel('Magnitude (%s)' % ('dB'))
        
        # Plot all the S-parameters
    else:
        for i in range(len(ydata[:,0])):
            plt.plot(fs, ydata[i])
        
        # Format the figures
        plt.axis([min(fs), max(fs), np.floor(np.min(ydata)), np.ceil(np.max(ydata))]) # Sets origin in upper-left corner
        plt.grid(True)
        
        plt.title('Frequency between %s and %s %s for %s num points and %s Hz IF bandwidth' % (f_start, f_stop, 'MHz', num_points, IF_bandwidth))
        plt.legend(s_param)
        plt.xlabel('Frequency (%s)' % ('MHz'))
        plt.ylabel('Magnitude (%s)' % ('dB'))
    
    
    print('MESSAGE: Data plotted')
