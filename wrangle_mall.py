import pandas as pd
import numpy as np
import env
import os


#connection set ip
def conn(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_mall_data():
    """ Acquires the Zillow housing data from the SQL database or a cached CSV file. Renames columns and outputs data as a Pandas DataFrame"""
    # Acquire data from CSV if exists
    if os.path.exists('mall.csv'):
        print("Using cached data")
        df = pd.read_csv('mall.csv',index_col = 0)
    # Acquire data from database if CSV does not exist
    else:
        print("Acquiring data from server")
        query = '''
        SELECT * FROM mall_customers.customers
        '''
        
        df = pd.read_sql(query, conn('zillow'))
        df.to_csv("mall.csv")
    return df

#get summary of data
def summary_mall_data(df):
    print("dataframe head")
    print()
    print(df.head())
    print()
    print("dataframe info")
    print()
    print(df.info())
    print()
    print("describe dataframe")
    print()
    print(df.describe().T)
    print()
    numerical_col = [col for col in df.columns if col in df.select_dtypes(include = ["number"])]
    categorical_col = [col for col in df.columns if col in df.select_dtypes(include = ["object"])]
    for col in df.columns:
        print("column name:", col)
        if col in categorical_col:
            print (df[col].value_counts())
            print()
        else:
            print (df[col].value_counts(bins = 10))
            print()