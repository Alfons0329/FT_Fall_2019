import numpy as np

def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape
    cash_have= 1000
    dp_record = np.zeros((days, 5), dtype=float)
    trans_record = np.zeros((days, 2), dtype=int)
    action_matrix = []

    # Use DP to find best possibilities
    sell_idx = -1
    for i in range(days):
        # init
        # input()
        # print('-----------')
        pa, pb, pc, pd = priceMat[i]
        if i == 0:
            dp_record[0] = [cash_have / pa * (1 - transFeeRate), cash_have / pb * (1 - transFeeRate), cash_have / pc * (1 - transFeeRate), cash_have / pd * (1 - transFeeRate), cash_have]
            trans_record[i] = [-1, 1000]
        else:
            # sell stock, update cash
            sell_idx = -1
            for j in range(0, 4):
                if dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate) > cash_have:
                    cash_have = dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate)
                    # print('%f x %f = %f ' % (dp_record[i - 1][j], priceMat[i][j], cash_have))
                    sell_idx = j
            dp_record[i][-1] = max(dp_record[i - 1][-1], cash_have)

            # buy stock, update stock
            for j in range(0, 4):
                # WRONG: dp_record[i][j] = max(dp_record[i - 1][j], dp_record[i - 1][-1] / priceMat[i][j] * (1 - transFeeRate))
                if cash_have / priceMat[i][j] * (1 - transFeeRate) > dp_record[i - 1][j]:
                    dp_record[i][j] = cash_have / priceMat[i][j] * (1 - transFeeRate)
                else:
                    dp_record[i][j] = dp_record[i - 1][j]

            trans_record[i] = [sell_idx, cash_have]

    '''
    for i in trans_record:
        print(i)
        input()
    '''
    maxx = 2 << 32 - 1
    input()
    for i in range(days - 2, -1, -1):
        a = trans_record[i][0]
        b = trans_record[i + 1][0]
        if a != b:
            action_matrix.append([i, a, b, trans_record[i][1]]) 

    for i in action_matrix:
        print(i)
    return action_matrix[::-1]
