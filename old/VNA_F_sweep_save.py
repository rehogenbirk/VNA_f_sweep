# =============================================================================
# ## Import libraries
# =============================================================================
import visa
import time

from VNA import vna_module as vna
# =============================================================================
# ## Input parameters
# =============================================================================

## Measurement settings
f_unit = 'MHZ' 

f_start     = 100   # in f_unit
f_stop      = 67000 # in f_unit

num_points = 'MAXimum' # MAX is 32001 points

amplitude = -50 # dBm
 
s_param = 'S11' 

window_num = 2

## Various names

date_time = str(time.strftime("%d%m_%H%M"))

# Setting file name to VNAdata_date_time
file_name = "C:\\Documents and Settings\\Administrator\\Desktop\\Rijk\\VNAdata" 
file = file_name + '_' + date_time + '.csv'

# Set measurement name
meas_name = 'meas_' + s_param + '_' + date_time

# =============================================================================
# #Setup measurement
# =============================================================================

## Make contact with the VNA and initialise it
PNA = vna.connect('GPIB0::16::INSTR')
vna.reset(PNA)
vna.clear(PNA)

## Define measurement and the s-parameters it measures
PNA.write(':CALCulate:PARameter:DEFine:EXTended "%s","%s"' % (meas_name, s_param))

## Create window and display measurement in it
vna.display_window(PNA, 2, 1)
PNA.write(str(':DISPlay:WINDow'+ str(window_num) + ':TRACe9:FEED "%s"') % (meas_name))

## Set output amplitude
PNA.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %G DBM' % (amplitude))

## Setup measurement parameters
PNA.write(str(':SENSe:FREQuency:STARt %G ' + f_unit) % (f_start))
PNA.write(str(':SENSe:FREQuency:STOP %G ' + f_unit) % (f_stop))
PNA.write(':SENSe:SWEep:POINts %s' % (num_points))

# =============================================================================
# Perform measurement and save data
# =============================================================================

## Start measurement and wait 3 seconds to let the measurement finish
PNA.write(':OUTPut:STATe %d' % (1))
time.sleep(3)

## Store the data locally on the VNA
#PNA.write(':MMEMory:STORe:DATA "%s","%s","%s","%s",%d' % (file, 'CSV Formatted Data', 'Auto', 'Displayed', 1))

# =============================================================================
# Reset VNA
# =============================================================================

## Wipe the settings and terminate the session
#PNA.write('*RST')
PNA.close()
rm.close()


