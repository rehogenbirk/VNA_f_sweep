# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:16:10 2018

@author: Rijk

Plotting resonance frequencies from script Jochem versus the values they should have

*_base      : baseline measurement
*_laser5    : measurement with laser on column 5
*_laser8    : measurement with laser on column 8

"""

import numpy as np
import matplotlib.pyplot as plt
import os
import data_analysis as dat

#%% Parameters

folder                  = r'C:\Users\Rijk\Documents\NAOJ Engineering\Vector Network Analyzer\Matlab analysis\181121 df0'

file_name_base          = 'LeakyFsweepbetween4and5_22KIDparam'
file_name_comparison    = 'LeakyFsweepcolumn5_22KIDparam'

name_base               = input('What is the name of the base file?\n')
name_comparison         = input('What is the name of the comparison file?\n')

#%% Loading data

file_base       = os.path.join(folder, file_name_base   + '.csv') 
file_comparison = os.path.join(folder, file_name_comparison  + '.csv')

delimiter = ','

f0_base         = np.loadtxt(file_base,     delimiter=',')[3]
f0_comparison   = np.loadtxt(file_comparison,   delimiter=',')[3]

# Name for final files

name_final          = 'fShifts_%s_vs_%s' % (name_base, name_comparison)

final_file_name     = os.path.join(folder, name_final)


#%% Code

# Reject outliers

#  <4.5 GHz and >5.8 GHz
def reject_outliers(f0s):
    f0s_checked     = []
    for i in range(len(f0s)):
        if f0s[i] > 4.5e9 and f0s[i] < 5.8e9:
            f0s_checked.append(f0s[i])
    
    return f0s_checked

f0_base         = reject_outliers(f0_base)
f0_comparison   = reject_outliers(f0_comparison)


# Compare number of KIDs found

if len(f0_base) != len(f0_comparison):
    print('Number of KIDs found is not the same for all data!\n')
    
    num_missing_f0s = abs(len(f0_base) - len(f0_comparison))
    
    if len(f0_base) > len(f0_comparison):
        print('%s f0(\'s) is/are missing in %s (blue)\n' % (num_missing_f0s, 'f0_comparison'))
    else:
        print('%s f0(\'s) is/are missing in %s (red)\n' % (num_missing_f0s, 'f0_base'))
    
    plt.figure()
    
    dat.bar_plot(f0_base, [1]*len(f0_base), barwidth=1)
    dat.bar_plot(f0_comparison, [1]*len(f0_comparison), color='r', barwidth=1)
    
    for i in range(len(f0_base)):
        plt.annotate(str(int(f0_base[i])), (f0_base[i], 1))
        plt.annotate(str(int(f0_comparison[i])), (f0_comparison[i], 1))
        
num_kids    = len(f0_base)

# Calculate frequency shifts

dfs     = np.zeros(num_kids)

for i in range(num_kids):
    dfs[i]   = f0_base[i]   - f0_comparison[i]
    
# Normalise wrt frequency resolution
#   for a range of 2e9 Hz and 16001 points, this is 125000 Hz
    
num_points  = 16001
f_range     = 2e9

f_res       = f_range / (num_points - 1)

dfs     = dfs / f_res

#%% Plot results
plt.close('all')
    
plt.figure()

plt.xlim([4.5e9, 5.8e9])

#for i in range(len(f0_base)):
#    plt.vlines(f0_base[i], min(0, dfs[i]), max(0, dfs[i]), color='b', linewidths=5)
    
dat.bar_plot(f0_base, dfs, barwidth=5, color='b')

plt.ylabel('Df (%s Hz)' % (f_res))
plt.xlabel('f (Hz)')

plt.title('Frequency shifts of f0\'s between:\n %s and %s' % (name_base, name_comparison))

plt.grid()

#%% Save results

dat.save_data(dfs, f0_base, final_file_name)

dat.save_plot(final_file_name)

f   = open(final_file_name + '_parameters.txt', 'w+')

f.write('Frequency shifts between:\n')
f.write('- %s\n' %(name_base))
f.write('- %s\n' %(name_comparison))

f.write('Measurements: \n-%s\n-%s\n\n' % (file_base, file_comparison))

f.write('Comments:\n%s' % (input('Comments?\n')))

f.close()
