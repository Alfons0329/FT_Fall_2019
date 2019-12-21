#!/usr/bin/env python
# coding: utf-8

# In[14]:


'''
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from pandas import DataFrame, read_csv
import pandas as pd

import matplotlib.pyplot as plt

import numpy as np
import regex as re
'''
import os, sys, math
import sys
import numpy as np
import pandas as pd

'''
Progress log note;

12/20: Try using the brute force search like HW2, but trying with daily scale approach
'''

def myStrategy(daily, minutely, openpricev, l, s, a, b):
    act = 0

    daily = daily['close'].values
    data_len = len(daily)

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

    if rsi_s > rsi_l or (rsi_s > a):
        action = 1
    elif rsi_s < rsi_l or (rsi_s < b):
        action = -1
    else:
        action = 0

    return act


# In[15]:


# from myStrategy import myStrategy

# dailyOhlcv = pd.read_csv(sys.argv[1])
# minutelyOhlcv = pd.read_csv(sys.argv[2])

dailyOhlcv = pd.read_csv('daily.csv')
minutelyOhlcv = pd.read_csv('minute.csv')


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

def evaluate(l, s, a, b):
    global dailyOhlcv, minutelyOhlcv, capital, capitalOrig, transFee, evalDays, action, realAction, total, Holding, openPricev, clearPrice

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

        total[evalDays-ic] = capital + float(Holding>0) * (Holding*currPrice-transFee)

    returnRate = (total[-1] - capitalOrig)/capitalOrig

    return returnRate


# In[21]:




def search_optimize():
    best_rr = -1000

    min_l = 0
    max_l = 100
    best_l = 0
    best_s = 0
    list_a = np.arange(0.0, 1.0, 0.1)
    list_b = np.arange(0.0, 1.0, 0.1)
    best_a = 0
    best_b = 0

    for l in range(min_l, max_l, 1):
        for s in range(0, l):
            for a in list_a:
                for b in list_b:

                    rr = evaluate(l, s, a, b)
                    if rr > best_rr:
                        best_l = l
                        best_s = s
                        best_a = a
                        best_b = b
                        best_rr = rr
                        print("Overall best settings: l = %d, s = %d, a = %f, b = %f rr = %f"%(best_l, best_s, best_a, best_b, best_rr))

                    print("Current settings: l = %d, s = %d, a = %f, b = %f rr = %f"%(l, s, a, b, rr))

    print("Overall best settings: l = %d, s = %d, a = %f, b = %f rr = %f"%(best_l, best_s, best_a, best_a, best_rr))

search_optimize()

