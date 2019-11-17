import numpy as np

def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape
    cash_have= 1000
    dp_record = np.zeros((days, 5), dtype=float)
    trans_record = np.zeros((days), dtype=int)
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
            trans_record[0] = -1 
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

        trans_record[i] = sell_idx
        # print(i, priceMat[i], dp_record[i])
        # print(trans_record[i])

    int_max = 2 << 32 - 1
    for i in range(days - 2, -1, -1):
        a = trans_record[i]
        b = trans_record[i + 1]
        if a != b: 
            action_matrix.append([i, a, b, int_max])

    return action_matrix[::-1]
