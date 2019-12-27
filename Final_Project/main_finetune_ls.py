#!/usr/bin/env python
# coding: utf-8
import os, sys, math
import sys
import numpy as np
import pandas as pd

'''
This code is used for fine tune the s parameter where the best_l has been determined.
'''

min_l = int(sys.argv[1])
max_l = int(sys.argv[2])
type_eval = int(sys.argv[3])
print('Search rsi small between [%d, %d) type_eval %d'%(min_l, max_l, type_eval))
f_name = 'search_' + str(min_l) + '_' + str(max_l) + '.txt'

def myStrategy(daily, minutely, openpricev, l, s, a, b):
    act = 0

    if type_eval == 0:
        daily = daily['close'].values
    else:
        daily = minutely['close'].values


    w_l = daily[-l:]
    w_s = daily[-s:]

    up = 0
    down = 0
    for i in range(l - 1):
        if w_l[i] < w_l[i + 1]:
            up += (w_l[i + 1] - w_l[i])
        elif w_l[i] > w_l[i + 1]:
            down += (w_l[i] - w_l[i + 1])

    if up + down == 0:
        up += 1
    rsi_l = float((up) / (up + down))

    up = down = 0

    for i in range(s - 1):
        if w_s[i] < w_s[i + 1]:
            up += (w_s[i + 1] - w_s[i])
        elif w_s[i] > w_s[i + 1]:
            down += (w_s[i] - w_s[i + 1])

    if up + down == 0:
        up += 1
    rsi_s = float((up) / (up + down))

    if rsi_s > rsi_l:
        act = 1
    elif rsi_s < rsi_l:
        act = -1
    else:
        act = 0

    return act

dailyOhlcv = pd.read_csv('daily.csv')
minutelyOhlcv = pd.read_csv('minute.csv')

def evaluate(l, s, a, b):
    capital = 500000.0
    capitalOrig=capital
    transFee = 100
    evalDays = 14
    action = np.zeros((evalDays,1))
    realAction = np.zeros((evalDays,1))
    total = np.zeros((evalDays,1))
    total[0] = capital
    Holding = 0.0
    openPricev = dailyOhlcv["open"].tail(evalDays).values
    clearPrice = dailyOhlcv.iloc[-3]["close"]

    for ic in range(evalDays,0,-1):
        dailyOhlcvFile = dailyOhlcv.head(len(dailyOhlcv)-ic)
        dateStr = dailyOhlcvFile.iloc[-1,0]
        minutelyOhlcvFile = minutelyOhlcv.head((np.where(minutelyOhlcv.iloc[:,0].str.split(expand=True)[0].values==dateStr))[0].max()+1)
        action[evalDays-ic] = myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPricev[evalDays-ic], l, s, a, b)
        currPrice = openPricev[evalDays-ic]
        if action[evalDays-ic] == 1:
            if Holding == 0 and capital > transFee:
                Holding = (capital-transFee)/currPrice
                capital = 0
                realAction[evalDays-ic] = 1
        elif action[evalDays-ic] == -1:
            if Holding > 0 and Holding*currPrice > transFee:
                capital = Holding*currPrice - transFee
                Holding = 0
                realAction[evalDays-ic] = -1
        elif action[evalDays-ic] == 0:
            realAction[evalDays-ic] = 0
        else:
            assert False
        if ic == 3 and Holding > 0: #遇到每個月的第三個禮拜三要平倉，請根據data的日期自行修改
            capital = Holding*clearPrice - transFee
            Holding = 0

        total[evalDays - ic] = capital + float(Holding > 0) * (Holding * currPrice - transFee)

    returnRate = (total[-1] - capitalOrig)/capitalOrig
    return returnRate

def search_optimize():
    best_rr = -1000.00
    best_l = 441

    for s in range(min_search, max_search):
        a = 0
        b = 1
        rr = evaluate(best_l, s, a, b)
        if rr > best_rr:
            best_s = s
            best_rr = rr

    overall_best = '\nOverall best settings: l = %d, s = %d, a = %f, b = %f rr = %f, '%(best_l, best_s, best_a, best_a, best_rr)
    print(overall_best)

search_optimize()
