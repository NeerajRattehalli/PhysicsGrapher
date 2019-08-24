# Importing the libraries
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from fractions import Fraction
import sys

error = 0.05

def extract_data_txt(filepath):
    with open(filepath) as fp:
       lines = fp.readlines()
       
    lines = [line[:-1] for line in lines]
    
    for i in range(len(lines)):
        if i > 1:
            lines[i] = float(lines[i])
    
    return lines
    
def convert_to_csv(file_current, file_csv, count):
    with open(file_current) as fp:
        lines = fp.readlines()

    with open(file_csv, 'w') as writeFile:
        for i in range(int(len(lines)/2)):
            row = lines[2*i][:-1] + ", " + lines[2*i+1]
            writeFile.write(row)
            
def getTitles(file_csv):
    with open(file_csv, 'r') as readFile:
        line = readFile.readline()
        part1, part2 = line.split(",")
        x_axis, x_unit = part1.split()
        y_axis, y_unit = part2.split()
        return [x_axis, x_unit[1:-1], y_axis, y_unit[1:-1]]
    
def getData(file_csv):
    dataset = pd.read_csv(file_csv)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1].values
    return X, y

def getTransformX(X, relation):
    for element in X:
        element[0] = element[0]**relation
    return X

def regression(X, y):
    return LinearRegression().fit(X, y)

def errorFunc(X, y, regressor):
    mae_sum = 0
    for i in range(len(X[0])):
        prediction = regressor.predict([[X[0][i]]])
        mae_sum += abs(y[i] - prediction)
    return mae_sum
        
        
def findBestLinearModel(X_orig, y, low_range, high_range):
    min_error = sys.maxsize
    bestPolynomial = low_range
    for i in range(low_range, high_range):
        if (i!=0):
            X = X_orig[:]
            print(id(X), id(X_orig))
            X = getTransformX(X, i)
            lm = regression(X, y)
            error = errorFunc(X, y, lm)
            if (error<min_error):
                min_error = error
                bestPolynomial = i
        print(X_orig, "\n\n\n", X)
    for i in range(low_range, high_range):
        if (i!=0):
            X = getTransformX(X_orig[:], 1/i)
            print(X)
            lm = regression(X, y)
            error = errorFunc(X, y, lm)
            if (error<min_error):
                min_error = error
                bestPolynomial = 1/(i)
        print(X)
    return regression(getTransformX(X_orig, bestPolynomial), y), bestPolynomial
                      
def getYSpread(y):
    return max(y) - min(y)

def getLineEquation(regressor, error, y_spread, titles, relation):
    slope = regressor.coef_[0]
    intercept = regressor.intercept_
    slope_error = slope*error
    intercept_error = y_spread*error
    equation = titles[2] + " = (" +  str(round(slope, 2)) + " $\pm$" + str(round(slope_error, 2)) +titles[1]
    equation += ") + (" + str(round(intercept, 2)) + " $\pm$" + str(round(intercept_error, 2)) + " " +titles[3] + ")"
    return equation

def scatter(X, y, regressor, titles, equation):
    plt.scatter(X, y, color = 'red')
    plt.plot(X, regressor.predict(X), color = 'blue')
    plt.xlabel(titles[1])
    plt.ylabel(titles[3])
    plt.title(equation)
    plt.show()


def enterXYRelation():
    relation = float(Fraction(input("What is the exponential relationship between the axes?     ")))
    return float(relation)

def knownRelation(txt_file, csv_file):
    convert_to_csv(txt_file, csv_file, 2)
    titles = getTitles(csv_file)
    X, y = getData(csv_file)
    relation = enterXYRelation()
    X = getTransformX(X, relation)
    regressor = regression(X, y)
    y_spread = getYSpread(y)
    equation = getLineEquation(regressor, error, y_spread, titles, relation)
    print(equation)
    print(type(X))
    scatter(X, y, regressor, titles, equation)
    
def automaticCurveFit(txt_file, csv_file):
    convert_to_csv(txt_file, csv_file, 2)
    titles = getTitles(csv_file)
    X, y = getData(csv_file)
    regressor, relation = findBestLinearModel(X, y, -5, 5) 
    y_spread = getYSpread(y)
    equation = getLineEquation(regressor, error, y_spread, titles, relation)
    print(equation)
    print(type(X))
    scatter(X, y, regressor, titles, equation)
    
    
automaticCurveFit("data.txt", "data.csv")
    

  