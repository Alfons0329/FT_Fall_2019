import numpy as np

def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape

    cash_max = 0 
    stock_max = 0
    cash_today = 0
    stock_today = 0
    cash_have= 0
    stock_have = 0
    
    action_matrix = np.zeros((days, 4), dtype=int)

    # Use DP to find best possibilities 
    for i in range(days):
        # Try sell to find the best stock selling
        price_a = priceMat[i][0]
        price_b = priceMat[i][1] 
        price_c = priceMat[i][2]
        price_d = priceMat[i][3]

        price_min = min(price_a, min(price_b, min(price_c, price_d)))
        idx_sell = -1
        idx_buy = -1
        # First, sell the stock or hold today
        if stock_have > 0:
            cash_today = 0
            cnt = 0
            for itr in [stock_have * price_a, stock_have * price_b, stock_have * price_c, stock_have * price_d]:
                if itr > cash_today:
                    cash_today = itr
                    idx_sell = cnt
                cnt += 1
                
            # sell only if situation results in a better cash 
            if cash_today > cash_have:
                cash_have = cash_today
                stock_have = 0

        # And then buy the stock using cash (at least more than the cheapest stock)
        if cash_have > price_min:
            stock_today = 0
            cnt = 0 
            for itr in [ cash_have // price_a, cash_have // price_b, cash_have // price_c, cash_have // price_d]:
                if itr > stock_today:
                    stock_today = itr
                    idx_buy = cnt
                cnt += 1

            # buy only if situation results in a better cash
            if stock_today > stock_have:
                stock_have = stock_today
                cash_have = 0

        # record best result and matrix
        cash_max = max(cash_max, cash_have)
        stock_max = max(stock_max, stock_have)
        
        action_matrix[i][0] = i
        action_matrix[i][1] = idx_sell 
        action_matrix[i][2] = idx_buy
        action_matrix[i][3] = cash_max 

    return action_matrix