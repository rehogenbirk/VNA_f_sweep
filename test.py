# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 16:04:35 2018

@author: Rijk
"""

import visa
import time

import vna_functions as vna

# =============================================================================
# #Setup measurement
# =============================================================================

## Make contact with the VNA and initialise it
rm = visa.ResourceManager()
PNA = vna.connect('GPIB0::16::INSTR')
vna.reset(PNA)
vna.clear(PNA)

# =============================================================================
# Test code
# =============================================================================
#vna.meas_create(PNA, 'CH1_S11_1', 'S11')

PNA.write(':CALCulate:PARameter:SELect "%s"' % ('CH1_S11_1'))
time.sleep(1)
temp_values = PNA.query_ascii_values(':CALCulate:DATA? %s' % ('FDATA'))



# =============================================================================
# Reset VNA
# =============================================================================

## Wipe the settings and terminate the session
PNA.close()
rm.close()