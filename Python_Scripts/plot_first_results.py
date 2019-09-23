# plot a bar plot for num_states and num_species
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mplt
#import seaborn as sns

# open two .tsv file
path = '../sbml2amici/NEW_stat_reac_par_447SBML.tsv'
tsv_file = pd.read_csv(path, sep='\t')

# no BioModels yet + delete nans at the end
tsv_file = tsv_file[27:423]
tsv_file = tsv_file.reset_index()
del tsv_file['index']


# take number of states for those models that worked
data_states_ok = []
for iLine in range(0, len(tsv_file['id'])):
    data_states_ok.append(tsv_file['states'][iLine])                 # no 'ignore_index=True' permitted

# take number of reactions for those models that worked
data_reactions_ok = []
for iLine in range(0, len(tsv_file['id'])):
    data_reactions_ok.append(tsv_file['reactions'][iLine])

# take number of parameters for those models that worked
data_parameters_ok = []
for iLine in range(0, len(tsv_file['id'])):
    data_parameters_ok.append(tsv_file['parameters'][iLine])


# histogram of states
fontsize = 18
labelsize = 16

# plots
plt.subplot(3,1,1)
# add title
#plt.title('Basic properties of all models', fontsize=20)
plot1 = plt.hist(x=data_states_ok, range=[0,100], bins=200, log=True) # range=[0,250],

#plt.xscale('log')
plt.xlim((None, 100)) #250 #100                                                                       # Froehlich2018: 1396
plt.ylim((None, 100))
plt.xlabel('Number of state variables', fontsize=fontsize, fontweight='bold')
plt.ylabel('Amount of models', fontsize=fontsize, fontweight='bold')
plt.tick_params(labelsize=labelsize)

# histogram of reactions
plt.subplot(3,1,2)
plot2 = plt.hist(x=data_reactions_ok, range=[0,100], bins=200, log=True) # range=[0,600],
#plt.xscale('log')
plt.xlim((None, 100)) #600 #100                                                                       # Froehlich2018: 2686
plt.ylim((None, 100))
plt.xlabel('Number of reactions', fontsize=fontsize, fontweight='bold')
plt.ylabel('Amount of models', fontsize=fontsize, fontweight='bold')
plt.tick_params(labelsize=labelsize)

# histogram of parameters
plt.subplot(3,1,3)
plot3 = plt.hist(x=data_parameters_ok, range=[0,350], bins=200, log=True) # range=[0,350],
#plt.xscale('log')
plt.xlim((None, 350)) #350 #1000                                                                       # Froehlich2018: 4704
plt.ylim((None, 100))
plt.xlabel('Number of parameters',  fontsize=fontsize, fontweight='bold')
plt.ylabel('Amount of models', fontsize=fontsize, fontweight='bold')
plt.tick_params(labelsize=labelsize)

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
#plt.savefig('../bachelor_thesis/New_Figures/Figures_study_1/stat_reac_par_447SBML_ylog.pdf')

# show figure
plt.show()