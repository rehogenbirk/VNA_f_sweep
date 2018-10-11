# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 17:05:42 2018

@author: Rijk
"""

import numpy as np

f = 'f'
s_param = ['S21']

for s in s_param:
    names = [f, s]

f_unit = 'MHz'
s_unit = 'dB'

units = [f_unit, s_unit]

test_data = np.random.random_sample((2, 30))

data_name = 'test' + '.csv'
np.savetxt(data_name, test_data, header='LOL', delimiter=',')
