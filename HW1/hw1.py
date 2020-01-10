#!/usr/bin/env python
import sys, csv

parsed_data = []
with open(sys.argv[1], encoding = 'big5') as f:
    all_data = csv.reader(f)
    next(all_data, None)
    focus_month = ''

    for each_row in all_data:
        if str(each_row[1][0:2]) == 'TX':
            if int(each_row[3]) >= 84500 and int(each_row[3]) <= 134500 and '/' not in each_row[2]:
                if each_row[0][0:8] <= '20190821':
                    focus_month = '201908'
                elif each_row[0][0:8] > '20190821' and each_row[0][0:8] <= '20190918':
                    focus_month = '201909'
                else:
                    focus_month = '201910'

                if each_row[2][0:6] == focus_month:
                    parsed_data.append(int(each_row[4]))

print(parsed_data[0], max(parsed_data), min(parsed_data), parsed_data[-1])
