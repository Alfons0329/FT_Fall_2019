'''
Work progress:
1010: Design the structure, using weighted moving average(weighted), check csv file
'''

'''
How my strategy is designed:

'''

import numpy as np
import pandas as pd
import os, sys, csv
import argparse

# implementation part of HW2
# param limits
WIN_LOWER = 200
WIN_UPPER = 300 + 1
ALPHA_MAX = 50
BETA_MAX = 50

def myStrategy(pastData, currPrice, stockType, w, a, b):
    action = 0
    data_len = len(pastData)

    if data_len < w:
        return 0

    windowed_data = pastData[-w:]
    weighted_sum = 0
    weighted_len = 0
    weighted_ma  = 0
    
    for i in range(0, len(windowed_data)):
        weighted_sum += windowed_data[i] * i
        weighted_len += i

    weighted_ma = weighted_sum / weighted_len
    action = 0
    if currPrice - a > weighted_ma:
        action = 1
    elif currPrice + b < weighted_ma:
        action = -1
    else:
        action = 0

    return action

# compute the return rate of my strategy, this code is from TA
def computeReturnRate(priceVec, stockType, w, a, b):
    capital=1000    # Initial available capital
    capitalOrig=capital     # original capital
    dataCount=len(priceVec)                # day size
    suggestedAction=np.zeros((dataCount,1))    # Vec of suggested actions    stockHolding=np.zeros((dataCount,1))      # Vec of stock holdings
    total=np.zeros((dataCount,1))         # Vec of total asset
    stockHolding=np.zeros((dataCount,1))  # Vec of stock holdings
    realAction=np.zeros((dataCount,1))    # Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
    
    # Run through each day
    for ic in range(dataCount):
        currentPrice=priceVec[ic]    # current price
        suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice, stockType, w, a, b)        # Obtain the suggested action
        
        # get real action by suggested action
        if ic>0:
            stockHolding[ic]=stockHolding[ic-1]    # The stock holding from the previous day
        if suggestedAction[ic]==1:    # Suggested action is "buy"
            if stockHolding[ic]==0:        # "buy" only if you don't have stock holding
                stockHolding[ic]=capital/currentPrice # Buy stock using cash
                capital=0    # Cash
                realAction[ic]=1
        elif suggestedAction[ic]==-1:    # Suggested action is "sell"
            if stockHolding[ic]>0:        # "sell" only if you have stock holding
                capital=stockHolding[ic]*currentPrice # Sell stock to have cash
                stockHolding[ic]=0    # Stocking holding
                realAction[ic]=-1
        elif suggestedAction[ic]==0:    # No action
            realAction[ic]=0
        else:
            assert False
        total[ic]=capital+stockHolding[ic]*currentPrice    # Total asset, including stock holding and cash 
    returnRate=(total[-1]-capitalOrig)/capitalOrig        # Return rate of this run
    
    return returnRate
    
if __name__=='__main__':
    file=sys.argv[1]    # input file
    file = 'SPY.csv'
    df=pd.read_csv(file)    
    adjClose=df["Adj Close"].values    # Get adj close as the price vector
    stockType=file[-7:-4]        # Get stock type
    bestReturnRate = 0
    
    w_best = 0
    a_best = 0
    b_best = 0
    
    for w in range(WIN_LOWER, WIN_UPPER, 5):
        for a in range(0, ALPHA_MAX):
            for b in range(0, BETA_MAX):
                
                returnRate = computeReturnRate(adjClose, stockType, w, a, b)    # Compute return rate
                
                if returnRate > bestReturnRate:
                    bestReturnRate = returnRate
                    w_best = w
                    a_best = a
                    b_best = b
                    print(w_best,',',a_best,',',b_best,',',bestReturnRate * 10000)

    result_str = str(w) + ',' + str(a) + ',' + str(b) + ',' + str(returnRate) + '\n'
    print(w_best,',',a_best,',',b_best,',',bestReturnRate * 10000)
    with open('1010weighted_ma.csv', 'a') as f:
        f.write(result_str)
        f.close()