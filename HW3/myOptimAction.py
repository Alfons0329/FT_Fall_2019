import numpy as np

def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape

    cash_max = 0
    cash_today = 0
    cash_have= 1000
    # stock_have = (amount, type)
    stock_have = (0, -1)

    action_matrix = np.zeros((days, 4), dtype=int)

    # Use DP to find best possibilities
    for i in range(days):
        # Try sell to find the best stock selling
        pa = priceMat[i][0]
        pb = priceMat[i][1]
        pc = priceMat[i][2]
        pd = priceMat[i][3]

        pmin = min(pa, min(pb, min(pc, pd)))
        idx_sell = -1
        idx_buy = -1
        print('day %d stock price %f %f %f %f' % (i, pa, pb, pc, pd))
        # First, sell the stock or hold today
        if stock_have[0] > 0:
            stock_type = stock_have[1]
            # if the result of selling current stock results in better cash, do it
            if priceMat[i][stock_type] * stock_have[0] > cash_have:
                cash_have = priceMat[i][stock_have[1]] * stock_have[0]
                idx_sell = stock_have[1]

        cash_max = max(cash_max, cash_have)
        # And then buy the stock using cash (at least more than the cheapest stock)
        if cash_have > pmin:
            stock_today = 0
            cnt = 0
            for itr in [ cash_have / pa, cash_have / pb, cash_have / pc, cash_have / pd]:
                if itr > stock_today:
                    stock_today = itr
                    idx_buy = cnt
                cnt += 1

            # buy only if situation results in the more amount of stock 
            if stock_today > stock_have[0]:
                stock_have = (stock_today, idx_buy)

        # record best result and matrix
        print('sell stock %d to have cash %f max_cash %f' % (idx_sell, cash_have, cash_max))
        print('buy stock %d to have stock %f' % (idx_buy, stock_have[0]))

        action_matrix[i][0] = i
        action_matrix[i][1] = int(idx_sell)
        action_matrix[i][2] = int(idx_buy)
        action_matrix[i][3] = int(cash_max)

        # input()

    return action_matrix
