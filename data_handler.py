#!/usr/bin/env python
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np

def get_daily_stock_data( ticker, country):
    url = 'https://financialmodelingprep.com/api/v3/historical-price-full/{}'.format(ticker)
    df_daily = json_normalize(pd.read_json(url)['historical'])
    df_daily['date']= pd.to_datetime(df_daily['date']) 
    return df_daily[['date', 'close', 'volume']]

def get_quarter_fundamentals( ticker, country):
    url = 'https://financialmodelingprep.com/api/v3/financials/income-statement/{}?period=quarter'.format(ticker)
    df_fundamentals = json_normalize(pd.read_json(url)['financials'])
    df_fundamentals['date']= pd.to_datetime(df_fundamentals['date']) 
    return df_fundamentals[['date', 'EPS' ]]

def get_estimated_growth(ticker, country):
    df_est = pd.read_html(r'http://financials.morningstar.com/valuate/annual-estimate-list.action?&t={}'.format(ticker),keep_default_na=False)
    df_est = pd.concat(df_est)
    df_est.replace('', np.nan, inplace=True)
    df_est.dropna(axis=0, how='all', inplace=True)
    df_est.dropna(axis=1, how='all', inplace=True)
    df_est.drop([1, 4], axis=1, inplace=True)
    df_est.drop([2], axis=0, inplace=True)
    df_est[0][0] = 'date'
    df_est.set_index([0], inplace=True)
    df_est = df_est.T
    df_est['date']= pd.to_datetime(df_est['date']) 
    return df_est