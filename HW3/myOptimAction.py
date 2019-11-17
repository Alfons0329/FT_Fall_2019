import numpy as np

def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape
    cash_have= 1000
    dp_record = np.zeros((days, 5), dtype=float)
    action_matrix = np.zeros((days, 4), dtype=int)

    # Use DP to find best possibilities
    for i in range(days):
        # init
        #input()
        print('-----------')
        pa, pb, pc, pd = priceMat[i]
        if i == 0:
            dp_record[0] = [cash_have / pa * (1 - transFeeRate), cash_have / pb * (1 - transFeeRate), cash_have / pc * (1 - transFeeRate), cash_have / pd * (1 - transFeeRate), cash_have]
        else:
            # sell stock, update cash
            for j in range(0, 4):
                if dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate) > cash_have:
                    print('cash)have %f calculate %f' % (cash_have, dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate)))
                    cash_have = dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate)
            dp_record[i][-1] = max(dp_record[i - 1][-1], cash_have)

            # buy stock, update stock
            for j in range(0, 4):
                dp_record[i][j] = max(dp_record[i - 1][j], dp_record[i - 1][-1] / priceMat[i][j] * (1 - transFeeRate))
            
        print(priceMat[i])
        print(i, dp_record[i])
    print(dp_record)
    return action_matrix[::-1]
