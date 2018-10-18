# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 14:46:47 2018

@author: Rijk
"""

# VNA_f_sweep setup measurement parameters function

import visa
#import time
#import numpy as np
#import matplotlib.pyplot as plt
import sys

import vna_functions as vna

def F_sweep_init():
        # %%
    # Initialisation
    # =============================================================================
    
    ## Make contact with the VNA and initialise it
    rm = visa.ResourceManager()
    PNA = vna.connect('GPIB0::16::INSTR')
    vna.reset(PNA) 
    vna.clear(PNA)
    
    # Close all measurements
    vna.meas_close_all(PNA)
    
    print('MESSAGE: VNA initialised')
    
    return PNA, rm

def F_sweep_close(PNA, rm):
        # %%
    # Reset VNA
    # =============================================================================
    ## Wipe the settings and terminate the session
    vna.reset(PNA)
    PNA.close()
    rm.close()
    
    print('MESSAGE: VNA reset and session closed')

def F_sweep_setup(PNA, f_start, f_stop, num_points_set, IF_bandwidth_set, amplitude, s_param):
    
    f_unit = 'MHZ'
    A_unit = 'DBM'
    
    s_param_str = ''
    for s in s_param:
        s_param_str += s
    
    # Display numbers
    window_num  = 1
    trace_num   = 2
    
    ## Error checking and turning strings into numbers
    
    if num_points_set > 32001:
        sys.exit('num_points is larger than the maximum amount possible')
    
    if IF_bandwidth_set not in [1, 2, 3, 5, 7, 10, 15, 20, 30, 50, 70, 100, 150, 200, 300, 500, 700, 1e3, 1.5e3, 2e3, 5e3, 7e3, 10e3, 5e3, 20e3, 30e3, 35e3, 40e3]:
        sys.exit('IF_bandwidth is not set to any of the allowed values')
    
    # In case num_points is a string, for the next step, it needs to be converted to a number
    if type(num_points_set) == str:
        if num_points_set[0:3].upper() == 'MAX':
            num_points_set = 32001 # Maximum number of points possible on current VNA
        elif num_points_set[0:3].upper() == 'MIN':
            num_points_set = 1 # Minimum number of points possible on current VNA
        else:
            sys.exit('num_points has been assigned an incorrect string, please try again')
    
    # =============================================================================

    
    # =============================================================================
    # %%
    # Measurement setup
    # =============================================================================
    
    ## Create window and display measurement in it
    vna.display_window(PNA, window_num, 'ON') # leads to VNA error when window is already open, but the error is harmless
    
    ## Create a measurement and the s-parameters it measures, then feed it to a window
    meas_names = []
    
    for s in range(len(s_param)):
        trace_num += 1
        meas_names.append('meas_%s' % (s_param[s]))
        vna.meas_create(PNA, meas_names[s], s_param[s])
        vna.meas_show(PNA, meas_names[s], window_num, trace_num)
    
    #meas_name = 'meas_%s_%s' % (s, date_time)
    #vna.meas_create(PNA, meas_name, s)
    #vna.meas_feed(PNA, meas_name, window_num, trace_num)
    
    ## Set output amplitude
    vna.set_amplitude(PNA, amplitude, A_unit)
    
    ## Setup measurement parameters
    #vna.set_Df_sweep(PNA, f_start, f_stop, f_unit)
    vna.set_f_start(PNA, f_start, f_unit)
    vna.set_f_stop(PNA, f_stop, f_unit)
    
    vna.set_num_points(PNA, num_points_set)
    num_points_actual = int(vna.get_num_points(PNA)) # gets number of points in case num_points was a string
    
    
    
    # Set IF bandwidth (low makes measurement very slow, 2000 Hz is reasonable)
    vna.set_if_bandwidth(PNA, IF_bandwidth_set, window_num)
    IF_bandwidth_actual = vna.get_if_bandwidth(PNA)
    
    #time.sleep(3) # Need to wait before one sweep is done before autoscalng can occur, as initially all values are at -200 dB
    #
    ## Autoscale y-axis
    #PNA.write(':DISPlay:WINDow:TRACe%s:Y:AUTO' % (trace_num))
    #PNA.write(':SENSe%s:BANDwidth:RESolution %G Hz' % (window_num, 100.0))
    
    print('MESSAGE: Measurement setup complete')
    
    return num_points_actual, IF_bandwidth_actual
    
def F_sweep_standard(PNA):
    f_start         = 100 
    f_stop          = 67000
    num_points      = 201
    IF_bandwidth    = 35000
    amplitude       = -17
    s_param         = ['S11']
    F_sweep_setup(PNA, f_start, f_stop, num_points, IF_bandwidth, amplitude, s_param)
    
PNA, rm = F_sweep_init()
F_sweep_standard(PNA)
#F_sweep_close(PNA, rm)
        
