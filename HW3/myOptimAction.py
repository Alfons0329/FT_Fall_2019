import numpy as np

def myOptimAction(priceMat, transFeeRate):
    days, types = priceMat.shape

    cash_have= 1000
    # means the transaction is performaned with cash
    use_cash = 4

    dp_record = np.zeros((days, 5), dtype=float)
    # trans_record = np.zeros((days, 2), dtype=int)
    trans_record = np.zeros((days, types + 2), dtype=int)
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
            trans_record[i] = [0, 1, 2, 3, 1000, 4]
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
                trans_record[i][-2] = cash_have * (100.0 / 99.0)
            # hold
            else:
                dp_record[i][-1] = dp_record[i - 1][-1]
                trans_record[i][-1] = use_cash
                trans_record[i][-2] = trans_record[i - 1][-2]

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

    maxx = 2 << 20 -1
    # print(dp_record)
    # print(trans_record)
    # input()
    # from the last round, check what has been sold (cash from sell stock, which stock has been sold for such amount of money)
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
            # print('i ', i,' buy_to ', buy_to, ' sell_from ', sell_from)
            action_matrix.append([i, sell_from, buy_to, trans_record[i][-2]])

        # we should buy stock we sell tomorrow from today for optimal solution
        # input()
        buy_to = sell_from
        # search how the stock is made of, hold or buy
        sell_from = trans_record[i - 1][buy_to]

    # for i in action_matrix:
        # print(i)
    return action_matrix[::-1]

# WRONG: dp_record[i][j] = max(dp_record[i - 1][j], dp_record[i - 1][-1] / priceMat[i][j] * (1 - transFeeRate))
