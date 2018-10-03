# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 11:22:18 2018

@author: Rijk

Reset the VNA
"""

import visa

rm = visa.ResourceManager()
VNA = rm.open_resource('GPIB0::16::INSTR')
VNA.write('*RST')
VNA.write('*CLS')