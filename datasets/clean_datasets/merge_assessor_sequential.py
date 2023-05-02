import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 

def cast_address_format(address): 
    lst_address = address.split(' ')
    lst_address[0] = lst_address[0][0:-2] + 'XX'
    return ' '.join(x for x in lst_address)

df = pd.read_csv('datasets/CleanedSequentialData.csv')
df.drop(columns=['Unnamed: 0', 'X3.Minute','X5.Minute', 'X7.Minute', 'X10.Minute', 'X15.Minute', 'X20.Minute'], inplace=True)

df['Address'] = df['Address'].apply(str.upper)

assessor_df = pd.read_csv('datasets/assessor.csv')
assessor_df.drop(columns=set(assessor_df.columns).difference(set(['Property Index Number','Property Address', 'Township Code', 'Neighborhood Code','Sale Price', 'Property Zip Code', 
                           'Age', 'Longitude', 'Latitude', 'Tract Median Income'])), inplace=True)
       
assessor_df.rename(columns={'Property Index Number': 'PIN', 'Property Address': 'Address', 'Property Zip Code': 'ZIP', 
                            'Municipality FIPS code': 'FIPS'}, inplace=True)

assessor_df = assessor_df[assessor_df['Address'].notna()]

assessor_df['Address'] = assessor_df['Address'].astype(str)
assessor_df['Address'] = assessor_df['Address'].apply(lambda x: cast_address_format(x))

merged = pd.merge(df,assessor_df,on="Address",how='left') 
merged = merged.sample(frac=1)
merged.drop_duplicates(subset=['Date.Sampled', 'Address', 'X1st.Draw'], inplace=True)
merged.sort_values(by=['Address'], inplace=True, ignore_index=True)

merged.to_csv('datasets/assessorSequential.csv')