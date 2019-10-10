# How to invoke this program:
#	python rrEstimate.py SPY.csv
import sys
import numpy as np
import pandas as pd
from myStrategy import myStrategy

# Compute return rate over a given price vector
def computeReturnRate(priceVec, stockType):
	capital=1000	# Initial available capital
	capitalOrig=capital	 # original capital
	dataCount=len(priceVec)				# day size
	suggestedAction=np.zeros((dataCount,1))	# Vec of suggested actions
	stockHolding=np.zeros((dataCount,1))  	# Vec of stock holdings
	total=np.zeros((dataCount,1))	 	# Vec of total asset
	realAction=np.zeros((dataCount,1))	# Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
	# Run through each day
	for ic in range(dataCount):
		currentPrice=priceVec[ic]	# current price
		suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice, stockType)		# Obtain the suggested action
		# get real action by suggested action
		if ic>0:
			stockHolding[ic]=stockHolding[ic-1]	# The stock holding from the previous day
		if suggestedAction[ic]==1:	# Suggested action is "buy"
			if stockHolding[ic]==0:		# "buy" only if you don't have stock holding
				stockHolding[ic]=capital/currentPrice # Buy stock using cash
				capital=0	# Cash
				realAction[ic]=1
		elif suggestedAction[ic]==-1:	# Suggested action is "sell"
			if stockHolding[ic]>0:		# "sell" only if you have stock holding
				capital=stockHolding[ic]*currentPrice # Sell stock to have cash
				stockHolding[ic]=0	# Stocking holding
				realAction[ic]=-1
		elif suggestedAction[ic]==0:	# No action
			realAction[ic]=0
		else:
			assert False
		total[ic]=capital+stockHolding[ic]*currentPrice	# Total asset, including stock holding and cash 
	returnRate=(total[-1]-capitalOrig)/capitalOrig		# Return rate of this run
	return returnRate
	
if __name__=='__main__':
	file=sys.argv[1];	# input file
	df=pd.read_csv(file)	
	adjClose=df["Adj Close"].values	# Get adj close as the price vector
	stockType=sys.argv[1][-7:-4]		# Get stock type
	rr=computeReturnRate(adjClose, stockType)	# Compute return rate
	print("rr=%f" %(rr))