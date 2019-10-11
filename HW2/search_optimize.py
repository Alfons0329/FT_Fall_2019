# This file is for param search (optimizing)
'''
Work progress:
1010: Design the structure, using weighted moving average(weighted), merge four csv files
1011: Check data trend, using weighted moving average, not use on merged four csv file,
but real separated csv file
'''

'''
How my strategy is designed:

'''

import numpy as np
import pandas as pd
import os, sys, csv

# Implementation part of HW2
def myStrategy(pastData, currPrice, stockType, l, s):
    import numpy as np

    # param config starts here
    a = 0
    b = 3
    w_l = l
    w_s = s
    # param config ends here
    action = 0
    data_len = len(pastData)

    if data_len < w_l:
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

    if stockType[0:3] == 'IAU':
        if rsi_s > rsi_l:
            action = 1
        elif rsi_s < rsi_l:
            action = -1
        else:
            action = 0
    else:
        if rsi_s > rsi_l:
            action = 1
        elif rsi_s < rsi_l:
            action = 1
        else:
            action = 1

    return action


# Compute the return rate of my strategy, this code is from TA
# Compute return rate over a given price vector, with 3 modifiable parameters
def computeReturnRate(priceVec, stockType, l, s):
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
        suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice, stockType, l, s)        # Obtain the suggested action
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
    fileList = ['SPY.csv', 'DSI.csv', 'IAU.csv', 'LQD.csv'] # Init file names
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
    lmin = 12; lmax = 240;
    lbest = 0; sbest = 0;
    for l in range(lmin, lmax):
        for s in range(5, l):
            # Evaluate the current confg
            rr=np.zeros((fileCount,1))
            
            for ic in range(fileCount):
                file=fileList[ic];
                df=pd.read_csv(file)
                adjClose=df["Adj Close"].values    # Get adj close as the price vector
                stockType=file[-7:-4]        # Get stock type
                rr[ic]=computeReturnRate(adjClose, stockType, l, s)    # Compute return rate
                print("File=%s ==> rr=%f" %(file, rr[ic]));
            
            returnRate = np.mean(rr)
            print("Current settings: l=%d, s=%d ==> avgReturnRate=%f" %(l, s, returnRate))        # Print the best result
            
            if returnRate>returnRateBest:        # Keep the best parameters
                lbest=l
                sbest=s
                returnRateBest=returnRate
                print("Current best settings: l=%d, s=%d ==> avgReturnRate=%f" %(lbest, sbest, returnRateBest))        # Print the best result

print("Overall best settings: l=%d, s=%d ==> bestAvgReturnRate=%f" %(lbest, sbest, returnRateBest))        # Print the best result        # Print the best result

# with open('1011_weighted_ma.txt', 'w') as f:
  # f.write()
