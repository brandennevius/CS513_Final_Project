import pandas as pd

# Get dataset
def getDataset():
    df = pd.read_csv('Winery-Kaggle/winemag-data-130k-v2.csv')
    print(df.head(10))
    return df

def removeMissingCountryRows(df_p):
    
    return df
    

# Defining main function
def main():
    print("test")
    df = getDataset()  
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()