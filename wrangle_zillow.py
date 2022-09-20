import pandas as pd
import numpy as np
import env
import os
import wrangle

#we are goning to define single homes as property which 1 main entrance door
def get_single_unit(zillow):
    single_home = ['Single Family Residential', 'Condominium', 
               'Townhouse', 'Manufactured, Modular, Prefabricated Homes', 
               'Mobile Home']
    zillow = zillow[zillow.propertylandusedesc.isin(single_home)]
    
    zillow = zillow[(zillow.unitcnt == 1 )|(zillow.unitcnt.isna())]
    
    return zillow

#dispplay null values by columns
def nulls_by_col(df):
    num_rows_missing = df.isnull().sum()
    pct_rows_missing = df.isnull().sum() / df.shape[0] * 100
    cols_missing = pd.DataFrame({
        "num_rows_missing" : num_rows_missing ,
        " pct_rows_missing" : pct_rows_missing
    })
    return cols_missing

#display null values by row
def nulls_by_rows(df):
    num_missing = df.isnull().sum(axis =1)
    pct_missing = (num_missing / df.shape[1]) * 100
    missing_values = pd.DataFrame({"num_missing":num_missing, "pct_missing":pct_missing})\
                    .reset_index().groupby(["num_missing","pct_missing"]).count()\
    .rename(index=str, columns={'index': 'num_rows'}).reset_index()
    return missing_values


#handle null 
def handle_missing_values(df,prop_required_columns,prop_required_row):
    threshold = int(round(prop_required_columns * len(df.index),0))
    df = df.dropna(axis = 1 , thresh = threshold)
    threshold = int(round(prop_required_row * len(df.columns),0 ))
    df = df.dropna(axis = 0, thresh = threshold)
    return df