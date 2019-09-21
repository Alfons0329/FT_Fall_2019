#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import numpy
import csv
import sys, os

df_orig = pd.read_csv('Daily_2018_10_01.csv', encoding = 'big5')
df = df_orig[df_orig['商品代號'] == 'TX     ']
#print(df.columns)
focus_day = df.iloc[[0]]['成交日期']
focus_month = df.iloc[[0]]['到期月份(週別)']
data_all = df.values.tolist()
data_parsed = []
for each_row in data_all:
    if('/' in each_row[2]):
        continue #ignore entry
        
    if int(each_row[0]) == int(focus_day.values)     and int(each_row[2]) == int(focus_month.values)     and int(each_row[3]) >= 84500     and int(each_row[3]) <= 134500:
        print('append -> ', each_row)
        data_parsed.append(float(each_row[4]))
        
print(int(data_parsed[0]), int(max(data_parsed)), int(min(data_parsed)), int(data_parsed[-1]))

