# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 11:22:18 2018

@author: Rijk

DESCRIPTION
Shortened VISA functions for the A.09.33.07 command set
Made for the Agilent/Keysight PNA Network Analyzer E8361C

COMMENTS
1.  Adding channels cannot be done inside the SCPI command set. 
    Therefore only the first channel is used and the default is 1 and should not be changed.
    The parameter was left in case a solution for this is found.

"""

import visa
import time

#channel_num = 1

## Resets the VNA
def reset(instrument):
    """Resets the instrument"""
    instrument.write('*RST')
    
## Clears the VNA
def clear(instrument):
    """Clears the instrument"""
    instrument.write('*CLS')
    
## 
def connect(address='GPIB0::16::INSTR'):
    """Sets up connection to the instrument at the address"""
    rm = visa.ResourceManager()
    return rm.open_resource(address)
    
# =============================================================================
# Controlling windows    
# =============================================================================

def display_window(instrument, window_num=1, status='ON'):
    """Turns a window on the instrument 'on' or 'off' """
    status.upper()
    if window_num != 1:
        command = ':DISPlay:WINDow%d:STATe %s' % (window_num, status)
        instrument.write(command)
    

# =============================================================================
# Control measurements
# =============================================================================

def meas_close_all(instrument):
    command = ':CALCulate:PARameter:DELete:ALL'
    instrument.write(command)

def meas_create(instrument, meas_name, s_parameters, channel_num=1):
    """Create a measurement of the S-parameters for the instrument"""
    command = ':CALCulate%d:PARameter:DEFine:EXTended "%s","%s"' % (channel_num, meas_name, s_parameters)
    instrument.write(command)
    
def meas_show(instrument, meas_name, window_num=1, trace_num=9):
    """Feeds the measuremnt to a window as a numbered trace, so it's displayed there"""
    command = ':DISPlay:WINDow%d:TRACe%d:FEED "%s"' % (window_num, trace_num, meas_name)
    instrument.write(command)
    
def meas_start(instrument):
    """Start measurement by turning on the RF power of the source"""
    command = ':OUTPut:STATe %d' % (1)
    instrument.write(command)

# =============================================================================
# Set measurement parameters
# =============================================================================

def set_amplitude(instrument, amplitude, unit='DBM', channel_num=1):
    """Sets output amplitude of the instrument in unit given"""
    command = ':SOURce%d:POWer:LEVel:IMMediate:AMPLitude %G %s' % (channel_num, amplitude, unit)
    instrument.write(command)
    
#def set_Df_sweep(instrument, f_start, f_stop, unit='MHZ', channel_num=1):
#    """Sets start and stop frequency of sweep of channel"""
#    command1 = ':SENSe%d:FREQuency:STARt %G %s' % (channel_num, f_start, unit)
#    command2 = ':SENSe%d:FREQuency:STOP %G %s' % (channel_num, f_stop, unit)
#    instrument.write(command1)
#    instrument.write(command2)
    
def set_f_start(instrument, f_start, unit='MHZ', channel_num=1):
    """Sets start frequency of sweep of channel"""
    command = ':SENSe%d:FREQuency:STARt %G %s' % (channel_num, f_start, unit)
    instrument.write(command)
    
def set_f_stop(instrument, f_stop, unit='MHZ', channel_num=1):
    """Sets stop frequency of sweep of channel"""
    command = ':SENSe%d:FREQuency:STOP %G %s' % (channel_num, f_stop, unit)
    instrument.write(command)

def set_num_points(instrument, num_points='MAXimum', channel_num=1):
    """Sets number of data points for a given channel"""
    command = ':SENSe%d:SWEep:POINts %s' % (channel_num, num_points)
    instrument.write(command)
    
def set_if_bandwidth(instrument, if_bandwidth, window_num=1, channel_num=1):
    """"Sets the bandwidth in Hz of the intermediate frequency (IF) bandpass filter, low values lead to slow measurements"""
    command = ':SENSe%s:BANDwidth:RESolution %G HZ' % (window_num, if_bandwidth)
    instrument.write(command)
    
def save_local(instrument, file_path, file_type='CSV Formatted Data', scope='Auto', file_format='Displayed', selector=1):
    command = ':MMEMory:STORe:DATA "%s","%s","%s","%s",%d' % (file_path, file_type, scope, file_format, selector)
    instrument.write(command)

# =============================================================================
# Queries
# =============================================================================

def get_meas_data(instrument, meas_name, channel_num=1):
    command = ':CALCulate%d:PARameter:SELect "%s"' % (channel_num, meas_name)
    instrument.write(command)
    data = instrument.query_ascii_values(':CALCulate:DATA? %s' % ('FDATA'))
    return data

def get_num_points(instrument):
    command = ':SENSe:SWEep:POINts?'
    num_points = instrument.query_ascii_values(command)[0]
    return num_points

def get_if_bandwidth(instrument):
    command = ':SENSe:BANDwidth:RESolution?'
    if_bandwidth = instrument.query_ascii_values(command)[0]
    return if_bandwidth










