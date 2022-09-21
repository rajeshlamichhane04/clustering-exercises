import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, QuantileTransformer
from env import user, password, host
import env
from sklearn.feature_selection import SelectKBest, f_regression, RFE
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import csv
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


def nulls_by_col(df):
    num_rows_missing = df.isnull().sum()
    pct_rows_missing = df.isnull().sum() / df.shape[0] * 100
    cols_missing = pd.DataFrame({
        "num_rows_missing" : num_rows_missing ,
        " pct_rows_missing" : pct_rows_missing
    })
    return cols_missing


def nulls_by_rows(df):
    num_missing = df.isnull().sum(axis =1)
    pct_missing = (num_missing / df.shape[1]) * 100
    missing_values = pd.DataFrame({"num_missing":num_missing, "pct_missing":pct_missing})\
                    .reset_index().groupby(["num_missing","pct_missing"]).count()\
    .rename(index=str, columns={'index': 'num_rows'}).reset_index()
    return missing_values



#lets make a function and transfer it to py file
def get_single_unit(zillow):
    single_home = ['Single Family Residential', 'Condominium', 
               'Townhouse', 'Manufactured, Modular, Prefabricated Homes', 
               'Mobile Home']
    zillow = zillow[zillow.propertylandusedesc.isin(single_home)]
    
    zillow = zillow[(zillow.unitcnt == 1 )|(zillow.unitcnt.isna())]
    
    return zillow


def handle_missing_values(df,prop_required_columns,prop_required_row):
    threshold = int(round(prop_required_columns * len(df.index),0))
    df = df.dropna(axis = 1 , thresh = threshold)
    threshold = int(round(prop_required_row * len(df.columns),0 ))
    df = df.dropna(axis = 0, thresh = threshold)
    return df




def remove_outliers(df, k, col_list):
    for col in col_list:
         #get the 1st and 3rd quantiles
        q1, q3 = df[col].quantile([.25, .75]) 
         # calculate interquartile range
        iqr = q3 - q1   
         # get upper bound
        upper_bound = q3 + k * iqr   
          # get lower bound
        lower_bound = q1 - k * iqr   
         # dataframe without outliers
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
        return df