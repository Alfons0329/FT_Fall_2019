import numpy as np

def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape

    cash_have= 1000
    # means the transaction is performaned with cash
    use_cash = 4

    dp_record = np.zeros((days, 5), dtype=float)
    # trans_record = np.zeros((days, 2), dtype=int)
    trans_record = np.zeros((days, types + 1), dtype=int)
    # trans_record means [(use_cash or same), (use_cash or same), (use_cash or same), (use_cash or same), (sell_stock or same)]
    # where same means no operation, for -1 in cash operation and same in stock operation
    action_matrix = []

    for i in range(days):
        # init
        # input()
        # print('-----------')
        pa, pb, pc, pd = priceMat[i]
        if i == 0:
            dp_record[0] = [cash_have / pa * (1 - transFeeRate), cash_have / pb * (1 - transFeeRate), cash_have / pc * (1 - transFeeRate), cash_have / pd * (1 - transFeeRate), cash_have]
            trans_record[i] = [0, 1, 2, 3, 4]
        else:
            # find out best possible 
            sell_idx = -1
            for j in range(0, 4):
                if dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate) > cash_have:
                    cash_have = dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate)
                    # print('%f x %f = %f ' % (dp_record[i - 1][j], priceMat[i][j], cash_have))
                    sell_idx = j
            
            # sell stock for more cash or just hold
            # sell for more cash
            if cash_have > dp_record[i - 1][-1]:
                dp_record[i][-1] = cash_have
                trans_record[i][-1] = sell_idx
            # hold
            else:
                dp_record[i][-1] = dp_record[i - 1][-1]
                trans_record[i][-1] = use_cash 

            # buy stock, update stock
            for j in range(0, 4):
                stock_have = cash_have / priceMat[i][j] * (1 - transFeeRate)
                if stock_have > dp_record[i - 1][j]:
                    dp_record[i][j] = stock_have
                    # the stock is bought from cash
                    trans_record[i][j] = use_cash
                else:
                    dp_record[i][j] = dp_record[i - 1][j]
                    # the stock remains the same
                    trans_record[i][j] = j

    
    cur_action = -1
    maxx = 2 << 64 - 1

    print(dp_record)
    input()
    print(trans_record)
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