from hashlib import new
from turtle import update
import pandas as pd

# Get dataset
def getDataset():
    df = pd.read_csv('Winery-Kaggle/winemag-data-130k-v2.csv')
    return df

def removeMissingCountryRows(df_p):
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
    
    """
    This prints all rows where the country is nan.
    I can use this to etst if removing the rows works.
    The following was used to test.
    
    df1 = df[df['country'].isna()]
    print(df1)
    df2 = removeMissingCountryRows(df)
    #print(df2[df2['country'].isna()])
    print(df.shape)
    print(df2.shape)
    """
    
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
# go through and see the varieties with 
def cleanVarietyCol(df_v):
    df = df_v[df_v['variety'].notna()]
    # get percentage of values in the variety column
    df['variety'] =df['variety'].str.replace('-',' ',regex=True)
    print(df['variety'])
    
    
# Using the special variable 
# __name__
if __name__=="__main__":
    main()
    
    