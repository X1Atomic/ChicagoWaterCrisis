import geopandas
import pandas as pd 
import matplotlib.pyplot as plt
from shapely.geometry import Point
import random 

def color_by_val(row): 
    val = row['avg']
    if 0 <= val < 5: 
        return 1 
    elif 5 <= val < 15: 
        return 2 
    else: 
        return 3
    
crs = {'init': 'epsg:4326'}
random.seed(1827)

# read dataframe 
df = pd.read_csv('.\datasets\AssessorSequential.csv')

# calculate average and lead interval 
df['avg'] = df[["X1st.Draw","X2nd.Draw","X3rd.Draw","X4th.Draw","X5th.Draw","X6th.Draw","X7th.Draw","X8th.Draw","X9th.Draw","X10th.Draw","X11th.Draw"]].mean(axis=1)
df['ppb_label'] = df.apply(lambda row: color_by_val(row), axis=1)

# take coordinates and lead label 
df = df[['Longitude', 'Latitude', 'avg', 'ppb_label']]

# create new geo dataframe 
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
geo_df = geopandas.GeoDataFrame(df, crs = crs, geometry = geometry)
geo_df.dropna(inplace=True)
print(geo_df)

# read Chicago shp map 
street_map = geopandas.read_file('geodata\geo_export_c315ae68-1c3e-40e9-b2a7-69885fdcc885.shp')

# plot data on the map 
fig, ax = plt.subplots(figsize = (15,15))
street_map.plot(ax = ax, alpha = .3, color = 'grey')
geo_df[geo_df['ppb_label'] == 1].plot(ax = ax, markersize = 10, color = 'green', label = '0 <= ppb < 5') 
geo_df[geo_df['ppb_label'] == 2].plot(ax = ax, markersize = 10, color = 'blue', label = '5 <= ppb < 10')
geo_df[geo_df['ppb_label'] == 3].plot(ax = ax, markersize = 10, color = 'red', label = '15 < ppb')

plt.title('Average Lead Levels from Sequential Testing')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.xlim(-87.855, -87.5)
plt.xticks(rotation=90)
plt.legend(prop={'size': 8})

plt.savefig('MeanPPBCoordinateGraph.png')

plt.show() 
