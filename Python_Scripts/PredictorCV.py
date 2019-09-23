# predict the outcome for simulation worked, best 10% and best setting via cross validation

import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
from sklearn import utils
from Y_testing import *
from sklearn.model_selection import cross_validate
from sklearn import svm
from Sigmoid import *


# important paths
data_path = '../bachelor_thesis/SolverAlgorithm/Input_Output_Data_best_updated_divided.tsv'
save_path = '../bachelor_thesis/SolverAlgorithm/best_best_predictions_5_mixed_2.tsv'

# open data file
data_file = pd.read_csv(data_path, sep='\t')
all_columns = data_file.columns

# rename 'levchenko' for uniqueness
names = data_file['model']
for iModel in range(0, len(names)):
    if names[iModel] == '{levchenko2000_fig2-user}' and data_file['num_x'][iModel] == 31:
        names[iModel] = '{levchenko2000_fig2-user}_1'
    elif names[iModel] == '{levchenko2000_fig2-user}' and data_file['num_x'][iModel] == 22:
        names[iModel] = '{levchenko2000_fig2-user}_2'
data_file['model'] = names

# define Input and Output
X = data_file.drop('value',axis=1)
X = X.drop('model', axis=1)
Y = data_file.drop(all_columns[1:len(all_columns)-1], axis=1)
Y = Y.drop('model', axis=1)

#### output must be categorical values for logistic regression, e.g. integers !!! #####
if utils.multiclass.type_of_target(Y) != 'multiclass':
    lab_enc = preprocessing.LabelEncoder()
    Y_encoded = lab_enc.fit_transform(Y)
    print(utils.multiclass.type_of_target(Y.astype('int')))
    print(utils.multiclass.type_of_target(Y_encoded))


#### Prediction #########
df_list_X = []
df_list_Y = []
for iModel in range(0,166):
    df_list_X.append(X[iModel*40 : (iModel+1)*40])
    df_list_Y.append(Y[iModel*40 : (iModel+1)*40])

X_mixed_one = df_list_X[0]
X_mixed_two = df_list_X[1]
X_mixed_three = df_list_X[2]
X_mixed_four = df_list_X[3]
X_mixed_five = df_list_X[4]
Y_mixed_one = df_list_Y[0]
Y_mixed_two = df_list_Y[1]
Y_mixed_three = df_list_Y[2]
Y_mixed_four = df_list_Y[3]
Y_mixed_five = df_list_Y[4]
for iListModel in range(1,33):
    X_mixed_one = X_mixed_one.append(df_list_X[5*iListModel])
    X_mixed_two = X_mixed_two.append(df_list_X[5 * iListModel + 1])
    X_mixed_three = X_mixed_three.append(df_list_X[5 * iListModel + 2])
    X_mixed_four = X_mixed_four.append(df_list_X[5 * iListModel + 3])
    X_mixed_five = X_mixed_five.append(df_list_X[5 * iListModel + 4])
    Y_mixed_one = Y_mixed_one.append(df_list_Y[5 * iListModel])
    Y_mixed_two = Y_mixed_two.append(df_list_Y[5 * iListModel + 1])
    Y_mixed_three = Y_mixed_three.append(df_list_Y[5 * iListModel + 2])
    Y_mixed_four = Y_mixed_four.append(df_list_Y[5 * iListModel + 3])
    Y_mixed_five = Y_mixed_five.append(df_list_Y[5 * iListModel + 4])

# one time 34 models
X_mixed_five = X_mixed_five.append(df_list_X[165])
Y_mixed_five = Y_mixed_five.append(df_list_Y[165])

# split X and Y into five blocks for "manual" cross validation with nicely distributed models
X1 = X_mixed_one                # 40*33
X2 = X_mixed_two                # 40*33
X3 = X_mixed_three              # 40*33
X4 = X_mixed_four               # 40*33
X5 = X_mixed_five               # 40*34
Y1 = Y_mixed_one                # 40*33
Y2 = Y_mixed_two                # 40*33
Y3 = Y_mixed_three              # 40*33
Y4 = Y_mixed_four               # 40*33
Y5 = Y_mixed_five               # 40*34

'''
X1 = X[:1320]               # 40*33
X2 = X[1320:2640]           # 40*33
X3 = X[2640:3960]           # 40*33
X4 = X[3960:5280]           # 40*33
X5 = X[5280:]               # 40*34
Y1 = Y_encoded[:1320]       # 40*33
Y2 = Y_encoded[1320:2640]   # 40*33
Y3 = Y_encoded[2640:3960]   # 40*33
Y4 = Y_encoded[3960:5280]   # 40*33
Y5 = Y_encoded[5280:]       # 40*34
'''

# joining data frames
V1 = X1.append(X2).append(X3).append(X4)
V2 = X1.append(X3).append(X4).append(X5)
V3 = X1.append(X2).append(X4).append(X5)
V4 = X1.append(X2).append(X3).append(X5)
V5 = X2.append(X3).append(X4).append(X5)
W1 = np.concatenate((Y1, Y2, Y3, Y4))
W2 = np.concatenate((Y1, Y3, Y4, Y5))
W3 = np.concatenate((Y1, Y2, Y4, Y5))
W4 = np.concatenate((Y1, Y2, Y3, Y5))
W5 = np.concatenate((Y2, Y3, Y4, Y5))

# list of all permutations
first_batch = [V1, X5, W1, Y5]                                                                      # [X-Train, X-Test, Y-Train, Y-Test]
second_batch = [V2, X2, W2, Y2]
third_batch = [V3, X3, W3, Y3]
fourth_batch = [V4, X4, W4, Y4]
fifth_batch = [V5, X1, W5, Y1]

All_permutations = [first_batch, second_batch, third_batch, fourth_batch, fifth_batch]

# amount of cross validations
cv = 5

####### logistic regression #######
# create whole + final data frame
whole_df = pd.DataFrame(columns=['model', 'first', 'second', 'third', 'fourth', 'fifth'], data=[])
final_df = pd.DataFrame(columns=['model', 'average'], data=[])
whole_df['model'] = data_file['model']
final_df['model'] = data_file['model']

# prediction
clf = []
for iCrossValidation in range(0, cv):
    X_training = All_permutations[iCrossValidation][0]
    X_testing = All_permutations[iCrossValidation][1]
    Y_training = All_permutations[iCrossValidation][2]
    Y_testing = All_permutations[iCrossValidation][3]
    clf.append(LogisticRegression())
    Fit = clf[iCrossValidation].fit(X_training, Y_training)
    ExpSigmoid = Fit.decision_function(X_testing)

    df_results = valuesSigmoid(ExpSigmoid)

    # assign values
    list_of_series = []
    if iCrossValidation == 0:
        list_of_series.append(df_results['h(x)'])
        list_of_series.append(pd.Series(np.zeros(6640 - len(df_results['h(x)']))))
        list_reindexed = pd.concat(list_of_series).reset_index(drop=True)
        whole_df['first'] = list_reindexed
    elif iCrossValidation == 1:
        list_of_series.append(df_results['h(x)'][:1320])
        list_of_series.append(pd.Series(np.zeros(6640 - len(df_results['h(x)']))))
        list_of_series.append(df_results['h(x)'][1320:])
        list_reindexed = pd.concat(list_of_series).reset_index(drop=True)
        whole_df['second'] = list_reindexed
    elif iCrossValidation == 2:
        list_of_series.append(df_results['h(x)'][:2640])
        list_of_series.append(pd.Series(np.zeros(6640 - len(df_results['h(x)']))))
        list_of_series.append(df_results['h(x)'][2640:])
        list_reindexed = pd.concat(list_of_series).reset_index(drop=True)
        whole_df['third'] = list_reindexed
    elif iCrossValidation == 3:
        list_of_series.append(df_results['h(x)'][:3960])
        list_of_series.append(pd.Series(np.zeros(6640 - len(df_results['h(x)']))))
        list_of_series.append(df_results['h(x)'][3960:])
        list_reindexed = pd.concat(list_of_series).reset_index(drop=True)
        whole_df['fourth'] = list_reindexed
    elif iCrossValidation == 4:
        list_of_series.append(pd.Series(np.zeros(6640 - len(df_results['h(x)']))))
        list_of_series.append(df_results['h(x)'])
        list_reindexed = pd.concat(list_of_series).reset_index(drop=True)
        whole_df['fifth'] = list_reindexed


##### average each model #####
for iRow in range(0, len(whole_df['model'])):
    average = (whole_df['first'][iRow] + whole_df['second'][iRow] + whole_df['third'][iRow] + whole_df['fourth'][iRow] + whole_df['fifth'][iRow])/4
    final_df['average'][iRow] = average

#### best of each model + index #####
best_df = pd.DataFrame(columns=['model', '{best}_{index}', '{second}_{index}', '{third}_{index}', '{fourth}_{index}', '{fifth}_{index}'], data=[])
amici = []
for iModel in range(0,166):
    best_df = best_df.append({}, ignore_index=True)
    some_model = final_df['average'][iModel*40 : (iModel+1)*40]
    best_df['model'][iModel] = final_df['model'][iModel*40]
    best_df['{best}_{index}'][iModel] = '{' + str(sorted(list(final_df['average'][iModel * 40: (iModel + 1) * 40]), reverse=True)[0]) + \
                                        '}_{' + str((np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))[len(np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))) - 1]) % 40) + '}'
    best_df['{second}_{index}'][iModel] = '{' + str(sorted(list(final_df['average'][iModel * 40: (iModel + 1) * 40]), reverse=True)[1]) + \
                                        '}_{' + str((np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))[len(np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))) - 2]) % 40) + '}'
    best_df['{third}_{index}'][iModel] = '{' + str(sorted(list(final_df['average'][iModel * 40: (iModel + 1) * 40]), reverse=True)[2]) + \
                                        '}_{' + str((np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))[len(np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))) - 3]) % 40) + '}'
    best_df['{fourth}_{index}'][iModel] = '{' + str(sorted(list(final_df['average'][iModel * 40: (iModel + 1) * 40]), reverse=True)[3]) + \
                                        '}_{' + str((np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))[len(np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))) - 4]) % 40) + '}'
    best_df['{fifth}_{index}'][iModel] = '{' + str(sorted(list(final_df['average'][iModel * 40: (iModel + 1) * 40]), reverse=True)[4]) + \
                                        '}_{' + str((np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))[len(np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))) - 5]) % 40) + '}'

    amici.append('{' + str(sorted(list(final_df['average'][iModel * 40: (iModel + 1) * 40]), reverse=True)[10]) + \
                                        '}_{' + str((np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))[len(np.argsort(list(final_df['average'][iModel * 40: (iModel + 1) * 40]))) - 11]) % 40) + '}')
    #best_df['best'][iModel] = sorted(list(final_df['average'][iModel*40 : (iModel+1)*40]), reverse=True)[0]
    #best_df['index'][iModel] = (np.argsort(list(final_df['average'][iModel*40 : (iModel+1)*40]))[len(np.argsort(list(final_df['average'][iModel*40 : (iModel+1)*40]))) - 1]) % 40

save = 1
#### save tsv file #####
best_df.to_csv(save_path, sep='\t', index=False)

#test_score = clf[iCrossValidation].predict(X_testing)            #(train_score > test_score)
