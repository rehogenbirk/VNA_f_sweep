# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 15:57:24 2018

@author: Rijk

Test file
- Creates two rows of data in same array
- Stores array as .csv file

"""



import numpy as np
import matplotlib.pyplot as plt


xs = np.linspace(0, 50)

y = np.zeros([2, 50])
y[0] = 50*xs
y[1] = xs**2

names = ['y0', 'y1']

#np.vstack((np.transpose(names), y)) # Trying to get the names in front of the row with the data

plt.figure(3)
plt.plot(xs, y[0], y[1])
#for i in range(len(names)):
#    plt.legend(labels=names[i])

plt.legend(names)