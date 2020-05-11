# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date
from scipy.optimize import curve_fit
import math
import datetime


# Read DataFrame from csv
df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')
col_name = ['Date', 'Country/Region', 'Province/State', 'Lat', 'Long', 'Confirmed', 'Recovered', 'Deaths', 'date']
newAgain = pd.DataFrame(columns = col_name)

rose = []
test = list(df['Country/Region'].unique())

for i in test:
    niles = df.groupby('Country/Region').get_group(i)
    rose.append(niles)
for r in rose:
    hold=[]
    timeD = r['Date'].tolist()
    for t in timeD:
        delt = datetime.datetime.strptime(t, "%Y-%m-%d").strftime("%m%d%Y")
        hold.append(delt)
    r['date'] = hold
    newAgain = pd.concat([newAgain, r])

# Replace string version of Date column with float version of Date column
newAgain = newAgain.drop(columns = 'Date').astype({'date':'float64'})
newAgain = newAgain.reindex(columns = ['date', 'Country/Region', 'Province/State', 'Lat', 'Long', 'Confirmed', 'Recovered', 'Deaths'])

# Filter DataFrame to include only US data
filtered_data = newAgain[newAgain["Country/Region"] =='US']
US = filtered_data.drop(columns = ['Province/State','Lat', 'Long']) 


x = filtered_data.Confirmed.values.reshape(-1,1)
y = filtered_data.Deaths.values.reshape(-1,1)

# To Predict Number of Deaths from Confirmed Cases:
train_x, test_x, train_y, test_y = train_test_split (x, y, test_size = 0.25, random_state = 1)
linear_model = LinearRegression()
linear_model.fit(train_x, train_y)

intercept = linear_model.intercept_
coeff = linear_model.coef_

test_prediction = linear_model.predict(test_x)

# Flatten the DataFrame of Actual Deaths per Confirmed Cases to a list 
df_DA = pd.DataFrame({'Actual Confirmed':x.flatten(),
                     'Actual Deaths':y.flatten(),})

# Flatten the DataFrame of Predicted Deaths per Confirmed Cases to a list
df_DP = pd.DataFrame({'Predicted Confirmed':test_x.flatten(),
                     'Predicted Deaths':test_prediction.flatten()})


# Plot Actual Deaths per Confirmed Cases and Predicted Deaths per Confirmed Cases
# on the same graph
plt.title("Prediction Model") 
plt.xlabel("Confirmed Cases") 
plt.ylabel("Deaths") 
plt.plot(x, y, label = 'Actual')
plt.plot(test_x, test_prediction, label = 'Predicted') 
plt.legend(loc = 'upper left')
plt.show()

# Output Actual Deaths per Confirmed Cases to a new csv
df_DA.to_csv('Death_Actual.csv', index = True, header = True)
# Output Predicted Deaths per Confirmed Cases to a new csv
df_DP.to_csv('Death_Predict.csv', index = True, header = True)