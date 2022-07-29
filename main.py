from fileinput import filename
from hashlib import new
from turtle import update
import pandas as pd
from dateutil.parser import parse
from datetime import datetime, tzinfo
import re
import numpy as np
import json
import matplotlib.pyplot as plt
from textblob import TextBlob
from itertools import chain, count
from collections import Counter
from collections import defaultdict
import csv
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

def getMostCommonYearPerCountry(listOfCountries_p, df_p):
    """
    This function determines what the most popular year is
    for each country and returns a dict of [country, most common
    year] pairs.
    print(mostCommonYearDict) was used to test.
    """
    dict = {}
    for i in listOfCountries_p:
        countrydf = df_p.query("country == @i")
        yearsForThisCountry = countrydf['year'].values
        yearCounts = np.bincount(yearsForThisCountry.astype(int))
        dict[i] = np.argmax(yearCounts)
    return dict
        
def getAveragePricePerCountry(listOfCountries_p, df_p):
    dict = {}
    for i in listOfCountries_p:
        countrydf = df_p.query("country == @i")
        pointsForThisCountry = countrydf['price'].values
        average = np.average(pointsForThisCountry)
        dict[i] = round(average,2)
    return dict

def getAdjectives(text):
    blob = TextBlob(text)
    return [ word for (word,tag) in blob.tags if tag == "JJ"]

def getAdjectivesFromDescription(listOfCountries_p, df_p):
    """
    This function is going to get the most common adjective
    across all descriptions per country. It will return a dict 
    of [country, most common adjective] pairs.
    I used the debugger to test this.
    """
    dict = {}
    for i in listOfCountries_p:
        adjectivesList = []
        countrydf = df_p.query("country == @i")
        descriptionsForThisCountry = countrydf['description'].values
        for y in descriptionsForThisCountry[0:100]:
            adjectives = getAdjectives(y)
            adjectivesList.append(adjectives)
        flattenedAdjectivesList = list(chain.from_iterable(adjectivesList))
        mostCommonWords = Counter(flattenedAdjectivesList).most_common()
        MostCommonWordTuple = mostCommonWords[0]
        dict[i] = MostCommonWordTuple[0]
    return dict

def createCleanedCsvFile(df_p):
    df_p.to_csv("cleanedDataset.csv")
    
def checkYearColumn(df_p):
    yearColumnIsOnlyInts = np.array_equal(df_p.year, df_p.year.astype(int))
    if not yearColumnIsOnlyInts:
        print("IC Check: Year Column is not ints.")
    else:
        print("IC Check: Year column is only ints.")
        
def checkColumnsForStrings(df_p):
    """
    Country, description, title, and variety.
    """
    countryColumnIsStrings = np.array_equal(df_p.country, df_p.country.astype(str))
    descriptionColumnIsStrings = np.array_equal(df_p.description, df_p.description.astype(str))
    titleColumnIsStrings = np.array_equal(df_p.title, df_p.title.astype(str))
    varietyColumnIsStrings = np.array_equal(df_p.variety, df_p.variety.astype(str))
    if (countryColumnIsStrings and descriptionColumnIsStrings) and (titleColumnIsStrings and varietyColumnIsStrings):
        print("IC Check: Country, description, title, and variety columns are strings.")
    else:
        print("IC Check: Country, description, title, and variety columns are not strings.")
        
def checkPriceColumn(df_p):
    priceColumnIsOnlyInts = np.array_equal(df_p.price, df_p.price.astype(int))
    if not priceColumnIsOnlyInts:
        print("IC Check: Price Column is not ints.")
    else:
        print("IC Check: Price column is only ints.")
        
def checkPointColumn(df_p):
    pointColumnIsOnlyInts = np.array_equal(df_p.points, df_p.points.astype(int))
    if not pointColumnIsOnlyInts:
        print("IC Check: Point Column is not ints.")
    else:
        print("IC Check: Point column is only ints.")
    
    
       
# Defining main function
def main():
    """
    We create a dataframe from the original CSV
    and make several function calls to clean this
    dataframe.
    """
    df = getDataset()
    df1 = removeCols(df)
    df2 = removeMissingCountryRows(df1)
    df3 = removeMissingPriceRows(df2)
    df4 = createYearColumn(df3)
    df5 = removeMissingYearFromTitleRows(df4)
    df6 = cleanVarietyCol(df5)
    
    """
    We use the resulting dataframe to create dicts
    that include country specific data.
    """
    mostCommonVarietyDict = mostPopularVarietyByCountry(df6)
    countries = getListOfCountries(df6) 
    averagePointsDict = getAveragePointsPerCountry(countries, df6)
    mostCommonYearDict = getMostCommonYearPerCountry(countries, df6)
    averagePriceDict = getAveragePricePerCountry(countries, df6)
    adjectiveDict = getAdjectivesFromDescription(countries, df6)
    makeProfile(mostCommonVarietyDict,mostCommonYearDict,averagePriceDict,averagePointsDict,adjectiveDict, countries)
    """
    We convert the resulting dataframe back into a csv
    file and check the cleaned csv file for null values.
    """
    createCleanedCsvFile(df6)
    
    """
    Integrity constraint checks.
    """
    getNullColumns(df6)
    checkYearColumn(df6)
    checkColumnsForStrings(df6)
    checkPointColumn(df6)
    checkPriceColumn(df6)


def BuildDataset(dictionary, name):
    filename = "%s.csv" % name
    fields = ['Country', 'Variety', 'Year', 'Price', 'Points', 'Adjective']
    with open(filename, 'w') as f:  # You will need 'wb' mode in Python 2.x
        w = csv.DictWriter(f, fields)
        w.writeheader()
        for k in dictionary:
            w.writerow({field: dictionary[k].get(field) or k for field in fields})
    

def makeProfile(d1,d2,d3,d4,d5,countries):
    dd = {key: None for key in countries}
    
    for c in countries:
        d_temp = dict.fromkeys(["Variety","Year","Price","Points","Adjective"])
        d_temp['Variety'] = d1[c]
        d_temp['Year'] = d2[c]
        d_temp['Price'] = d3[c]
        d_temp['Points'] = d4[c]
        d_temp['Adjective'] = d5[c]
        dd[c] = d_temp       
    BuildDataset(dd,'Profiles')
    return dd
    
"""
getNullColumns prints the number of null values per column
"""
def getNullColumns(df_p):
    null_columns=df_p.columns[df_p.isnull().any()]
    if null_columns.empty:
        print("IC Check: No null values exist.")
    else: 
        print("IC Check: Null values exist")

"""
removeCols is used to remove unecessary columns
"""
def removeCols(df):
    new_df = df.drop('region_1', axis=1)
    new_df = new_df.drop('region_2', axis=1)
    new_df = new_df.drop('taster_name', axis=1)
    new_df = new_df.drop('taster_twitter_handle', axis=1)
    new_df = new_df.drop('designation', axis=1)
    new_df = new_df.drop('province', axis=1)
    new_df = new_df.drop('winery', axis=1)
    return new_df
    """
    Tests:
    print(new_df.shape()) # should be 9 columns
    """
    
"""
cleanVarietyCol() cleans the variety column by: 
 - removing the rows with Null values
 - removing rows where entry contains 
   values with characters not in the alphabet
"""
def cleanVarietyCol(df_v):
    df1 = df_v[df_v['variety'].notna()]
    df2 = df1.loc[df1.variety.str.contains('^[a-zA-Z][a-zA-Z, ]*$')]
    return df2
    """
    Tests: 
    print(len(df_v['variety']))
    df1 = df_v[df_v['variety'].notna()]
    print(len(df1['variety']))
    df2 = df1.loc[df1.variety.str.contains('^[a-zA-Z][a-zA-Z, ]*$')]
    print(len(df2['variety']))
    """

def mostPopularVarietyByCountry(df_vp):
    new_df = df_vp.groupby(['country'])['variety'].apply(lambda x: x.value_counts().index[0]).reset_index()
    most_common = dict(zip(new_df.country, new_df.variety))
    # print(json.dumps(most_common, indent = 4))
    return most_common

# Using the special variable 
# __name__
if __name__=="__main__":
    main()
    
    