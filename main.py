import pandas as pd

# Get dataset
def getDataset():
    df = pd.read_csv('Winery-Kaggle/winemag-data-130k-v2.csv')
    return df
    # print(df.to_string()) 

# Defining main function
def main():
    print("test")
    # getDataset()


# Count the Null columns
"""
Prints the count of the null values for each column 
"""
def getNullColumns():
    df = getDataset()
    null_columns=df.columns[df.isnull().any()]
    print(df[null_columns].isnull().sum())

getNullColumns()

# Remove the region 1 and region 2
"""
Region 1 contains 16% null data 
Region 2 contains 61% data 
param col_name : String of the column name we want to delete
"""
def removeCol(col_name):
    df = df.drop(col_name, axis=1)

  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()
    removeCol('region_1')
    removeCol('region_2')
    removeCol('taster_name')
    removeCol('taster_twitter_handle')
    removeCol('description')
    