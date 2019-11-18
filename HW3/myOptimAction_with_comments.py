import numpy as np

def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape
    cash_have= 1000
    use_cash = 4
    dp_record = np.zeros((days, 5), dtype=float)
    trans_record = [[0 for r in range(types + 2)] for i in range(days)]
    # [(formation of stock0, 1, 2, 3,), stock1 , stock]
    action_matrix = []

    for i in range(days):
        pa, pb, pc, pd = priceMat[i]
        if i == 0:
            dp_record[0] = [cash_have / pa * (1 - transFeeRate), cash_have / pb * (1 - transFeeRate), cash_have / pc * (1 - transFeeRate), cash_have / pd * (1 - transFeeRate), cash_have]
            trans_record[i] = [0, 1, 2, 3, 1000.0, 4]
        else:
            sell_idx = -1
            for j in range(0, 4):
                if dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate) > cash_have:
                    cash_have = dp_record[i - 1][j] * priceMat[i][j] * (1 - transFeeRate)
                    sell_idx = j

            # sell stock for more cash or just hold
            if cash_have > dp_record[i - 1][-1]:
                dp_record[i][-1] = cash_have
                trans_record[i][-1] = sell_idx
                trans_record[i][-2] = cash_have * (100.0 / 99.0)
            else:
                dp_record[i][-1] = dp_record[i - 1][-1]
                trans_record[i][-1] = use_cash
                trans_record[i][-2] = trans_record[i - 1][-2]

            # buy stock for more stock or just hold
            for j in range(0, 4):
                stock_have = cash_have / priceMat[i][j] * (1 - transFeeRate)
                if stock_have > dp_record[i - 1][j]:
                    dp_record[i][j] = stock_have
                    # the stock is bought from cash
                    # trans_record[i][j] = use_cash --> wrong answer, need to record from which stock
                    trans_record[i][j] = sell_idx
                else:
                    dp_record[i][j] = dp_record[i - 1][j]
                    # the stock remains the same
                    trans_record[i][j] = j

    maxx = 2 << 20 -1
    print(trans_record[0:20])
    # backtrace from the last round, check what has been sold (cash from sell stock, which stock has been sold for such amount of money)
    sell_from = trans_record[-1][-1]
    # from the last round, we will not perform buy
    buy_to = -1
    for i in range(days - 1, -1, -1):
        # does not perform sell, just hold
        if sell_from == use_cash:
            sell_from = -1
        # does not perform buy, just hold
        if buy_to == use_cash:
            buy_to = -1

        # valid transaction
        if sell_from != buy_to:
            action_matrix.append([i, sell_from, buy_to, trans_record[i][-2]])

        # we should buy stock we sell tomorrow from today for optimal solution
        buy_to = sell_from
        # search how the stock is made of, hold or buy
        sell_from = trans_record[i - 1][buy_to]

    return action_matrix[::-1]
