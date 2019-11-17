import numpy as np

def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape
    cash_have= 1000
    dp_record = np.zeros((days, 5), dtype=float)
    action_matrix = np.zeros((days, 4), dtype=int)

    # Use DP to find best possibilities
    for i in range(days):
        # init
        pa, pb, pc, pd = priceMat[i]
        if i == 0:
            cash_original = cash_have
            cash_have *= (1 - transFeeRate)
            dp_record[0] = [cash_have / pa, cash_have / pb, cash_have / pc, cash_have / pd, cash_original]
        else:
            # sell stock, update cash
            cash_today = 0 
            for j in range(0, 4):
                if dp_record[i - 1][j] * priceMat[i][j] > cash_today:
                    cash_today = dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate)
            dp_record[i][-1] = max(dp_record[i - 1][-1], cash_today)

            # buy stock, update stock
            for j in range(0, 4):
                dp_record[i][j] = max(dp_record[i - 1][j], dp_record[i - 1][-1] / priceMat[i][j] * (1 - transFeeRate))
            
    print(dp_record)
    return action_matrix[::-1]
