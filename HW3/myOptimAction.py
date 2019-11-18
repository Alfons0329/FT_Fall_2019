import numpy as np

def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape
    cash_have= 1000
    dp_record = np.zeros((days, 5), dtype=float)
    trans_record = np.zeros((days, types + 1), dtype=int)
    action_matrix = []

    sell_idx = -1
    for i in range(days):
        # init
        # input()
        # print('-----------')
        pa, pb, pc, pd = priceMat[i]
        if i == 0:
            dp_record[0] = [cash_have / pa * (1 - transFeeRate), cash_have / pb * (1 - transFeeRate), cash_have / pc * (1 - transFeeRate), cash_have / pd * (1 - transFeeRate), cash_have]
            trans_record[i] = [-1, 0, 0, 0, 1000]
        else:
            # sell stock, update cash
            sell_idx = -1
            cash_today = -1
            stock_today = -1

            for j in range(0, 4):
                if dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate) > cash_today:
                    cash_today = dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate)
                    sell_idx = j

             # sell stock to get greater cash
            if cash_today > dp_record[i][-1]:
                dp_record[i][-1] = cash_today
                # sell stock at sell_idx to get geater cash
                trans_record[i][-1] = sell_idx
            # just hold
            else: 
                dp_record[i][-1] = dp_record[i - 1][-1]
                # no sell at that day
                trans_record[i][-1] = -1

            # update for stock buying
            for j in range(0, 4):
                dp_record[i][j] = dp_record[i - 1][j]
                trans_record[i][j] = j

            # buy stock, update stock
            for j in range(0, 4):
                stock_today = cash_have / priceMat[i][j] * (1 - transFeeRate)
                if  stock_today > dp_record[i - 1][j]:
                    dp_record[i][j] = stock_today
                    # stock is bought with cash
                    trans_record[i][j] = -1
                else:
                    dp_record[i][j] = dp_record[i - 1][j]
                    # stock is the same
                    trans_record[i][j] = j
        
        # update
        dp_record[i][-1] = dp_record[i - 1][-1]
        trans_record[i][-1] = -1
    
    cur_action = -1
    maxx = 2 << 64 - 1

    print(dp_record)
    for i in range(days - 2, -1, -1):
        sell_from = i
        buy_to = i + 1

        if cur_action != -1 and trans_record[buy_to][cur_action] == -1:
            action_matrix.append([i, -1, cur_action, maxx])

        if cur_action == -1 and trans_record[sell_from][cur_action] == -1:
            action_matrix.append([i, trans_record[sell_from][cur_action], -1, maxx])
            cur_action = trans_record[sell_from][cur_action]

    return action_matrix[::-1]

# WRONG: dp_record[i][j] = max(dp_record[i - 1][j], dp_record[i - 1][-1] / priceMat[i][j] * (1 - transFeeRate))