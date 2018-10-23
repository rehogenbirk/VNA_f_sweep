# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 17:50:27 2018

@author: Rijk
"""

# Calculates points per dip for given num_points and frequency range width

def points_per_dip(f_range, num_points):
    f0  = 5e9
    Q   = 1e4 
    Df  = f0/Q # Bandwidth of dip
    
    points_per_hz = num_points / f_range
    
    points_per_dip = points_per_hz * Df
    print(points_per_dip)
    return points_per_dip

points_per_dip(2e9, 8001)
points_per_dip(2e9, 16001)
points_per_dip(2e9, 32001)
points_per_dip(1e9, 8001)
points_per_dip(1e9, 16001)
points_per_dip(1e9, 32001)

