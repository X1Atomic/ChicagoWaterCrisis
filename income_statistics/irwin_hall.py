# this code runs a one-sided hypothesis test using the Irwin-Hall distribution 
# Irwin-Hall: sum of m variables X ~i.i.d. U(0,1)
# take X to be the quantile of income 
# H_0: there is no relationship between average lead levels and income. 
# H_A: there is a relationship between average lead levels and income. 
# for some ppb threshold k, take x_hat = sum of income quantiles of data points whose average exceeds k ppb (n points)
# calculate P(X <= x_hat) for significance 

import numpy as np
import pandas as pd 
import math
from matplotlib import pyplot as plt
import scipy.stats as stats

# Code for the IrwinHallCDF provided by Professor Robert B. Ellis. Much thanks! 

# Adapted from https://en.wikipedia.org/wiki/Irwin%E2%80%93Hall_distribution
def IrwinHallCDF(n, x, approx="None"):
  # For n<=20, the CDF is numerically stable.
  # For n >20, set approx="Normal" to get the normal approximation to the CDF
  #     Exact standardized CDF will be within .0015 of normal approximation CDF
  if n>20 and approx=="None":
    print("Numerically unstable above n=20.")
    return(None)
  
  # To convert to approximate normal statistic, subtract mean n/2 and
  #   divide by sqrt of variance; a single uniform[0,1] has variance 1/12
  #   and variance is additive for independent random variables
  if approx=="Normal":
    return(stats.norm.cdf((x-n/2)*math.sqrt(12/n)))

  else:  
    sum = np.float128(0)
    a = np.array(
        [(-1)**k * (1/(np.float128(math.factorial(k))*np.float128(math.factorial(n-k))))*
        (np.float128(x)-k)**n for k in range(0,math.floor(x)+1)], 
        dtype=np.float128)
    return(np.sum(a, dtype=np.float128))

# run one-sided significance test 
def one_side_test_low(ppb_threshold, df): 
    
    df_above_thresh=df[df['avg']>=ppb_threshold]

    # n = number of points of interest 
    # x = sum of quantiles of points of interest
    n = len(df_above_thresh.index)
    x_hat = sum(df_above_thresh['quantile'])
    print(ppb_threshold, n)

    # return test statistic 
    return IrwinHallCDF(n=n, x=x_hat, approx="Normal")

# read dataset 
df = pd.read_csv('datasets/assessorSequential.csv')
df.drop(columns=['Unnamed: 0', 'PIN','Township Code', 'Sale Price', 'Neighborhood Code','Age','ZIP','Longitude','Latitude'], inplace=True)

df = df[df['Tract Median Income'].notna()]

# calculate average ppb 
df['avg'] = df.filter(like='Draw').apply(lambda x: x.mean(), axis=1)

# nQuantiles = total data points (m)
nQuantiles = len(df.index)

df = df[['Tract Median Income', 'avg']]
df.sort_values(by=['Tract Median Income'], inplace=True)

# calculate quantiles of income 
quantiles = np.linspace(float(1/(2*nQuantiles)), 1-float(1/(2*nQuantiles)), nQuantiles)
df['quantile'] = quantiles

# list of thresholds k 
thresholds = [x for x in range(5,25)]

one_side_low = [] 
for ppb in thresholds:  
  one_side_low.append(one_side_test_low(ppb,df))

# plot of thresholds and statistical significance 
plt.scatter(thresholds, one_side_low, s=13)
plt.title('One-Sided Test Statistic: Irwin-Hall Distribution')
plt.xlabel('ppb Threshold')
plt.ylabel('log(p-value)')
plt.grid(True)
plt.axhline(0.05, c='r')
plt.xticks(thresholds)
plt.yscale("log")
plt.show() 

# plot for math newbies
# plt.scatter(thresholds, one_side_low, s=25)
# plt.title('Irwin-Hall Distribution Test Statistic')
# plt.xlabel('lead level threshold (ppb)')
# plt.ylabel('log(p-value)')
# plt.grid(True)
# plt.axhline(0.05, c='r')
# plt.xticks(thresholds)
# plt.yscale("log")
# plt.show() 

