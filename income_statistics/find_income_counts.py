import pandas as pd 

# calculate the total counts of income for all assessor data 
df = pd.read_csv('datasets/Assessor.csv')
df = df[['Tract Median Income']]
df['Tract Median Income'] = df['Tract Median Income'].apply(lambda x: round(x / 10000.0) * 10000.0)
count = df['Tract Median Income'].value_counts().sort_index()
print(df)
print(count)
