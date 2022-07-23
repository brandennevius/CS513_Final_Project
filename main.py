from hashlib import new
from turtle import update
import pandas as pd
from dateutil.parser import parse
from datetime import datetime
import re
import numpy as np
pd.set_option('max_columns', None)

# Get dataset
def getDataset():
    df = pd.read_csv('Winery-Kaggle/winemag-data-130k-v2.csv')
    return df

def removeMissingCountryRows(df_p):
    """
    I can use this to test if removing the rows works.
    
    df1 = df[df['country'].isna()]
    print(df1)
    df2 = removeMissingCountryRows(df)
    #print(df2[df2['country'].isna()])
    print(df.shape)
    print(df2.shape)
    """
    df = df_p[df_p['country'].notna()]
    return df

# Defining main function
def main():
    print("test")
    df = getDataset()
    df = removeCols(df)
    # print(df.head())
    # print(getNullColumns())
    df2 = removeMissingCountryRows(df)
    print(cleanVarietyCol(df2))
    
def removeMissingPriceRows(df_p):
    """
    I can use this to test if removing the rows works.
    
    df1 = df[df['price'].isna()]
    print(df1)
    df2 = removeMissingCountryRows(df)
    #print(df2[df2['price'].isna()])
    print(df.shape)
    print(df2.shape)
    """
    df = df_p[df_p['price'].notna()]
    return df

def checkYearColumnForDate(x):
    """
    This function is used to catch the value error
    returned by the parse function when searching the
    title column for a year.
    """
    try:
        return parse(x, fuzzy=True).year
    except ValueError as e:
        return
    
def createYearColumn(df_p):
    """
    The following was used for testing. I used
    the head print to compare the year in the title
    to the year in the year column.
      
    df4 = createYearColumn(df)
    print(df4.shape)
    df5 = removeMissingYearFromTitleRows(df4)
    print(df5.shape)
    print(df5.head(50))
    """
    df = df_p.copy()
    df['year'] = df['title'].apply(lambda x: checkYearColumnForDate(x))
    return df
        
def removeMissingYearFromTitleRows(df_p):
    df = df_p[df_p['year'].notna()]
    return df

def getListOfCountries(df_p):
    """
    The following was used for testing.
    print(countries)
    """
    return df_p['country'].unique()

def getAveragePointsPerCountry(listOfCountries_p, df_p):
    """
    This function is going to return a dict of [country,
    average points] pairs.
    I printed the dict to test this.
    """
    dict = {}
    for i in listOfCountries_p:
        countrydf = df_p.query("country == @i")
        pointsForThisCountry = countrydf['points'].values
        average = np.average(pointsForThisCountry)
        dict[i] = average
    return dict
        
    

# Defining main function
def main():
    print("test")
    df = getDataset()
    df1 = removeCols(df)
    df2 = removeMissingCountryRows(df1)
    df3 = removeMissingPriceRows(df2)
    df4 = createYearColumn(df3)
    df5 = removeMissingYearFromTitleRows(df4)
    df6 = cleanVarietyCol(df5)
    countries = getListOfCountries(df6) 
    averagePointsDict = getAveragePointsPerCountry(countries, df6)

    
# Count the Null columns
"""
Prints the count of the null values for each column 
"""
def getNullColumns():
    df = getDataset()
    null_columns=df.columns[df.isnull().any()]
    print(df[null_columns].isnull().sum())

# Remove the region 1 and region 2
"""
Region 1 contains 16% null data 
Region 2 contains 61% data 
param col_name : String of the column name we want to delete
"""
def removeCols(df):
    new_df = df.drop('region_1', axis=1)
    new_df = new_df.drop('region_2', axis=1)
    new_df = new_df.drop('description', axis=1)
    new_df = new_df.drop('taster_name', axis=1)
    new_df = new_df.drop('taster_twitter_handle', axis=1)
    return new_df
    
# Function to clean the variety 

def cleanVarietyCol(df_v):
    """
    test if the variety row is cleaned up
    print(len(df_v['variety']))
    df1 = df_v[df_v['variety'].notna()]
    print(len(df1['variety']))

    df2 = df1.loc[df1.variety.str.contains('^[a-zA-Z][a-zA-Z, ]*$')]
    print(len(df2['variety']))
    """
    #remove na values
    df1 = df_v[df_v['variety'].notna()]
    # remove any entry that contains special characters
    df2 = df1.loc[df1.variety.str.contains('^[a-zA-Z][a-zA-Z, ]*$')]
    return df2
    
    
    
    
# Using the special variable 
# __name__
if __name__=="__main__":
    main()
    
    