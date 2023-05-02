import numpy as np
import pandas as pd
from argparse import ArgumentParser
import os.path
import argparse


def df_cleaned(df):
    df = pd.read_csv(df)
    print(df.shape)
    df = df.drop(0) 
    df = df.drop("Index",axis=1)
    df['Date.Sampled'] = pd.to_datetime(df['Date.Sampled'])
    for i in range(3,len(col_name)):
        df[col_name[i]] = df[col_name[i]].apply(pd.to_numeric)
    df.drop(df.columns[[13,14,15,16,17,18]],axis=1,inplace=True) 
    col_new = df.columns
    draw_cols = col_new[2:]

    for i in range(len(draw_cols)):
        df = df[df[draw_cols[i]].notnull()]
    return df


def main():
    parser = argparse.ArgumentParser(description='Make barchart from csv.')
    parser.add_argument('-d', '--debug', help='Debugging output', action='store_true')
    parser.add_argument('csvfile', type=argparse.FileType('r'), help='Input csv file')
    args = parser.parse_args()

    print('main(): type(args.csvfile)) = {}'.format(args.csvfile))
    print('')

    ### This works 
    foo_df = pd.read_csv(args.csvfile)

    print(foo_df.describe())
    print('')
    print(foo_df.head(5))
    print('')

if __name__ == '__main__':
    main()



