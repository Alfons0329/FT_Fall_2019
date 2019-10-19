# This file is for param search (optimizing)
'''
'''

import numpy as np
import pandas as pd
import os, sys, csv
from progress.bar import Bar

# Implementation part of HW2
def myStrategy(pastData, currPrice, stockType, l, s, au, bl):

    # stock-wise param config starts here
    if stockType[0:3] == 'SPY':
        w_l = 2
        w_s = 101
        alpha = 0.447
        beta = 0.04
    elif stockType[0:3] == 'DSI':
        w_l = 6
        w_s = 4
        alpha = 0.9
        beta = 0.0
    elif stockType[0:3] == 'IAU':
        w_l = 11
        w_s = 5
        alpha = 0.95
        beta = 0.0
    elif stockType[0:3] == 'LQD':
        w_l = 6
        w_s = 4
        alpha = 0.8
        beta = 0.0
    # stock-wise param config rnds here

    action = 0
    data_len = len(pastData)
    if data_len < max(w_s, w_l):
        return 0

    # rsi index for estimation
    windowed_data_l = pastData[-w_l:]
    windowed_data_s = pastData[-w_s:]

    up = 0
    down = 0
    rsi_l = 0
    rsi_s = 0

    for i in range(w_l - 1):
        if windowed_data_l[i] < windowed_data_l[i + 1]:
            up += (windowed_data_l[i + 1] - windowed_data_l[i])
        elif windowed_data_l[i] > windowed_data_l[i + 1]:
            down += (windowed_data_l[i] - windowed_data_l[i + 1])

    rsi_l = float((up + 1) / (up + down + 1))

    up = down = 0
    for i in range(w_s - 1):
        if windowed_data_s[i] < windowed_data_s[i + 1]:
            up += (windowed_data_s[i + 1] - windowed_data_s[i])
        elif windowed_data_s[i] > windowed_data_s[i + 1]:
            down += (windowed_data_s[i] - windowed_data_s[i + 1])

    rsi_s = float((up + 1) / (up + down + 1))

    if stockType[0:3] == 'IAU' or stockType[0:3] == 'DSI' or stockType[0:3] == 'LQD':
        if rsi_s > rsi_l or (rsi_s > alpha and rsi_s < au):
            action = 1
        elif rsi_s < rsi_l or (rsi_s < beta and rsi_s > bl):
            action = -1
        else:
            action = 0
    elif stockType[0:3] == 'SPY':
        if rsi_s > rsi_l or (rsi_s > alpha and rsi_s < au):
            action = 1
        elif rsi_s < rsi_l or (rsi_s < beta and rsi_s > bl):
            action = -1
        else:
            action = 0

    return action


# Compute the return rate of my strategy, this code is from TA
# Compute return rate over a given price vector, with 3 modifiable parameters
def computeReturnRate(priceVec, stockType, l, s, a, b):
    capital=1000    # Initial available capital
    capitalOrig=capital     # original capital
    dataCount=len(priceVec)                # day size
    suggestedAction=np.zeros((dataCount,1))    # Vec of suggested actions
    stockHolding=np.zeros((dataCount,1))      # Vec of stock holdings
    total=np.zeros((dataCount,1))         # Vec of total asset
    realAction=np.zeros((dataCount,1))    # Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing).

    # Run through each day
    for ic in range(dataCount):
        currentPrice=priceVec[ic]    # current price
        suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice, stockType, l, s, a, b)        # Obtain the suggested action
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
    returnRateBest=-1.00     # Init best return rate
    fileList = ['SPY.csv'] # Init file names
    fileCount=len(fileList)

    # MA search algorithm
    '''
    # Config search range
    windowSizeMin=200; windowSizeMax=500;    # Range of windowSize to explore
    alphaMin=0; alphaMax=30;            # Range of alpha to explore
    betaMin=0; betaMax=20;                # Range of beta to explore

    # Start exhaustive search

    for windowSize in range(windowSizeMin, windowSizeMax+1):        # For-loop for windowSize
        for alpha in range(alphaMin, alphaMax+1):            # For-loop for alpha
            for beta in range(betaMin, betaMax+1):        # For-loop for beta
    '''

    # RSI search algotrithm
    lmin = 101; lmax = 101;
    lbest = 0; sbest = 0;

    alist = np.arange(0.447, 1.0, 0.001)
    blist = np.arange(0.04, 1.0, 0.001)
    abest = 0; bbest = 0;

    for l in range(lmin, lmax + 1, 2):
        for s in range(2, 3):
            for a in alist:
                for b in blist:
                    rr=np.zeros((fileCount,1))
                    for ic in range(fileCount):
                        file=fileList[ic];
                        df=pd.read_csv(file)
                        adjClose=df["Adj Close"].values    # Get adj close as the price vector
                        stockType=file[-7:-4]        # Get stock type
                        rr[ic]=computeReturnRate(adjClose, stockType, l, s, a, b)    # Compute return rate
                        #print("File=%s ==> rr=%f" %(file, rr[ic]));

                    returnRate = np.mean(rr)
                    if returnRate > returnRateBest:        # Keep the best parameters
                        lbest = l
                        sbest = s
                        abest = a
                        bbest = b
                        returnRateBest=returnRate
                        # print("Current best settings: l=%d, s=%d ==> avgReturnRate=%f" %(lbest, sbest, returnRateBest))
                        # print("Current best settings: a=%f, b=%f ==> avgReturnRate=%f" %(abest, bbest, returnRateBest))
                        print("Current best settings: l=%d, s=%d, a=%f, b=%f ==> avgReturnRate=%f" %(lbest, sbest, abest, bbest, returnRateBest))

# print("Overall best settings: l=%d, s=%d ==> bestAvgReturnRate=%f" %(lbest, sbest, returnRateBest))
# print("Overall best settings: a=%f, b=%f ==> bestReturnRate=%f" %(abest, bbest, returnRateBest))
print("Overall best settings: l=%d, s=%d, a=%f, b=%f ==> avgReturnRate=%f" %(lbest, sbest, abest, bbest, returnRateBest))

# with open('1011_weighted_ma.txt', 'w') as f:
  # f.write()
