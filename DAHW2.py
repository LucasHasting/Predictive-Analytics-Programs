#Name: Lucas Hasting
#Class: DA 460
#Date: 10/1/2025
#Instructor: Dr. Imbrogno
#Description: Python work for HW#2

import pandas as pd

#formula for min/max normalization
def min_max_normalization(x, old_min, old_max, new_min, new_max):
    return ((x - old_min) / (old_max - old_min) * (new_max - new_min) + new_min)

#formula for z-score normalization
def z_score_normalization(x, mean, s):
    return (x - mean) / (s)

#formula for supremum distance
def supremum_distance(lst1, lst2): #len(lst1) = len(lst2)
    distances = []
    for i in range(len(lst1)):
        distances.append(abs(lst1[i] - lst2[i]))
    return max(distances)

#formula for manhattan distance
def manhattan_distance(lst1, lst2): #len(lst1) = len(lst2)
    distances = []
    for i in range(len(lst1)):
        distances.append(abs(lst1[i] - lst2[i]))
    return sum(distances)

#formula for euclidean distance
def euclidean_distance(lst1, lst2): #len(lst1) = len(lst2)
    distances = []
    for i in range(len(lst1)):
        distances.append((lst1[i] - lst2[i])**2)
    return (sum(distances))**(1/2)

#function used to cleanly print a matrix
def print_matrix(matrix):
    for i in matrix:
        for j in i:
            print(f"{j:.2f}", end='\t')
        print()
    print()

#----Question #1 - min/max normalization, range: [0, 1]
print("--Question #1:")

#get data
df = pd.DataFrame({'Age': [25, 57, 38, 48, 23, 37],
                   'Income': [49000, 118000, 89000,
                              33500, 52000, 44000]})

#get old min/old max of Age and Income
age_min = df['Age'].min()
age_max = df['Age'].max()
income_min = df['Income'].min()
income_max = df['Income'].max()

#the solution
print("Age:")
for x in df['Age'].values.tolist():
    print(f"{min_max_normalization(x, age_min, age_max, 0, 1):.2f}")
print()

print("Income:")
for x in df['Income'].values.tolist():
    print(f"{min_max_normalization(x, income_min, income_max, 0, 1):.2f}")

print()

#----Question #2 - imputing
print("--Question #2:")

#get data - renamed file to convenience
df = pd.read_excel("Homework-2-Excel.xlsx", sheet_name=0)

#filter for gender = M and hair color = PURPLE
df_male = df[df['Gender'] == 'M']
df_purple = df[df['Hair Color'] == 'PURPLE']

#solution
print(f"Mean of non-missing values: {df['Salary'].mean():.2f}") 
print(f"Median of non-missing values: {df['Salary'].median():.2f}")
print(f"Mean of non-missing values where gender = M: {df_male['Salary'].mean():.2f}")
print(f"Mean of non-missing values where hair color = PURPLE: {df_purple['Salary'].mean():.2f}")
print()

#----Question #3 - more normalization
print("--Question #3:")

#get data
df = pd.DataFrame({'X': [288,304,806,471,609,1113,677,532]})

#find old min/old max, mean, and standard deviation
X_min = df['X'].min()
X_max = df['X'].max()
X_mean = df['X'].mean()
X_s = df['X'].std()

#solution
print("X (data value) - min/max:")
for x in df['X'].values.tolist():
    print(f"{min_max_normalization(x, X_min, X_max, 500, 2500):.2f}")
print()

print("X (data value) - z-score:")
for x in df['X'].values.tolist():
    print(f"{z_score_normalization(x, X_mean, X_s):.2f}")
print()

#----Question #4 - dissimilarity matrices
print("--Question #4:")

#create data matrix
data_matrix = [[5,11,3,10],
               [12,3,8,3],
               [7,14,9,5],
               [13,2,9,9],
               [6,14,10,7],
               [11,10,5,5]]

#init matrix used to store the result
result_matrix = []
for i in range(len(data_matrix)):
    result_matrix.append([])
    for j in range(len(data_matrix)):
        result_matrix[i].append(0)

#solution
print("Supremum Distance:")
for i in range(len(data_matrix)):
    for j in range(len(data_matrix)):
        result_matrix[i][j] = supremum_distance(data_matrix[i],data_matrix[j])
print_matrix(result_matrix)

print("Manhattan Distance:")
for i in range(len(data_matrix)):
    for j in range(len(data_matrix)):
        result_matrix[i][j] = manhattan_distance(data_matrix[i],data_matrix[j])
print_matrix(result_matrix)

print("Euclidean Distance:")
for i in range(len(data_matrix)):
    for j in range(len(data_matrix)):
        result_matrix[i][j] = euclidean_distance(data_matrix[i],data_matrix[j])
print_matrix(result_matrix)
