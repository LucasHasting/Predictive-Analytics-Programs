#Name: Lucas Hasting
#Class: DA 460
#Date: 9/22/2025
#Instructor: Dr. Imbrogno
#Description: Python work for HW#1, did not use excel

import pandas as pd
import math

#information gain formula
def information_gain(A, B, C, D):
    if(A == 0 and B == 0 and C == 0 and D == 0):
        return 0
    return (f((A+C),(B+D)) - f(A,B) - f(C,D))/(A + B + C + D)

#function used for information gain
def f(X, Y):
    if(X == 0 or Y == 0):
        return 0
    return X*math.log((X+Y)/X,2) + Y*math.log((X+Y)/Y,2)

#get's the split information and outputs to user
def check_split(df, col, var):
    temp = df[df["Play?"] == "PLAYED"]
    temp = temp[temp[col] == var]
    print(f"{col} = {var}, yes, played: {temp['Outlook'].size}")

    temp = df[df["Play?"] == "DID NOT PLAY"]
    temp = temp[temp[col] == var]
    print(f"{col} = {var}, yes, not played: {temp['Outlook'].size}")

    temp = df[df["Play?"] == "PLAYED"]
    temp = temp[temp[col] != var]
    print(f"{col} = {var}, no, played: {temp['Outlook'].size}")

    temp = df[df["Play?"] == "DID NOT PLAY"]
    temp = temp[temp[col] != var]
    print(f"{col} = {var}, no, not played: {temp['Outlook'].size}")

    print()

#get DT regression info
def check_split_regress(df, col, var, eq):
    #get data for yes
    if(eq):
        obs1 = df[df[col] == var]
    else:
        obs1 = df[df[col] > var]
    obs1 = obs1["outcome"].astype(float)
    size1 = obs1.size
    mean1 = obs1.mean()

    #get data for no
    if(eq):
        obs2 = df[df[col] != var]
    else:
        obs2 = df[df[col] <= var]
    obs2 = obs2["outcome"]
    size2 = obs2.size
    mean2 = obs2.mean()

    #get SSE for yes
    obs1 = obs1 - mean1 #error
    obs1 = obs1 * obs1 #squared error
    sse1 = sum(obs1) #sum squared error

    #get SSE for no
    obs2 -= mean2 #error
    obs2 = obs2 * obs2 #squared error
    sse2 = sum(obs2) #sum squared error

    if(eq):
        print(f"{col} = {var}, size: {size1}, mean: {mean1}, sse: {sse1}")
    else:
        print(f"{col} > {var}, size: {size1}, mean: {mean1}, sse: {sse1}")

    if(eq):
        print(f"{col} != {var}, size: {size2}, mean: {mean2}, sse: {sse2}")
    else:
        print(f"{col} <= {var}, size: {size2}, mean: {mean2}, sse: {sse2}")
    print(f"Total SSE: {sse1 + sse2}")
    print()


#Number 4 - split info

#renamed file to convenience
df = pd.read_excel("Homework-1-Excel.xlsx", sheet_name=0) 

print("--Number 4:")
check_split(df, "Outlook", "Rain")
check_split(df, "Outlook", "Sunny")
check_split(df, "Outlook", "Overcast")
check_split(df, "Temperature", "Hot")
check_split(df, "Temperature", "Mild")
check_split(df, "Temperature", "Cool")
check_split(df, "Windy", True)
check_split(df, "Windy", False)

#Number 6 - info gain on rain
print("--Number 6:")
print(f"f(20, 13) = {f(20, 13)}")
print(f"f(4, 8) = {f(4, 8)}")
print(f"f(16, 5) = {f(16, 5)}")
print(f"IG(4, 8, 16, 5) = {information_gain(4, 8, 16, 5)}")
print()

#Number 7 - rain split info
df = df[df["Outlook"] == "Rain"]

print("--Number 7:")
check_split(df, "Outlook", "Rain")
check_split(df, "Outlook", "Sunny")
check_split(df, "Outlook", "Overcast")
check_split(df, "Temperature", "Hot")
check_split(df, "Temperature", "Mild")
check_split(df, "Temperature", "Cool")
check_split(df, "Windy", True)
check_split(df, "Windy", False)

#Number 8/9/10 - checking gain
print("--Number 8/9/10:")
print(f"IG(4, 8, 0, 0) = {information_gain(4, 8, 0, 0)}")
print(f"IG(0, 0, 4, 8) = {information_gain(0, 0, 4, 8)}")
print(f"IG(4, 5, 8, 1) = {information_gain(4, 5, 8, 1)}")
print(f"IG(9, 2, 3, 4) = {information_gain(9, 2, 3, 4)}")
print(f"IG(4, 2, 8, 4) = {information_gain(4, 2, 8, 4)}")
print(f"IG(7, 0, 5, 6) = {information_gain(7, 0, 5, 6)}")
print(f"IG(4, 0, 0, 4) = {information_gain(4, 0, 0, 4)}")
print()

#Number 11 - regression decession tree split
print("--Number 11:")
df = pd.read_excel("Homework-1-Excel.xlsx", sheet_name=1)
check_split_regress(df, "Var1", "yes", True)
check_split_regress(df, "Var2", "up", True)
check_split_regress(df, "Var3", 19, False)
check_split_regress(df, "Var3", 16, False)
check_split_regress(df, "Var3", 13, False)
