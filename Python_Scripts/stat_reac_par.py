# script to get states, reactions and parameters of all imported sbml models with correct state trajectories

import pandas as pd
from execute_loadModels import *
import os
import libsbml

# create data frame
tsv_table = pd.DataFrame(columns=['id', 'states', 'reactions', 'parameters'])

# important paths
import_path = '../sbml2amici/amici_models'
correct_path = '../sbml2amici/correct_amici_models'
save_path = '../sbml2amici'

# set counter
counter = 0

# list of all directories + SBML files
list_directory_amici = sorted(os.listdir(import_path))       # (import_path)

for iModel in list_directory_amici:

    list_directory_sbml = sorted(os.listdir(import_path + '/' + iModel))     # (import_path)

    for iFile in list_directory_sbml:

        # Append additional row in .tsv file
        tsv_table = tsv_table.append({}, ignore_index=True)

        if os.path.exists('./BioModelsDatabase_models/' + iModel + '/sbml_models/' + iFile + '.xml'):
            if iModel == 'Leloup1999':
                #counter = counter + 1
                continue
            # open .xml file
            xml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.xml'
            sbml_file = libsbml.readSBML(xml_path)
        else:
            # open .sbml file
            sbml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.sbml'
            sbml_file = libsbml.readSBML(sbml_path)

        # reactions
        all_properties = sbml_file.getModel()
        num_reactions = len(all_properties.getListOfReactions())

        # states + parameters
        try:
            model = all_settings(iModel, iFile)
        except:
            #counter = counter + 1
            continue
        num_states = len(model.getStateNames())
        num_parameters = len(model.getParameters())

        # Fill in data frame
        tsv_table.loc[counter].id = '{' + iModel + '}_{' + iFile + '}'
        tsv_table.loc[counter].states = num_states
        tsv_table.loc[counter].reactions = num_reactions
        tsv_table.loc[counter].parameters = num_parameters

        # raise counter
        counter = counter + 1

# save data frame
tsv_table.to_csv(path_or_buf=save_path + '/NEW_stat_reac_par_447SBML.tsv', sep='\t', index=False)