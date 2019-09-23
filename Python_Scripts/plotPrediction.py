# scatter plot of the prediction settings against amici default settings

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from averageTime import *

# important paths
amici_default_path = '../bachelor_thesis/SolverAlgorithm/Total/2_9_16_08.tsv'
predictor_path_one = '../bachelor_thesis/SolverAlgorithm/Total/2_9_08_06.tsv'
predictor_path_two = '../bachelor_thesis/SolverAlgorithm/Total/2_9_10_14.tsv'

# open .tsv files
amici_tsv_file = pd.read_csv(amici_default_path, sep='\t')
predictor_tsv_file_one = pd.read_csv(predictor_path_one, sep='\t')
predictor_tsv_file_two = pd.read_csv(predictor_path_two, sep='\t')

# average from 210 to 166 models
amici_tsv_file = averaging(amici_tsv_file)
predictor_tsv_file_one = averaging(predictor_tsv_file_one)
predictor_tsv_file_two = averaging(predictor_tsv_file_two)

# create list of doubles for scatter plot
amici_predictor_x = []          # red
amici_predictor_y = []
predictor_amici_x = []          # green
predictor_amici_y = []
equal_x = []                    # yellow
equal_y = []
amici_zero_x = []
amici_zero_y = []
predictor_zero_x = []
predictor_zero_y = []
equal_zero_x = []
equal_zero_y = []

for iModel in range(0, len(amici_tsv_file['t_intern_ms'])):
    # for second best success rate
    #if iModel in [3,8,13,18,23,28,33,38,43,48,53,58,63,68,73,78,83,88,93,98,103,108,113,118,123,128,133,138,143,148,153,158,163]:
     #   y_predictor_data = predictor_tsv_file_two['t_intern_ms'][iModel]
    #else:
    y_predictor_data = predictor_tsv_file_one['t_intern_ms'][iModel]
    x_amici_data = amici_tsv_file['t_intern_ms'][iModel]

    if x_amici_data != 0 and y_predictor_data != 0:
        if x_amici_data > y_predictor_data:
            predictor_amici_x.append(x_amici_data)
            predictor_amici_y.append(y_predictor_data)
        elif y_predictor_data > x_amici_data:
            amici_predictor_x.append(x_amici_data)
            amici_predictor_y.append(y_predictor_data)
        elif x_amici_data == y_predictor_data:
            equal_x.append(x_amici_data)
            equal_y.append(y_predictor_data)
    elif x_amici_data == 0 and y_predictor_data != 0:
        amici_zero_x.append(250)
        amici_zero_y.append(y_predictor_data)
    elif x_amici_data != 0 and y_predictor_data == 0:
        predictor_zero_x.append(x_amici_data)
        predictor_zero_y.append(250)
    elif x_amici_data == 0 and y_predictor_data == 0:
        equal_zero_x.append(250)
        equal_zero_y.append(250)


# plot a scatter plot + diagonal line
fontsize = 22
labelsize = 18
titlesize = 30

ax = plt.axes()
z = range(0,250)
plt1 = ax.scatter(amici_predictor_x, amici_predictor_y, s=70, c='red', label='Amici default setting is better than BDF_KLU_8_6: ' + str(round(len(amici_predictor_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %', zorder=10, clip_on=False)
plt2 = ax.scatter(predictor_amici_x, predictor_amici_y, s=70, c='blue', label='BDF_KLU_8_6 is better than Amicis default setting: ' + str(round(len(predictor_amici_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %', zorder=10, clip_on=False)
plt3 = ax.scatter(equal_x, equal_y, s=70,  c='grey', label='Both are equally good: ' + str(round(len(equal_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %', zorder=10, clip_on=False)
plt4 = ax.scatter(amici_zero_x, amici_zero_y, marker='D', s=120, facecolors='none', edgecolors='blue', label='Amici default failed to integrate the model: ' + str(round(len(amici_zero_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %', zorder=10, clip_on=False)
plt5 = ax.scatter(predictor_zero_x, predictor_zero_y, s=120, facecolors='none', edgecolors='red', marker='D', label='Prediction setting failed to integrate the model: ' + str(round(len(predictor_zero_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %', zorder=10, clip_on=False)
plt6 = ax.scatter(equal_zero_x, equal_zero_y, s=120, facecolors='none', edgecolors='grey', marker='D', label='Both failed to integrate the model: ' + str(round(len(equal_zero_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %', zorder=10, clip_on=False)
ax.plot(z)
ax.set_xlim([0.5, 250])
ax.set_ylim([0.5, 250])
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Amicis default simulation time [ms]', fontsize=titlesize, fontweight='bold')
ax.set_ylabel('BDF_KLU_8_6 simulation time [ms]', fontsize=titlesize, fontweight='bold')
ax.set_title('Amici default vs. BDF_KLU_8_6', fontsize=titlesize, fontweight='bold', pad=30)
ax.legend(loc=2, fontsize=labelsize - 6)
plt.tick_params(labelsize=labelsize)
plt.gca().set_aspect('equal', adjustable='box')

'''
leg = Legend(ax, [plt1, plt2, plt3, plt4, plt5, plt6], [str(round(len(amici_predictor_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %',
                                                        str(round(len(predictor_amici_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %',
                                                        str(round(len(equal_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %',
                                                        str(round(len(amici_zero_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %',
                                                        str(round(len(predictor_zero_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %',
                                                        str(round(len(equal_zero_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %'], loc='lower right', frameon=True)
ax.add_artist(leg)
'''

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
#plt.savefig('../bachelor_thesis/New_Figures/Figures_study_5/Predictor_vs_Amici_166SBML.pdf')

# show figure
plt.show()