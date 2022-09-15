import pandas as pd
import numpy as np
import env
import os


#connection set ip
def conn(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def wrangle_zillow():
    """ Acquires the Zillow housing data from the SQL database or a cached CSV file. Renames columns and outputs data as a Pandas DataFrame"""
    # Acquire data from CSV if exists
    if os.path.exists('zillow.csv'):
        print("Using cached data")
        df = pd.read_csv('zillow.csv',index_col = 0)
    # Acquire data from database if CSV does not exist
    else:
        print("Acquiring data from server")
        query = """
                SELECT parcelid, airconditioningtypeid, airconditioningdesc, architecturalstyletypeid, architecturalstyledesc,
                bathroomcnt, bedroomcnt, buildingclasstypeid, buildingclassdesc, buildingqualitytypeid,
                decktypeid, calculatedfinishedsquarefeet, fips, fireplacecnt, fireplaceflag, garagecarcnt, garagetotalsqft,
                hashottuborspa, latitude, longitude, lotsizesquarefeet, poolcnt, poolsizesum, propertycountylandusecode,
                propertylandusetypeid, propertylandusedesc, propertyzoningdesc, rawcensustractandblock, 
                regionidcity, regionidcounty, regionidneighborhood, roomcnt, threequarterbathnbr, typeconstructiontypeid, typeconstructiondesc, unitcnt, yearbuilt, numberofstories, structuretaxvaluedollarcnt, taxvaluedollarcnt, assessmentyear, 
                landtaxvaluedollarcnt, taxamount, censustractandblock, logerror, transactiondate 
                FROM properties_2017 AS p
                JOIN predictions_2017 USING (parcelid)
                INNER JOIN (SELECT parcelid, MAX(transactiondate) AS transactiondate
                FROM predictions_2017
                GROUP BY parcelid) 
                AS t USING (parcelid, transactiondate)
                LEFT JOIN airconditioningtype USING (airconditioningtypeid)
                LEFT JOIN architecturalstyletype USING (architecturalstyletypeid)
                LEFT JOIN buildingclasstype USING (buildingclasstypeid)
                LEFT JOIN heatingorsystemtype USING (heatingorsystemtypeid)
                LEFT JOIN propertylandusetype USING (propertylandusetypeid)
                LEFT JOIN storytype USING (storytypeid)
                LEFT JOIN typeconstructiontype USING (typeconstructiontypeid)
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL 
                AND transactiondate LIKE "2017%%";
                """
    
        # Read fresh data from db into a DataFrame
        df = pd.read_sql(query, conn('zillow'))
        
        # Cache data
        df.to_csv('zillow.csv')

    return df
        
    