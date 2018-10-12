# -*- coding: utf-8 -*-
"""
Detection of Lorentzian peaks

Created on Thu Oct  4 10:25:59 2018

@author: Rijk


Goal: Get center frequency of Lorentzian peaks within a frequency spectrum

"""

import numpy               as np
import matplotlib.pyplot   as plt

## Generate data

xs = np.linspace(-1, 50)

ys = xs**3
der_exact = 3*xs**2
der2_exact = 6*xs

dx = xs[1] - xs[0]


der = np.gradient(ys, dx)
der2 = np.gradient(der, dx)

#der_y = np.insert(der_y, 0, 0) # Inserts a zero at the start

plt.figure(2)

plt.plot(xs, der_exact)
plt.plot(xs, der)

plt.figure(3)

plt.plot(xs, der2_exact)
plt.plot(xs, der2)

# Format the figures
#plt.axis([np.min(xs[2:]), np.max(xs[2:]), np.min(der_y), np.max(der_y)]) # Sets origin in upper-left corner
plt.grid()
#plt.xlabel('Frequency (%s)' % (f_unit))
#plt.ylabel('Magnitude (%s)' % ('dB'))