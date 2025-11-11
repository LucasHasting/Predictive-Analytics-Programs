#Name: Lucas Hasting
#Class: DA 460
#Date: 10/20/2025
#Instructor: Dr. Imbrogno
#Description: Python work for HW#3

#libraries and suppress deprecation warning (don't care)
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

#formula for min/max normalization
def min_max_normalization(x, old_min, old_max, new_min, new_max):
    return ((x - old_min) / (old_max - old_min) * (new_max - new_min) + new_min)

#formula for euclidean distance
def euclidean_distance(lst1, lst2): #len(lst1) = len(lst2)
    distances = []
    for i in range(len(lst1)):
        distances.append((lst1[i] - lst2[i])**2)
    return (sum(distances))**(1/2)

#function to make a prediction using k-nn
def knn(df, outcome, Obs, n, test):
    #get outcome list and obs list used for pridictions
    outcomes = df[outcome].to_list()
    outcomes_result = []

    obs = df[Obs].to_list()
    obs_result = []

    #drop outcome and obs columns before distance is checked
    df = df.drop(outcome, axis=1)
    df = df.drop(Obs, axis=1)
    
    #loop n (k) times
    for i in range(n):

        #list to keep up with distance
        distance = []
        
        #loop through df
        for i in range(len(outcomes)):
            row = df.iloc[i]
            row = row.to_list()

            #store distance from test obs
            distance.append(euclidean_distance(row, test))

        #store obs and outcome for smallest distance 
        min_value = min(distance)
        to_remove = distance.index(min_value)
        
        outcomes_result.append(outcomes[to_remove])
        outcomes.pop(to_remove)
        
        obs_result.append(obs[to_remove])
        obs.pop(to_remove)

        #remove obs with closest distance
        df = df.iloc[df.index != to_remove]

    #get obs with highest count, that is the prediction
    prediction = max(set(outcomes_result), key=outcomes_result.count)

    #display the outcome and observations - parallel list
    print(outcomes_result, obs_result)
    return prediction


#----Question #2: KNN
print("----Question 2:")
df = pd.read_excel("Homework-3-Excel.xlsx", sheet_name=0,skiprows=1)

#get dummies for nominal data
df = pd.get_dummies(df, columns=['x1'], prefix='x1', dtype=int)
df = pd.get_dummies(df, columns=['x2'], prefix='x2', dtype=int)
df = pd.get_dummies(df, columns=['x3'], prefix='x3', dtype=int)

#get orderings for ordinal data, get to 0,1 range (range of all other values)
mapping = {'low': 0, 'medium': 1, 'high': 2}
df['x4'] = df['x4'].replace(mapping)
lst = df['x4'].to_list()
old_max = max(lst)
old_min = min(lst)
lst = [min_max_normalization(x, old_min, old_max, 0, 1) for x in lst]
df['x4'] = pd.DataFrame(lst)

#normalize x5 to 0, 1 range (range of all other values)
lst = df['x5'].to_list()
old_max = max(lst)
old_min = min(lst)
lst = [min_max_normalization(x, old_min, old_max, 0, 1) for x in lst]
df['x5'] = pd.DataFrame(lst)

#get testing data and repeat process
test = df.loc[:, 'x1.1':'x5.1']
test = test.drop(range(5,25))

#get dummies for nominal data
test = pd.get_dummies(test, columns=['x1.1'], prefix='x1', dtype=int)
test = pd.get_dummies(test, columns=['x2.1'], prefix='x2', dtype=int)
test = pd.get_dummies(test, columns=['x3.1'], prefix='x3', dtype=int)

#get orderings for ordinal data, get to 0,1 range (range of all other values)
mapping = {'low': 0, 'medium': 1, 'high': 2}
test['x4.1'] = df['x4.1'].replace(mapping)
lst = test['x4.1'].to_list()
old_max = max(lst)
old_min = min(lst)
lst = [min_max_normalization(x, old_min, old_max, 0, 1) for x in lst]
test['x4.1'] = pd.DataFrame(lst)

#normalize x5 to 0, 1 range (range of all other values)
lst = test['x5.1'].to_list()
old_max = max(lst)
old_min = min(lst)
lst = [min_max_normalization(x, old_min, old_max, 0, 1) for x in lst]
test['x5.1'] = pd.DataFrame(lst)

#drop testing data from training data, drop prediction column, drop unnamed columns
df = df.drop('x1.1', axis=1)
df = df.drop('x2.1', axis=1)
df = df.drop('x3.1', axis=1)
df = df.drop('x4.1', axis=1)
df = df.drop('x5.1', axis=1)
df = df.drop('prediction', axis=1)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

#get predictions for test data
for i in range(5):
    print(knn(df, "outcome", 'Obs', 3, test.iloc[i].to_list()))
    print()

#----Question #3: K-NN but again
print()
print("----Question 3:")
df = pd.read_excel("Homework-3-Excel.xlsx", sheet_name=1)

#get dummies for nominal data
df = pd.get_dummies(df, columns=['x1'], prefix='x1', dtype=int)
df = pd.get_dummies(df, columns=['x3'], prefix='x3', dtype=int)
df = pd.get_dummies(df, columns=['x4'], prefix='x4', dtype=int)
df = pd.get_dummies(df, columns=['x5'], prefix='x5', dtype=int)
df = pd.get_dummies(df, columns=['x6'], prefix='x6', dtype=int)

#get orderings for ordinal data, get to 0,1 range (range of all other values)
mapping = {'light': 0, 'medium': 1, 'heavy': 2}
df['x2'] = df['x2'].replace(mapping)
lst = df['x2'].to_list()
old_max = max(lst)
old_min = min(lst)
lst = [min_max_normalization(x, old_min, old_max, 0, 1) for x in lst]
df['x2'] = pd.DataFrame(lst)

#converted test data to numerical data based on the rules above
#'x2', 'x1_off', 'x1_on', 'x3_bad', 'x3_good', 'x4_above',
#'x4_below', 'x5_center', 'x5_left', 'x5_right', 'x6_down', 'x6_up'
test = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0]

#get predictions for test data
for i in range(1, 8, 2):
    print(knn(df, "outcome", 'Obs', i, test))
    print()
