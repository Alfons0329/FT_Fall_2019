'''
Work progress:
1010: Design the structure, using weighted moving average(weighted), checkCSV
'''

'''
How my strategy is designed:

'''

import numpy as np
import pandas as pd
import os, sys, csv
import argparse

# implementation part of HW2
## for brute force search argument parsing
'''
parser.add_argument('--alpha', type = int, 10)
parser.add_argument('--beta', type = int, 10)
parser.add_argument('--windows_size', type = int, 290)
args = parser.parse_args()
'''

# param limits
WIN_LOWER = 50
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
    if currPrice + b < weighted_ma:
        action = -1
    else:
        action = 0

    return action

def calculateReturnRate(file, stocksType, w, a, b):
    # stocksType = "SPY" or "IAU" or "DSI" , "LQD"
    # read file
    file = 'SPY.csv'
    df = pd.read_csv(file)
    adjClose = df["Adj Close"].values   # get adj close
    dataCount=len(adjClose) # day size

    # init.
    capital = 1  # 持有資金
    capitalOrig = capital  # cost
    suggestedAction = np.zeros((dataCount,1))  # 判斷action
    stockHolding = np.zeros((dataCount,1))  # 持有股票
    total = np.zeros((dataCount,1))  # 結算資金
    realAction = np.zeros((dataCount,1))  # 實際action

    # run each day
    for ic in range(dataCount):
        currPrice = adjClose[ic]  # 當天價格
        suggestedAction[ic] = myStrategy(adjClose[0:ic], currPrice, stocksType, w, a, b) # 取得當天action

        # get real action by suggested action
        if ic > 0:
            # 更新手上持有股票
            stockHolding[ic] = stockHolding[ic-1]
        if suggestedAction[ic] == 1:
            # 若未持有股票: 買
            if stockHolding[ic] == 0:
                stockHolding[ic] = capital/currPrice # 買入股票
                capital = 0   # 持有資金
                realAction[ic] = 1
        elif suggestedAction[ic] == -1:
            # 若持有股票： 賣
            if stockHolding[ic] > 0:
                capital = stockHolding[ic] * currPrice # 賣出股票
                stockHolding[ic] = 0  # 持有股票
                realAction[ic] = -1
        elif suggestedAction[ic] == 0:
            # 不買不賣
            realAction[ic]=0
        else:
            assert False
        # 當天結算資金
        total[ic] = capital + stockHolding[ic] * currPrice
    # 最終盈利率
    returnRate = (total[-1] - capitalOrig) / capitalOrig
    return returnRate

if __name__ == '__main__':

    for w in range(WIN_LOWER, WIN_UPPER):
        for a in range(0, ALPHA_MAX):
            for b in range(0, BETA_MAX):
                #print('strategy win %d alpha %d beta %d '%(w, a, b))
                returnRate = calculateReturnRate(sys.argv[1], sys.argv[1][-7 : -4], w, a, b) # (file , stock_name)
                result_str = str(w) + ',' + str(a) + ',' + str(b) + ',' + str(returnRate) + '\n'
                with open('1010compare.csv', 'a') as f:
                    f.write(result_str)
                    f.close()

                print(w,',',a,',',b,',',returnRate)


