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
            # sell stock
            cash_have = dp_record[i - 1][-1]
            for j in range(0, 4):
                if dp_record[i - 1][j] * priceMat[i][j] > cash_have:
                    cash_have = dp_record[i - 1][j] * priceMat[i][j]

            # update stock holdings
            dp_record[i][-1] = cash_have
            cash_have *= (1 - transFeeRate)
            for j in range(0, 4):
                dp_record[i][j] = max(dp_record[i - 1][j], cash_have / priceMat[i][j])

    print(dp_record)
    return action_matrix[::-1]
