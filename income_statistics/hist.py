# plot the counts of lead level intervals by income 

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 

df = pd.read_csv('datasets/assessorSequential.csv')
df.drop(columns=['Unnamed: 0'])

# calculate lead intervals 
df['avg'] = df.filter(like='Draw').apply(lambda x: x.mean(), axis=1)
df['interval'] = ['ppb < 5' if (x < 5) else '5 <= ppb < 15' if (x < 15) else '15 <= ppb' for x in df['avg']]

# specify colors and labels of stacked bars
colors=['darkred', 'navy', 'seagreen']
names=['ppb >= 15', '5 <= ppb < 15', 'ppb < 5']


# -------------------#
# Income 
# -------------------#

df = df[df['Tract Median Income'].notna()]
df['Tract Median Income'] = df['Tract Median Income'].apply(lambda x: round(x / 10000.0) * 10000.0)

# 1217 points in dataframe 
n = len(df)

n_extreme = len(df[df['avg']>=15].index)

# calculate cross-tabulation 
cross_tab_prop = pd.crosstab(index=df['Tract Median Income'], columns=df['interval'], normalize='index')
cross_tab =  pd.crosstab(index=df['Tract Median Income'], columns=df['interval']) 

# calculate expected counts
incomes = np.linspace(10000, 180000, 18)
counts_incomes = [1680, 27455, 66595, 112770, 85617, 74224, 59169, 55476, 37026, 56028, 25550, 32266, 24040, 7140, 3671, 6563, 872, 2514]
total_counts_chicago = sum(counts_incomes)
proportion_of_incomes = [x/total_counts_chicago for x in counts_incomes]

# expected counts of each income  
prop_counts_incomes = [np.round(x*n) for x in proportion_of_incomes]
# expected counts of more than 15 ppb of each income 
prop_extreme_points = [np.round(x*n_extreme) for x in proportion_of_incomes]

c1 = ['expected count based on distribution of income in Chicago']*len(incomes)
c2 = ['expected ppb more than 15 ppb'] * len(incomes)

# create cross-tabulation of expected counts 
prop_cross = pd.crosstab(index=incomes[1:], columns=c1[1:], values=prop_counts_incomes[1:], aggfunc=sum)
prop_cross_extreme = pd.crosstab(index=incomes[1:], columns=c2[1:], values=prop_extreme_points[1:], aggfunc=sum) 

ax1 = plt.axes()

# plot the histogram 
cross_tab.plot(ax=ax1, kind='bar', stacked=True, color=colors, label=names, alpha = .7, figsize=(10,6))
prop_cross.plot(ax=ax1, kind='bar', edgecolor='black', color='none', linewidth=3, alpha=1)
prop_cross_extreme.plot(ax=ax1, kind='bar', edgecolor='lightpink', color='none', linewidth=2)
plt.title('Frequency of Lead Levels by Income')
plt.xticks(size=7)
plt.yticks(size = 8)
plt.ylabel('Frequency')
plt.xlabel('Median Income')
plt.legend(labels=names, fontsize=20)
# plt.legend(fontsize = 15)
plt.show() 


# Similar histogram for each ZIP code 
#--------  ZIP CODE --------- 

# zips = [60645, 60626, 60631, 60646, 60659, 60660, 
# 60656, 60630, 60625, 60640, 60634, 60641, 60618, 60613, 
# 60657, 606707, 60739, 60647, 60614, 60651, 60622, 
# 60610, 60654, 60611, 60601, 606, 60661, 60606, 60602, 
# 60603, 60604, 60644, 60624, 60612, 60607, 60605, 
# 60623, 60608, 60616, 
# 60632, 606099, 60653, 60615, 60638, 60629, 60636, 60621, 
# 60637, 60649, 60652, 60619, 60620, 60617, 
# 60655, 60643, 60628, 60633, 60827]

# zips = [str(x) for x in zips]

# def shorten_zip(zip): 
#     if len(str(zip))!= 10: 
#         return np.NaN
#     return zip[:5]

# df['ZIP'] = df['ZIP'].apply(lambda x: shorten_zip(x))
# df = df[df['ZIP'].notna()]

# # calculate average lead level and which interval it is in 
# df_zips = set(df['ZIP'])

# zip_list = [] 
# for z in zips: 
#     if z in df_zips: 
#         zip_list.append(z)

# cross_tab_prop = pd.crosstab(index=df['ZIP'], columns=df['interval'], normalize='index')
# cross_tab =  pd.crosstab(index=df['ZIP'], columns=df['interval']) 

# cross_tab_prop = cross_tab_prop[names]
# cross_tab = cross_tab[names]

# cross_tab_prop=cross_tab_prop.transpose()
# cross_tab=cross_tab.transpose()

# cross_tab_prop = cross_tab_prop[zip_list]
# cross_tab=cross_tab[zip_list]

# cross_tab_prop=cross_tab_prop.transpose()
# cross_tab=cross_tab.transpose()

# print(cross_tab)

# cross_tab_prop.plot(kind='bar', stacked=True, color=colors, label=names, alpha = .6, figsize=(10,6))
# plt.title('Proportion of Average Lead Intervals by ZIP Code')
# plt.xticks(size=7)
# plt.yticks(size = 8)
# plt.ylabel('Proportion')
# plt.legend(names, loc='upper right')

# plt.show() 

# cross_tab.plot(kind='bar', stacked=True, color=colors, label=names, alpha = .6, figsize=(10,6))
# plt.title('Frequency of Average Lead Intervals by ZIP Code')
# plt.xticks(size=7)
# plt.yticks(size = 8)
# plt.ylabel('Frequency')
# plt.legend(names, loc='upper right')

# plt.show() 
