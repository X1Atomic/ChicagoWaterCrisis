# exploratory visualization: plots the sequential data by location, colored by income class

import geopandas
import pandas as pd 
import matplotlib.pyplot as plt
from shapely.geometry import Point
import random 

crs = {'init': 'epsg:4326'}
random.seed(1827)

# read dataframe 
df = pd.read_csv('.\datasets\AssessorSequential.csv')

# take coordinates and income data 
df = df[['Longitude', 'Latitude', 'Tract Median Income']]

# create new geo dataframe 
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
geo_df = geopandas.GeoDataFrame(df, crs = crs, geometry = geometry)
geo_df.dropna(inplace=True)
print(geo_df)

# read Chicago shp map 
street_map = geopandas.read_file('geodata\geo_export_c315ae68-1c3e-40e9-b2a7-69885fdcc885.shp')

# # plot data on the map 
fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax = ax, alpha = .3, color = 'grey')

geo_df.plot(column='Tract Median Income', ax=ax, markersize=10, legend=True, cmap='plasma')

plt.title('Median Income')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.xlim(-87.855, -87.5)
plt.xticks(rotation=90)
plt.legend(prop={'size': 8})

plt.show() 
