import numpy as np

def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape

    cash_max = 0, stock_max = 0
    cash_today = 0, stock_today = 0
    cash_have= 0, stock_have = 0
    
    action_matrix = np.zeros((days, 4), dtype=int)

    # Use DP to find best possibilities 
    for i in range(days):
        # Try sell to find the best stock selling
        price_a = priceMat[i][0]
        price_b = priceMat[i][1] 
        price_c = priceMat[i][2]
        price_d = priceMat[i][3]

        price_min = min(price_a, min(price_b, min(price_c, price_d)))
        idx_sell = 0
        idx_buy = 0
        # First, sell the stock or hold today
        if stock_have > 0:
            cash_today = max(stock_have * price_a, max(stock_have * price_b, max(stock_have * price_c, stock_have * price_d))) * (1 - transFeeRate)
            # sell only if situation results in a better cash 
            if cash_today > cash_have:
                cash_have = cash_today
                stock_have = 0

        # And then buy the stock using cash (at least more than the cheapest stock)
        if cash_have > price_min: 
            stock_today = max(cash_have // price_a, max(cash_have // price_b, max(cash_have // price_c, cash_have // price_d))) * (1 - transFeeRate)
            # buy only if situation results in a better cash
            if stock_today > stock_have:
                stock_have = stock_today
                cash_have = 0

        # record best result and matrix
        cash_max = max(cash_max, cash_have)
        stock_max = max(stock_max, stock_have)
        
        action_matrix[i][0] = i
        action_matrix[i][1] =  
        action_matrix[i][2] = 
        action_matrix[i][3] = cash_have

    return action_matrix