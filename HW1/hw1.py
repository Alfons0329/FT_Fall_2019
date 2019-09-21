#!/usr/bin/env python
# coding: utf-8
# In[21]:
import csv
import sys

parsed_data = []
with open(sys.argv[1], encoding = 'big5') as f:
    all_data = csv.reader(f)
    row_idx = 0
    flg = 0
    focus_month = ''

    for each_row in all_data:
        if row_idx:
            if str(each_row[1][0:2]) == 'TX':
                if flg == 0 and '/' not in each_row[2] and int(each_row[3]) == 84500:
                    focus_month = each_row[2]
                    flg = 1
                if int(each_row[3]) >= 84500 and int(each_row[3]) <= 134500 and each_row[2] == focus_month:
                    parsed_data.append(int(each_row[4]))

        row_idx += 1

print(parsed_data[0], max(parsed_data), min(parsed_data), parsed_data[-1])
