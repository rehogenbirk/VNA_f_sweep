# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 17:37:56 2018

@author: Rijk
"""

import matplotlib.pyplot as plt
import numpy as np

x   = np.linspace(0, 2*np.pi, 100)
y   = np.sin(x)
cos = np.cos(x)

dx = x[1] - x[0]

dy          = np.zeros(y.shape,np.float)
dy[0:-1]    = np.diff(y)/np.diff(x)
dy[-1]      = (y[-1] - y[-2])/(x[-1] - x[-2])

grad = np.gradient(y, dx)

grad2 = -1*np.gradient(grad, dx)

plt.plot(x, y)
plt.plot(x, cos)
plt.plot(x, dy)
plt.plot(x, grad)
plt.plot(x, grad2)

plt.legend(['Sine','Cosine','dx(sin)', 'grad(sin)', '-grad2(sin)'])