# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:11:48 2020

@author: Hitesh
"""



def get_predict(market, variety, mode, obs_no):
    import pandas as pd
    from fbprophet import Prophet
    data=pd.read_csv(r'G:\Hitesh\cotton-price-sih-master\Data\Usilampatty.csv')
    data.columns = ['ds','y']
    data['ds'] =pd.to_datetime(data.ds,format="%d/%m/%Y")
    m1 = Prophet(daily_seasonality=True)
    m1.fit(data)
    if obs_no==1:
        future1 = m1.make_future_dataframe(periods=7)
        forecast1 = m1.predict(future1)
        return forecast1.iloc[-7:,-1].tolist()
    if obs_no==2:
        future1 = m1.make_future_dataframe(periods=14)
        forecast1 = m1.predict(future1)
        return forecast1.iloc[-14:,-1].tolist()
    if obs_no==3:
        future1 = m1.make_future_dataframe(periods=30)
        forecast1 = m1.predict(future1)
        return forecast1.iloc[-30:,-1].tolist()
        
