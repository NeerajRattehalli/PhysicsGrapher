# Importing the libraries
import matplotlib.pyplot as plt
import pandas as pd

filepath = 'data.txt'
with open(filepath) as fp:
   lines = fp.readlines()
   
lines = [line[:-1] for line in lines]

for i in range(len(lines)):
    if i > 1:
        lines[i] = float(lines[i])

x_axis = lines[0]
y_axis = lines[1]
lines = lines[2:]
X = [lines[2*i] for i in range(int(len(lines)/2))]
y = [lines[2*i+1] for i in range(int(len(lines)/2))]
X_inv = [el**(-1) for el in X]
x_inv_axis = "1/V 1/(m^3)"

dataset1 = pd.DataFrame({x_axis: X, y_axis: y})
dataset2 = pd.DataFrame({x_inv_axis: X_inv, y_axis: y})

# Importing the dataset
X = dataset1.iloc[:, :-1].values
y = dataset1.iloc[:, 1].values

#Visualizing the Training Set Results
plt.scatter(X, y, color = 'red')
#plt.plot(X_train, regressor.predict(X_train), color = 'blue')
plt.xlabel(x_axis)
plt.ylabel(y_axis)
plt.show()

# Importing the dataset
X = dataset2.iloc[:, :-1].values
y = dataset2.iloc[:, 1].values

#Fitting Simple Linear Regression to the Training Set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X, y)

#Predicting the Test set Results
y_pred = regressor.predict(X)

slope = regressor.coef_[0]
intercept = regressor.intercept_
error = 0.05

slope_error = slope*error
intercept_error = intercept*error

plt.scatter(X_inv, y, color = 'red')
plt.plot(X, regressor.predict(X), color = 'blue')
plt.xlabel(x_axis)
plt.ylabel(y_axis)
title = x_inv_axis[:-7] + "= (" + str(round(slope, 2)) + "$\pm$" + str(round(slope_error, 2)) + ")" + y_axis
title = title[:-7] + " + (" + str(round(intercept, 2)) + "$\pm$" + str(abs(round(intercept_error, 2))) + ")"

plt.title(str(title))
plt.show()
