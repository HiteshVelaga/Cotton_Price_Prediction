# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:21:31 2020

@author: Hitesh
"""

import pandas as pd
import numpy as np

data1=pd.read_csv(r'C:\Users\Hitesh\new\cotton-price-sih-master\Cotton_2010.csv')
data2=pd.read_csv(r'C:\Users\Hitesh\new\cotton-price-sih-master\Cotton_2011.csv')
data3=pd.read_csv(r'C:\Users\Hitesh\new\cotton-price-sih-master\Cotton_2012.csv')
data4=pd.read_csv(r'C:\Users\Hitesh\new\cotton-price-sih-master\Cotton_2013.csv')
data5=pd.read_csv(r'C:\Users\Hitesh\new\cotton-price-sih-master\Cotton_2014.csv')
data6=pd.read_csv(r'C:\Users\Hitesh\new\cotton-price-sih-master\Cotton_2015.csv')
data7=pd.read_csv(r'C:\Users\Hitesh\new\cotton-price-sih-master\Cotton_2016.csv')
data8=pd.read_csv(r'C:\Users\Hitesh\new\cotton-price-sih-master\Cotton_2017.csv')
data9=pd.read_csv(r'C:\Users\Hitesh\new\cotton-price-sih-master\Cotton_2018.csv')
data10=pd.read_csv(r'C:\Users\Hitesh\new\cotton-price-sih-master\Cotton_2019.csv')

data1=data1.append(data2)
data1=data1.append(data3)
data1=data1.append(data4)
data1=data1.append(data5)
data1=data1.append(data6)
data1=data1.append(data7)
data1=data1.append(data8)
data1=data1.append(data9)
data1=data1.append(data10)


markets=data1.market.unique().tolist()
data1['market'].value_counts()

Usilampatty=data1[data1['market']=='Usilampatty']

Usilampatty.drop(columns=['state','district','market','variety','commodity','min_price','max_price'],inplace=True)
Usilampatty.to_csv(r'G:\Hitesh\cotton-price-sih-master\Data\Usilampatty.csv',index=False)










































data=pd.read_csv(r'G:\Hitesh\cotton-price-sih-master\Data\Cotton.csv')
X=data.iloc[:,1:3]
y=data.iloc[:,3]
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X1 = LabelEncoder()
labelencoder_X2 = LabelEncoder()
X.iloc[:, 0] = labelencoder_X1.fit_transform(X.iloc[:, 0])
X.iloc[:, 1] = labelencoder_X2.fit_transform(X.iloc[:, 1])
ct = ColumnTransformer([('encoder', OneHotEncoder(), [0,1])], remainder='passthrough')
X = ct.fit_transform(X).toarray()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

from sklearn.preprocessing import StandardScaler
sc_x = StandardScaler()
sc_y=StandardScaler()
X_train = sc_x.fit_transform(X_train)
X_test = sc_x.transform(X_test)
y_train=y_train.values.reshape(1, -1)
y_train = sc_y.fit_transform(y_train)

X_train_demo = np.reshape(X_train, (X_train.shape[0], X_train.shape[1],60))
num_steps = 20
# training set
X_train_shaped = np.reshape(X_train, newshape=(1, num_steps, 940))
y_train_shaped = np.reshape(y_train, newshape=(-1, num_steps, 940))
assert X_train_shaped.shape[0] == y_train_shaped.shape[0]
# test set
x_test_shaped = np.reshape(X_test, newshape=(-1, num_steps, 940))
y_test_shaped = np.reshape(y_test, newshape=(-1, num_steps, 940))
assert X_test_shaped.shape[0] == y_test_shaped.shape[0]

def lstm_data_transform(x_data, y_data, num_steps=5):
    """ Changes data to the format for LSTM training 
for sliding window approach """
    # Prepare the list for the transformed data
    X, y = list(), list()
    # Loop of the entire data set
    for i in range(x_data.shape[0]):
        # compute a new (sliding window) index
        end_ix = i + num_steps
        # if index is larger than the size of the dataset, we stop
        if end_ix >= x_data.shape[0]:
            break
        # Get a sequence of data for x
        seq_X = x_data[i:end_ix]
        # Get only the last element of the sequency for y
        seq_y = y_data[end_ix]
        # Append the list with sequencies
        X.append(seq_X)
        y.append(seq_y)
    # Make final arrays
    x_array = np.array(X)
    y_array = np.array(y)
    return x_array, y_array

num_steps = 20
# training set
(x_train_transformed,
 y_train_transformed) = lstm_data_transform(X_train, y_train, num_steps=num_steps)
assert x_train_transformed.shape[0] == y_train_transformed.shape[0]
# test set
(x_test_transformed,
 y_test_transformed) = lstm_data_transform(X_test, y_test, num_steps=num_steps)
assert x_test_transformed.shape[0] == y_test_transformed.shape[0]















































from keras.models import Sequential
from keras.layers import Dense
model = Sequential()
model.add(Dense(units = 570, kernel_initializer='normal', activation = 'relu', input_dim = 940))
model.add(Dense(units = 285, kernel_initializer='normal', activation = 'relu'))
model.add(Dense(units = 1))
model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['mse'])
model.fit(X_train, y_train, batch_size = 10, epochs = 100)
pred=model.predict(X_train, y_train, batch_size = 10, epochs = 100)

def forWeek(market,variety,X,y):
    displayData=[]
    market=labelencoder_X1.transform(market)
    variety=labelencoder_X2.transform(variety)
    x_forWeek=pd.DataFrame(columns=['market','variety'])
    x_forWeek=ct.tranform(x_forWeek)
    temp_X=X
    temp_y=y
    for x in range(7):
        Prediction = model.predict(x)
        temp_y.append(Prediction)
        temp_X.append(x_forWeek)
        model.fit(temp_X,temp_y)
        displayData.append(Prediction)
    return displayData

#forMonth
def forMonth(market,variety,X,y):
    displayData=[]
    market=labelencoder_X1.transform(market)
    variety=labelencoder_X2.transform(variety)
    x_forWeek=pd.DataFrame(columns=['market','variety'])
    x_forWeek=ct.tranform(x_forWeek)
    temp_X=X
    temp_y=y
    for x in range(30):
       Prediction = model.predict(x)
       temp_y.append(Prediction)
       temp_X.append(x_forWeek)
       model.fit(temp_X,temp_y)
       displayData.append(Prediction)
    return displayData

#for2Months
def for_Two_Month(market,variety,X,y):
    displayData=[]
    market=labelencoder_X1.transform(market)
    variety=labelencoder_X2.transform(variety)
    x_forWeek=pd.DataFrame(columns=['market','variety'])
    x_forWeek=ct.tranform(x_forWeek)
    temp_X=X
    temp_y=y
    for x in range(60):
        Prediction = model.predict(x)
        temp_y.append(Prediction)
        temp_X.append(x_forWeek)
        model.fit(temp_X,temp_y)
        displayData.append(Prediction)  
    return displayData

#returningVlaues
def get_predict(market, variety, mode, X,y):
    display=[]
    if mode==0:
        display.extend(forWeek(market,variety,X,y))
    elif mode==1:
         display.extend(forMonth(market,variety,X,y))
    elif mode==2:
        display.extend(for_Two_Month(market,variety,X,y))
    display = [x * 100 for x in display]
    return display
