# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 14:26:23 2018

@author: Rijk
"""

# Calibrates the VNA when the chip is at 10 K, i.e. superconducting throughline without MKID dips in spectrum

# Test Command Expert Sequence and then export it here and turn it into usable functions

# Performing calibration steps makes the VNA crash....

import time
import numpy as np
import sys
import vna_functions as vna
import sweep_functions as fsweep


def create_cal_set(cal_name):
    # Parameters    
    f_start         = 100      # MHz
    f_stop          = 10000    # MHz
    num_points      = 201
    IF_bandwidth    = 35000    # Hz
    amplitude       = -17      # dBm
    s_param         = ['S11']  # List of strings
    
    
    
    ###     Code
    #%%
    ## Setup Measurement
    VNA, rm = fsweep.init()
    fsweep.setup(VNA, f_start, f_stop, num_points, 
                              IF_bandwidth, amplitude, s_param)
        
    
    #%%
    ## Calibration
    
    # Select measurement to calibrate
#    VNA.write(':CALCulate:PARameter:SELect "%s"' % (meas_names[0]))
    
    # Specify to save calibration as a UserSet and set its name
    VNA.write(':SENSe:CORRection:PREFerence:CSET:SAVE %s' % ('USER'))
    #VNA.write(':SENSe:CORRection:CSET:NAME "%s"' % (cal_set_name))
    
    
    
    # Specify connectors for all the ports, if used, else set to unused
    VNA.write(':SENSe:CORRection:COLLect:GUIDed:CONNector:PORT1:SELect "%s"' % ('1.85 mm female'))
    VNA.write(':SENSe:CORRection:COLLect:GUIDed:CONNector:PORT2:SELect "%s"' % ('1.85 mm female'))
    VNA.write(':SENSe:CORRection:COLLect:GUIDed:CONNector:PORT3:SELect "%s"' % ('Not used'))
    VNA.write(':SENSe:CORRection:COLLect:GUIDed:CONNector:PORT4:SELect "%s"' % ('Not used'))
    
    time.sleep(1)
    
    # Specify Calibration kit for used ports
    VNA.write(':SENSe:CORRection:COLLect:GUIDed:CKIT:PORT1:SELect "%s"' % ('85058B Databased'))
    VNA.write(':SENSe:CORRection:COLLect:GUIDed:CKIT:PORT2:SELect "%s"' % ('85058B Databased'))
    
    # Specify which port pairs to calibrate over
    VNA.write(':SENSe:CORRection:COLLect:GUIDed:THRU:PORTs %s' % ('1,2'))
    
    
    #%%
    # Initiate calibration
    VNA.write(':SENSe:CORRection:COLLect:GUIDed:INITiate:IMMediate')
    
    # Query number of steps in calibration kit
    temp_values = VNA.query_ascii_values(':SENSe:CORRection:COLLect:GUIDed:STEPs?')
    steps = int(temp_values[0])
    del temp_values
    
    # WARNING: This part crashed the VNA!!!
    #for i in np.arange(steps)+1:
    #    prompt = VNA.query(':SENSe:CORRection:COLLect:SESSion:DESCription? %d' % (i))
    #    input('Wait until calibration step is done, then press Enter')
    #    VNA.write(':SENSe:CORRection:COLLect:GUIDed:ACQuire %s' % ('STAN'))
    
    VNA.write(':SENSe:CORRection:COLLect:GUIDed:SAVE:CSET "%s"' % (cal_name))
    
#    # Get actual calibration set name
#    calibration_name_stored = VNA.query(':SENSe1:CORRection:CSET:NAME?')
    
    
    #VNA.close()
    #rm.close()
    
    # end of Untitled

VNA, rm = fsweep.init()
fsweep.standard_sweep(VNA)
vna.cal_load(VNA, 'calibration_Rijk_10K')






    