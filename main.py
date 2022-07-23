from hashlib import new
from turtle import update
import pandas as pd
from dateutil.parser import parse
from datetime import datetime
import re

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
    df_p['year'] = df_p['title'].apply(lambda x: checkYearColumnForDate(x))
    return df_p
        
def removeMissingYearFromTitleRows(df_p):
    df = df_p[df_p['year'].notna()]
    return df

# Defining main function
def main():
    print("test")
    df = getDataset()
    df = removeCols(df)
    df2 = removeMissingCountryRows(df)
    df3 = removeMissingPriceRows(df2)
    df4 = createYearColumn(df3)
    df5 = removeMissingYearFromTitleRows(df4)
    
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
    

  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()
    
    