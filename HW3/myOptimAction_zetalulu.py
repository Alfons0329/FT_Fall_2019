import numpy as np

def myOptimAction(priceMat, transFeeRate):
    # default 
    cash = 1000

    #start
    nextDay = 1
    dataLen, stockCount = priceMat.shape  # day size & stock count   
    actionMat = []  # An k-by-4 action matrix which holds k transaction records.
    dp = [np.zeros(stockCount+1) for i in range(dataLen)]
    bt = [[0 for j in range(stockCount+1)] for i in range(dataLen)]

    dp[0][0] = cash
    for i in range(stockCount):
        dp[0][i+1] = cash*(1-transFeeRate)/priceMat[0][i]
        bt[0][i+1] = 0
    
    for day in range( 1, dataLen ) :
        dayPrices = priceMat[day]  # Today price of each stock
        preCash = dp[day-1][0]
        preStock = dp[day-1][1:]
        dp[day][0] = preCash
        for i in range(stockCount):
            if dp[day][0] < preStock[i]*dayPrices[i]*(1-transFeeRate):
                dp[day][0] = preStock[i]*dayPrices[i]*(1-transFeeRate)
                bt[day][0] = i+1
        for i in range(stockCount):
            bt[day][i+1]=i+1
            dp[day][i+1]=preStock[i]
            if dp[day][i+1]<preCash*(1-transFeeRate)/dayPrices[i]:
                dp[day][i+1]=preCash*(1-transFeeRate)/dayPrices[i]
                bt[day][i+1]=0
            for j in range(stockCount):
                if dp[day][i+1] <preStock[j]*dayPrices[j]*(1-transFeeRate)*(1-transFeeRate)/dayPrices[i]:
                    dp[day][i+1]=preStock[j]*dayPrices[j]*(1-transFeeRate)*(1-transFeeRate)/dayPrices[i]
                    bt[day][i+1]=j+1

    mxi=0; mx=dp[day][0]
    for i in range(stockCount):
        if mx<preStock[i]*priceMat[-1][i]*(1-transFeeRate):
            mx=preStock[i]*priceMat[-1][i]*(1-transFeeRate)
            mxi=i+1
    now=mxi
    for day in reversed(range(dataLen)):
        if now!=bt[day][now]:
            pre = bt[day][now]
            if pre==0:
                actionMat.append([day,pre-1,now-1,dp[day-1][0]])
            else:
                actionMat.append([day,pre-1,now-1,dp[day-1][pre]*priceMat[day][pre-1]])
            now = pre
    print(list(reversed(actionMat)))
    return list(reversed(actionMat))

    
