#Name: Lucas Hasting
#Class: DA 460
#Date: 11/12/2025
#Instructor: Dr. Imbrogno
#Description: Python work for HW#4, did not use excel

#libaries
import pandas as pd
import math
import warnings 
warnings.filterwarnings('ignore')

#formula for euclidean distance
def euclidean_distance(lst1, lst2): #len(lst1) = len(lst2)
    distances = []
    for i in range(len(lst1)):
        distances.append((lst1[i] - lst2[i])**2)
    return (sum(distances))**(1/2)

#formula for match distance (assume nominal)
def match_distance(lst1, lst2): #len(lst1) = len(lst2)
    distances = []
    count = 0
    for i in range(len(lst1)):
        if(lst1[i] == lst2[i]):
            count += 1
    return len(lst1) - count

#formula for weighted mean
def weighted_mean(x, w):
    return sum([x[i]*w[i] for i in range(len(x))]) / sum(w)

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
    return prediction

#function to make a prediction using k-nn regression
def knn_regression(df, outcome, Obs, n, b, test):
    #get outcome list and obs list used for pridictions
    outcomes = df[outcome].to_list()
    obs = df[Obs].to_list()

    #drop outcome and obs columns before distance is checked
    df = df.drop(outcome, axis=1)
    df = df.drop(Obs, axis=1)

    #list to keep up with distance
    weights = []
        
    #loop through df
    for i in range(len(outcomes)):
        row = df.iloc[i]
        row = row.to_list()

        #store weight of each obs 
        weights.append(round(math.exp(-match_distance(row, test) / b),2))

    #return weighted mean as prediction
    return weighted_mean(outcomes, weights)

#function used to find best k with loccov
def loccov(df, outcome, Obs, n):
    #init accuracys and k
    k = 1
    accuracy = []

    #loop for values of k
    while(k < n):
        #keep track of correct predictions
        correct = 0
        
        for i in range(n):
            #keep copy of original
            origin = df.copy()
            original_predictor = df.iloc[i]
            
            #leave one out (LOO)
            predictor = df.iloc[i]
            predictor.pop(Obs)
            predictor.pop(outcome)
            predictor = predictor.to_list()
            predictor = [x.item() for x in predictor]
            df = df.drop(i)

            #test on LOO
            prediction = knn(df, outcome, Obs, k, predictor)
            predictor = original_predictor
            
            #if LOO is good, increase correct prediction count
            if(predictor[outcome] == prediction):
                correct += 1

            #put obs back in
            df = origin

        #keep track of k accuracy
        accuracy.append(correct/(n-1))

        #increment k
        k += 2

    #returns the accuracy list, best accuracy, and best k 
    return accuracy, max(accuracy), (accuracy.index(max(accuracy))*2)+1

#function to make use of bayes theorem to find probabilities
def bayes(df, outcome, Obs, test, col, clas):
    #init variables
    prob = 0
    num = 0

    for i in df[outcome].unique():
        #get P(C_i)
        P_C = df[outcome].value_counts()[i] / len(df)

        #get P(X | C_i)
        origin = df.copy()
        df = df[df[outcome] == i]
        for j in range(len(test)):
            P_C *= df[col[j]].value_counts()[test[j]] / len(df)
        df = origin

        #get numerator
        if(clas == i):
            num = P_C

        #sum of P(X | C_i)
        prob += P_C
    
    #return the probability
    return num/prob

#---------------

#file was renamed and modified for convience (submitted in canvas)
#some values were placed manually in the python script (moved from excel -> python script)

#--------QUESTION #1
print("--QUESTION #1:")

#get data
df = pd.read_excel("Homework-4-Excel.xlsx", sheet_name=0,skiprows=1)

#use loccov function to find best k
acc, result, k = loccov(df,"color","Obs",20)

#show all k accuracy and best k
for i in range(len(acc)):
    print(f"k={2*i+1}: {round(acc[i]*100, 2)}")
print()
print(f"Best k: k={k} with accuracy {round(result*100, 2)}")
print()

#--------QUESTION #2
#get data
df = pd.read_excel("Homework-4-Excel.xlsx", sheet_name=1,skiprows=1)

#used to store predictions
predictions = []
counter = 0

#use knn regression to make predictions and append to preditctions list for QUESTION #3
print("--QUESTION #2:")
for i in range(1, 6, 2):
    predictions.append([])
    prediction = knn_regression(df,"outcome","Obs",25,i,["yes","up","right","medium","in"])
    predictions[counter].append(prediction)
    print(f"prediction #1, b = {i}, outcome = {prediction:.2f}")
    prediction = knn_regression(df,"outcome","Obs",25,i,["yes","down","left","low","out"])
    predictions[counter].append(prediction)
    print(f"prediction #2, b = {i}, outcome = {prediction:.2f}")
    prediction = knn_regression(df,"outcome","Obs",25,i,["no","down","left","low","out"])
    predictions[counter].append(prediction)
    print(f"prediction #3, b = {i}, outcome = {prediction:.2f}")
    prediction = knn_regression(df,"outcome","Obs",25,i,["no","down","right","medium","in"])
    predictions[counter].append(prediction)
    print(f"prediction #4, b = {i}, outcome = {prediction:.2f}")
    prediction = knn_regression(df,"outcome","Obs",25,i,["yes","down","right","high","out"])
    predictions[counter].append(prediction)
    print(f"prediction #5, b = {i}, outcome = {prediction:.2f}")
    prediction = knn_regression(df,"outcome","Obs",25,i,["no","up","left","high","in"])
    predictions[counter].append(prediction)
    print(f"prediction #6, b = {i}, outcome = {prediction:.2f}")
    counter += 1
    
print()

#--------QUESTION #3

#predictions found in QUESTION #2
print("--QUESTION #3:")

#store actual for each obs
actual = [17.2,16.4,14.8,17.3,16.9,19.1]
SSEs = []

#get SSE to find best b
for i in predictions:
    #used to store current SSE
    SSE = 0
    for j in range(len(i)):
        #sum squared error
        SSE += (actual[j] - i[j])**2
    #add SSE to SSE list
    SSEs.append(round(SSE,2))

#display SSEs
for i in range(len(SSEs)):
    print(f"SSE for b={2*i+1}: {SSEs[i]}")
print()

#--------QUESTION #4
print("--QUESTION #4:")
df = pd.read_excel("Homework-4-Excel.xlsx", sheet_name=2,skiprows=1)

#store test observations
obs = [["yes","up","right","on","high"],
       ["yes","down","right","on","medium"],
       ["no", "up", "left", "on", "medium"],
       ["no", "up", "right", "off", "low"],
       ["yes", "down", "left", "off", "high"]
      ]

#get prob of every class for each obs using bayes theorem
counter = 1
for test in obs:
    print(f"prediction #{counter}")
    print(f'red: {round(bayes(df,"outcome","Obs",test,["x1","x2","x3","x4","x5"], "red")*100,2)}')
    print(f'blue: {round(bayes(df,"outcome","Obs",test,["x1","x2","x3","x4","x5"], "blue")*100,2)}')
    print(f'purple: {round(bayes(df,"outcome","Obs",test,["x1","x2","x3","x4","x5"], "purple")*100,2)}')
    print()
    counter += 1
