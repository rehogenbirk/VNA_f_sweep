# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 15:18:02 2018

@author: Rijk
"""
import numpy as np
import matplotlib.pyplot as plt
import math as m

## 3.4 GHz

T = np.array([4.5,
              5,
              6,
              7,
              8,
              9,
              10,
              11,
              12])

mag = np.array([-7.8585777,
-7.888826036,
-8.010502305,
-8.15647343,
-8.335170378,
-8.66435417,
-9.372127966,
-10.76848787,
-16.72348347
])

T0  = T[0]
T   = T -T0

mag0    = mag[0]
mag     = mag - mag0

a = -0.006205
b = 0.9671


matlab_fit = a*np.exp(b*T)

plt.plot(T, mag, marker='o')
plt.plot(T, matlab_fit, marker='*')

plt.title('Plot of data and exponential fit of S21(T) at 7.15GHz')
plt.legend(['Data', 'Fit'])

plt.ylabel('S21 (dB)')
plt.xlabel('T (K)')
