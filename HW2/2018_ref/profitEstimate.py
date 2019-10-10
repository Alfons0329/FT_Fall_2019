import sys
import numpy as np
import pandas as pd
from myStrategy import myStrategy

def calculateReturnRate( file, stocksType ) :
    # stocksType = "SPY" or "IAU" or "DSI" , "LQD"
    # read file
    df = pd.read_csv(file)
    adjClose = df["Adj Close"].values   # get adj close
    dataCount=len(adjClose) # day size
    
    # init.
    capital=1  # 持有資金
    capitalOrig=capital  # cost
    suggestedAction= np.zeros((dataCount,1))  # 判斷action
    stockHolding=np.zeros((dataCount,1))  # 持有股票
    total = np.zeros((dataCount,1))  # 結算資金
    realAction=np.zeros((dataCount,1))  # 實際action
    
    # run each day
    for ic in range(dataCount):
        currPrice=adjClose[ic]  # 當天價格
        suggestedAction[ic]=myStrategy(adjClose[0:ic], currPrice, stocksType) # 取得當天action
        
        # get real action by suggested action
        if ic > 0: 
            # 更新手上持有股票
            stockHolding[ic]=stockHolding[ic-1]
        if suggestedAction[ic] == 1:
            # 若未持有股票: 買
            if stockHolding[ic]==0:            
                stockHolding[ic]=capital/currPrice # 買入股票
                capital=0   # 持有資金
                realAction[ic]=1
        elif suggestedAction[ic] == -1:
            # 若持有股票： 賣
            if stockHolding[ic]>0:
                capital=stockHolding[ic]*currPrice # 賣出股票
                stockHolding[ic]=0  # 持有股票
                realAction[ic]=-1
        elif suggestedAction[ic] == 0:
            # 不買不賣
            realAction[ic]=0
        else:
            assert False
        # 當天結算資金
        total[ic]=capital+stockHolding[ic]*currPrice
    # 最終盈利率
    returnRate=(total[-1]-capitalOrig)/capitalOrig 
    return returnRate
    
if __name__ == '__main__':
    returnRate = calculateReturnRate( sys.argv[1], sys.argv[1][-7:-4] ) # ( file , stock_name ) 
    print( returnRate )