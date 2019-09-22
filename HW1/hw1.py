#!/usr/bin/env python
# coding: utf-8
# In[21]:
import csv
import sys
from datetime import datetime, timedelta

parsed_data = []
def nth_weekday(date, week, day):
    tmp = date.replace(day = 1) # restart from month
    adj = (day - tmp.weekday()) % 7 # weekday shift
    tmp += timedelta(days = adj) # shift to specified day of first week
    tmp += timedelta(weeks = week - 1) # shift to specified day of specified weel count
    return tmp

def is_in_month(date):
    datetime_obj = datetime.strptime(date, '%Y%m%d')
    cmp_obj = nth_weekday(datetime(datetime_obj.year, datetime_obj.month, datetime_obj.day), 3, 2)

    focus_month = ''
    if cmp_obj.day < datetime_obj.day: # go next month
        if cmp_obj.month < 9:
            focus_month = str(cmp_obj.year) + '0' + str(int(cmp_obj.month) + 1)
        elif cmp_obj.month == 12:
            focus_month = str(int(cmp_obj.year) + 1) + str(int(cmp_obj.month) + 1)
        else:
            focus_month = str(cmp_obj.year) + str(int(cmp_obj.month) + 1)
    else: # in this month
        if cmp_obj.month <= 9:
            focus_month = str(cmp_obj.year) + '0' + str(int(cmp_obj.month))
        else:
            focus_month = str(cmp_obj.year) + str(int(cmp_obj.month))

    return focus_month

with open(sys.argv[1], encoding = 'big5') as f:
    all_data = csv.reader(f)
    row_idx = 0
    flg = 0
    focus_month = ''

    for each_row in all_data:
        if row_idx:
            if str(each_row[1][0:2]) == 'TX':
                if flg == 0 and '/' not in each_row[2] and int(each_row[3]) == 84500:
                    focus_month = is_in_month(each_row[0])
                    flg = 1
                if int(each_row[3]) >= 84500 and int(each_row[3]) <= 134500 \
                and '/' not in each_row[2] and each_row[2][0:6] == focus_month[0:6]:
                    parsed_data.append(int(each_row[4]))

        row_idx += 1

print(parsed_data[0], max(parsed_data), min(parsed_data), parsed_data[-1])
