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

# Compute the return rate of my strategy, this code is from TA
# Compute return rate over a given price vector, with 3 modifiable parameters
def computeReturnRate(priceVec, stockType, windowSize, alpha, beta):
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
        suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice, stockType, windowSize, alpha, beta)        # Obtain the suggested action
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

    # Config search range
    windowSizeMin=200; windowSizeMax=500;    # Range of windowSize to explore
    alphaMin=0; alphaMax=30;            # Range of alpha to explore
    betaMin=0; betaMax=20;                # Range of beta to explore

    # Start exhaustive search
    for windowSize in range(windowSizeMin, windowSizeMax+1):        # For-loop for windowSize
        for alpha in range(alphaMin, alphaMax+1):            # For-loop for alpha
            for beta in range(betaMin, betaMax+1):        # For-loop for beta

                # Evaluate the current confg
                rr=np.zeros((fileCount,1))
                for ic in range(fileCount):
                    file=fileList[ic];
                    df=pd.read_csv(file)
                    adjClose=df["Adj Close"].values    # Get adj close as the price vector
                    stockType=file[-7:-4]        # Get stock type
                    rr[ic]=computeReturnRate(adjClose, stockType, windowSize, alpha, beta)    # Compute return rate
                    print("File=%s ==> rr=%f" %(file, rr[ic]));

                returnRate = np.mean(rr)
                print("Current settings: windowSize=%d, alpha=%d, beta=%d ==> avgReturnRate=%f" %(windowSize, alpha, beta ,returnRate))        # Print the best result

                returnRate = np.mean(rr)
                if returnRate>returnRateBest:        # Keep the best parameters
                    windowSizeBest=windowSize
                    alphaBest=alpha
                    betaBest=beta
                    returnRateBest=returnRate
                    print("Current best settings: windowSize=%d, alpha=%d, beta=%d ==> avgReturnRate=%f" %(windowSizeBest,alphaBest,betaBest,returnRateBest))        # Print the best result

    print("Overall best settings: windowSize=%d, alpha=%d, beta=%d ==> bestReturnRate=%f" %(windowSizeBest,alphaBest,betaBest,returnRateBest))        # Print the best result

   # with open('1011_weighted_ma.txt', 'w') as f:
      # f.write()
