"""
Description:
Script to let the VNA perform a measurement of S-parameters with a variable frequency and a set amplitude.

Rijk Hogenbirk, started on 24/09/18
"""

# =============================================================================
# ## Import libraries
# =============================================================================
import visa
import time
import numpy as np
import matplotlib.pyplot as plt

import vna_functions as vna
# =============================================================================
# %%
# ## Input parameters
# =============================================================================

## Measurement settings
f_unit  = 'MHZ'
f_start = 4000   # in f_unit
f_stop  = 6000 # in f_unit

num_points  = 'MAX' # MAX is 32001 points, 8001 is chosen as otherwise the acquisition is very slow

A_unit      = 'DBM'
amplitude   = -50

s_param = ['S11', 'S21', 'S22']
#s_param = ['S21']

s_param_str = ''
for s in s_param:
    s_param_str += s

# Display numbers
window_num  = 1
trace_num   = 2

# Error correction
error_correction = 0

## Data storage parameters

date_time = str(time.strftime("%y%m%d_%H%M%S"))

# Setting file name to VNAdata_date_time
file_path   = "C:\\Documents and Settings\\Administrator\\Desktop\\Rijk\\VNAdata"
file_name   = '%s_%s.csv' % (s_param_str, date_time)
file        = file_path + file_name

file_type   = 'CSV Formatted Data'
scope       = 'Displayed'
file_format = 'Displayed'
selector    = 1

# In case num_points is a string, for the next step, it needs to be converted to a number
if type(num_points) == str:
    if num_points[0:3].upper() == 'MAX':
        num_points = 32001 # Maximum number of points possible on current VNA
    elif num_points[0:3].upper() == 'MIN':
        num_points = 1 # Minimum number of points possible on current VNA
    else:
        print('num_points has been assigned an incorrect string, please try again')


# =============================================================================
# %%
#Setup measurement
# =============================================================================

## Make contact with the VNA and initialise it
rm = visa.ResourceManager()
PNA = vna.connect('GPIB0::16::INSTR')
vna.reset(PNA) 
vna.clear(PNA)


# Close all measurements
vna.meas_close_all(PNA)

## Create window and display measurement in it
vna.display_window(PNA, window_num, 'ON') # leads to VNA error when window is already open, but the error is harmless

## Create a measurement and the s-parameters it measures, then feed it to a window
meas_names = []

for s in range(len(s_param)):
    meas_names.append('meas_%s' % (s_param[s]))
    vna.meas_create(PNA, meas_names[s], s_param[s])
    vna.meas_feed(PNA, meas_names[s], window_num, trace_num)
    trace_num += 1

#meas_name = 'meas_%s_%s' % (s, date_time)
#vna.meas_create(PNA, meas_name, s)
#vna.meas_feed(PNA, meas_name, window_num, trace_num)

## Set output amplitude
vna.set_amplitude(PNA, amplitude, A_unit)

## Setup measurement parameters
vna.set_Df_sweep(PNA, f_start, f_stop, f_unit)
vna.set_num_points(PNA, num_points)
num_points = int(vna.get_num_points(PNA)) # gets number of points in case num_points was a string



# Set IF bandwidth (low makes measurement very slow, 2000 Hz is reasonable)
PNA.write(':SENSe%s:BANDwidth:RESolution %G HZ' % (window_num, 1000.0))

#time.sleep(3) # Need to wait before one sweep is done before autoscalng can occur, as initially all values are at -200 dB
#
## Autoscale y-axis
#PNA.write(':DISPlay:WINDow:TRACe%s:Y:AUTO' % (trace_num))
#PNA.write(':SENSe%s:BANDwidth:RESolution %G Hz' % (window_num, 100.0))

# =============================================================================
# %%
# Perform measurement
# =============================================================================

## Start measurement and wait 3 seconds to let the measurement finish
vna.meas_start(PNA)
time.sleep(3) #asynchronous programming would be better

# =============================================================================
# %%
# Save data
# =============================================================================

### Store the data locally on the VNA
#vna.save_local(PNA, file, file_type, scope, file_format, selector)
#time.sleep(4) #asynchronous programming would be better

## Get the data from all measurements
data = np.zeros((len(meas_names), num_points))

t = time.time()
elapsed = np.ones(len(meas_names))

for m in range(len(meas_names)):
    data[m] = vna.get_meas_data(PNA, meas_names[m]) # very slow (~3 min) for max num_points
    elapsed[m] = time.time() - t

#time.sleep(2)

## Error correction
# Does not work if two -200 values are adjacent

if (error_correction == 1):
    for i in range(len(data[:, 0])):
        for j in range(len(data[i])):
            if data[i,j] == -200:
                average = (data[i,j-1] + data[i,j+1]) / 2
                data[i,j] = average

elapsed_time = elapsed[-1] - t
elapsed = np.append(elapsed, elapsed_time)

data_name = file_name + '.npy'
np.save(data_name, data)

elapsed_time = elapsed[-1] - t
elapsed = np.append(elapsed, elapsed_time)
# =============================================================================
# %%
# Reset VNA
# =============================================================================

## Wipe the settings and terminate the session
vna.reset(PNA)
PNA.close()
rm.close()

# =============================================================================
# %%
# Plot data
# =============================================================================
plt.close('all') # Closes all open figures

# Create x-axis (as none are gotten from get_meas_data)
fs = np.linspace(f_start, f_stop, num_points)


# Plot the data
for i in range(len(data[:,0])):
    plt.plot(fs, data[i])

# Format the figures
plt.axis([min(fs), max(fs), np.min(data), 0]) # Sets origin in upper-left corner
plt.grid()
plt.xlabel('Frequency (%s)' % (f_unit))
plt.ylabel('Magnitude (%s)' % ('dB'))
