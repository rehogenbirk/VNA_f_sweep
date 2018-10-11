# -*- coding: utf-8 -*-
"""
Detection of Lorentzian peaks

Created on Thu Oct  4 10:25:59 2018

@author: Rijk


Goal: Get center frequency of Lorentzian peaks within a frequency spectrum

"""

import numpy               as np
import matplotlib.pyplot   as plt

# Generate data

xs = np.linspace(-1, 50)

ys = xs**3

def derivative(xs, ys):
    """Takes numerical derivative of y(x)"""
    dxs = np.diff(xs)
    dys = np.diff(ys)
    der = dys/dxs
    return der

def derivative2(xs, ys):
    """Takes second numerical derivative of y(x)"""
    der1 = derivative(xs, ys)
    der2 = derivative(xs[1:], der1)
    return der2

der_y = np.zeros([len(xs), 2])

der_y[:, 0]   = derivative(xs, ys)
der_y[:, 1]  = derivative2(xs, ys)

#der_y = np.insert(der_y, 0, 0) # Inserts a zero at the start

plt.figure(2)

plt.plot(xs[1:], der_y[0])
plt.plot(xs[2:], der_y[1])

# Format the figures
plt.axis([np.min(xs[2:]), np.max(xs[2:]), np.min(der_y), np.max(der_y)]) # Sets origin in upper-left corner
plt.grid()
#plt.xlabel('Frequency (%s)' % (f_unit))
#plt.ylabel('Magnitude (%s)' % ('dB'))