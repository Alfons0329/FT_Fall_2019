#!/usr/bin/env python
# coding: utf-8

# In[86]:


import pandas as pd
import numpy
import csv
import sys, os
import warnings
warnings.filterwarnings('ignore')

input_day = sys.argv[1]
input_day = input_day.replace('Daily_', '')
input_day = input_day.replace('_', '')
input_day = input_day.replace('.csv', '')

df_orig = pd.read_csv('Daily_2019_09_20.csv', encoding = 'big5')
#print(df.columns)
df = df_orig[df_orig['商品代號'] == 'TX     ']
df = df[df['成交日期'] == int(input_day)]
print(df_orig.iloc[[df['成交時間'].argmin()]]['成交價格'].values,      df_orig.iloc[[df['成交價格'].argmax()]]['成交價格'].values,      df_orig.iloc[[df['成交價格'].argmin()]]['成交價格'].values,      df_orig.iloc[[df['成交時間'].argmax()]]['成交價格'].values, )

