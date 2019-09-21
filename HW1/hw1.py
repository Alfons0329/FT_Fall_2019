#!/usr/bin/env python
# coding: utf-8
# In[21]:
import pandas as pd
import numpy
import csv
import sys, os

''' try pandas later discussion
df_orig = pd.read_csv(sys.argv[1], encoding = 'big5')
df = df_orig[df_orig['商品代號'] == 'TX     ']
focus_month = df.iloc[[0]]['到期月份(週別)']
df = df[df['到期月份(週別)'] == int(focus_month)]
print(df)
'''

parsed_data = []
with open(sys.argv[1], encoding = 'big5') as f:
    all_data = csv.reader(f)
    row_idx = 0
    flg = 0
    focus_month = ''
    focus_date = ''

    for each_row in all_data:
        if row_idx:
            if '/' not in each_row[2] and str(each_row[1]) == 'TX     ':
                if flg == 0 and int(each_row[3]) == 84500:
                    focus_date = each_row[0]
                    focus_month = each_row[2]
                    flg = 1
                if each_row[0] == focus_date and each_row[2] == focus_month and int(each_row[3]) >= 84500 and int(each_row[3]) <= 134500:
                    parsed_data.append(int(each_row[4]))

        row_idx += 1

print(parsed_data[0], max(parsed_data), min(parsed_data), parsed_data[-1])
