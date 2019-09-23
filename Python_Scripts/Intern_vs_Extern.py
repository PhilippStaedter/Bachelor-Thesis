# plot a bar plot for 16_08_9_2 vs state variables
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from averageTime import *

# open .tsv file
path = '../bachelor_thesis/Tolerance/16_08.tsv'
tsv_file = pd.read_csv(path, sep='\t')

# get new .tsv file
tsv_file = averaging(tsv_file)

# take intern_time
intern_time = []
for iLine in range(len(tsv_file['id']) - 1):
    intern_time.append(tsv_file['t_intern_ms'][iLine])

# take extern_time
extern_time = []
for iLine in range(len(tsv_file['id']) - 1):
    extern_time.append(tsv_file['t_extern_ms'][iLine])

# take number of state variables
state_variable = []
for iLine in range(len(tsv_file['id']) - 1):
    state_variable.append(tsv_file['state_variables'][iLine])

# take number of reactions
parameters = []
for iLine in range(len(tsv_file['id']) - 1):
    parameters.append(tsv_file['parameters'][iLine])


##### several plots
fontsize = 22
labelsize = 16
titlesize = 30

# plots
plt.subplot(2,2,1)
# scatter plot of data
plt.scatter(state_variable, intern_time, alpha=0.8, c='blue', edgecolors='none', s=40, label='Intern Time')
plt.scatter(state_variable, extern_time, alpha=0.8, c='red', edgecolors='none', s=40, label='Extern Time')
plt.xscale("log")
plt.yscale("log")
plt.xlim((0.3, 2000))
plt.ylim((0.3, 2000))
plt.ylabel('Simulation time in milliseconds', fontsize=labelsize, fontweight='bold')
plt.tick_params(labelsize=labelsize)

# title + legend
plt.title('AMICI- vs Python routine', fontsize=titlesize, fontweight='bold')
plt.legend(loc=2, fontsize=fontsize - 2)

#######
plt.subplot(2,2,3)
# percental deviation
time_difference = []
for iTime in range(0, len(intern_time)):
    time_difference.append((extern_time[iTime] - intern_time[iTime])/intern_time[iTime])
plt.scatter(state_variable, time_difference, alpha=0.8, c='grey', edgecolors='none', s=40, label=r'$\frac{t_{python} - t_{amici}}{t_{amici}}$')
plt.xscale("log")
plt.yscale("log")
plt.xlim((0.3, 2000))
plt.ylim((0.001, 10))
plt.xlabel('Number of state variables', fontsize=labelsize, fontweight='bold')
plt.ylabel('Time difference in milliseconds', fontsize=labelsize, fontweight='bold')
plt.tick_params(labelsize=labelsize)

# title + legend
plt.title('Relative Time Difference', fontsize=titlesize, fontweight='bold')
plt.legend(loc=2, fontsize=fontsize - 2)

######
plt.subplot(2,2,2)
# scatter plot of data
plt.scatter(parameters, intern_time, alpha=0.8, c='blue', edgecolors='none', s=40, label='Intern Time')
plt.scatter(parameters, extern_time, alpha=0.8, c='red', edgecolors='none', s=40, label='Extern Time')
plt.xscale("log")
plt.yscale("log")
plt.xlim((0.3, 6000))
plt.ylim((0.3, 2000))
plt.tick_params(labelsize=labelsize)

# title + legend
plt.title('AMICI- vs Python routine', fontsize=titlesize, fontweight='bold')
plt.legend(loc=2, fontsize=fontsize - 2)

#######
plt.subplot(2,2,4)
# percental deviation
time_difference = []
for iTime in range(0, len(intern_time)):
    time_difference.append((extern_time[iTime] - intern_time[iTime])/intern_time[iTime])
plt.scatter(parameters, time_difference, alpha=0.8, c='grey', edgecolors='none', s=30, label=r'$\frac{t_{python} - t_{amici}}{t_{amici}}$')
plt.xscale("log")
plt.yscale("log")
plt.xlim((0.3, 6000))
plt.ylim((0.001, 10))
plt.xlabel('Number of parameters', fontsize=labelsize, fontweight='bold')
plt.tick_params(labelsize=labelsize)

# title + legend
plt.title('Relative Time Difference', fontsize=titlesize, fontweight='bold')
plt.legend(loc=2, fontsize=fontsize - 2)


###########
# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
#plt.savefig('../bachelor_thesis/New_Figures/Figures_study_1/amici_vs_time()_447SBML_ylog.pdf')

# show figure
plt.show()